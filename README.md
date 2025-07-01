# DotNet AI DocGen

This project uses OpenRouter (GPT-3.5 free) to generate technical documentation from a .NET codebase and publish it using Sphinx + GitHub Pages.

## How to Use

1. Add your OpenRouter API key as `OPENROUTER_API_KEY` in GitHub secrets.
2. Push changes to `main` branch.
3. GitHub Actions will auto-generate and publish documentation.
