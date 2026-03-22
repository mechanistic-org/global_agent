import os
import boto3
import mimetypes
import argparse
from botocore.exceptions import NoCredentialsError

# Import centralized configuration mapping
from global_config import get_repo_root

# ─── Canonical Project → R2 Bucket Map ───────────────────────────────────────
# All projects use the {project}-assets/R2_STAGING/ local staging pattern.
# Add new projects here as they are onboarded.
BUCKET_MAP = {
    'eriknorris':  'assets-eriknorris-com',
    'portfolio':   'assets-eriknorris-com',   # portfolio-assets still feeds eriknorris bucket
    'mechanistic': 'assets-mechanistic-com',
    'mootmoat':    'assets-mootmoat-com',
    'moreplay':    'assets-moreplay-com',
    'MO':          'assets-mo',
    'hyphen':      'assets-hyphen-com',
}

def get_r2_credentials(target: str) -> dict:
    """Extracts R2 credentials from the global environment.
    
    Bucket name is resolved from BUCKET_MAP based on --target,
    not from a single R2_BUCKET_NAME env var (which caused cross-bucket uploads).
    """
    bucket = BUCKET_MAP.get(target)
    if not bucket:
        known = ', '.join(BUCKET_MAP.keys())
        raise ValueError(f"Unknown target '{target}'. Known targets: {known}")
    return {
        'ACCOUNT_ID':       os.getenv('R2_ACCOUNT_ID'),
        'ACCESS_KEY_ID':    os.getenv('R2_ACCESS_KEY_ID'),
        'SECRET_ACCESS_KEY': os.getenv('R2_SECRET_ACCESS_KEY'),
        'BUCKET_NAME':      bucket,
    }

def get_r2_client(creds):
    """Creates the boto3 client for Cloudflare R2."""
    try:
        return boto3.client(
            's3',
            endpoint_url=f"https://{creds['ACCOUNT_ID']}.r2.cloudflarestorage.com",
            aws_access_key_id=creds['ACCESS_KEY_ID'],
            aws_secret_access_key=creds['SECRET_ACCESS_KEY'],
            region_name='auto' # Required for R2
        )
    except Exception as e:
        print(f"❌ Error creating R2 client: {e}")
        return None

def get_remote_files(s3, bucket_name):
    """Returns a set of all keys in the bucket."""
    print("📋 Fetching remote file list...")
    paginator = s3.get_paginator('list_objects_v2')
    remote_keys = set()
    try:
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                for obj in page['Contents']:
                    remote_keys.add(obj['Key'])
    except Exception as e:
        print(f"❌ Error fetching remote list: {e}")
        return None
    return remote_keys

def get_target_directory(target_repo: str) -> str:
    """
    Resolves the local R2_STAGING directory for the specified project.
    
    All projects use the universal pattern:
      D:\\GitHub\\{project}-assets\\R2_STAGING\\
    
    The 'eriknorris' special case (which originated this pattern) is now
    handled the same as every other project.
    """
    # Handle naming quirks between target alias and local dir name
    dir_name_map = {
        'eriknorris':  'eriknorris-assets',
        'portfolio':   'portfolio-assets',
        'mechanistic': 'mechanistic-assets',
        'mootmoat':    'mootmoat-assets',
        'moreplay':    'moreplay-assets',
        'MO':          'MO-assets',
        'hyphen':      'hyphen-assets',
    }
    dir_name = dir_name_map.get(target_repo, f"{target_repo}-assets")
    base_path = get_repo_root(dir_name)
    staging = base_path / 'R2_STAGING'
    if not staging.exists():
        raise FileNotFoundError(
            f"R2_STAGING not found at '{staging}'. "
            f"Create the directory first: mkdir '{staging}'"
        )
    return str(staging)

def sync_assets():
    parser = argparse.ArgumentParser(description="Global Sync Assets to Cloudflare R2")
    parser.add_argument('--target', type=str, required=True, help="The target repository name to sync from (e.g., eriknorris, mechanistic)")
    parser.add_argument('--prune', action='store_true', help="Delete remote files that do not exist locally")
    parser.add_argument('--dry-run', action='store_true', help="Show what would happen without making changes")
    parser.add_argument('--force', action='store_true', help="Force upload even if sizes match")
    args = parser.parse_args()

    try:
        creds = get_r2_credentials(args.target)
    except ValueError as e:
        print(f"❌ {e}")
        return

    env_creds = [creds['ACCOUNT_ID'], creds['ACCESS_KEY_ID'], creds['SECRET_ACCESS_KEY']]
    if not all(env_creds):
        print("❌ Missing R2 credentials in global .env file. Required: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY")
        return

    s3 = get_r2_client(creds)
    if not s3: return


    try:
        staging_dir = get_target_directory(args.target)
    except FileNotFoundError as e:
        print(e)
        return

    staging_path = os.path.normpath(staging_dir)

    action_label = "Syncing (Mirror)" if args.prune else "Syncing (Additive)"
    if args.dry_run: action_label += " [DRY RUN]"
    if args.force: action_label += " [FORCE]"
    
    print(f"🚀 Starting {action_label}")
    print(f"   Target Repo Context: {args.target}")
    print(f"   Local Source: {staging_path}")
    print(f"   Cloudflare Bucket: {creds['BUCKET_NAME']}")
    
    if not os.path.exists(staging_path):
        print(f"❌ Error: Staging directory '{staging_path}' not found.")
        return

    uploaded_count = 0
    skipped_count = 0
    deleted_count = 0
    error_count = 0
    
    local_files_set = set()

    # --- 1. UPLOAD & UPDATE ---
    for root, dirs, files in os.walk(staging_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, staging_path)
            s3_key = relative_path.replace('\\', '/') # Ensure forward slashes
            local_files_set.add(s3_key)

            # Determine Content-Type
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                content_type = 'application/octet-stream'
            if file.lower().endswith('.svg'):
                content_type = 'image/svg+xml'

            try:
                # Check for existing
                should_upload = True
                if not args.force:
                    try:
                        metadata = s3.head_object(Bucket=creds['BUCKET_NAME'], Key=s3_key)
                        remote_size = metadata['ContentLength']
                        local_size = os.path.getsize(local_path)
                        
                        if remote_size == local_size:
                            skipped_count += 1
                            should_upload = False
                    except:
                        # File doesn't exist, proceed
                        pass

                if should_upload:
                    if args.dry_run:
                        print(f"📝 [DRY RUN] Would upload: {s3_key} ({content_type})")
                        uploaded_count += 1
                    else:
                        print(f"⬆️  Uploading {s3_key} ({content_type})...")
                        with open(local_path, 'rb') as data:
                            s3.put_object(
                                Bucket=creds['BUCKET_NAME'],
                                Key=s3_key,
                                Body=data,
                                ContentType=content_type
                            )
                        uploaded_count += 1

            except Exception as e:
                print(f"❌ Failed to process {s3_key}: {e}")
                error_count += 1
    
    # --- 2. PRUNE (If requested) ---
    if args.prune:
        remote_files = get_remote_files(s3, creds['BUCKET_NAME'])
        if remote_files is not None:
            orphans = remote_files - local_files_set
            
            if orphans:
                print(f"\n🗑️  Found {len(orphans)} orphaned files in R2...")
                for key in orphans:
                    if args.dry_run:
                        print(f"📝 [DRY RUN] Would delete: {key}")
                        deleted_count += 1
                    else:
                        print(f"🔥 Deleting: {key}")
                        try:
                            s3.delete_object(Bucket=creds['BUCKET_NAME'], Key=key)
                            deleted_count += 1
                        except Exception as e:
                            print(f"❌ Failed to delete {key}: {e}")
                            error_count += 1
            else:
                print("\n✨ No orphaned files found.")

    print(f"\n✅ {action_label} Complete.")
    print(f"   Uploaded: {uploaded_count}")
    print(f"   Skipped:  {skipped_count}")
    if args.prune:
        print(f"   Deleted:  {deleted_count}")
    print(f"   Errors:   {error_count}")

if __name__ == "__main__":
    sync_assets()
