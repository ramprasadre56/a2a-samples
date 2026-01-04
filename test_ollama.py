import litellm
import os

# Turn on debug logging
litellm.set_verbose = True

try:
    print("Attempting to call local Ollama with gemma3:1b...")
    response = litellm.completion(
        model="ollama/gemma3:1b",
        messages=[{"role": "user", "content": "Hi, who are you?"}],
        api_base="http://localhost:11434"
    )
    print("\nResponse received:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"\nError: {e}")
