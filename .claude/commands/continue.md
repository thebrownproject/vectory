---
description: Resume development from where you left off
---

You are resuming development on the Vectory project. Follow these steps to get oriented and continue work:

## Step 1: Read Project Context

Read the following files to understand the project:
- `prd.md` - Project requirements and scope
- `tasks.md` - Development roadmap and task status
- `development-notes.md` - Session notes and important decisions

## Step 2: Check Git Status

Run the following git commands:
- `git branch --show-current` - Check current branch
- `git status --short` - Check for uncommitted changes

## Step 3: Analyze Current State

Based on `tasks.md`:
1. Identify the current phase (look for the phase that has incomplete tasks)
2. Find the last completed task (marked with `[x]`)
3. Find the next pending task (marked with `[ ]`)
4. Determine which phase branch you should be on (e.g., `feature/phase-2-vector-adapter`)

## Step 4: Validate Branch Consistency

Check if current git branch matches the expected branch for the current phase:
- If working on Phase 2 tasks, should be on `feature/phase-2-*` branch
- If working on Phase 3 tasks, should be on `feature/phase-3-*` branch
- etc.

If branch doesn't match, warn the user.

## Step 5: Present Summary

Display a clear summary in this format:

```
📍 Development Context

**Current Branch:** [branch name]
**Current Phase:** [Phase X - Name]

**Progress:**
✅ Last completed: [Task ID - Description]
⏭️  Next task: [Task ID - Description]

**Git Status:**
[Any uncommitted changes or "Working tree clean"]

**Important Notes from development-notes.md:**
- [Any critical TODOs or blockers from latest session]

---

Ready to proceed with [Next Task ID]?
```

## Step 6: Wait for User Confirmation

After presenting the summary, ask: "Would you like to proceed with [Next Task ID]?"

If user confirms, begin working on the next task following the workflow in CLAUDE.md.

## Additional Checks

- If there are uncommitted changes, warn the user before proceeding
- If on `main` branch but tasks show an active phase, suggest creating the feature branch
- If all tasks in current phase are complete, suggest merging and starting next phase
