# Git Workflow for Group 13

To keep our code clean, we follow these rules:

1.  **Never push to `main` directly.** The `main` branch is only for finished code.
2.  **Use the `develop` branch.** This is where we combine our work.
3.  **Create "Feature Branches".** When you start a new task (like "API" or "Map"), create a new branch:
    * `git checkout -b feature/my-task-name`
4.  **Merge Requests.** When finished, push your branch and open a Merge Request on GitLab to merge it into `develop`.