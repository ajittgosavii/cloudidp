"""Anthropic Claude AI Helper"""

class AnthropicHelper:
    """Helper class for Claude AI integration"""
    
    def __init__(self, api_key: str):
        """Initialize the Anthropic helper
        
        Args:
            api_key: Anthropic API key
        """
        self.api_key = api_key
        self.model = "claude-sonnet-4-20250514"
        self.max_tokens = 4096
    
    def get_completion(self, prompt: str, system_prompt: str = None, temperature: float = 1.0) -> str:
        """Get completion from Claude AI
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            temperature: Randomness in responses (0.0-1.0)
            
        Returns:
            Claude's response text or error message
        """
        try:
            import requests
            
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            data = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=60  # Add timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error: Network error - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_architecture(self, architecture_description: str) -> str:
        """Analyze an architecture design using Claude
        
        Args:
            architecture_description: Description of the architecture
            
        Returns:
            Analysis and recommendations
        """
        prompt = f"""Analyze the following AWS architecture and provide detailed feedback:

Architecture Description:
{architecture_description}

Please provide:
1. Architecture strengths
2. Potential issues or risks
3. Security considerations
4. Cost optimization opportunities
5. Recommendations for improvement
"""
        
        system_prompt = """You are an expert AWS Solutions Architect with deep knowledge of 
cloud architecture best practices, security, compliance, and cost optimization. Provide 
thorough, actionable analysis."""
        
        return self.get_completion(prompt, system_prompt, temperature=0.7)
