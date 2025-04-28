# 🛠️ GitHelper

A tiny Python tool that makes Git commits and pushes much easier!

---

## 🚀 Install

1.  Clone the repository:

```bash
git clone git@github.com:aalbrightpdx/githelper.git ~/.bin/githelper
chmod +x ~/.bin/githelper
```

## Create a Global Launcher Script

1.  Create a small wrapper so you can run githelper from anywhere:

```bash
nano ~/.bin/githelper-cli
```

2.  Paste this inside:

```bash
#!/bin/bash
python3 ~/.bin/githelper/githelper.py
```

3.  ✅ Save and exit (CTRL+O, Enter, CTRL+X), make it executable:

```bash
chmod +x ~/.bin/githelper
```

---

## ➕ Add to PATH

If you want to run `githelper` from anywhere:

1. Add the PATH="$HOME/.bin:$PATH"' to ~/.bashrc:

    ```bash
    echo 'export PATH="$HOME/.bin:$PATH"' >> ~/.bashrc
    ```

3. Reload your shell:

    ```bash
    source ~/.bashrc
    ```

✅ Now you can just type `githelper` from any Git project!

---

## ⚡ Usage

```bash
githelper
```

It will:

- Show the current Git status
- Confirm before adding and committing
- Prompt you for a commit message
- Confirm again before pushing to GitHub

Safe, fast, and friendly.

---

## 📝 License

MIT License.  
See `LICENSE` for full details.

