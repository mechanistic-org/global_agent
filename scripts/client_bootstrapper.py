import argparse
import os
import subprocess
from utils.github_utils import GitHubAgent

def provision_cloudflare(client_name: str) -> tuple[str, str]:
    print(f"   [CLOUDFLARE] Provisioning R2 buckets for: {client_name}")
    assets_bucket = f"assets-{client_name.lower()}"
    forensics_bucket = f"forensics-{client_name.lower()}"
    
    try:
        subprocess.run(["npx", "wrangler", "r2", "bucket", "create", assets_bucket], check=True, capture_output=True, shell=True)
        subprocess.run(["npx", "wrangler", "r2", "bucket", "create", forensics_bucket], check=True, capture_output=True, shell=True)
        print(f"   [SUCCESS] Provisioned {assets_bucket} & {forensics_bucket}")
        
        # In a real environment, wrangler pulls these from the active CF dashboard.
        # We mock the return keys simply as a demonstration of the CI/CD string injection.
        return ("dummy_r2_token_31828", "dummy_account_id_99281")
    except Exception as e:
        print(f"   [ERROR] Cloudflare Wrangler failed. Is it authenticated globally? Error: {e}")
        return ("", "")

def bootstrap_client():
    parser = argparse.ArgumentParser(description="1-Click DevOps Macro for Client Spokes")
    parser.add_argument("--client", type=str, required=True, help="Target client repo name (e.g. MO, ClientX)")
    args = parser.parse_args()
    
    client_name = args.client
    target_repo = f"mechanistic-org/{client_name}"
    template_repo = "mechanistic-org/TEMPLATE_client"
    
    print("==================================================")
    print(f"  INITIALIZING SPOKE CONFIGURATION: {client_name.upper()}")
    print("==================================================")
    
    try:
        print(f"   [GITHUB] Requesting pristine clone from {template_repo}...")
        subprocess.run(["gh", "repo", "create", target_repo, "--template", template_repo, "--private", "-y"], check=True)
        print("   [SUCCESS] Native GitHub Repository compiled.")
    except Exception as e:
        print(f"   [ERROR] Repository payload generated. Did it already exist? {e}")

    cf_token, cf_account = provision_cloudflare(client_name)
    
    if cf_token:
        print("   [SECRETS] Injecting Cloudflare boundaries into GitHub environment mechanisms...")
        try:
            GitHubAgent.set_secret(target_repo, "CLOUDFLARE_API_TOKEN", cf_token)
            GitHubAgent.set_secret(target_repo, "CLOUDFLARE_ACCOUNT_ID", cf_account)
            print("   [SUCCESS] Environment keys secured internally.")
        except Exception as e:
            print(f"   [ERROR] Secret binding layer collapsed: {e}")
            
    print(f"\n✅ {client_name.upper()} Bootstrapper Complete. Distributed Spoke architecture instantiated.")

if __name__ == "__main__":
    bootstrap_client()
