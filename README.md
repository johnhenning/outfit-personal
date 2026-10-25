# Personal Outfit profiles

Public, nonsecret personal selections layered on the general outfit-profiles
bundle. Profile choices and static configs can be downloaded without GitHub
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

Everyday selects only the SSH baseline/include and 1Password agent fragment.
Dev additionally selects shell, tmux, Git ignore/config, and a small Neovim
starter config. These are reviewed starting configs, not copies of the current
workstation's full settings or plugin setup. Local include files keep additional
settings separate. Existing private SSH files always require manual merging.

`john-dev` is a compatibility name for the same explicit Mac Dev selections;
it now means a Mac desktop, not a portable development environment. The schema
has no profile platform constraint; the Mac-specific choices are unsupported on
other platforms. `john-compute` and `john-media` are still unreviewed starting
profiles. Their existing package and dotfile selections are retained for later
review.

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
  The SSH fragment uses the documented Mac agent socket; it does not export keys
  or authorize requests. Keep host entries in local SSH fragments and identity
  or signing choices in `~/.config/git/local.config`.
- Oh My Zsh and Powerlevel10k remain guided manual installs in the runtime.
  The shell enables the theme only once its files are present. Keep prompt
  customization in `~/.p10k.zsh` and machine settings in `~/.zshrc.machine`.

Use the updated public profiles with these configs: the generic public shell
loads the private `.zshrc.local`, which owns the personal shell preferences.
Package setup and dotfile application are separate; preview both before applying.

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
