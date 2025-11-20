# Quick Start Guide

Get started with DotNet AI DocGen in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up API Key (OPTIONAL - Skip for Free!)

**🆓 FREE OPTION: Skip this step!** The tool works without any API keys using free models.

**OR** for better performance, get a free OpenRouter key (2 minutes, no credit card):

1. Sign up at [openrouter.ai](https://openrouter.ai) (free, no credit card)
2. Get your key at [openrouter.ai/keys](https://openrouter.ai/keys)
3. Create `.env` file:
   ```bash
   # On Windows
   copy .env.example .env
   
   # On Linux/Mac
   cp .env.example .env
   ```
4. Add to `.env`:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

> 🆓 **See [FREE_AI_SETUP.md](FREE_AI_SETUP.md) for complete free setup guide!**

## Step 3: Generate Documentation

Run the generator with a GitHub repository URL:

```bash
python generate_docs.py https://github.com/dotnet/corefx
```

Or use your own repository:

```bash
python generate_docs.py https://github.com/your-username/your-repo
```

## Step 4: View Documentation (Web UI)

**Easy way - One command:**
```bash
python serve_docs.py
```

This automatically:
- ✅ Builds the HTML documentation
- ✅ Starts a web server
- ✅ Opens your browser

**Manual way:**
```bash
# Build HTML
cd docs
make html  # On Windows: make.bat html

# Serve and view
cd ../..
python serve_docs.py
```

The documentation opens at `http://localhost:8000` in your browser!

## Example Output

The tool will:
- ✅ Clone the repository
- ✅ Find all C# files
- ✅ Generate documentation for each file
- ✅ Create a project overview
- ✅ Build searchable HTML documentation

## Troubleshooting

**"All AI API calls failed"**
- The tool should work automatically with free models
- If it fails, wait a minute and try again (free models may be busy)
- Or get a free OpenRouter key for better reliability (see Step 2)

**"Failed to clone repository"**
- Check the repository URL is correct
- For private repos, add `GITHUB_TOKEN` to `.env`

**"No C# files found"**
- Ensure the repository contains `.cs` files
- Check the branch name (default is `main`)

## Next Steps

- Read the full [README.md](README.md) for advanced features
- Set up GitHub Actions for automatic documentation updates
- Customize the Sphinx theme in `docs/source/conf.py`

