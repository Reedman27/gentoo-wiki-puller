# Gentux-AI: Gentoo Assistant

An AI-assisted guide system for Gentoo Linux that stays current by syncing with the Gentoo Wiki.

## Features
- **RAG Architecture**: Uses ChromaDB to provide local context to the AI.
- **Wiki-Sync**: Weekly automated scraping of the official Gentoo Wiki.
- **Hardware Optimized**: Designed to run on low-resource hardware (AMD A4 / 8GB RAM) using Phi-3.

## Setup
1. Install Ollama and pull Phi-3: `ollama pull phi3:mini`
2. Set up venv: `python3 -m venv venv && source venv/bin/activate`
3. Install deps: `pip install chromadb ollama langchain-text-splitters requests beautifulsoup4`
4. Ingest data: `python3 ingest.py`
5. Chat: `python3 chat.py`

## License
Licensed under the GNU General Public License v3.0 (GPLv3). See LICENSE for details.
last thing idk if this will work
