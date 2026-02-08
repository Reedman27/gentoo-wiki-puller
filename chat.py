import chromadb
import ollama

# Connect to your local brain
client = chromadb.PersistentClient(path="./gentoo_db")
collection = client.get_collection(name="gentux_knowledge")

def chat():
    print("\n\033[1;34m[Gentux Living Assistant Loaded]\033[0m")
    print("Ask about your guide or latest Wiki updates. Type 'exit' to quit.\n")

    while True:
        user_input = input("\033[1;32m➜ \033[0m")
        if user_input.lower() == 'exit': break

        # 1. Search DB for the most relevant technical snippets
        results = collection.query(query_texts=[user_input], n_results=5)
        context = "\n".join(results['documents'][0])

        # 2. Construct the prompt
        system_prompt = (
            "You are a Gentoo Linux expert. Use the provided context to answer. "
            "If the Wiki context is newer than the Guide context, prioritize the Wiki."
        )
        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Question: {user_input}"

        # 3. Stream the response so it feels faster on your CPU
        print("\033[1;34mGentux:\033[0m ", end="")
        stream = ollama.generate(model='phi3:mini', prompt=full_prompt, stream=True)
        
        for chunk in stream:
            print(chunk['response'], end='', flush=True)
        print("\n")

if __name__ == "__main__":
    chat()
