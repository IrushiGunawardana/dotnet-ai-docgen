# 🆓 Free AI Setup Guide

**Good news!** This tool works **completely FREE** - no paid API keys required!

## ✅ Free Option: OpenRouter (No API Key Needed!)

OpenRouter provides **free AI models** that you can use without any API key or payment!

### How It Works

The tool automatically uses OpenRouter's free tier if no API keys are configured. **You don't need to do anything!**

### Free Models Available

The tool will automatically try these free models (in order):

1. **Mistral 7B Instruct** (`mistralai/mistral-7b-instruct:free`)
   - Great for code documentation
   - Fast and reliable
   - 7 billion parameters

2. **Google Gemini Flash 1.5** (`google/gemini-flash-1.5:free`)
   - Excellent for technical writing
   - Good code understanding
   - Fast responses

3. **Meta Llama 3.2 3B** (`meta-llama/llama-3.2-3b-instruct:free`)
   - Lightweight and efficient
   - Good for documentation
   - Fast processing

## 🚀 Quick Start (100% Free)

### Option 1: No Configuration Needed (Easiest!)

Just run the tool - it will automatically use free models:

```bash
python generate_docs.py https://github.com/owner/repo-name
```

**That's it!** No `.env` file needed, no API keys required!

### Option 2: Get Free API Key (Recommended for Better Performance)

While not required, getting a free OpenRouter API key gives you:
- Higher rate limits
- Better reliability
- Priority access

**Steps:**

1. **Sign up for free** at [openrouter.ai](https://openrouter.ai)
   - Click "Sign Up" (top right)
   - Use GitHub, Google, or email
   - **100% free, no credit card required**

2. **Get your API key**
   - Go to [openrouter.ai/keys](https://openrouter.ai/keys)
   - Click "Create Key"
   - Copy the key

3. **Add to `.env` file** (optional):
   ```env
   OPENROUTER_API_KEY=sk-or-v1-...
   ```

## 📊 Free Tier Limits

### Without API Key (Anonymous)
- ✅ Unlimited requests
- ✅ All free models available
- ⚠️ Lower rate limits (may be slower during peak times)

### With Free API Key
- ✅ Higher rate limits
- ✅ Better reliability
- ✅ Priority access to free models
- ✅ Usage tracking dashboard
- ✅ **Still 100% free!**

## 🎯 Which Free Option Should I Use?

| Scenario | Recommendation |
|----------|---------------|
| Just trying it out | **No setup needed** - just run it! |
| Regular use | **Get free OpenRouter key** for better performance |
| Production/CI/CD | **Get free OpenRouter key** for reliability |

## 💡 Tips for Best Free Experience

1. **Be patient**: Free models may be slightly slower than paid ones
2. **Smaller projects first**: Test with small repos to see results
3. **Get the free API key**: Takes 2 minutes, improves experience significantly
4. **Check model status**: If one free model is down, the tool automatically tries others

## 🔄 How the Tool Chooses Models

The tool tries models in this order:

1. **Azure OpenAI** (if configured - paid)
2. **OpenAI** (if configured - paid)
3. **OpenRouter with API key** (if configured - free)
4. **OpenRouter without API key** (automatic - free) ← **You are here!**

So even if you don't configure anything, it will work!

## ❓ FAQ

### Q: Is it really free?
**A:** Yes! OpenRouter's free tier is completely free with no credit card required.

### Q: Will I be charged?
**A:** No. The free models on OpenRouter are completely free. You only pay if you choose to use paid models (which this tool doesn't use by default).

### Q: What if free models are down?
**A:** The tool automatically tries multiple free models. If all are down, wait a few minutes and try again.

### Q: Can I use this in production?
**A:** Yes! The free tier is suitable for most use cases. For high-volume production, consider getting a free OpenRouter API key for better rate limits.

### Q: How do I know which model is being used?
**A:** The tool prints which model it's using when it runs. Look for messages like:
```
✓ Using OpenRouter FREE model: mistralai/mistral-7b-instruct:free (no API key needed!)
```

## 🎉 Ready to Go!

You're all set! Just run:

```bash
python generate_docs.py https://github.com/your-username/your-repo
```

No configuration needed - it will automatically use free AI models! 🚀

## 📚 Other Free Alternatives

If you want to explore other free options:

- **Hugging Face Inference API** - Some free models available
- **Ollama** (local) - Run models on your own machine (requires setup)
- **Google Colab** - Free GPU access for running models

But for this tool, **OpenRouter's free tier is the easiest and most reliable option!**

