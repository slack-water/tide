---
title: Dev Environment
created: 2026-05-20
updated: 2026-05-20
folder: 60
type: reference
status: active
importance: 3
schema-version: 1.0
ai-assisted: true
---

# Dev Environment

*the specification for my personal computing environment. opinionated and specific enough to hand to claude and get real config files back. when setting up a new machine, start here.*

> **trim note:** after a few weeks of regular use, run `history | awk '{print $1}' | sort | uniq -c | sort -rn | head -50` and share the output. prune packages from the cli toolkit that aren't showing up.

---

## the vibe

warm, focused, slightly anachronistic. the aesthetic is amber CRT — the terminal as a tool with weight and presence, not a chrome app. dark background, warm amber and earth tones, monospaced type that feels like it means business. nothing blinks. nothing pulses. the environment recedes so the work can come forward.

---

## terminal — ghostty

[Ghostty](https://ghostty.org) is the terminal. fast, native, configured in a single flat file at `~/.config/ghostty/config`.

```ini
# ~/.config/ghostty/config

theme = GruvboxDark

font-family = "IBM Plex Mono"
font-size = 14

background-opacity = 1.0
cursor-style = block
cursor-style-blink = false

window-padding-x = 12
window-padding-y = 10

shell-integration = zsh
```

**font:** IBM Plex Mono — designed at IBM, carries the weight of that lineage. feels terminal-native without being a costume.

**theme:** GruvboxDark — warm amber and brown highlights on a deep charcoal background. the canonical warm retro palette. Ghostty ships this theme.

**cursor:** non-blinking block. it sits there. it does not perform.

---

## shell — zsh + oh-my-zsh

oh-my-zsh with a minimal plugin set. no theme bloat. the prompt should tell me what i need and nothing else.

**plugins:**

```bash
# in ~/.zshrc
plugins=(git github)
```

- `git` — git aliases and prompt context (`gst`, `gco`, `gcmsg`, etc.)
- `github` — git shortcuts for github operations, `empty_gh` for new repos

**prompt theme:** `robbyrussell` (omz default) or `af-magic` for slightly more context. keep it single-line. no powerline glyphs that require patched fonts.

**`.zshrc` additions — paste below the omz source line:**

```bash
# ── path ──────────────────────────────────────────────────────────────────────
# homebrew (apple silicon — change to /usr/local for intel)
eval "$(/opt/homebrew/bin/brew shellenv)"

# ── editor ────────────────────────────────────────────────────────────────────
export EDITOR="nvim"
export VISUAL="nvim"
alias vi="nvim"
alias vim="nvim"

# ── tool integrations ─────────────────────────────────────────────────────────
# fzf — fuzzy finder shell bindings (ctrl+r history, ctrl+t file, alt+c cd)
source <(fzf --zsh)

# zoxide — smarter cd; use 'z' instead of 'cd'
eval "$(zoxide init zsh)"

# bat — themed to match gruvbox
export BAT_THEME="gruvbox-dark"

# ── aliases ───────────────────────────────────────────────────────────────────
# navigation
alias ..="cd .."
alias ...="cd ../.."
alias cat="bat"                        # bat replaces cat
alias ls="eza"                         # eza replaces ls
alias ll="eza -lah --git"             # long list with git status
alias lt="eza --tree --level=2"       # tree view

# git (beyond omz)
alias gs="git status"
alias gl="git log --oneline --graph --decorate"

# tools
alias top="btop"
alias du="ncdu"
alias find="fd"
```

**gitconfig additions for delta:**

```ini
# ~/.gitconfig
[core]
    pager = delta
[interactive]
    diffFilter = delta --color-only
[delta]
    navigate = true
    side-by-side = true
    syntax-theme = gruvbox-dark
```

---

## editor — neovim

neovim with `lazy.nvim` as the plugin manager. config lives at `~/.config/nvim/`. the goal is a terminal editor that does what an IDE does without requiring a mouse or an electron app.

`ripgrep`, `fd`, and `fzf` must be installed (see cli toolkit) — telescope uses all three.

### core behavior

```lua
-- options (lua/options.lua or init.lua)
vim.opt.number = true           -- line numbers
vim.opt.relativenumber = true   -- relative numbers (easy jumping with [n]j/[n]k)
vim.opt.cursorline = true       -- highlight current line
vim.opt.signcolumn = "yes"      -- always show sign column (no layout shift)
vim.opt.wrap = false            -- no line wrap
vim.opt.scrolloff = 8           -- keep 8 lines above/below cursor
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.termguicolors = true    -- full color support
```

### plugin list

```lua
-- lazy.nvim plugin spec
{
  -- colorscheme
  { "ellisonleao/gruvbox.nvim",
    priority = 1000,
    config = function()
      require("gruvbox").setup({ contrast = "hard" })
      vim.cmd("colorscheme gruvbox")
    end },

  -- syntax highlighting
  { "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter.configs").setup({
        ensure_installed = { "lua", "python", "javascript", "typescript",
                             "bash", "markdown", "yaml", "json" },
        highlight = { enable = true },
        indent   = { enable = true },
      })
    end },

  -- status line
  { "nvim-lualine/lualine.nvim",
    config = function()
      require("lualine").setup({ options = { theme = "gruvbox" } })
    end },

  -- file explorer
  { "nvim-tree/nvim-tree.lua",
    config = function()
      require("nvim-tree").setup()
    end },

  -- fuzzy finder — uses ripgrep (live_grep) and fd (find_files) automatically
  { "nvim-telescope/telescope.nvim",
    dependencies = {
      "nvim-lua/plenary.nvim",
      { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
    },
    config = function()
      local telescope = require("telescope")
      telescope.setup({
        defaults = {
          vimgrep_arguments = {
            "rg", "--color=never", "--no-heading", "--with-filename",
            "--line-number", "--column", "--smart-case",
          },
        },
        pickers = {
          find_files = {
            find_command = { "fd", "--type", "f", "--strip-cwd-prefix" },
          },
        },
      })
      telescope.load_extension("fzf")
    end },

  -- lazygit inside neovim
  { "kdheepak/lazygit.nvim",
    dependencies = { "nvim-lua/plenary.nvim" } },

  -- completion
  { "hrsh7th/nvim-cmp",
    dependencies = {
      "hrsh7th/cmp-nvim-lsp",
      "hrsh7th/cmp-buffer",
      "hrsh7th/cmp-path",
    }},

  -- lsp
  { "neovim/nvim-lspconfig" },
  { "williamboman/mason.nvim",           config = true },
  { "williamboman/mason-lspconfig.nvim" },

  -- pairs and surround
  { "windwp/nvim-autopairs", event = "InsertEnter", config = true },
  { "kylechui/nvim-surround",            config = true },

  -- git signs in gutter
  { "lewis6991/gitsigns.nvim",           config = true },

  -- comment toggle
  { "numToStr/Comment.nvim",             config = true },
}
```

### key mappings

```lua
-- leader key
vim.g.mapleader = " "

-- file explorer
vim.keymap.set("n", "<leader>e",  ":NvimTreeToggle<CR>")

-- telescope
vim.keymap.set("n", "<leader>ff", "<cmd>Telescope find_files<cr>")
vim.keymap.set("n", "<leader>fg", "<cmd>Telescope live_grep<cr>")
vim.keymap.set("n", "<leader>fb", "<cmd>Telescope buffers<cr>")

-- lazygit
vim.keymap.set("n", "<leader>lg", ":LazyGit<CR>")

-- lsp (set in lsp on_attach)
-- gd           → go to definition
-- gr           → references
-- K            → hover docs
-- <leader>rn   → rename
```

---

## cli toolkit

all installed via homebrew. every package here lands on `$PATH` automatically via the `brew shellenv` line in `.zshrc`.

```bash
# formulae
brew install \
  tree bat ripgrep fzf fd jq gh tmux \
  eza zoxide btop wget ncdu tldr \
  yazi hyperfine lazygit glow git-delta \
  neovim

# post-install: fzf shell bindings
# (handled by 'source <(fzf --zsh)' in .zshrc — no separate step needed)
```

| package | command | what it does |
|---------|---------|-------------|
| `tree` | `tree` | directory tree visualization |
| `bat` | `bat` / aliased to `cat` | cat with syntax highlighting |
| `ripgrep` | `rg` | fast grep — powers telescope live_grep |
| `fzf` | `fzf` | fuzzy finder — ctrl+r history, ctrl+t files |
| `fd` | `fd` | fast find — powers telescope find_files |
| `jq` | `jq` | json processor and pretty-printer |
| `gh` | `gh` | github cli |
| `tmux` | `tmux` | persistent terminal sessions, split panes |
| `eza` | `eza` / aliased to `ls` | modern ls with git status |
| `zoxide` | `z` | frecency-based cd — `z tide` jumps to ~/code/tide |
| `btop` | `btop` / aliased to `top` | process and resource monitor |
| `wget` | `wget` | http downloader |
| `ncdu` | `ncdu` / aliased to `du` | disk usage ncurses ui |
| `tldr` | `tldr` | simplified man pages with examples |
| `yazi` | `yazi` | terminal file manager |
| `hyperfine` | `hyperfine` | cli benchmarking |
| `lazygit` | `lazygit` / `<leader>lg` in nvim | terminal ui for git |
| `glow` | `glow` | markdown renderer — `glow vault/00-system/VALUES.md` |
| `git-delta` | `delta` | syntax-highlighted git diffs (configured via gitconfig) |

---

## colorscheme — gruvbox dark

the single theme across terminal, editor, and anything else that takes a color scheme.

**palette reference:**

| role | color | hex |
|------|-------|-----|
| background | dark0 hard | `#1d2021` |
| background soft | dark0 | `#282828` |
| foreground | light1 | `#ebdbb2` |
| red | bright_red | `#fb4934` |
| green | bright_green | `#b8bb26` |
| yellow | bright_yellow | `#fabd2f` |
| blue | bright_blue | `#83a598` |
| purple | bright_purple | `#d3869b` |
| aqua | bright_aqua | `#8ec07c` |
| orange | bright_orange | `#fe8019` |

**use `contrast = "hard"`** in gruvbox.nvim for the darkest background. medium and soft are warmer but harder to read in bright environments.

---

## new machine checklist

```bash
# 1. homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/opt/homebrew/bin/brew shellenv)"   # add to .zshrc permanently afterward

# 2. core tools + cli toolkit
brew install \
  git zsh neovim \
  tree bat ripgrep fzf fd jq gh tmux \
  eza zoxide btop wget ncdu tldr \
  yazi hyperfine lazygit glow git-delta

# 3. casks
brew install --cask ghostty font-ibm-plex-mono

# 4. oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 5. configure .zshrc
#    - set plugins=(git github)
#    - paste the .zshrc additions block from the shell section above

# 6. configure gitconfig
#    - paste the delta block from the shell section above

# 7. ghostty config
#    - write ~/.config/ghostty/config (see terminal section above)

# 8. neovim
#    - create ~/.config/nvim/init.lua
#    - bootstrap lazy.nvim (see https://github.com/folke/lazy.nvim#-installation)
#    - paste plugin list and keymaps
#    - open nvim — lazy installs everything on first launch
#    - run :TSUpdate

# 9. wire the vault
#    - clone tide and tide-private to ~/code/
#    - run: make install (from ~/code/tide/)
```
