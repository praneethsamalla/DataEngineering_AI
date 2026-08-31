import os
import anthropic
if not os.environ.get("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

client = anthropic.Anthropic()

print("Client created successfully. Key found:", bool(os.environ.get("ANTHROPIC_API_KEY")))