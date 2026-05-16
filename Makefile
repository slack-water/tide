.PHONY: lint validate links spell check all

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
