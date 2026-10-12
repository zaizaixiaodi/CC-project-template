---
name: implement
description: Implement a piece of work based on a spec or set of tickets.
---

Implement the work described by the user in the spec or tickets. Capture the starting Git HEAD before editing and pass that fixed point plus the local plan to the review stage.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Read [tdd](../tdd/SKILL.md) and use it where meaningful, at pre-agreed seams. An already approved plan can establish the seams; do not repeat settled questions.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, read [code-review](../code-review/SKILL.md) and review the work against the agreed plan and project standards. Review the working diff before committing, using the starting HEAD as the fixed point.

Commit to the current branch only when the user authorized a commit. Otherwise report the tested changes without committing. Never push or close external work items without authorization.
