---
description: The official protocol for syncing local *-assets staging directories to Cloudflare R2 buckets.
---
# R2 Asset Sync Workflow

Syncs a local `{project}-assets/R2_STAGING/` directory to its corresponding Cloudflare R2 bucket via `sync_r2.py`.

## Project → Bucket Map
| `--target` | Local Dir | R2 Bucket |
|---|---|---|
| `eriknorris` | `eriknorris-assets/R2_STAGING` | `assets-eriknorris-com` |
| `mechanistic` | `mechanistic-assets/R2_STAGING` | `assets-mechanistic-com` |
| `mootmoat` | `mootmoat-assets/R2_STAGING` | `assets-mootmoat-com` |
| `moreplay` | `moreplay-assets/R2_STAGING` | `assets-moreplay-com` |
| `MO` | `MO-assets/R2_STAGING` | `assets-mo` |
| `hyphen` | `hyphen-assets/R2_STAGING` | `assets-hyphen-com` |

## Usage

1. Dry run first to preview changes.
// turbo
```powershell
python scripts/sync_r2.py --target mechanistic --dry-run
```

2. Additive sync (upload new/changed, keep remote orphans).
// turbo
```powershell
python scripts/sync_r2.py --target mechanistic
```

3. Mirror sync (upload + prune remote orphans — use carefully).
```powershell
python scripts/sync_r2.py --target mechanistic --prune
```

## Adding a New Project
Add an entry to `BUCKET_MAP` and `dir_name_map` in `scripts/sync_r2.py`, create the R2 bucket in Cloudflare, and create `D:\GitHub\{project}-assets\R2_STAGING\`.
