#  How to Run the Documentation Generator

## Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web server)
- Sphinx (documentation builder)
- OpenAI libraries
- Other required packages

### Step 2: Get FREE API Key (Required)

**OpenRouter now requires an API key (but it's FREE!):**

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Click **"Sign Up"** (top right)
3. Sign up with GitHub, Google, or Email (no credit card!)
4. Go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
5. Click **"Create Key"**
6. Copy the key (starts with `sk-or-v1-...`)

### Step 3: Create .env File

Create a file named `.env` in the project root:

**Windows:**
```bash
# Create .env file
notepad .env
```

**Linux/Mac:**
```bash
# Create .env file
nano .env
```

**Add your API key:**
```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### Step 4: Run the Web Application

```bash
python web_app.py
```

The browser will automatically open to `http://localhost:5000`

## Using the Web UI

1. **Enter Repository URL**
   - Example: `https://github.com/IrushiGunawardana/PropertyManagementSystem`
   - Press Enter or click outside the field
   - Branches will load automatically

2. **Select Branch**
   - Choose from the dropdown (default branch is pre-selected)

3. **Click "Load Files"**
   - Wait for files to load
   - You'll see all C# files in the repository

4. **Select Files**
   - Check the files you want to document
   - Or click "Select All"

5. **Click "Generate Documentation"**
   - Watch the progress bar
   - Wait for completion

6. **View & Download**
   - Click "View Documentation" to see in browser
   - Click "Download as PDF" for PDF
   - Click "Download as ZIP" for HTML package

## Alternative: Command Line

If you prefer command line:

```bash
python generate_docs.py https://github.com/owner/repo-name
```

This will:
- Clone the repository
- Generate documentation for all files
- Build HTML
- Open browser automatically

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "No API key configured" error
- Make sure `.env` file exists
- Check the API key is correct
- Restart the application

### Port 5000 already in use
Change the port in `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to 8080
```

### Browser doesn't open
Manually open: `http://localhost:5000`

## File Structure

```
.
 web_app.py          # Main web application
 .env                # Your API keys (create this!)
 requirements.txt    # Dependencies
 web_templates/      # UI files
```

## Need Help?

- **API Key Issues**: See [GET_API_KEY.md](GET_API_KEY.md)
- **General Help**: See [README.md](README.md)
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run web app
python web_app.py

# Run command line version
python generate_docs.py https://github.com/owner/repo

# View generated docs (after generation)
python docs_server.py
```

That's it! You're ready to generate documentation! 

