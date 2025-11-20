# How to Get Azure OpenAI Credentials

This guide will walk you through obtaining your Azure OpenAI API key, endpoint, and deployment name.

## Prerequisites

- An Azure account (sign up at [azure.microsoft.com](https://azure.microsoft.com) if you don't have one)
- Access to Azure OpenAI service (may require approval/whitelisting)

## Step-by-Step Guide

### Step 1: Create an Azure OpenAI Resource

1. **Sign in to Azure Portal**
   - Go to [portal.azure.com](https://portal.azure.com)
   - Sign in with your Azure account

2. **Create a new resource**
   - Click **"Create a resource"** (top left)
   - Search for **"Azure OpenAI"**
   - Click **"Azure OpenAI"** from the results
   - Click **"Create"**

3. **Fill in the resource details**
   - **Subscription**: Select your Azure subscription
   - **Resource Group**: Create new or select existing
   - **Region**: Choose a region (e.g., East US, West Europe)
   - **Name**: Give your resource a unique name (e.g., `my-openai-resource`)
   - **Pricing Tier**: Select a tier (usually "Standard S0")
   - Click **"Review + create"**, then **"Create"**

4. **Wait for deployment**
   - This may take a few minutes
   - Click **"Go to resource"** when deployment completes

### Step 2: Get Your Endpoint

1. **In your Azure OpenAI resource page**
   - Look for the **"Keys and Endpoint"** section in the left menu
   - Click on **"Keys and Endpoint"**

2. **Copy the Endpoint**
   - You'll see a field labeled **"Endpoint"**
   - It will look like: `https://your-resource-name.openai.azure.com/`
   - Copy this entire URL (including `https://` and trailing `/`)
   - This is your `AZURE_OPENAI_ENDPOINT`

### Step 3: Get Your API Key

1. **In the same "Keys and Endpoint" page**
   - You'll see two keys: **KEY 1** and **KEY 2**
   - Either key will work (they're interchangeable)
   - Click the **copy icon** next to KEY 1
   - This is your `AZURE_OPENAI_API_KEY`

   ⚠️ **Important**: Keep this key secret! Never commit it to version control.

### Step 4: Create a Model Deployment

1. **Navigate to Model deployments**
   - In the left menu, click **"Model deployments"**
   - Click **"Create"** or **"+ Create"**

2. **Configure the deployment**
   - **Deployment name**: Give it a name (e.g., `gpt-4`, `gpt-35-turbo`, `gpt-4o`)
     - This name is what you'll use as `AZURE_OPENAI_DEPLOYMENT`
   - **Model**: Select a model from the dropdown:
     - `gpt-4` (or `gpt-4-32k` for longer context)
     - `gpt-35-turbo` (faster, cheaper)
     - `gpt-4o` (latest GPT-4 model)
     - `gpt-4o-mini` (smaller, faster)
   - **Model version**: Usually auto-selected (use the latest)
   - Click **"Create"**

3. **Wait for deployment**
   - This usually takes 1-2 minutes
   - The status will change to "Succeeded"

4. **Note the deployment name**
   - The name you gave in step 2 is your `AZURE_OPENAI_DEPLOYMENT`
   - Common names: `gpt-4`, `gpt-35-turbo`, `gpt-4o`

### Step 5: Configure Your .env File

1. **Create or edit `.env` file** in your project root:

```env
AZURE_OPENAI_API_KEY=your_actual_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

2. **Replace the values**:
   - `your_actual_key_here` → Your KEY 1 from Step 3
   - `your-resource-name.openai.azure.com` → Your endpoint from Step 2
   - `gpt-4` → Your deployment name from Step 4

### Example .env File

```env
AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
AZURE_OPENAI_ENDPOINT=https://my-docgen-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

## Quick Reference

| What | Where to Find | Example |
|------|---------------|---------|
| **API Key** | Azure Portal → Your Resource → Keys and Endpoint → KEY 1 | `abc123...xyz` |
| **Endpoint** | Azure Portal → Your Resource → Keys and Endpoint → Endpoint | `https://my-resource.openai.azure.com/` |
| **Deployment** | Azure Portal → Your Resource → Model deployments → Deployment name | `gpt-4` |

## Troubleshooting

### "Access denied" or "Resource not found"
- Make sure you have access to Azure OpenAI (may require approval)
- Verify you're using the correct subscription
- Check that the resource exists in the selected region

### "Deployment not found"
- Make sure you've created a model deployment (Step 4)
- Verify the deployment name matches exactly (case-sensitive)
- Check that the deployment status is "Succeeded"

### "Invalid API key"
- Verify you copied the entire key (no spaces, no extra characters)
- Make sure you're using KEY 1 or KEY 2 from the Keys and Endpoint page
- Regenerate the key if needed (this will invalidate the old one)

### "Endpoint format error"
- Make sure the endpoint includes `https://` at the beginning
- Include the trailing `/` at the end
- Example: `https://your-resource.openai.azure.com/`

## Cost Considerations

- Azure OpenAI charges based on usage (tokens processed)
- Different models have different pricing:
  - `gpt-4` / `gpt-4o`: More expensive, higher quality
  - `gpt-35-turbo` / `gpt-4o-mini`: Less expensive, still very capable
- Check [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current rates
- Set up spending limits in Azure to avoid unexpected charges

## Security Best Practices

1. **Never commit `.env` to Git**
   - Already in `.gitignore` ✅
   - Use GitHub Secrets for CI/CD

2. **Rotate keys regularly**
   - Regenerate keys in Azure Portal if compromised
   - Update all applications using the key

3. **Use least privilege**
   - Only grant access to necessary resources
   - Use separate keys for different environments

## Alternative: Using OpenAI Directly

If you prefer to use OpenAI directly (not through Azure):

1. Get an API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Add to `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. The tool will automatically use OpenAI instead of Azure OpenAI

## Need Help?

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure OpenAI Service Overview](https://azure.microsoft.com/products/ai-services/openai-service)
- [OpenAI API Documentation](https://platform.openai.com/docs)

