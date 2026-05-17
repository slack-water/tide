# tide

*the ocean of information is overwhelming*
*tide makes it feel more organized and predictable*

---

More information arrives each day than you can hold. Most systems for managing this ask you to commit to a method, a tool, a subscription, a version of yourself that has it all organized. tide asks for almost nothing: an architecture, a convention, plain text files.

if the tools change — and they will — your files don't.

```mermaid
%%{init: { 'gitGraph': { 'mainBranchName': 'vault' } } }%%
gitGraph
    commit id: "initial structure"
    branch values
    checkout values
    commit id: "depth over breadth"
    commit id: "hospitality"
    branch inbox
    checkout inbox
    commit id: "web clip"
    commit id: "voice note"
    commit id: "quick idea"
    commit id: "slack thread"
    checkout values
    merge inbox id: "reset — reviewed against values"
    checkout vault
    merge values id: "vault grows"
    checkout inbox
    commit id: "more arrives"
    commit id: "article saved"
    checkout values
    merge inbox id: "reset — reviewed"
    checkout vault
    merge values id: "vault grows deeper"
```

two repositories — one public, one private — symlinked into a single vault your editor sees as one. one branch for the structure, one branch for your life. schema changes flow in one direction. your data never touches the template.

---

[philosophy](PHILOSOPHY.md) &nbsp;·&nbsp; [how it works](vault/00-system/SYSTEM.md) &nbsp;·&nbsp; [how to use it](vault/00-system/GUIDE.md) &nbsp;·&nbsp; [set it up](SETUP.md)

---

## reference

| document | purpose |
|----------|---------|
| [`PHILOSOPHY.md`](PHILOSOPHY.md) | why the system is shaped the way it is |
| [`SETUP.md`](SETUP.md) | full bootstrap: layout, git, symlinks, tooling |
| [`REPO-MANAGEMENT.md`](REPO-MANAGEMENT.md) | repo hygiene: PRs, branches, CI, changelog |
| [`vault/00-system/SYSTEM.md`](vault/00-system/SYSTEM.md) | full spec: schema, folder weights, cascade protocol, weekly ritual |
| [`vault/00-system/GUIDE.md`](vault/00-system/GUIDE.md) | day-to-day: capturing, inbox, projects, committing |
| [`vault/00-system/PRAXIS.md`](vault/00-system/PRAXIS.md) | how you operate: agency, decisions, known failure modes |
| [`vault/00-system/ANXIETIES.md`](vault/00-system/ANXIETIES.md) | anxiety tracker: structured challenge and resolution |
| [`vault/00-system/SCHEMA-CHANGELOG.md`](vault/00-system/SCHEMA-CHANGELOG.md) | schema version history; referenced when merging main → personal |

---

[CC BY 4.0](LICENSE)
