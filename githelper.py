#!/usr/bin/env python3

import subprocess
import sys

def run_cmd(cmd, capture_output=True, check_success=False):
    """Run a system command."""
    result = subprocess.run(cmd, shell=True, text=True,
                             capture_output=capture_output)
    if not capture_output:
        return result.returncode == 0
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if check_success:
        return result.returncode == 0
    return result

def in_git_repo():
    """Check if inside a git repo."""
    return subprocess.run("git rev-parse --is-inside-work-tree", shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def get_remote_url():
    """Get the remote origin URL."""
    result = subprocess.run("git remote get-url origin", shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def main():
    if not in_git_repo():
        print("❌ Not inside a git repository. Please 'cd' into one first.")
        sys.exit(1)

    remote_url = get_remote_url()
    if not remote_url:
        print("❌ No remote origin URL found. Please set a remote first.")
        sys.exit(1)

    print(f"\n📦 Remote repository detected: {remote_url}")

    confirm_repo = input("\n✅ Is this the correct repository you want to update? (y/n): ").strip().lower()
    if confirm_repo != 'y':
        print("❌ Aborted to prevent mistakes.")
        sys.exit(0)

    print("\n🔍 Checking git status...\n")
    if not run_cmd("git status", capture_output=True, check_success=True):
        print("❌ Error running git status.")
        sys.exit(1)

    confirm = input("\n✅ Does everything look correct? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Aborted.")
        sys.exit(0)

    if not run_cmd("git add .", capture_output=False, check_success=True):
        print("❌ Error running git add.")
        sys.exit(1)

    # Commit message loop
    while True:
        commit_msg = input("\n📝 Enter your commit message: ").strip()
        if commit_msg:
            break
        print("⚠️ Commit message cannot be empty. Please enter a message.")

    # Try to commit
    commit_result = subprocess.run(f'git commit -m "{commit_msg}"', shell=True, text=True, capture_output=True)

    # Analyze commit output
    if commit_result.returncode != 0:
        output = (commit_result.stdout + commit_result.stderr).lower()
        if "nothing to commit" in output or "working tree clean" in output:
            print("\n⚠️ Nothing to commit. Working tree is already clean.")
            print("✅ No action needed.\n")
        else:
            print("❌ Error committing.")
            sys.exit(1)
    else:
        print("\n✅ Commit successful!\n")
        print(commit_result.stdout.strip())

    confirm_push = input("\n🚀 Ready to push to GitHub? (y/n): ").strip().lower()
    if confirm_push != 'y':
        print("❌ Push canceled.")
        sys.exit(0)

    if not run_cmd("git push", capture_output=True, check_success=True):
        print("❌ Error pushing to GitHub.")
        print("💡 Tip: You may need to run `git pull --rebase origin main` or `git push --force` if conflicts exist.")
        sys.exit(1)

    print("\n🎉✅ All done! Your changes are pushed!")

if __name__ == "__main__":
    main()

