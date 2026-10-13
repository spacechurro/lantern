# End-to-end example

This repo and [lantern-docs](https://github.com/spacechurro/lantern-docs) show Grok Build opening a documentation pull request after a code pull request merges.

`lantern` is a small command that checks whether a URL is up. The guides live in the other repo. A merged pull request here checks out both repos and runs one prompt. Grok reads the merged diff beside the current guides. When the change is something a user would read, Grok opens a pull request on lantern-docs. When the change is tests or a refactor, it prints `No docs update needed.` and stops.

## Files to read

The setup is two files in this repo:

- [`.github/prompts/sync-docs.md`](.github/prompts/sync-docs.md) is the instruction Grok follows.
- [`.github/workflows/sync-docs.yml`](.github/workflows/sync-docs.yml) runs that prompt when a pull request merges.

The workflow needs two Actions secrets on this repo: `XAI_API_KEY`, and `DOCS_REPO_TOKEN`, a fine-grained token that can write to lantern-docs and open pull requests there. The token GitHub gives the workflow cannot do that second part.

The command itself is [`lantern.py`](lantern.py). The change in the example adds `watch`.

The pages Grok is allowed to edit are in lantern-docs:

- [README.md](https://github.com/spacechurro/lantern-docs/blob/main/README.md)
- [getting-started.md](https://github.com/spacechurro/lantern-docs/blob/main/getting-started.md)
- [cli.md](https://github.com/spacechurro/lantern-docs/blob/main/cli.md)
- [configuration.md](https://github.com/spacechurro/lantern-docs/blob/main/configuration.md)

## What ran

Look at these in order.

1. [Add lantern watch](https://github.com/spacechurro/lantern/pull/1) merged into this repo. It adds a command a user would read about. It does not edit the docs repo.
2. [Sync docs](https://github.com/spacechurro/lantern/actions/runs/38405947317) is the workflow run for that merge. The step named "Update the docs" is Grok.
3. [Document lantern#1: add watch command and interval config](https://github.com/spacechurro/lantern-docs/pull/1) is the pull request that run opened. The first commit describes `watch` on the getting-started page, the command reference, and the config page, and the body links back to the code pull request. The second commit only closes two broken code fences in that generated text.
