import ollama
try:
    response = ollama.list()
    print("Success! Python can talk to Ollama.")
except Exception as e:
    print(f"Error: {e}")
