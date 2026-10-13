# Lantern

A small command that checks whether a URL is up.

```bash
python3 lantern.py check https://example.com
```

The guides live in [lantern-docs](https://github.com/spacechurro/lantern-docs). This repo updates them with Grok Build when a pull request merges.

## Docs follow the code

[`.github/workflows/sync-docs.yml`](.github/workflows/sync-docs.yml) checks out this repo and the docs repo, then runs the prompt in [`.github/prompts/sync-docs.md`](.github/prompts/sync-docs.md):

```bash
grok --cwd ../lantern-docs --prompt-file /tmp/prompt.md --yolo --no-auto-update
```

The prompt is the product. Grok reads the merged diff beside the current guides. If a user would notice the change, Grok opens a pull request on lantern-docs. If the change is tests or a refactor, Grok prints `No docs update needed.` and stops.

### Secrets

Add these under Settings → Secrets and variables → Actions before you merge a pull request you want documented.

| Secret | What to put there |
| --- | --- |
| `XAI_API_KEY` | An API key from [console.x.ai](https://console.x.ai) |
| `DOCS_REPO_TOKEN` | A fine-grained personal access token for `spacechurro/lantern-docs` only. Contents: Read and write. Pull requests: Read and write. |

The token GitHub gives this workflow can read this repo. It cannot open a pull request on lantern-docs. `DOCS_REPO_TOKEN` is that missing permission.

### Try it

[EXAMPLE.md](EXAMPLE.md) is the walkthrough of the run that already happened: the merged code pull request, the workflow run, and the docs pull request Grok opened.

Run the tests with `python3 -m unittest`.
