#!/usr/bin/env python3

import subprocess
import sys

# ─────────────────────────────────────────────
# Flag Parsing
# ─────────────────────────────────────────────
args = sys.argv[1:]
FLAG_NO_EXPLAIN = "--no-explain" in args
FLAG_YES = "--yes" in args
FLAG_HELP = "--help" in args or "-h" in args

# ─────────────────────────────────────────────
# Optional Banner Display (coming soon ✨)
# ─────────────────────────────────────────────
def print_banner():
    banner = (
        "\033[1;36m" +  # Bright magenta (classic LORD feel)
        " _____ _ _   _   _      _                 \n"
        "|  __ (_) | | | | |    | |                \n"
        "| |  \\/_| |_| |_| | ___| |_ __   ___ _ __ \n"
        "| | __| | __|  _  |/ _ \\ | '_ \\ / _ \\ '__|\n"
        "| |_\\ \\ | |_| | | |  __/ | |_) |  __/ |   \n"
        " \\____/_|\\__\\_| |_|\\___|_| .__/ \\___|_|   \n"
        "                         | |              \n"
        "                         |_|              \n"
        "\033[0m"  # Reset formatting
    )
    print(banner)

def show_help():
    print("""
Usage: githelper [options]

Options:
  --yes         Automatically confirm all prompts
  --no-explain  Suppress helpful Git explanations
  --help, -h    Show this help message

Description:
  githelper is a friendly Git push assistant that:
    - Confirms your remote repo
    - Checks for untracked files and modified files
    - Offers to stage everything
    - Detects detached HEAD state and explains it
    - Offers diff preview before commit
    - Stages, commits, and pushes your changes
""")
    sys.exit(0)

if FLAG_HELP:
    show_help()

# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────
def run_cmd(cmd, capture_output=True, check_success=False):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=capture_output)
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
    return subprocess.run("git rev-parse --is-inside-work-tree", shell=True,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def get_remote_url():
    result = subprocess.run("git remote get-url origin", shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None

def is_detached_head():
    status = run_cmd("git status", capture_output=True)
    return "HEAD detached" in status if isinstance(status, str) else False

def has_merge_conflict():
    result = subprocess.run("git ls-files -u", shell=True, capture_output=True, text=True)
    return bool(result.stdout.strip())

# ─────────────────────────────────────────────
# Main Flow
# ─────────────────────────────────────────────
def main():
    print_banner()
    
    if not in_git_repo():
        print("❌ Not inside a git repository. Please 'cd' into one first.")
        sys.exit(1)

    remote_url = get_remote_url()
    if not remote_url:
        print("❌ No remote origin URL found. Please set a remote first.")
        sys.exit(1)

    print(f"\n📦 Remote repository detected: {remote_url}")
    if not FLAG_YES:
        confirm_repo = input("\n✅ Is this the correct repository you want to update? (y/n): ").strip().lower()
        if confirm_repo != 'y':
            print("❌ Aborted to prevent mistakes.")
            sys.exit(0)

    # Detect detached HEAD
    if is_detached_head():
        print("⚠️  Detached HEAD state detected!")
        if not FLAG_NO_EXPLAIN:
            print("""
📘 Detached HEAD means:
    - You’re on a specific commit, not a branch
    - Commits made now could be lost if you switch away
💡 Create a branch to save changes:
    git checkout -b my-branch
""")

    # Detect merge conflicts
    if has_merge_conflict():
        print("❌ Merge conflict detected! Resolve it before continuing.")
        print("💡 Use `git status` and `git mergetool` to resolve conflicts.")
        sys.exit(1)

    # Get status
    print("\n🔍 Checking git status...\n")
    status_raw = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
    status_output = status_raw.stdout.strip()

    if not status_output:
        print("✅ Working directory clean. Nothing to commit.")
        sys.exit(0)
    else:
        print(status_output)

    # Detect untracked files
    untracked_detected = any(line.startswith("??") for line in status_output.splitlines())
    if untracked_detected:
        print("\n⚠️ You have untracked files! These won't be included unless you add them.")
        if FLAG_YES or input("→ Add all untracked files now? [y/n]: ").strip().lower() == 'y':
            if not run_cmd("git add .", capture_output=False, check_success=True):
                print("❌ git add failed.")
                sys.exit(1)
            print("✅ All files staged.")
        else:
            print("🛑 Leaving untracked files untouched.")
            if not FLAG_YES:
                proceed = input("\nContinue without adding untracked files? [y/n]: ").strip().lower()
                if proceed != 'y':
                    print("❌ Aborted.")
                    sys.exit(0)
    else:
        if FLAG_YES or input("\n✅ Stage all changes and continue? [y/n]: ").strip().lower() == 'y':
            if not run_cmd("git add .", capture_output=False, check_success=True):
                print("❌ git add failed.")
                sys.exit(1)
        else:
            print("❌ Aborted.")
            sys.exit(0)

    # Confirm staged changes
    staged_check = subprocess.run("git diff --cached --quiet", shell=True)
    if staged_check.returncode == 0:
        print("⚠️ No changes staged. Nothing to commit.")
        sys.exit(0)

    if not FLAG_NO_EXPLAIN:
        if FLAG_YES or input("\n👀 Would you like to preview what will be committed? [y/n]: ").strip().lower() == 'y':
            print("\n📋 Staged diff:")
            run_cmd("git diff --cached", capture_output=True)

    # Commit message
    if FLAG_YES:
        commit_msg = "Update files"
    else:
        while True:
            commit_msg = input("\n📝 Enter your commit message: ").strip()
            if commit_msg:
                break
            print("⚠️ Commit message cannot be empty.")

    # Commit
    commit_result = subprocess.run(f'git commit -m "{commit_msg}"', shell=True, text=True, capture_output=True)
    if commit_result.returncode != 0:
        output = (commit_result.stdout + commit_result.stderr).strip().lower()
        if "nothing to commit" in output:
            print("⚠️ Nothing to commit. Working tree is clean.")
        else:
            print("❌ Error committing.")
            print(commit_result.stdout)
            print(commit_result.stderr)
        sys.exit(1)
    else:
        print("\n✅ Commit successful!\n")
        print(commit_result.stdout.strip())

    # Push
    if FLAG_YES or input("\n🚀 Ready to push to GitHub? [y/n]: ").strip().lower() == 'y':
        if not run_cmd("git push", capture_output=True, check_success=True):
            print("❌ Error pushing to GitHub.")
            print("💡 Tip: You may need to run `git pull --rebase origin main` or `git push --force`.")
            sys.exit(1)
        print("\n🎉✅ All done! Your changes are pushed!")
    else:
        print("❌ Push canceled.")

if __name__ == "__main__":
    main()

