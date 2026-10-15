# Yoga learning dataset

CSV source files for yoga diagrams, timelines, vocab, and teaching scripts. Use these to generate Mermaid diagrams and Notion databases, and to keep both up to date.

## Files

| File | Purpose | Diagram it feeds |
|---|---|---|
| `yoga_timeline.csv` | Vedic → Upaniṣadic → Patañjali → Haṭha → modern | Mermaid `timeline` |
| `yoga_lineages.csv` | Tree of traditions and modern styles (`parent_id`; `secondary_parent_ids`) | Mermaid `graph TD` / `flowchart` |
| `yoga_founders.csv` | Teachers and scholars from the last ~150 years (`lineage_ids` links to lineages) | Table; timeline |
| `yoga_asana_etymology.csv` | Āsana names broken into Sanskrit roots and stems | Mermaid `mindmap` grouped by `root_or_stem` or `category` |
| `yoga_prakriti_gunas.csv` | Sāṃkhya 25 tattvas as a tree (`parent_id`) | Mermaid `graph TD` / `mindmap` |
| `yoga_gunas.csv` | Sattva / rajas / tamas detail (`parent_id` = P002) | Table; small mindmap |
| `yoga_vocab.csv` | Glossary with roots and pronunciation | Notion database |
| `yoga_teaching_scripts.csv` | Personal teaching scripts (3 placeholder rows only) | Notion database |

## Conventions

- IDs are stable prefixes: `T` timeline, `L` lineage, `F` founder, `A` āsana, `P` prakṛti tree, `G` guṇa, `V` vocab, `S` script. Never reuse an ID. Cross-references use IDs; multiple values are separated by `;`.
- Within cells, `;` is the separator and commas are avoided, so files stay valid CSV. Quote a field if a comma is truly needed.
- Years are integers; BCE years are negative.
- Romanization is IAST (diacritics); `plain_spelling` in vocab is the studio spelling.
- `confidence` (timeline and founders) is high / medium / low. Early dating is genuinely contested.

## Caveats

- Drafted from memory by Claude without live sources. Verify dates, verse numbers, and attributions before teaching or publishing them. Add a `source_url` column as you verify.
- Rows about teacher misconduct (marked "verify before citing") summarize public allegations or findings only at a general level; check primary reporting before repeating them.
- Many modern postures have no premodern textual source; `earliest_source` is blank where unknown, not "none".
- Scripts are placeholders. Replace them with your own voice.

## Suggested Claude Code tasks

1. "Generate Mermaid for the lineage tree from `yoga_lineages.csv` (solid edges for `parent_id`; dotted for `secondary_parent_ids`) and the timeline from `yoga_timeline.csv`. Write them to `diagrams/*.mmd`."
2. "Build a `mindmap` of `yoga_prakriti_gunas.csv` from the root (puruṣa and prakṛti) down."
3. "Group `yoga_asana_etymology.csv` by `category` and produce a mindmap; then a second grouped by root."
4. "Add new rows for X; keep IDs sequential; re-run the diagram generation."
5. "Validate all CSVs: column counts, unique IDs, and that every cross-referenced ID exists."

## Notion

Import each CSV as a database (Notion: Import → CSV). Paste the generated Mermaid into a code block with language set to Mermaid.
