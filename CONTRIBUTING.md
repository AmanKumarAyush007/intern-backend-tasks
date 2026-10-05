# Contributor Guide

## How to Submit

1. Fork this repository
2. Clone your fork locally
3. Create a branch: `git checkout -b feat/<your-name>/exercise-3.X`
4. Copy the starter: `cp -r exercises/3.X-<name>/starter/ submissions/<your-username>/3.X/`
5. Complete the exercise
6. Run: `python scripts/verify.py --exercise 3.X --user <your-username>`
7. Commit and push to your fork
8. Open a Pull Request targeting the `main` branch of this repo

## Branch Naming Convention

```
feat/<your-name>/exercise-3.1
feat/<your-name>/exercise-3.2
...
```

## Submission Directory Structure

```
submissions/
└── alice/
    ├── 3.1/
    │   ├── project/
    │   │   ├── settings.py
    │   │   └── urls.py
    │   ├── calls/
    │   │   ├── models.py
    │   │   ├── views.py
    │   │   └── ...
    │   └── requirements.txt
    └── 3.2/
        └── ...
```

## Code Standards

- Follow PEP 8 (max 120 chars per line)
- Use `logging` not `print()`
- No credentials in source code — use environment variables
- Write docstrings on all public methods
- Handle exceptions — never `except: pass`

## Getting Help

- Re-read the exercise doc in `docs/`
- Check `docs/CHEATSHEET.md` for quick reference
- Ask your mentor in the PR comment — use `@mention`
- Do NOT share solutions with other interns

## Questions?

Open a GitHub Issue with the label `question` and your mentor will respond within 24 hours.
