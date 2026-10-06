#!/usr/bin/env python3
"""
Generate cached AWS Polly audio for breath-cue.html's spoken cues.

Requires the AWS CLI configured with Polly access (`aws configure`, or an
env var / SSO profile that's already set up — this script never touches
credentials itself, it just shells out to `aws`).

    python3 generate_audio.py                       # default voice, sanskrit-only cues
    python3 generate_audio.py --voice Matthew
    python3 generate_audio.py --lang en
    python3 generate_audio.py --profile admin

Writes mp3s into audio/ and rewrites the <script id="audioManifest"> block
in breath-cue.html so the page finds them. Safe to re-run: text that hasn't
changed reuses its existing file (same visible cue text -> same hash), so
editing one cue's wording only re-synthesizes that one clip. Use --force to
regenerate everything even when the cache thinks it's current (needed after
changing voice, engine, or a pose's ipa_sa — none of those change the cached
filename, since it's keyed on the cue text, not on how it's pronounced).

Sanskrit pronunciation: when a step has an `ipa_sa` field, that's sent to
Polly as an SSML <phoneme alphabet="ipa"> tag instead of plain text, giving
real per-sound control (dental vs. retroflex consonants, vowel length,
aspiration) instead of relying on English spelling. Polly maps the IPA onto
the voice's own English phoneme inventory, so it's a real improvement over
guessing from English spelling, not a native-speaker-perfect rendering —
sounds with no English equivalent (retroflex stops, breathy voicing) get
approximated to their closest English sound.

Cost: Polly neural voices run about $16 per million characters billed
(standard voices ~$4/million). One round of this sequence is under 1,000
characters, so a full regenerate costs a fraction of a cent.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

HERE = Path(__file__).parent
HTML = HERE / "breath-cue.html"
AUDIO_DIR = HERE / "audio"


def block_pattern(block_id):
    return re.compile(
        rf'(<script type="application/json" id="{block_id}">)(.*?)(</script>)', re.S
    )


def read_block(html, block_id, required=True):
    m = block_pattern(block_id).search(html)
    if not m:
        if required:
            raise SystemExit(f"couldn't find #{block_id} block in {HTML.name}")
        return None
    return m.group(2)


def write_block(html, block_id, payload):
    pattern = block_pattern(block_id)
    if not pattern.search(html):
        raise SystemExit(f"couldn't find #{block_id} block in {HTML.name} to update")
    return pattern.sub(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3), html, count=1)


def pose_name(step, lang):
    sa = step.get("say_sa") or step.get("pose_sa") or ""
    en = step.get("pose_en") or ""
    if lang == "sa":
        return sa
    if lang == "en":
        return en
    return ", ".join(x for x in (sa, en) if x)


def step_cues(step, lang):
    """Mirror stepPhases() in breath-cue.html's <logic> block. Keep in sync by hand
    if that function changes — there's no shared source, this is a deliberate duplicate.

    Returns (plain_text, ssml) pairs: plain_text is the manifest key — it must match
    what the page's own poseName()/stepPhases() compute, since that's how the page
    looks up which recording to play. ssml is what's actually sent to Polly; it's
    only richer than plain_text when the step has an ipa_sa to wrap in a phoneme tag.
    """
    cues = []
    if step.get("breaths"):
        n = step["breaths"]
        for i in range(1, n + 1):
            q = f" {step['quality']}" if i == 1 and step.get("quality") else ""
            in_text = f"Inhale. Breath {i} of {n}.{q}"
            cues.append((in_text, f"<speak>{escape(in_text)}</speak>"))
            cues.append(("Exhale.", "<speak>Exhale.</speak>"))
    else:
        word = {"in": "Inhale", "out": "Exhale"}.get(step.get("breath"), "")
        say = pose_name(step, lang)
        parts = [p.strip().rstrip(". ") for p in (word, step.get("move"), say) if p]
        plain_text = ". ".join(parts) + "."

        ipa = step.get("ipa_sa") if lang == "sa" else None
        if ipa and say:
            lead = ". ".join(p.strip().rstrip(". ") for p in (word, step.get("move")) if p)
            pose_display = step.get("pose_sa") or say
            phoneme = f'<phoneme alphabet="ipa" ph={quoteattr(ipa)}>{escape(pose_display)}</phoneme>'
            body = f"{escape(lead)}. {phoneme}." if lead else f"{phoneme}."
        else:
            body = escape(plain_text)
        cues.append((plain_text, f"<speak>{body}</speak>"))
    return cues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice", default="Joanna", help="Polly voice id (default: Joanna)")
    ap.add_argument("--engine", default="neural", choices=["neural", "standard"])
    ap.add_argument("--lang", default="sa", choices=["sa", "en", "both"],
                     help="which pose-name language to synthesize (default: sa, matching the page default)")
    ap.add_argument("--profile", default=None, help="AWS CLI profile (defaults to your current AWS_PROFILE)")
    ap.add_argument("--dry-run", action="store_true", help="print what would be synthesized without calling AWS")
    ap.add_argument("--force", action="store_true",
                     help="regenerate every clip even if the cache looks current — needed after changing "
                          "voice, engine, or an ipa_sa, since none of those change the cache key")
    args = ap.parse_args()

    html = HTML.read_text()
    seq = json.loads(read_block(html, "defaultSeq"))
    manifest = json.loads(read_block(html, "audioManifest", required=False) or "{}")

    unique = {}   # plain_text -> ssml, first occurrence wins (should be identical if it recurs)
    for step in seq:
        for plain_text, ssml in step_cues(step, args.lang):
            unique.setdefault(plain_text, ssml)

    if args.dry_run:
        for text, ssml in sorted(unique.items()):
            status = "cached" if manifest.get(text) and (HERE / manifest[text]).exists() else "would synthesize"
            note = " [phoneme]" if "<phoneme" in ssml else ""
            print(f"  [{status}]{note} {text}")
        print(f"\n{len(unique)} unique cue(s), {sum(len(t) for t in unique)} characters.")
        return

    AUDIO_DIR.mkdir(exist_ok=True)
    generated = 0
    billed_chars = 0
    for text, ssml in sorted(unique.items()):
        key = hashlib.sha1(text.encode()).hexdigest()[:10]
        rel = f"audio/{key}.mp3"
        dest = HERE / rel
        if not args.force and dest.exists() and manifest.get(text) == rel:
            continue
        cmd = [
            "aws", "polly", "synthesize-speech",
            "--output-format", "mp3",
            "--voice-id", args.voice,
            "--engine", args.engine,
            "--text-type", "ssml",
            "--text", ssml,
        ]
        if args.profile:
            cmd += ["--profile", args.profile]
        cmd.append(str(dest))
        print(f"  synthesizing: {text[:70]!r}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            dest.unlink(missing_ok=True)
            print(f"    aws polly failed:\n{r.stderr.strip()}", file=sys.stderr)
            sys.exit(1)
        manifest[text] = rel
        billed_chars += len(text)
        generated += 1

    html = write_block(html, "audioManifest", json.dumps(manifest, indent=2, ensure_ascii=False))
    HTML.write_text(html)

    reused = len(unique) - generated
    rate = 16 if args.engine == "neural" else 4
    print(f"\n{generated} clip(s) synthesized, {reused} reused, {len(unique)} total.")
    if billed_chars:
        print(f"~{billed_chars} characters billed this run (~${billed_chars * rate / 1_000_000:.4f} at "
              f"{args.engine} rates).")
    print(f"manifest written into {HTML.name} ({len(manifest)} entries, voice={args.voice}, lang={args.lang}).")
    print("stale entries for wording you've since changed are left in place; run with --dry-run to spot them.")


if __name__ == "__main__":
    main()
