# githelper

 _____ _ _   _   _      _                 
|  __ (_) | | | | |    | |                
| |  \/_| |_| |_| | ___| |_ __   ___ _ __ 
| | __| | __|  _  |/ _ \ | '_ \ / _ \ '__|
| |_\ \ | |_| | | |  __/ | |_) |  __/ |   
 \____/_|\__\_| |_/\___|_| .__/ \___|_|   
                         | |              
                         |_|         

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

## 🧰 Setup Instructions

To use `githelper` as a system-wide command, follow these steps:

### 1. Make sure you have the following files:

- `githelper.py` → the actual script
- `setup.py` → a small installer script

### 2. Install `githelper` locally (editable mode)

Run this in the same directory where `setup.py` and `githelper.py` are located:

```bash
pip install -e .
```

This tells Python to install githelper as a system-wide command in “editable” mode — meaning any changes you make to githelper.py will take effect immediately.

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

pip install -e .
```



## 🚀 Usage

Once installed, run:

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

