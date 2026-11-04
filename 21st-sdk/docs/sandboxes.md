# Sandboxes & Infrastructure

Sandbox specs, shared volumes, lifecycle hooks, concurrent users, and persistent storage.

## What are the sandbox hardware specs?

Default sandboxes run with up to 8 CPU and 8 GB RAM. For higher specs, contact support for a custom plan through E2B.

## What happens when two users write in the same chat?

Last user wins. Each API call spawns a separate Claude process. If two users send messages to the same thread simultaneously, both receive their own responses, but Claude's internal conversation file retains the history from whichever request finishes last. Use separate threads within the same sandbox to avoid conflicts.

## Can I share files between sandboxes?

E2B supports shared volumes backed by S3. You can also reuse a single sandbox with multiple threads, or build a custom solution using a tool that uploads/downloads from S3 or Supabase Storage.

## One sandbox with multiple threads vs. multiple sandboxes?

One sandbox, multiple threads - shared filesystem, good for shared state. Multiple sandboxes - fully isolated, good for heavy compute. Use shared volumes if you need common files across sandboxes.

## Are there sandbox lifecycle hooks (onResume / onPause)?

Lifecycle hooks are on the roadmap. Use startup scripts in your agent's `template/` directory for initialization logic.

## What happens when a sandbox times out?

Idle sandboxes are destroyed after a timeout. The next message automatically creates a new sandbox. The agent URL stays the same.