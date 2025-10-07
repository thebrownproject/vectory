You are wrapping up the current development session before ending the chat. Follow these steps to properly document progress and commit work:

## Step 1: Update tasks.md

1. Read `tasks.md` to identify which tasks were completed in this session
2. Mark completed tasks with `[x]` instead of `[ ]`
3. Update any task notes or subtasks if needed
4. Identify the current phase and next pending task

## Step 2: Add Session Notes to development-notes.md

1. Read the existing `development-notes.md` to see the format
2. Add a new session entry with today's date following the existing template:
   - Session number and date
   - Phase and tasks completed
   - Important decisions made (technical choices, architecture, patterns used)
   - Bug fixes or issues encountered and how they were resolved
   - Current branch name
   - Next steps for the following session

Keep notes concise but informative - focus on decisions and context that future sessions will need.

## Step 3: Create Git Commit

1. Check `git status` to see all modified/new files
2. Stage all changes with `git add -A`
3. Create a descriptive commit message following this format:

```
<Brief summary of what was completed>

- Bullet point of specific changes
- Another change
- Additional context if needed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

4. Commit with the message
5. Show the commit hash and confirm success

## Step 4: Provide Summary

Give the user a brief summary:
- What was completed this session
- What files were created/modified
- The commit hash
- What to work on next session
- Current branch name

## Important Notes

- This command is specifically for END OF SESSION - don't use it mid-session
- Only mark tasks as complete if they are truly finished
- Session notes should help future Claude sessions understand context
- Commit messages should be clear and descriptive
- Always include the Claude Code attribution footer in commits
