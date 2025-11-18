"""Anthropic Claude AI Helper"""

class AnthropicHelper:
    """Helper class for Claude AI integration"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "claude-sonnet-4-20250514"
        self.max_tokens = 4096
    
    def get_completion(self, prompt: str, system_prompt: str = None, temperature: float = 1.0) -> str:
        """Get completion from Claude AI"""
        try:
            import requests
            
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            messages = [{"role": "user", "content": prompt}]
            
            data = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": temperature,
                "messages": messages
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
