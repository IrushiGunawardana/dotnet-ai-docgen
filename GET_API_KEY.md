#  Get Your FREE API Key (Required)

## Quick Setup (2 Minutes)

OpenRouter now requires an API key even for free models. Don't worry - it's **100% FREE** and takes just 2 minutes!

### Step 1: Sign Up (Free, No Credit Card)

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Click **"Sign Up"** (top right)
3. Sign up with:
   - GitHub (easiest)
   - Google
   - Email

**No credit card required!** 

### Step 2: Get Your API Key

1. After signing up, go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Click **"Create Key"**
3. Give it a name (e.g., "DocGen")
4. Copy the key (starts with `sk-or-v1-...`)

### Step 3: Add to Your Project

Create or edit `.env` file in your project root:

```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### Step 4: Restart the Application

```bash
python web_app.py
```

That's it! You're ready to generate documentation! 

## Why Do I Need a Key?

OpenRouter requires API keys to:
- Track usage (still free!)
- Prevent abuse
- Provide better service

**You still get:**
-  Free models
-  No credit card
-  No charges
-  Better reliability

## Troubleshooting

### "Invalid API key"
- Make sure you copied the entire key
- Check for extra spaces
- Verify the key starts with `sk-or-v1-`

### "Key not working"
- Make sure it's in `.env` file
- Restart the application
- Check key is active at openrouter.ai/keys

### "Still getting errors"
- Try creating a new key
- Check you're using the latest key from openrouter.ai/keys
- Make sure `.env` file is in the project root

## Alternative: Other AI Services

If you prefer, you can use:

### Azure OpenAI
```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

### OpenAI
```env
OPENAI_API_KEY=sk-...
```

See [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md) for Azure setup.

## Need Help?

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenRouter Discord](https://discord.gg/openrouter)
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

