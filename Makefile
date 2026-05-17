.PHONY: lint validate links spell check all init

MARKDOWN_FILES := $(shell find . -name '*.md' -not -path './.git/*')

lint:
	npx markdownlint-cli2 '**/*.md' '#.git/**'

validate:
	python3 scripts/validate-frontmatter.py

links:
	npx markdown-link-check $(MARKDOWN_FILES) --quiet

spell:
	npx cspell '**/*.md' --no-progress

check: lint validate

all: lint validate links spell

init: ## remove example files after forking — run once
	rm -f vault/00-system/PRAXIS_example.md
	rm -f vault/00-system/VALUES_example.md
	rm -f vault/00-system/ANXIETIES_example.md
	rm -f vault/00-system/FAILURE-MODES_example.md
	@echo "example files removed. your vault is ready."

upgrade: ## tag notes with outdated schema-version as needs-review
	python3 scripts/schema-upgrade.py
