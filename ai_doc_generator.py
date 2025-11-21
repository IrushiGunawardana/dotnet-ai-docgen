"""
AI Documentation Generator
Generates documentation using Azure OpenAI or OpenRouter API.
"""
import os
import requests
from typing import Optional, Dict, List
from openai import AzureOpenAI
from openai import OpenAI


class AIDocGenerator:
    """Generates documentation using AI services."""
    
    def __init__(self):
        """Initialize AI documentation generator."""
        self.azure_openai_client = None
        self.openai_client = None
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize Azure OpenAI if available
        if self.azure_api_key and self.azure_endpoint:
            try:
                self.azure_openai_client = AzureOpenAI(
                    api_key=self.azure_api_key,
                    api_version="2024-02-15-preview",
                    azure_endpoint=self.azure_endpoint
                )
                print("✓ Azure OpenAI client initialized")
            except Exception as e:
                print(f"Warning: Could not initialize Azure OpenAI: {e}")
        
        # Initialize OpenAI if available
        if self.openai_api_key:
            try:
                self.openai_client = OpenAI(api_key=self.openai_api_key)
                print("✓ OpenAI client initialized")
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI: {e}")
    
    def generate_angular_documentation(self, code: str, file_path: str) -> str:
        """Generate documentation for Angular/TypeScript code."""
        prompt = f"""You are an expert Angular/TypeScript developer and technical writer. Generate comprehensive documentation for the following Angular/TypeScript code.

File: {file_path}

Requirements:
1. Provide a clear overview of the component/service/module purpose
2. Document each public method, property, and decorator
3. Explain Angular-specific features (@Component, @Injectable, etc.)
4. Document inputs, outputs, and dependencies
5. Include usage examples
6. Format the output in reStructuredText (RST) format suitable for Sphinx

Code:
```typescript
{code}
```

Generate comprehensive documentation in RST format:"""
        
        return self._call_ai_api(prompt)
    
    def generate_html_documentation(self, code: str, file_path: str) -> str:
        """Generate documentation for HTML/CSS/JavaScript code."""
        file_ext = file_path.split('.')[-1].lower()
        
        if file_ext == 'html':
            prompt = f"""You are an expert web developer and technical writer. Generate comprehensive documentation for the following HTML code.

File: {file_path}

Requirements:
1. Document the structure and purpose
2. Explain key elements and their relationships
3. Document any scripts, styles, or external resources
4. Include accessibility considerations
5. Format the output in reStructuredText (RST) format suitable for Sphinx

HTML Code:
```html
{code}
```

Generate comprehensive documentation in RST format:"""
        elif file_ext in ['css', 'scss']:
            prompt = f"""You are an expert CSS developer and technical writer. Generate comprehensive documentation for the following CSS code.

File: {file_path}

Requirements:
1. Document the styling approach and design system
2. Explain key selectors and their purpose
3. Document responsive breakpoints and media queries
4. Include usage examples
5. Format the output in reStructuredText (RST) format suitable for Sphinx

CSS Code:
```css
{code}
```

Generate comprehensive documentation in RST format:"""
        else:  # JavaScript
            prompt = f"""You are an expert JavaScript developer and technical writer. Generate comprehensive documentation for the following JavaScript code.

File: {file_path}

Requirements:
1. Provide a clear overview of the script's purpose
2. Document each function, class, and method
3. Explain parameters, return values, and side effects
4. Include usage examples
5. Format the output in reStructuredText (RST) format suitable for Sphinx

JavaScript Code:
```javascript
{code}
```

Generate comprehensive documentation in RST format:"""
        
        return self._call_ai_api(prompt)
    
    def generate_class_documentation(self, code: str, file_path: str, namespace: Optional[str] = None) -> str:
        """
        Generate documentation for a C# class or file.
        
        Args:
            code: C# code content
            file_path: Path to the source file
            namespace: Optional namespace
            
        Returns:
            Generated documentation in RST format
        """
        prompt = f"""You are an expert .NET software architect and technical writer. Generate comprehensive documentation for the following C# code.

File: {file_path}
Namespace: {namespace or "N/A"}

Requirements:
1. Provide a clear overview of the class/file purpose
2. Document each public method with:
   - Purpose and functionality
   - Parameters (type, name, description)
   - Return values (type and description)
   - Exceptions that may be thrown
   - Example usage if applicable
3. Document properties, fields, and events if present
4. Include any important implementation details or design patterns used
5. Format the output in reStructuredText (RST) format suitable for Sphinx

C# Code:
```csharp
{code}
```

Generate comprehensive documentation in RST format:"""
        
        return self._call_ai_api(prompt)
    
    def generate_project_overview(self, project_structure: Dict) -> str:
        """
        Generate project overview documentation.
        
        Args:
            project_structure: Project structure dictionary
            
        Returns:
            Generated overview documentation
        """
        structure_summary = f"""
Project Structure:
- Root Path: {project_structure.get('root_path')}
- Solution Files: {len(project_structure.get('solution_files', []))}
- Project Files: {len(project_structure.get('project_files', []))}
- C# Files: {len(project_structure.get('csharp_files', []))}

Files:
"""
        for file_info in project_structure.get('csharp_files', [])[:20]:  # Limit to first 20
            structure_summary += f"- {file_info['relative_path']} ({file_info['classes_count']} classes)\n"
        
        prompt = f"""You are an expert .NET software architect. Generate a comprehensive project overview documentation based on the following project structure.

{structure_summary}

Generate:
1. Project overview and purpose
2. Architecture description
3. Key components and their relationships
4. Technology stack (if identifiable)
5. Project organization

Format the output in reStructuredText (RST) format suitable for Sphinx:"""
        
        return self._call_ai_api(prompt)
    
    def _call_ai_api(self, prompt: str) -> str:
        """
        Call AI API (Azure OpenAI, OpenAI, or OpenRouter).
        
        Args:
            prompt: Prompt to send to AI
            
        Returns:
            AI-generated response
        """
        # Try Azure OpenAI first
        if self.azure_openai_client:
            try:
                response = self.azure_openai_client.chat.completions.create(
                    model=self.azure_deployment,
                    messages=[
                        {"role": "system", "content": "You are an expert .NET software architect and technical writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=4000
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Warning: Azure OpenAI call failed: {e}, trying fallback...")
        
        # Try OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert .NET software architect and technical writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=4000
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Warning: OpenAI call failed: {e}, trying fallback...")
        
        # Fallback to OpenRouter (FREE TIER AVAILABLE)
        # Try with API key first, then try without (free tier)
        openrouter_models = [
            "mistralai/mistral-7b-instruct:free",  # Free
            "google/gemini-flash-1.5:free",  # Free
            "meta-llama/llama-3.2-3b-instruct:free",  # Free
        ]
        
        # Try with API key if available
        if self.openrouter_api_key:
            for model in openrouter_models:
                try:
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_api_key}",
                            "HTTP-Referer": "https://github.com/IrushiGunawardana/dotnet-ai-docgen",
                            "X-Title": "DotNet DocGen"
                        },
                        json={
                            "model": model,
                            "messages": [
                                {"role": "system", "content": "You are an expert .NET software architect and technical writer."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.3,
                            "max_tokens": 4000
                        },
                        timeout=60
                    )
                    response.raise_for_status()
                    data = response.json()
                    print(f"✓ Using OpenRouter model: {model}")
                    return data['choices'][0]['message']['content']
                except Exception as e:
                    print(f"  Trying next free model... ({model} failed: {str(e)[:50]})")
                    continue
        
        # OpenRouter now requires API key even for free models
        # Provide helpful error message
        error_msg = """
❌ No AI API key configured!

OpenRouter now requires a free API key even for free models.

🔑 Get your FREE API key (takes 2 minutes, no credit card):
   1. Visit: https://openrouter.ai
   2. Sign up (free, no credit card required)
   3. Go to: https://openrouter.ai/keys
   4. Create a new key
   5. Add to .env file: OPENROUTER_API_KEY=sk-or-v1-...

💡 Alternative: Use Azure OpenAI or OpenAI API keys
   See README.md for setup instructions.

For more help, see: FREE_AI_SETUP.md
"""
        raise Exception(error_msg)

