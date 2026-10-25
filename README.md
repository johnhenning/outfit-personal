# Personal Outfit profiles

Private personal selections layered on the public outfit-profiles bundle. This repo contains profile choices, optional private host metadata, and references to credentials. Secret values and private SSH keys belong in 1Password.

Initial profiles (`john-dev`, `john-compute`, `john-media`) are proposed starting selections based on the workstation inventory; review them in Outfit before applying.

```sh
outfit personalize --repo johnhenning/outfit-personal
outfit plan --source /path/to/public/profiles --personal /private/overlay/path --profile john-dev
```

GitHub sign-in is required only when fetching this repository. 1Password CLI/SSH agent authorization is separate and occurs when credentials are actually used. Never commit auth caches, .env files with secret values, private keys, or resolved secret templates.
