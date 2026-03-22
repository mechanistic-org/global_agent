import subprocess

class GitHubAgent:
    """
    Standardized utility for handling GitHub operations via the `gh` CLI.
    Replaces brute-force subprocess calls with structured, error-handled methodology.
    """
    
    @staticmethod
    def run_cmd(args: list[str], cwd: str = None) -> str:
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=True, cwd=cwd)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"GitHub CLI Error: {e.stderr.strip() or e.stdout.strip()}")

    @classmethod
    def clone_repo(cls, org_repo: str, target_dir: str):
        return cls.run_cmd(["gh", "repo", "clone", org_repo, target_dir])

    @classmethod
    def create_pr(cls, title: str, body: str, head_branch: str, base_branch: str = "main", cwd: str = None):
        return cls.run_cmd(["gh", "pr", "create", "--title", title, "--body", body, "--head", head_branch, "--base", base_branch], cwd=cwd)

    @classmethod
    def set_secret(cls, repo: str, secret_name: str, secret_value: str):
        # We use Popen instead of run_cmd since secrets must be piped via fast stdin
        process = subprocess.Popen(["gh", "secret", "set", secret_name, "--repo", repo], stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=secret_value)
        if process.returncode != 0:
            raise RuntimeError(f"Failed to set secret {secret_name}: {stderr.strip()}")
        return f"Secret {secret_name} successfully set for {repo}."
