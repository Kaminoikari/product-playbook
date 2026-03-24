# 🔁 Progress Persistence & Interruption Recovery

> Loaded when the user says "pause," "save," or when the skill checks for progress at startup.

## Progress File Format

After each step is completed, create or update `.product-playbook-progress.md` in the project directory:

```
# Product Playbook Progress Save

- Mode: [Quick Mode / Full Mode / ...]
- Product type: [B2C / B2B / ...]
- Product description: [User's product description]
- Current progress: S[X] / S[Y]
- Last updated: [timestamp]

## Completed Steps

### S1: [Step name] ✅
[Core output of this step — retain enough detail so it does not need to be redone upon recovery]

### S2: [Step name] ✅
[Same as above]

## Pending Steps
- S3: [Step name]
- S4: [Step name]
- ...
```

### Feature Extension Mode Example
```markdown
Mode: Feature Extension
Step: S2/S4
S1: Problem + existing system context ✅
S2: Three parallel solutions + AI recommendation ▶️
S3: Risk assessment ⬜
S4: Execution scope ⬜
```

## Trigger Rules

1. **Auto-save**: After each step is completed and confirmed by the user, immediately update the progress file
2. **Check on startup**: When the skill is triggered, first check whether `.product-playbook-progress.md` exists. If it does, display:
```
Detected unfinished product planning progress ([mode name], S[X]/S[Y]):
  1️⃣ Continue — Resume from S[X]
  2️⃣ Start over — Clear old progress and begin from scratch
(Enter 1 or 2)
```
3. **Pause command**: When the user says "pause," "do something else first," or "save," confirm the progress file has been updated and reply: "Progress saved to .product-playbook-progress.md (S[X]/S[Y]). It will be automatically detected next time you start the skill in this project."
4. **Cleanup on completion**: After the entire flow is completed and final documents are produced, ask the user whether to delete the progress file
6. **Version control reminder**: When `.product-playbook-progress.md` is created for the first time, remind the user: "⚠️ We recommend adding `.product-playbook-progress.md` to `.gitignore` — this file may contain sensitive product strategy information."
5. **Interruption save**: When an unrelated prompt is detected during the flow (see SKILL.md flow interruption handling rules), save progress even if the current step is not yet complete. Use 🔶 (in progress) instead of ✅ for the current step in the save format, and preserve the partially produced content:
```
### S[X]: [Step name] 🔶 (in progress, partially completed)
[Partially produced content]
⚠️ This step is not yet complete — resume from here upon recovery
```
