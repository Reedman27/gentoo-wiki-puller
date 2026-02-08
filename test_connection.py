import ollama
import pytest

def test_ollama_connection():
    """
    Tests that the python client can connect to the Ollama server.
    """
    try:
        ollama.list()
    except Exception as e:
        pytest.fail(f"Failed to connect to Ollama: {e}")