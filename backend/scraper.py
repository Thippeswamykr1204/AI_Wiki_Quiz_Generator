"""
Wikipedia scraper with preview functionality
Fetches and cleans Wikipedia article content
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Tuple, Dict


def preview_wikipedia_url(url: str) -> Dict:
    """
    Preview Wikipedia article without full scraping
    Returns basic info for validation and caching check
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        dict: Preview information
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1', {'id': 'firstHeading'})
        title = title_elem.get_text().strip() if title_elem else url.split('/wiki/')[-1].replace('_', ' ')
        
        # Extract first paragraph for summary
        content_div = soup.find('div', {'id': 'mw-content-text'})
        summary = None
        if content_div:
            first_para = content_div.find('p')
            if first_para:
                summary = first_para.get_text().strip()[:300]
                summary = re.sub(r'\[\d+\]', '', summary)  # Remove citation numbers
        
        # Try to get image from infobox
        image_url = None
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            img = infobox.find('img')
            if img and img.get('src'):
                image_url = 'https:' + img['src'] if img['src'].startswith('//') else img['src']
        
        # Estimate word count
        word_count = None
        if content_div:
            text = content_div.get_text()
            word_count = len(text.split())
        
        return {
            "url": url,
            "title": title,
            "summary": summary,
            "is_valid": True,
            "image_url": image_url,
            "word_count": word_count
        }
        
    except Exception as e:
        return {
            "url": url,
            "title": None,
            "summary": None,
            "is_valid": False,
            "error": str(e)
        }


def scrape_wikipedia(url: str) -> Tuple[str, str, str]:
    """
    Scrape Wikipedia article and return cleaned content
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        tuple: (cleaned_text, article_title, raw_html)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"  → Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1', {'id': 'firstHeading'})
        title = title_elem.get_text().strip() if title_elem else url.split('/wiki/')[-1].replace('_', ' ')
        print(f"  → Title: {title}")
        
        # Find main content
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            raise ValueError("Could not find main content")
        
        content_wrapper = content_div.find('div', {'class': 'mw-parser-output'})
        if not content_wrapper:
            content_wrapper = content_div
        
        # Remove unwanted elements
        for selector in ['sup', 'table', 'div.reflist', 'div.navbox', 'div.infobox',
                        'span.mw-editsection', 'style', 'script', 'noscript']:
            for element in content_wrapper.select(selector):
                element.decompose()
        
        # Extract paragraphs
        paragraphs = []
        for p in content_wrapper.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 20:
                paragraphs.append(text)
        
        cleaned_text = ' '.join(paragraphs)
        
        # Clean up text
        cleaned_text = re.sub(r'\[\d+\]', '', cleaned_text)  # Remove citations
        cleaned_text = re.sub(r'\[citation needed\]', '', cleaned_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Normalize whitespace
        
        # Limit text length for efficiency
        words = cleaned_text.split()
        if len(words) > 5000:
            cleaned_text = ' '.join(words[:5000])
            print(f"  → Truncated to 5000 words")
        
        print(f"  → Extracted {len(words)} words")
        
        if len(cleaned_text) < 200:
            raise ValueError("Content too short (less than 200 characters)")
        
        return cleaned_text, title, response.text
        
    except Exception as e:
        raise Exception(f"Scraping error: {str(e)}")


if __name__ == "__main__":
    # Test scraper
    test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    try:
        text, title, html = scrape_wikipedia(test_url)
        print(f"\n✅ Successfully scraped: {title}")
        print(f"📝 Content length: {len(text)} characters")
    except Exception as e:
        print(f"\n❌ Error: {e}")