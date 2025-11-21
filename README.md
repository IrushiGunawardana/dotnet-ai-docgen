# DotNet AI DocGen

DotNet AI DocGen is a professional documentation automation platform for .NET, Angular, and HTML/CSS repositories. It clones GitHub projects, parses language-specific files, drives AI models to explain the code, and publishes the result via Sphinx.

## System Architecture

1. **Language-aware parsing** (`language_parser.py`) enumerates C#, TypeScript, HTML, CSS, and JavaScript files, excluding build artifacts. It exposes namespaces, class details, component/service metadata, selectors, templates, scripts, and styles.
2. **AI layer** (`ai_doc_generator.py`) contains tailored prompts for each language; it calls OpenRouter, Azure OpenAI, or OpenAI in priority order and falls back automatically if a key is missing.
3. **Input methods** include repository URLs, copy/pasted code, or single-file uploads. Each source is normalized, analyzed, and fed to the same AI pipeline.
4. **Publishing pipeline** writes reStructuredText files into `docs_web/source`, runs Sphinx to build `docs_web/build/html`, and exposes the viewer via `web_app.py` and `docs_server.py`.

## Features

- Language selection that adjusts the parser, metadata extraction, and prompt style.
- Flexible input channels (GitHub, paste, upload) to match both quick tests and full repository runs.
- AI-generated overviews for projects, files, classes, methods, and templates.
- Responsive Sphinx viewer with search and navigation; use your browser to print or save a local copy.
- CLI (`generate_docs.py`) for automation scripts.
- CI/CD ready workflow at `.github/workflows/docs.yml`.
- Supporting documentation captured in the Markdown files referenced below.

## Requirements

1. Python 3.8 or newer.
2. Git installed and accessible from the command line.
3. At least one AI key:
   - OpenRouter (free) — see [GET_API_KEY.md](GET_API_KEY.md)
   - Azure OpenAI — see [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md)
   - OpenAI
4. Optional: `GITHUB_TOKEN` for private repositories.

Install dependencies:

```
pip install -r requirements.txt
```

## Configuration

Create a `.env` file (ignored by Git) with the keys you intend to use:

```
OPENROUTER_API_KEY=sk-or-v1-your-key
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp-...
```

Reference the companion guides for deeper information:

- [GET_API_KEY.md](GET_API_KEY.md)
- [FREE_AI_SETUP.md](FREE_AI_SETUP.md)
- [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md)
- [HOW_TO_RUN.md](HOW_TO_RUN.md)
- [QUICKSTART.md](QUICKSTART.md)
- [FEATURE_ROADMAP.md](FEATURE_ROADMAP.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Web UI Workflow

```bash
python web_app.py
```

1. Navigate to `http://localhost:5000`.
2. Select the target language (C#, Angular, or HTML/CSS).
3. Pick an input method (GitHub cluster, paste, or upload).
4. Generate documentation and monitor the progress indicator.
5. Click “View Documentation” to open the generated HTML.
6. Use your browser’s Print/Save dialog to capture a local copy (download buttons were removed to keep dependencies minimal).

## Command Line Usage

```bash
python generate_docs.py https://github.com/owner/repo-name
python generate_docs.py https://github.com/owner/repo-name branch-name
```

Set `GITHUB_REPO_URL` and `GITHUB_BRANCH` environment variables instead of passing arguments if you prefer automation.

## Viewing Output

```bash
python docs_server.py
```

Open `http://localhost:8000` to browse the Sphinx output. The UI includes search, navigation, and responsive styling.

## Project Layout

```
dotnet-ai-docgen/
├── web_app.py              # Flask UI + APIs
├── generate_docs.py        # CLI entry point
├── github_repo_handler.py  # Clones GitHub repositories
├── language_parser.py      # Language-aware file discovery
├── ai_doc_generator.py     # AI prompt logic
├── docs_web/               # Sphinx source + HTML output
├── docs_server.py          # Lightweight HTTP server
├── requirements.txt        # Python dependencies
├── FEATURE_ROADMAP.md      # Short-term and long-term plans
├── HOW_TO_RUN.md           # Guided walkthrough
├── QUICKSTART.md           # Minimal start steps
├── GET_API_KEY.md          # OpenRouter key instructions
├── FREE_AI_SETUP.md        # Free-mode guidance
├── AZURE_OPENAI_SETUP.md   # Azure-specific instructions
├── TROUBLESHOOTING.md      # Extended help
└── README.md               # This summary
```

## CI/CD Integration

The workflow at `.github/workflows/docs.yml` checks out the repo, installs dependencies, runs `python generate_docs.py`, builds the HTML (`cd docs && make html`), and publishes to GitHub Pages via `peaceiris/actions-gh-pages`. Adapt it for GitLab, Azure DevOps, or your own runner if needed.

## Troubleshooting

- **No files detected**: Confirm the repository contains files for the selected language and that the branch exists.
- **AI/API errors**: Validate your API keys, quotas, and rate limits.
- **Git clone failures**: Ensure Git is installed and set `GITHUB_TOKEN` when cloning private repos.
- **Missing PDF downloads**: Print or save from the viewer; download buttons were removed deliberately.

## Security

- Never commit `.env` or secret files.
- Store API keys and tokens in environment variables or GitHub Secrets for CI/CD.
- Rotate keys regularly and use the minimum required scope.

## Contribution & License

MIT License. Contributions, issues, and pull requests are welcome.
