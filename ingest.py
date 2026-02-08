import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
WIKI_URLS = [
    "https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Installation",
    "https://wiki.gentoo.org/wiki/AMD64/CPU_Flags",
    "https://wiki.gentoo.org/wiki/Kernel/Configuration"
]
GUIDE_PATH = "base_guide.txt"

# 1. Initialize ChromaDB (Local Storage)
# This creates a folder 'gentoo_db' in your directory
db_client = chromadb.PersistentClient(path="./gentoo_db")
collection = db_client.get_or_create_collection(name="gentux_knowledge")

# 2. Function to scrape Wiki
def scrape_wiki(url):
    print(f"Scraping {url}...")
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(res.text, 'html.parser')
        content = soup.find(id="mw-content-text")
        if not content:
            print(f"Warning: Could not find main content in {url}")
            return None
        return content.get_text(separator=' ', strip=True)
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

# 3. Text Splitter (Vital for your 8GB RAM)
# We break text into 1000-character chunks so the AI doesn't choke
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# --- EXECUTION ---

# Step A: Process Static Guide
with open(GUIDE_PATH, "r") as f:
    guide_text = f.read()
    guide_chunks = text_splitter.split_text(guide_text)
    # Add to DB
    collection.add(
        documents=guide_chunks,
        ids=[f"guide_{i}" for i in range(len(guide_chunks))]
    )

# Step B: Process Live Wiki
for i, url in enumerate(WIKI_URLS):
    wiki_text = scrape_wiki(url)
    if wiki_text:
        wiki_chunks = text_splitter.split_text(wiki_text)
        collection.add(
            documents=wiki_chunks,
            ids=[f"wiki_{i}_{j}" for j in range(len(wiki_chunks))]
        )

print(f"Success! Knowledge base now contains {collection.count()} chunks.")
