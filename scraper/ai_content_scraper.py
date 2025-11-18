#!/usr/bin/env python3
"""
AI Content Scraper
Scrapes the web for articles, blog posts, and media about AI overstepping,
deleting projects, data harvesting, and other AI-related issues.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin, urlparse


class AIContentScraper:
    """Scraper for finding AI-related problematic content on the web."""
    
    def __init__(self):
        self.search_terms = [
            "AI deleting project",
            "AI overstepping boundaries",
            "AI data harvesting",
            "AI opt-out privacy",
            "AI gone wrong",
            "AI mistakes deleted",
            "ChatGPT deleting code",
            "Copilot privacy concerns",
            "AI assistant data collection",
            "AI training on private data",
            "AI unexpected behavior",
            "AI harmful suggestions"
        ]
        
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_google_news(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search Google News for articles matching the query.
        Note: This is a simplified version. For production, consider using Google News API.
        """
        articles = []
        search_url = f"https://news.google.com/search?q={query.replace(' ', '+')}"
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Parse Google News results
                for article in soup.find_all('article', limit=num_results):
                    title_elem = article.find('a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')
                        if link.startswith('./'):
                            link = 'https://news.google.com' + link[1:]
                        
                        articles.append({
                            'title': title,
                            'url': link,
                            'source': 'Google News',
                            'search_term': query,
                            'date_found': datetime.now().isoformat()
                        })
        except Exception as e:
            print(f"Error searching Google News for '{query}': {e}")
        
        return articles
    
    def search_hacker_news(self, query: str) -> List[Dict]:
        """Search Hacker News using Algolia API."""
        articles = []
        api_url = f"https://hn.algolia.com/api/v1/search?query={query.replace(' ', '+')}&tags=story"
        
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for hit in data.get('hits', [])[:10]:
                    articles.append({
                        'title': hit.get('title', ''),
                        'url': hit.get('url', f"https://news.ycombinator.com/item?id={hit.get('objectID')}"),
                        'source': 'Hacker News',
                        'points': hit.get('points', 0),
                        'num_comments': hit.get('num_comments', 0),
                        'search_term': query,
                        'date_found': datetime.now().isoformat(),
                        'created_at': hit.get('created_at', '')
                    })
        except Exception as e:
            print(f"Error searching Hacker News for '{query}': {e}")
        
        return articles
    
    def search_reddit(self, query: str, subreddits: List[str] = None) -> List[Dict]:
        """Search Reddit for relevant posts."""
        if subreddits is None:
            subreddits = ['technology', 'programming', 'artificial', 'MachineLearning', 
                         'ChatGPT', 'OpenAI', 'LocalLLaMA']
        
        posts = []
        for subreddit in subreddits:
            try:
                # Using Reddit's JSON API (no auth required for public data)
                url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query.replace(' ', '+')}&restrict_sr=1&limit=10"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for post in data.get('data', {}).get('children', []):
                        post_data = post.get('data', {})
                        posts.append({
                            'title': post_data.get('title', ''),
                            'url': f"https://www.reddit.com{post_data.get('permalink', '')}",
                            'source': f'Reddit r/{subreddit}',
                            'score': post_data.get('score', 0),
                            'num_comments': post_data.get('num_comments', 0),
                            'search_term': query,
                            'date_found': datetime.now().isoformat(),
                            'created_utc': post_data.get('created_utc', 0)
                        })
                
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"Error searching Reddit r/{subreddit} for '{query}': {e}")
        
        return posts
    
    def scrape_all(self, max_per_term: int = 5) -> List[Dict]:
        """Run all scrapers for all search terms."""
        all_results = []
        
        print("Starting AI content scraping...")
        print(f"Searching for {len(self.search_terms)} different terms\n")
        
        for i, term in enumerate(self.search_terms, 1):
            print(f"[{i}/{len(self.search_terms)}] Searching for: '{term}'")
            
            # Search Hacker News
            print("  - Searching Hacker News...")
            hn_results = self.search_hacker_news(term)
            all_results.extend(hn_results[:max_per_term])
            print(f"    Found {len(hn_results)} results")
            
            time.sleep(1)  # Rate limiting
            
            # Search Reddit
            print("  - Searching Reddit...")
            reddit_results = self.search_reddit(term)
            all_results.extend(reddit_results[:max_per_term])
            print(f"    Found {len(reddit_results)} results")
            
            time.sleep(1)  # Rate limiting
            
            # Optional: Search Google News (may be blocked by some networks)
            # print("  - Searching Google News...")
            # news_results = self.search_google_news(term, max_per_term)
            # all_results.extend(news_results)
            # print(f"    Found {len(news_results)} results")
            
            print()
        
        self.results = all_results
        return all_results
    
    def filter_duplicates(self) -> List[Dict]:
        """Remove duplicate URLs from results."""
        seen_urls = set()
        unique_results = []
        
        for result in self.results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        self.results = unique_results
        return unique_results
    
    def save_to_json(self, filename: str = 'scraped_content.json'):
        """Save results to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'scrape_date': datetime.now().isoformat(),
                'total_results': len(self.results),
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {filename}")
    
    def save_to_markdown(self, filename: str = 'SCRAPED_CONTENT.md'):
        """Save results to markdown file organized by source."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# AI-as-a-Trojan: Scraped Content\n\n")
            f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"Total articles found: {len(self.results)}\n\n")
            f.write("---\n\n")
            
            # Group by source
            by_source = {}
            for result in self.results:
                source = result.get('source', 'Unknown')
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(result)
            
            # Write each source section
            for source, articles in sorted(by_source.items()):
                f.write(f"## {source}\n\n")
                for article in articles:
                    f.write(f"### {article.get('title', 'No title')}\n\n")
                    f.write(f"- **URL**: {article.get('url', 'N/A')}\n")
                    f.write(f"- **Search term**: {article.get('search_term', 'N/A')}\n")
                    
                    if 'points' in article:
                        f.write(f"- **Points**: {article['points']}\n")
                    if 'score' in article:
                        f.write(f"- **Score**: {article['score']}\n")
                    if 'num_comments' in article:
                        f.write(f"- **Comments**: {article['num_comments']}\n")
                    
                    f.write(f"- **Found on**: {article.get('date_found', 'N/A')}\n")
                    f.write("\n")
                
                f.write("---\n\n")
        
        print(f"Markdown report saved to {filename}")
    
    def generate_categorized_structure(self):
        """Generate a categorized folder structure similar to Microsoft/Copilot-in-Word."""
        category_map = {
            'Microsoft': ['copilot', 'microsoft', 'bing', 'azure'],
            'OpenAI': ['openai', 'chatgpt', 'gpt'],
            'Google': ['google', 'bard', 'gemini'],
            'GitHub': ['github', 'copilot'],
            'Privacy': ['privacy', 'data harvesting', 'opt-out', 'data collection'],
            'Deleted-Projects': ['deleted', 'deleting', 'lost project', 'wiped'],
            'AI-Mistakes': ['mistake', 'wrong', 'harmful', 'unexpected behavior']
        }
        
        categorized = {}
        for result in self.results:
            title = result.get('title', '').lower()
            search_term = result.get('search_term', '').lower()
            combined_text = f"{title} {search_term}"
            
            matched = False
            for category, keywords in category_map.items():
                if any(keyword in combined_text for keyword in keywords):
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(result)
                    matched = True
                    break
            
            if not matched:
                if 'Other' not in categorized:
                    categorized['Other'] = []
                categorized['Other'].append(result)
        
        return categorized


def main():
    """Main entry point for the scraper."""
    scraper = AIContentScraper()
    
    # Scrape content
    results = scraper.scrape_all(max_per_term=5)
    
    # Remove duplicates
    scraper.filter_duplicates()
    
    print(f"\nTotal unique results: {len(scraper.results)}")
    
    # Save results
    scraper.save_to_json('scraper/scraped_content.json')
    scraper.save_to_markdown('scraper/SCRAPED_CONTENT.md')
    
    # Generate categorized view
    categorized = scraper.generate_categorized_structure()
    print("\nResults by category:")
    for category, items in sorted(categorized.items()):
        print(f"  {category}: {len(items)} items")


if __name__ == '__main__':
    main()
