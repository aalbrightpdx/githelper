<!-- # GitHelper -->
<p align="center">
  <img src="assets/githelper.png" alt="githelper banner" width="40%">
</p>

🛠️ A smart, friendly CLI assistant for safely staging, committing, and pushing Git changes — with built-in teaching moments and power-user flags.

---

## ✨ What It Does

- Detects and stages untracked or modified files
- Prompts before committing and pushing
- Explains detached HEAD state when detected
- Prevents commits during merge conflicts
- Shows diff preview before commit (optional)
- Flags to suppress prompts and explanations

---

## 🧰 Clone the GitHelper repository to your system:

Open your terminal and run:

```bash
git clone git@github.com:aalbrightpdx/githelper.git
```

Or, if you prefer HTTPS:

```bash
git clone https://github.com/aalbrightpdx/githelper.git
```

```bash
cd githelper
```

## 🧰 Install

In the project directory:

```bash
pipx install .
```

## 🚀 Usage

Once installed, from any directory run:

```bash
githelper              # Start interactive assistant
githelper --yes        # Auto-confirm everything
githelper --no-explain # Skip explanations
githelper -h           # Show help
```

Example workflow:

```bash
📦 Remote repository detected: git@github.com:your/repo.git
✅ Is this the correct repository you want to update? [y/n]: y
🔍 Checking git status...
✅ Stage all changes and continue? [y/n]: y
📝 Enter your commit message: Add CLI help flags
🚀 Ready to push to GitHub? [y/n]: y
🎉✅ All done! Your changes are pushed!
```

Uninstall
```bash
pip uninstall githelper
```

## 💡 Requirements

- Python 3.6+
- Git installed and available in your system PATH

## 📜 License

MIT — free to use, modify, and share.
