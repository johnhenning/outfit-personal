# Personal Outfit profile guide

- This repository is public. Keep only nonsecret personal app selections here, layered over the general outfit-profiles templates. Personal config files belong in johnhenning/dotfiles; do not duplicate them here or select general config presets in these personal profiles.
- Keep credentials, SSH private keys, private host metadata and synced account data in 1Password or the relevant authenticated service. Version only nonsecret references.
- Never commit .env values, cloud/kube auth caches, browser sessions, local 1Password account config, or rendered secrets.
- Add uniquely named personal profiles; do not silently override public package/role/preset definitions.
- Review changes with `outfit plan --source PUBLIC_DIRECTORY --personal . --profile PERSONAL_PROFILE`.
- Tests/CI may validate data and plans only. Never authenticate to 1Password, contact personal SSH hosts or apply machine changes in CI.
- Public runtime and template release versions are independently pinned. Coordinate schema migrations with Outfit.
