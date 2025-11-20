# Troubleshooting Guide

## Common Issues and Solutions

### Issue: "No C# files found in the repository!"

**Possible Causes:**

1. **Wrong Branch**
   - The repository might have C# files in a different branch
   - **Solution:** Specify the branch explicitly:
     ```bash
     python generate_docs.py https://github.com/owner/repo branch-name
     ```

2. **Repository Structure**
   - C# files might be in a subdirectory
   - The tool will show what directories it finds
   - Check the output for "Top-level directories"

3. **Empty or Non-.NET Repository**
   - Repository might not contain .NET code
   - Check the repository on GitHub to verify

4. **Repository is Empty**
   - The repository might be newly created
   - Make sure code has been committed and pushed

**How to Change Branch:**

```bash
# Default branch (usually 'main')
python generate_docs.py https://github.com/owner/repo

# Specific branch
python generate_docs.py https://github.com/owner/repo develop
python generate_docs.py https://github.com/owner/repo feature/my-feature
python generate_docs.py https://github.com/owner/repo release/v1.0

# Using environment variable
export GITHUB_BRANCH=develop
python generate_docs.py https://github.com/owner/repo
```

### Issue: Permission Error on Windows Cleanup

**Error:**
```
PermissionError: [WinError 5] Access is denied
```

**Cause:**
- Windows sometimes locks files in temporary directories
- Git files might be in use

**Solutions:**

1. **Automatic Retry** (Already implemented)
   - The tool now retries cleanup automatically
   - If it fails, it will just warn you

2. **Manual Cleanup**
   - The tool will show the temp directory path
   - You can manually delete it later if needed
   - Usually located in: `C:\Users\<YourName>\AppData\Local\Temp\docgen_*`

3. **Close Other Programs**
   - Close any programs that might be accessing the files
   - Close file explorers showing the temp directory

### Issue: "Failed to clone repository"

**Possible Causes:**

1. **Invalid Repository URL**
   - Check the URL format
   - Should be: `https://github.com/owner/repo` or `owner/repo`

2. **Private Repository**
   - Need GitHub token for private repos
   - **Solution:** Add to `.env`:
     ```env
     GITHUB_TOKEN=your_github_token
     ```

3. **Network Issues**
   - Check internet connection
   - GitHub might be down

4. **Branch Doesn't Exist**
   - The specified branch might not exist
   - Tool will try 'main' as fallback

**Solutions:**

```bash
# For private repos, add GitHub token
export GITHUB_TOKEN=your_token
python generate_docs.py https://github.com/owner/private-repo

# Or add to .env file
GITHUB_TOKEN=your_token
```

### Issue: "All AI API calls failed"

**Possible Causes:**

1. **Free Models Temporarily Unavailable**
   - Free models might be busy
   - **Solution:** Wait a minute and try again

2. **Network Issues**
   - Check internet connection
   - Firewall might be blocking requests

3. **Rate Limiting**
   - Too many requests
   - **Solution:** Get a free OpenRouter API key for better limits

**Solutions:**

```bash
# Get free OpenRouter key (improves reliability)
# 1. Go to https://openrouter.ai
# 2. Sign up (free, no credit card)
# 3. Get key from https://openrouter.ai/keys
# 4. Add to .env:
OPENROUTER_API_KEY=sk-or-v1-...
```

### Issue: Repository Has Files But No .cs Files Found

**Check:**

1. **File Extensions**
   - Tool looks for `.cs` files
   - Check if files have different extensions
   - The tool will show what file types it found

2. **Directory Structure**
   - Check the "Top-level directories" output
   - C# files might be in a subdirectory
   - The tool searches recursively, so this should work

3. **Hidden Files**
   - Files might be in `.git` or other hidden directories
   - These are automatically excluded

**Debug Steps:**

The tool now shows:
- Total files found
- Top-level directories
- File types found (if no .cs files)

Use this information to understand the repository structure.

### Issue: Slow Performance

**Possible Causes:**

1. **Large Repository**
   - Many files take time to process
   - **Solution:** Be patient, or process specific directories

2. **Free Models**
   - Free models are slower than paid ones
   - **Solution:** Get free OpenRouter key for better performance

3. **Network Speed**
   - Slow internet connection
   - **Solution:** Check your connection

### Getting Help

If you're still having issues:

1. **Check the Output**
   - The tool provides detailed error messages
   - Look for specific error details

2. **Verify Repository**
   - Check the repository on GitHub
   - Make sure it has C# files
   - Verify the branch exists

3. **Test with Public Repository**
   ```bash
   python generate_docs.py https://github.com/dotnet/corefx
   ```
   - If this works, the issue is with your specific repository

4. **Check Logs**
   - All output is printed to console
   - Look for warning messages
   - Check for specific error details

## Quick Reference

### Change Branch
```bash
python generate_docs.py <repo-url> <branch-name>
```

### Private Repository
```bash
# Add to .env
GITHUB_TOKEN=your_token
```

### Free AI (No Keys)
```bash
# Just run it - works automatically!
python generate_docs.py <repo-url>
```

### Better Performance
```bash
# Get free OpenRouter key
# Add to .env
OPENROUTER_API_KEY=sk-or-v1-...
```

