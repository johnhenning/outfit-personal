# Personal Outfit profile guide

- This repository is private. Keep personal selections and optional nonsecret host metadata here, layered over public outfit-profiles.
- A private repository is not a secret store. Keep credentials and SSH private keys in 1Password. Version only references.
- Never commit .env values, cloud/kube auth caches, browser sessions, local 1Password account config, or rendered secrets.
- Add uniquely named personal profiles; do not silently override public package/role/preset definitions.
- Review changes with `outfit plan --source PUBLIC_DIRECTORY --personal . --profile PERSONAL_PROFILE`.
- Tests/CI may validate data and plans only. Never authenticate to 1Password, contact personal SSH hosts or apply machine changes in CI.
- Public runtime and template release versions are independently pinned. Coordinate schema migrations with Outfit.
