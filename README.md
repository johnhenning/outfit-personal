# Personal Outfit profiles

Public, nonsecret personal selections layered on the general outfit-profiles
bundle. Profile choices can be downloaded without GitHub
sign-in. Credentials, private host metadata, SSH private keys, sessions and synced
account data belong in 1Password or the relevant authenticated service.

## Mac profiles

`john-mac-everyday` and `john-mac-dev` have independent, explicit selections.
Neither inherits the other or the public software presets. Editing Everyday
will not add apps to Dev. Their empty desktop role supplies no software defaults.

- Everyday: 1Password, ChatGPT, Claude, Obsidian, Dia, Notion, Spotify, Setapp,
  CleanShot X and Paste through Setapp, Bartender, Rectangle Pro, and Raycast.
- Dev: explicitly includes 1Password, ChatGPT, Claude, Obsidian, Dia and Notion,
  plus the reviewed development tools: Git/GitHub CLI, curl, uv, jq, CMake,
  Ninja, Node/pnpm, Ruff, pre-commit, Rust, Tailscale, Zsh/Oh My Zsh/Powerlevel10k,
  tmux, ripgrep, fd, bat, Neovim, Chrome, VS Code, Podman, Ghostty, iTerm2 and Warp.
  Dia, VS Code and iTerm2 are preferred install selections; this does not change
  macOS default-app associations. Neovim remains installed and is the shell editor.

These profiles now select apps only. Personal shell, PATH, tmux, uv, Git and
the preserved workstation NvChad setup live independently in
[johnhenning/dotfiles](https://github.com/johnhenning/dotfiles).
Preview that setup separately:

```sh
curl -fsSL https://raw.githubusercontent.com/johnhenning/dotfiles/main/install.sh | sh
```

Add `--apply` with `sh -s -- --apply` after reviewing. Existing managed configs
are backed up before replacement. Credentials and private SSH hosts remain local;
the 1Password SSH example is opt-in. Previously published bundles keep their
original contents; use the new app-only release when available.

`john-dev` is a compatibility name for the same explicit Mac Dev selections;
it now means a Mac desktop, not a portable development environment. The schema
has no profile platform constraint; the Mac-specific choices are unsupported on
other platforms. `john-compute` and `john-media` are still unreviewed starting
profiles. Their existing package selections are retained for later review;
dotfiles are now managed separately for all personal profiles.

```sh
git clone https://github.com/johnhenning/outfit-personal.git
outfit plan --source /path/to/public/profiles --personal /private/overlay/path --profile john-mac-everyday --target macos-arm64
outfit plan --source /path/to/public/profiles --personal /private/overlay/path --profile john-mac-dev --target macos-arm64
```

Fetching these public selections does not require GitHub sign-in. Sign in to
1Password and individual apps afterward to access credentials and private synced
data. This is a follow-up authentication step, not automatic account/session
restoration. Never commit auth caches, .env files with secret values, private
keys, or resolved secret templates.

## Steps that still need interaction

- Sign in to Setapp and install CleanShot X and Paste there. The plan deliberately
  records manual steps rather than installing independently licensed editions.
- Activate paid software with your own licenses; purchasing is never automated.
- Enable launch at login for Bartender, Rectangle Pro and Raycast, in Everyday
  only. This is a manual action in the install plan, not automatic login-item
  management. Installers can register their own startup defaults; Outfit does not
  audit or disable those. Dev has no requested startup apps.
- Sign in to 1Password and enable its SSH agent in Settings > Developer. Dev also
  installs `op`; enable CLI integration in the app if you want desktop authorization.
  The standalone dotfiles repo includes an optional Mac agent socket example.
  It does not export keys or authorize requests. Keep host entries local and identity
  or signing choices in `~/.config/git/local.config`.
- Oh My Zsh and Powerlevel10k remain guided manual installs in the runtime.
  The shell enables the theme only once its files are present. Keep prompt
  customization in `~/.p10k.zsh`. The standalone dotfiles repo also offers pinned
  optional framework setup with `dotfiles plugins --apply` and machine settings
  under `~/.config/shell/`, `~/.config/zsh/` and `~/.config/bash/`.

Package setup and personal dotfile application are independent; preview both
before applying. Public template dotfiles remain generic and optional.

## Standalone public releases

`scripts/bundle.py` asks Outfit to validate and merge this overlay with an exact
general-profile checkout, then packages only the manifest and its allowlisted
static dotfile sources. Unlisted repository files are excluded. Release CI
builds and attests a deterministic archive with SHA-256 checksums; site scripts
pin that archive independently of the engine. No Git or authentication is needed
on the destination machine to download a standalone public bundle.

General installers live at `https://getoutfit.dev/`. Personal Mac entry points
live at `https://johnhenning.dev/tools/outfit/profiles/mac/everyday.sh` and
`https://johnhenning.dev/tools/outfit/profiles/mac/dev.sh`. Check deployment
status before using new endpoints; the source config alone does not deploy them.

Sources: [Bartender cask](https://formulae.brew.sh/cask/bartender),
[CleanShot on Setapp](https://setapp.com/apps/cleanshot),
[Paste on Setapp](https://setapp.com/apps/paste),
[1Password SSH setup](https://developer.1password.com/docs/ssh/get-started/).
Bartender and the current Paste release require macOS 14 or later; check vendor
requirements for older Macs. Outfit's target architecture check is not an OS
version compatibility check.
