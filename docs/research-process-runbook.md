# Bounded research-process runbook

This runbook governs long-running exploratory calculations, exact algebra,
solver calls, and verifier development processes.  It is an operational
safety contract.  It does not change the evidentiary status of any output.

## Ownership rule

The launching task owns a process until it exits or is explicitly handed off.
Before the task completes, merges, changes scope, or abandons an execution
session, the owner must do one of the following:

1. wait for the process and inspect its result;
2. preserve or checkpoint useful output, terminate the owned process tree,
   and verify that it exited; or
3. record a live handoff containing the run identifier, command, worktree,
   process identity, resource budget, log location, current state, and the new
   owner.

Do not infer that a command stopped because a tool call timed out, a terminal
closed, an agent turn ended, or a PR merged.  Do not terminate a process based
only on a stale PID.  Revalidate the executable name, creation time,
command/worktree, ownership, and relevant output immediately before stopping
it.

## Standard runner

For a computation expected to exceed 60 seconds, prefer:

```powershell
python tools/research/run_bounded.py `
  --run-id gld84-rank-seven-chart-001 `
  --timeout-seconds 3600 `
  --memory-mb 8192 `
  -- `
  python claims/arbitrary-order/example_verifier.py
```

The command is launched noninteractively and without a shell; stdin is closed.
Use a durable script or module for a long Python calculation.  The runner
rejects long `python -` and `python -c` commands because their program text and
provenance are too easy to lose.

The default local run root is `.research-runs/`, which is ignored by Git.  A
timestamped directory contains:

- `run.json`: run identifier, owner PID, exact argument vector, working
  directory, resource declarations, timestamps, child PID, and terminal
  status;
- `run.log`: combined stdout and stderr, also streamed to the terminal; and
- `<run-id>.lock`: a crash-releasing advisory lock that prevents two active
  runners from using the same identifier.

Run identifiers should describe the mathematical instance or chart.  Reusing
one while its lock is held fails with exit code `73`; it does not launch a
second calculation.

## Limits and process-tree semantics

The wall-clock limit is mandatory.  A timeout terminates the owned process
tree and returns exit code `124`.  An interactive interruption returns `130`.
A launch failure returns `127`; otherwise the runner returns the child exit
code.

On Windows, the runner first assigns a gated containment child to a Job Object
and only then permits it to launch the requested command.  This closes the
usual launch-before-assignment race.  The Job Object uses `KILL_ON_JOB_CLOSE`
and an aggregate job-memory limit.  Closing or killing the runner therefore
closes the Job Object and terminates its owned descendants.  The
`--memory-mb` value is an aggregate committed-memory ceiling for that job.

On POSIX systems, the runner creates a process group, terminates that group on
timeout or interruption, and applies `RLIMIT_AS` where available.  POSIX
address-space accounting and descendant aggregation differ by operating
system, so the JSON declaration remains a budget but is not claimed to be
identical to Windows Job Object accounting.

## Long-run checklist

Before launch:

- inspect current process and worktree ownership;
- use a durable checked-in or intentionally untracked script rather than
  stdin;
- select a unique run identifier;
- declare realistic time and memory bounds;
- avoid overlapping an equivalent calculation; and
- decide which output is a checkpoint and which is disposable.

Before task completion:

- inspect the runner metadata and terminal status;
- verify that the child tree exited;
- preserve only scientifically meaningful, privacy-safe artifacts;
- distinguish timeout, failure, experiment, and proof-producing evidence; and
- document any explicit live handoff.

The runner cannot decide whether a computation is mathematically useful.  In
particular, a successful process exit, modular experiment, or solver result is
not a theorem without the repository's required mathematical bridge and
certificate semantics.
