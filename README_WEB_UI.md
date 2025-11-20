# 🌐 Web UI Documentation

## Overview

The Web UI provides a complete browser-based interface for generating .NET documentation. No command line needed!

## Features

- ✅ **Web-based Interface**: Everything runs in your browser
- ✅ **Repository Selection**: Enter GitHub repo URL and branch
- ✅ **File Browser**: See all C# files in the repository
- ✅ **Selective Documentation**: Choose which files to document
- ✅ **Real-time Progress**: Watch documentation generation in real-time
- ✅ **View & Download**: View generated docs and download as ZIP

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Web Application

```bash
python setup_web.py
```

### 3. Start Web Server

```bash
python web_app.py
```

The browser will automatically open to `http://localhost:5000`

## Usage

### Step 1: Enter Repository Information
- Enter GitHub repository URL (e.g., `https://github.com/owner/repo` or `owner/repo`)
- Select branch (main, master, develop, or custom)
- Click "Load Files"

### Step 2: Select Files
- Browse all C# files found in the repository
- Select individual files or use "Select All"
- See file metadata (namespace, classes, interfaces, enums)

### Step 3: Generate Documentation
- Click "Generate Documentation"
- Watch real-time progress
- Wait for completion

### Step 4: View & Download
- Click "View Documentation" to see in browser
- Click "Download as ZIP" to download complete documentation

## API Endpoints

### `POST /api/repo/files`
Load files from repository
```json
{
  "repo_url": "https://github.com/owner/repo",
  "branch": "main"
}
```

### `POST /api/generate`
Start documentation generation
```json
{
  "repo_url": "https://github.com/owner/repo",
  "branch": "main",
  "files": ["path/to/file1.cs", "path/to/file2.cs"]
}
```

### `GET /api/status`
Get generation status
```json
{
  "status": "generating|completed|error",
  "progress": 75,
  "message": "Processing files...",
  "files_processed": 3,
  "total_files": 4
}
```

### `GET /api/view`
Check if docs are ready
```json
{
  "success": true,
  "url": "/docs/index.html"
}
```

### `GET /api/download/html`
Download documentation as ZIP file

## Troubleshooting

**Port 5000 already in use?**
- Change port in `web_app.py`: `app.run(port=8080)`

**Files not loading?**
- Check repository URL format
- Verify branch exists
- Check GitHub token for private repos (set `GITHUB_TOKEN` in environment)

**Generation fails?**
- Check AI API keys are set
- Verify selected files exist
- Check console for error messages

**Documentation not building?**
- Ensure Sphinx is installed: `pip install sphinx sphinx-rtd-theme`
- Check `docs_web/source/conf.py` exists

## Configuration

### Environment Variables
```env
# AI API (at least one required)
OPENROUTER_API_KEY=your_key
AZURE_OPENAI_API_KEY=your_key
OPENAI_API_KEY=your_key

# GitHub (for private repos)
GITHUB_TOKEN=your_token
```

### Custom Port
Edit `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## Architecture

- **Frontend**: HTML/CSS/JavaScript (single page application)
- **Backend**: Flask (Python web framework)
- **Documentation**: Sphinx (HTML generation)
- **AI**: Azure OpenAI / OpenAI / OpenRouter

## File Structure

```
.
├── web_app.py              # Flask application
├── web_templates/          # HTML templates
│   └── index.html          # Main UI
├── web_static/             # Static files (CSS, JS)
├── docs_web/               # Generated documentation
│   ├── source/             # RST source files
│   └── build/html/         # Built HTML docs
└── setup_web.py            # Setup script
```

## Development

### Running in Development Mode
```bash
python web_app.py
```
Runs with debug mode enabled (auto-reload on changes)

### Production Deployment
1. Set `debug=False` in `web_app.py`
2. Use production WSGI server (gunicorn, uWSGI)
3. Configure reverse proxy (nginx)

## Security Notes

- Web UI runs on localhost by default (safe)
- For remote access, use proper authentication
- Don't expose API keys in frontend code
- Use environment variables for secrets

