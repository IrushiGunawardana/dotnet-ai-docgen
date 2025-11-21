# Documentation Generator for Code

Documentation Generator for Code is a full-stack workflow for turning live source code into rich, AI-assisted documentation. It can clone .NET/C#, Angular/TypeScript, or HTML/CSS repositories, understand the structure of every file, ask OpenRouter/Azure/OpenAI (or any configured provider) for natural-language summaries, and compile the output into a Sphinx-powered HTML site you can read, print, or deploy.

## Full Guidance & References

- **Primary walkthrough**: This README consolidates every major concept—architecture, requirements, install, configuration, usage, troubleshooting, and deployment—into one authoritative source.
- **Supplemental guides**: When you need deep dives or reference material, consult:
  - `FEATURE_ROADMAP.md` – Planned enhancements and prioritization.
  - `HOW_TO_RUN.md` – Step-by-step UI walkthrough with screenshots and tips.
  - `QUICKSTART.md` – Minimal commands for fast experimentation.
  - `GET_API_KEY.md` – How to obtain a free OpenRouter key.
  - `FREE_AI_SETUP.md` – Running the system without paid API keys.
  - `AZURE_OPENAI_SETUP.md` – Configuring Azure OpenAI credentials and deployments.
  - `TROUBLESHOOTING.md` – Detailed diagnostics for common problems.

## System Architecture

1. **Input Layer** – Accepts a GitHub repository URL (with dynamic branch listing), direct copy/paste, or file upload. The UI guides you through language selection (.NET, Angular, HTML/CSS) before exposing the applicable inputs.
2. **Parsing Layer** – `language_parser.py` walks the cloned tree, honors ignore directories (e.g., `bin/`, `obj/`, `node_modules/`), and extracts metadata such as namespaces, classes, interfaces, Angular selectors, templates, scripts, and CSS rules.
3. **AI Layer** – `ai_doc_generator.py` stores language-specific prompts; it calls the configured provider in priority order (OpenRouter → Azure OpenAI → OpenAI). Missing keys or rate limits trigger automatic fallbacks.
4. **Publishing Layer** – AI-generated RST files are written under `docs_web/source`. Sphinx builds the HTML site into `docs_web/build/html`, and `web_app.py` (plus optional `docs_server.py`) serves it for consumption.
5. **Viewer Layer** – The web UI displays progress, status, and a single “View Documentation” button. Use the browser’s print/save workflow for offline copies (PDF/ZIP downloads were removed intentionally to simplify dependency management).

## Key Features

- **Language Selection**: Choose C#, Angular, or HTML/CSS to tune parsing and prompts.
- **Flexible Inputs**: GitHub repo + branch, manual paste, or single-file upload funnel into the same backend generation.
- **AI Documentation**: Detailed project overviews, per-file summaries, class/method breakdowns, parameter explanations, and template descriptions.
- **Responsive Viewer**: Search, navigation, and mobile-friendly UI powered by Sphinx; print/save from the browser.
- **CLI & Automation**: `generate_docs.py` runs everything headless and can be wired into scripts and CI/CD pipelines.
- **CI/CD Ready**: `.github/workflows/docs.yml` shows how to generate docs on push and publish to GitHub Pages via `peaceiris/actions-gh-pages`.
- **Supporting Guides**: Each companion Markdown file adds context without cluttering this primary README.

## Requirements

1. Python 3.8 or later.
2. Git installed and on your PATH.
3. At least one AI key:
   - OpenRouter (free): see [GET_API_KEY.md](GET_API_KEY.md).
   - Azure OpenAI (paid): see [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md).
   - OpenAI (paid).
4. Optional: `GITHUB_TOKEN` for private repositories.

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create `.env` (this file is ignored by Git) with the keys you intend to use:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp-...
```

See the supplemental guides for details:

- `GET_API_KEY.md`, `FREE_AI_SETUP.md`, `AZURE_OPENAI_SETUP.md` (API keys)
- `HOW_TO_RUN.md`, `QUICKSTART.md` (usage and walkthrough)
- `FEATURE_ROADMAP.md` (future vision)
- `TROUBLESHOOTING.md` (diagnostics)

## Web UI Workflow

```bash
python web_app.py
```

1. Visit `http://localhost:5000`.
2. Select a language: .NET/C#, Angular, or HTML/CSS.
3. Pick your input method (GitHub, paste, upload).
4. Load files, select the ones you want documented, and click “Generate Documentation.”
5. Watch the progress indicator; status updates appear via `/api/status`.
6. Click “View Documentation” to open `docs_web/build/html` in your browser, then use Print/Save for offline copies.

The UI is intentionally simplified: only the key buttons and guidance are shown so you can focus on the code.

## Command Line Usage

```bash
python generate_docs.py https://github.com/owner/repo-name
python generate_docs.py https://github.com/owner/repo-name branch-name
```

Set `GITHUB_REPO_URL` and `GITHUB_BRANCH` environment variables when integrating into scripts or CI/CD:

```bash
export GITHUB_REPO_URL=https://github.com/owner/repo
export GITHUB_BRANCH=develop
python generate_docs.py
```

The CLI performs the same parsing + AI steps as the web UI, but runs entirely in the terminal.

## Viewing Output

```bash
python docs_server.py
```

Open `http://localhost:8000` to browse the generated Sphinx site, which includes search, navigation, and responsive layout. Printing or saving via the browser is the primary way to capture PDFs or HTML copies.

## Project Layout

```
dotnet-ai-docgen/
├── web_app.py              # Flask UI + APIs
├── generate_docs.py        # CLI entry point
├── github_repo_handler.py  # GitHub cloning helper
├── language_parser.py      # Language-aware file discovery
├── ai_doc_generator.py     # AI prompt logic
├── docs_web/               # Sphinx source + HTML output
├── docs_server.py          # Viewer server
├── requirements.txt        # Python dependencies
├── FEATURE_ROADMAP.md      # Roadmap and future features
├── HOW_TO_RUN.md           # Guided walkthrough and screenshots
├── QUICKSTART.md           # Minimal commands
├── GET_API_KEY.md          # OpenRouter key instructions
├── FREE_AI_SETUP.md        # Free-mode guidance
├── AZURE_OPENAI_SETUP.md   # Azure-specific instructions
├── TROUBLESHOOTING.md      # Detailed diagnostics
└── README.md               # This comprehensive reference
```

## CI/CD + Automation

`.github/workflows/docs.yml` demonstrates how to:

1. Checkout the repository.
2. Install dependencies.
3. Run `python generate_docs.py`.
4. Build the HTML (`cd docs && make html`).
5. Deploy to GitHub Pages via `peaceiris/actions-gh-pages`.

Adapt the workflow for other platforms like GitLab or Azure DevOps by swapping the runner steps.

## Troubleshooting

- **No files detected**: Confirm the repo contains the expected language files and you selected the correct branch.
- **AI/API errors**: Verify API keys/quota, restart the app after editing `.env`, and inspect `ai_doc_generator.py` logs.
- **Git clone failures**: Ensure Git is installed. Provide `GITHUB_TOKEN` for private repos.
- **Missing download buttons**: We removed the PDF/ZIP exports; print or save directly from the viewer instead.

## Security Practices

- Never commit `.env` or secret files to the repository.
- Store API keys and tokens in environment variables or GitHub Secrets for CI/CD.
- Rotate keys regularly and assign the minimum permissions needed.

## Contribution & License

MIT License. Contributions, issues, and pull requests are welcome—extend languages, prompts, UI flows, or automation scripts as needed.

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
   - OpenRouter (free)  see [GET_API_KEY.md](GET_API_KEY.md)
   - Azure OpenAI  see [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md)
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
5. Click View Documentation to open the generated HTML.
6. Use your browsers Print/Save dialog to capture a local copy (download buttons were removed to keep dependencies minimal).

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
 web_app.py              # Flask UI + APIs
 generate_docs.py        # CLI entry point
 github_repo_handler.py  # Clones GitHub repositories
 language_parser.py      # Language-aware file discovery
 ai_doc_generator.py     # AI prompt logic
 docs_web/               # Sphinx source + HTML output
 docs_server.py          # Lightweight HTTP server
 requirements.txt        # Python dependencies
 FEATURE_ROADMAP.md      # Short-term and long-term plans
 HOW_TO_RUN.md           # Guided walkthrough
 QUICKSTART.md           # Minimal start steps
 GET_API_KEY.md          # OpenRouter key instructions
 FREE_AI_SETUP.md        # Free-mode guidance
 AZURE_OPENAI_SETUP.md   # Azure-specific instructions
 TROUBLESHOOTING.md      # Extended help
 README.md               # This summary
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
