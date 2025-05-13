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
FLAG_PREVIEW = "--preview" in args  # NEW

# ─────────────────────────────────────────────
# Optional Banner Display
# ─────────────────────────────────────────────
def print_banner():
    banner = (
        "\033[1;36m" +
        " _____ _ _   _   _      _                 \n"
        "|  __ (_) | | | | |    | |                \n"
        "| |  \\/_| |_| |_| | ___| |_ __   ___ _ __ \n"
        "| | __| | __|  _  |/ _ \\ | '_ \\ / _ \\ '__|\n"
        "| |_\\ \\ | |_| | | |  __/ | |_) |  __/ |   \n"
        " \\____/_|\\__\\_| |_|\\___|_| .__/ \\___|_|   \n"
        "                         | |              \n"
        "                         |_|              \n"
        "\033[0m"
    )
    print(banner)

# ─────────────────────────────────────────────
# Help Output
# ─────────────────────────────────────────────
def show_help():
    print("""
Usage: githelper [options]

Options:
  --yes         Automatically confirm all prompts
  --no-explain  Suppress helpful Git explanations
  --preview     Ask to preview the commit diff before committing
  --help, -h    Show this help message

Description:
  githelper is a friendly Git push assistant that:
    - Confirms your remote repo
    - Checks for untracked or modified files
    - Offers to stage, commit, and push
    - Detects detached HEAD state and explains it
    - Warns on merge conflicts
""")
    sys.exit(0)

# ─────────────────────────────────────────────
# Utility Functions
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
# Main Logic
# ─────────────────────────────────────────────
def main():
    if FLAG_HELP:
        show_help()

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

    # Detached HEAD warning
    if is_detached_head():
        print("⚠️  Detached HEAD state detected!")
        if not FLAG_NO_EXPLAIN:
            print("""
📘 Detached HEAD means:
    - You're on a specific commit, not a branch.
    - Commits made now could be lost.
💡 Create a branch to save your work:
    git checkout -b my-fix-branch
""")

    # Conflict check
    if has_merge_conflict():
        print("❌ Merge conflict detected! Resolve it before continuing.")
        print("💡 Use `git status` and `git mergetool` to resolve conflicts.")
        sys.exit(1)

    # Git status check
    print("\n🔍 Checking git status...\n")
    status_raw = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
    status_output = status_raw.stdout.strip()

    if not status_output:
        print("✅ Working directory clean. Nothing to commit.")
        sys.exit(0)
    else:
        print(status_output)

    # Handle untracked files
    untracked_detected = any(line.startswith("??") for line in status_output.splitlines())
    if untracked_detected:
        print("\n⚠️ You have untracked files.")
        if FLAG_YES or input("→ Add all untracked files now? [y/n]: ").strip().lower() == 'y':
            if not run_cmd("git add .", capture_output=False, check_success=True):
                print("❌ git add failed.")
                sys.exit(1)
            print("✅ All files staged.")
        else:
            print("🛑 Leaving untracked files untouched.")
            if not FLAG_YES:
                proceed = input("Continue without them? [y/n]: ").strip().lower()
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

    # Confirm staging
    staged_check = subprocess.run("git diff --cached --quiet", shell=True)
    if staged_check.returncode == 0:
        print("⚠️ No changes staged. Nothing to commit.")
        sys.exit(0)

    # Diff preview (only if --preview passed)
    if FLAG_PREVIEW:
        if FLAG_YES or input("\n👀 Would you like to preview what will be committed? [y/n]: ").strip().lower() == 'y':
            print("\n📋 Staged diff:\n")
            run_cmd("git diff --cached", capture_output=True)

    # Commit
    if FLAG_YES:
        commit_msg = "Update files"
    else:
        while True:
            commit_msg = input("\n📝 Enter your commit message: ").strip()
            if commit_msg:
                break
            print("⚠️ Commit message cannot be empty.")

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
            print("💡 Tip: Try `git pull --rebase` or `git push --force` if needed.")
            sys.exit(1)
        print("\n🎉✅ All done! Your changes are pushed!")
    else:
        print("❌ Push canceled.")

if __name__ == "__main__":
    main()

