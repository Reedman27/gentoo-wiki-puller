import pytest
from unittest.mock import MagicMock
import requests
from ingest import scrape_wiki

@pytest.fixture
def mock_requests_get(mocker):
    """Fixture to mock requests.get."""
    return mocker.patch('requests.get')

def test_scrape_wiki_success(mock_requests_get):
    """
    Test that scrape_wiki successfully scrapes content when the request is successful.
    """
    mock_response = MagicMock()
    mock_response.text = '<html><body><div id="mw-content-text">Hello World</div></body></html>'
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    text = scrape_wiki("http://fakeurl.com")
    assert text == "Hello World"
    mock_requests_get.assert_called_once_with("http://fakeurl.com", timeout=10)

def test_scrape_wiki_request_exception(mock_requests_get):
    """
    Test that scrape_wiki returns None when a RequestException occurs.
    """
    mock_requests_get.side_effect = requests.exceptions.RequestException("Test error")
    text = scrape_wiki("http://fakeurl.com")
    assert text is None
    mock_requests_get.assert_called_once_with("http://fakeurl.com", timeout=10)

def test_scrape_wiki_bad_status(mock_requests_get):
    """
    Test that scrape_wiki returns None when the response has a bad status.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_requests_get.return_value = mock_response

    text = scrape_wiki("http://fakeurl.com")
    assert text is None
    mock_requests_get.assert_called_once_with("http://fakeurl.com", timeout=10)

def test_scrape_wiki_no_content(mock_requests_get):
    """
    Test that scrape_wiki returns None when the content div is not found.
    """
    mock_response = MagicMock()
    mock_response.text = '<html><body><div>No content here</div></body></html>'
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    text = scrape_wiki("http://fakeurl.com")
    assert text is None
    mock_requests_get.assert_called_once_with("http://fakeurl.com", timeout=10)
