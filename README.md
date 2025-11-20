# DotNet AI DocGen - Enhanced

An advanced automated documentation generation tool for .NET projects that connects to GitHub repositories and generates comprehensive technical documentation using AI and Sphinx.

**🆓 100% FREE to use!** No API keys required - works automatically with free AI models!

## 🚀 Features

- **🌐 Complete Web UI**: Full browser-based interface - no command line needed!
  - Enter repo URL and branch
  - Browse and select files
  - Generate documentation with one click
  - View and download results
- **GitHub Integration**: Automatically clones and analyzes any GitHub repository
- **Comprehensive .NET Parsing**: Discovers all C# files, classes, methods, interfaces, and enums
- **Multi-AI Support**: Works with Azure OpenAI, OpenAI, or OpenRouter (with automatic fallback)
- **Full Documentation Generation**: Creates detailed documentation for entire projects, not just single files
- **🎨 Modern Web UI**: Beautiful, responsive documentation interface with enhanced styling
- **📥 Download Features**: Download documentation as PDF, HTML (ZIP), or Markdown
- **🌐 Auto-Open Browser**: Automatically opens documentation in browser after generation
- **Sphinx Integration**: Generates beautiful, searchable HTML documentation
- **Project Overview**: Automatically generates project architecture and overview documentation
- **GitHub Actions Ready**: Seamless CI/CD integration

## 📋 Requirements

- Python 3.8 or higher
- Git (for repository cloning)
- **AI API Key: OPTIONAL!** 🆓
  - **No key needed** - Uses free OpenRouter models automatically!
  - OpenRouter API key (free, recommended for better performance)
  - Azure OpenAI (paid, optional)
  - OpenAI API key (paid, optional)

## 🛠️ Setup

### Option A: Web UI (Recommended - Easiest!)

**Perfect for interactive use - everything in your browser!**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup web application
python setup_web.py

# 3. Start web server
python web_app.py
```

The browser opens automatically at `http://localhost:5000` with a beautiful UI where you can:
- Enter repository URL and branch
- Browse and select files
- Generate documentation
- View and download results

**See [README_WEB_UI.md](README_WEB_UI.md) for detailed web UI guide.**

### Option B: Command Line

**For automation and CI/CD:**

### 2. Configure API Keys (OPTIONAL - Works Without Any Keys!)

**🆓 FREE OPTION: No configuration needed!** The tool automatically uses free AI models from OpenRouter.

**OR** create a `.env` file for better performance:

```env
# Option 1: OpenRouter (FREE - Recommended!)
# Get free key at: https://openrouter.ai/keys (takes 2 minutes, no credit card)
OPENROUTER_API_KEY=your_openrouter_api_key

# Option 2: Azure OpenAI (Paid)
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4

# Option 3: OpenAI (Paid)
OPENAI_API_KEY=your_openai_api_key

# Optional: GitHub Token (for private repos)
GITHUB_TOKEN=your_github_token
```

> 🆓 **Want to use it for FREE?** See [FREE_AI_SETUP.md](FREE_AI_SETUP.md) - No API keys needed!
> 
> 💰 **Need help with paid options?** See [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md) for Azure OpenAI setup.

The tool will automatically use the first available API in this order:
1. Azure OpenAI
2. OpenAI
3. OpenRouter

### 3. Generate Documentation

#### From Command Line

```bash
# Basic usage
python generate_docs.py https://github.com/owner/repo-name

# Specify branch
python generate_docs.py https://github.com/owner/repo-name main

# Or use environment variable
export GITHUB_REPO_URL=https://github.com/owner/repo-name
python generate_docs.py
```

#### From Environment Variables

```bash
export GITHUB_REPO_URL=https://github.com/owner/repo-name
export GITHUB_BRANCH=main
python generate_docs.py
```

### 4. View Documentation (Enhanced Web UI)

**🎯 Automatic - Just run generate_docs.py!**
```bash
python generate_docs.py https://github.com/owner/repo
```
This automatically:
- ✅ Generates documentation
- ✅ Builds HTML
- ✅ Starts enhanced web server
- ✅ Opens browser with modern UI
- ✅ Includes download features

**Manual way:**
```bash
# Start enhanced server (auto-builds if needed)
python docs_server.py
```

**Features in the UI:**
- 🎨 Modern, responsive design
- 📥 Download as PDF, HTML (ZIP), or Markdown
- 🔍 Enhanced search and navigation
- 📱 Mobile-friendly layout

The documentation opens at `http://localhost:8000` with a beautiful interface!

## 📖 Usage Examples

### Example 1: Public Repository

```bash
python generate_docs.py https://github.com/dotnet/corefx
```

### Example 2: Private Repository

```bash
export GITHUB_TOKEN=your_github_token
python generate_docs.py https://github.com/your-org/private-repo
```

### Example 3: Specific Branch

```bash
python generate_docs.py https://github.com/owner/repo develop
```

## 🏗️ Project Structure

```
dotnet-ai-docgen/
├── generate_docs.py          # Main entry point
├── github_repo_handler.py    # GitHub repository operations
├── dotnet_parser.py          # .NET project parsing
├── ai_doc_generator.py       # AI-powered documentation generation
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not in repo)
└── docs/
    ├── source/              # Generated RST files
    └── build/               # Built HTML documentation
```

## 🔧 How It Works

1. **Repository Cloning**: The tool clones the specified GitHub repository to a temporary directory
2. **Project Discovery**: Parses the repository to find:
   - Solution files (`.sln`)
   - Project files (`.csproj`)
   - All C# source files (`.cs`)
3. **Code Analysis**: Extracts:
   - Namespaces
   - Classes and their methods
   - Interfaces
   - Enums
4. **AI Documentation**: For each file and the overall project:
   - Generates comprehensive documentation using AI
   - Documents methods, parameters, return values
   - Creates usage examples
   - Provides architecture overview
5. **Sphinx Generation**: Converts AI-generated content to RST format and builds HTML documentation

## 🎯 Generated Documentation Includes

- **Project Overview**: Architecture, purpose, and key components
- **File Documentation**: Detailed documentation for each C# file
- **Class Documentation**: Purpose, methods, properties
- **Method Documentation**: Parameters, return values, exceptions, examples
- **Repository Information**: Stars, forks, description from GitHub

## 🔐 Security Notes

- Never commit `.env` files to version control
- Use GitHub Secrets for CI/CD pipelines
- For private repositories, use a GitHub Personal Access Token

## 🤖 GitHub Actions Integration

Example workflow (`.github/workflows/docs.yml`):

```yaml
name: Generate Documentation

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Generate documentation
        env:
          GITHUB_REPO_URL: ${{ github.repositoryUrl }}
          AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
          AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
          AZURE_OPENAI_DEPLOYMENT: ${{ secrets.AZURE_OPENAI_DEPLOYMENT }}
        run: python generate_docs.py
      
      - name: Build documentation
        run: |
          cd docs
          make html
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build/html
```

## 🐛 Troubleshooting

### No C# files found
- Ensure the repository contains `.cs` files
- Check that the branch name is correct
- Verify repository access (for private repos)

### API errors
- Verify your API keys are set correctly
- Check API rate limits
- Ensure you have sufficient credits/quota

### Git clone errors
- Ensure Git is installed and in PATH
- For private repos, set `GITHUB_TOKEN`
- Check repository URL format

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## 🙏 Acknowledgments

- Built with [Sphinx](https://www.sphinx-doc.org/)
- AI-powered by Azure OpenAI, OpenAI, and OpenRouter
- Documentation theme by [Read the Docs](https://sphinx-rtd-theme.readthedocs.io/)
