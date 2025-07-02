# DotNet AI DocGen

This project uses OpenRouter (GPT-3.5 free) to generate technical documentation from a .NET codebase and publish it using Sphinx + GitHub Pages.

## Features

- Automatic technical documentation generation from .NET codebase
- Uses OpenRouter (GPT-3.5 free) for AI-powered doc generation
- Publishes docs with Sphinx and GitHub Pages
- Seamless integration with GitHub Actions

## Requirements

- .NET 6 or higher
- GitHub repository with access to GitHub Actions
- OpenRouter API key

## Setup

1. Fork or clone this repository.
2. Add your `OPENROUTER_API_KEY` to the repository secrets on GitHub.
3. Ensure your .NET code is in the repository.
4. Push your changes to the `main` branch.

## Documentation Output

- Documentation is generated in the `docs/` directory.
- Published automatically to GitHub Pages at `https://<your-username>.github.io/<repo-name>/`.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.