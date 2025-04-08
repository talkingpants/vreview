#  Git Quick Commands Cheat Sheet

##  Everyday Workflow

| Action                    | Command |
|---------------------------|---------|
| Check status              | `git status` |
| Stage all changes         | `git add .` |
| Stage specific file       | `git add path/to/file` |
| Commit with message       | `git commit -m "your message"` |
| Pull from remote          | `git pull` |
| Push to remote            | `git push origin main` |

---

##  Branching

| Action                          | Command |
|----------------------------------|---------|
| Create a new branch              | `git checkout -b feature/my-branch` |
| Switch to another branch         | `git checkout main` |
| Merge another branch             | `git merge feature/my-branch` |
| Delete a branch                  | `git branch -d feature/my-branch` |

---

##  Fix / Undo

| Action                           | Command |
|----------------------------------|---------|
| Unstage a file                   | `git restore --staged file.py` |
| Discard all changes              | `git restore .` |
| Clean untracked files/folders    | `git clean -fd` |
| Amend last commit                | `git commit --amend` |

---

##  Inspection

| Action                           | Command |
|----------------------------------|---------|
| View log (short/graph)           | `git log --oneline --graph --all` |
| View recent commit details       | `git show` |
| Diff current vs. last commit     | `git diff HEAD` |
| Diff staged vs. last commit      | `git diff --cached` |

---
