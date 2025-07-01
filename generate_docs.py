import os
import requests
from dotenv import load_dotenv

"""
This script reads a .NET C# code file (Program.cs),
sends the content to OpenRouter for documentation generation,
and writes the result into an .rst file for Sphinx.
"""

# Load API key from .env file
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct:free"

def get_summary(code):
    """
    Sends C# code to OpenRouter and returns the AI-generated documentation.
    """
    prompt = f"""
You are an expert software architect. Document the following C# class with:
- Purpose of each method
- Parameters
- Return values
- Example usage

```csharp
{code}
```
"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/IrushiGunawardana/dotnet-ai-docgen",
            "X-Title": "DotNet DocGen"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        data = response.json()
        return data['choices'][0]['message']['content']
    except KeyError:
        print("❌ API response error!")
        print("Status code:", response.status_code)
        print("Response JSON:")
        print(response.text)
        raise

def main():
    """
    Reads Program.cs, generates documentation, and writes it to ai_generated.rst
    """
    with open("DotNetExample/Program.cs", "r", encoding="utf-8") as f:
        code = f.read()

    summary = get_summary(code)

    os.makedirs("docs/source", exist_ok=True)

    with open("docs/source/ai_generated.rst", "w", encoding="utf-8") as out:
        out.write("AI-Generated Documentation\n===========================\n\n")
        out.write(summary)

if __name__ == "__main__":
    main()