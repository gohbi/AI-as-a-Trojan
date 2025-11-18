# AI Content Scraper

A Python-based web scraper that searches for and collects articles, blog posts, and media about AI overstepping, deleting projects, data harvesting, and other AI-related issues.

## Features

- **Multi-source scraping**: Searches Hacker News, Reddit, and optionally Google News
- **Comprehensive search terms**: Covers AI deletion, privacy concerns, data harvesting, and unexpected behavior
- **Duplicate filtering**: Removes duplicate URLs from results
- **Multiple output formats**: JSON and Markdown
- **Categorized results**: Automatically categorizes findings by company and issue type
- **Rate limiting**: Respects API rate limits to avoid blocking

## Requirements

- Python 3.7 or higher
- Internet connection (for accessing Hacker News, Reddit, and other APIs)
- No API keys required for basic functionality

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:

```bash
cd scraper
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python ai_content_scraper.py
```

This will:
- Search for 12 different AI-related terms
- Query Hacker News and Reddit for each term
- Save results to `scraped_content.json` and `SCRAPED_CONTENT.md`

### Output Files

- **scraped_content.json**: Raw JSON data with all findings
- **SCRAPED_CONTENT.md**: Human-readable markdown report organized by source

See [EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md) for a sample of what the scraped content looks like.

### Search Terms

The scraper searches for:
- AI deleting project
- AI overstepping boundaries
- AI data harvesting
- AI opt-out privacy
- AI gone wrong
- AI mistakes deleted
- ChatGPT deleting code
- Copilot privacy concerns
- AI assistant data collection
- AI training on private data
- AI unexpected behavior
- AI harmful suggestions

### Categories

Results are automatically categorized into:
- **Microsoft**: Copilot, Bing, Azure related
- **OpenAI**: ChatGPT, GPT related
- **Google**: Bard, Gemini related
- **GitHub**: GitHub Copilot related
- **Privacy**: Data harvesting, opt-out issues
- **Deleted-Projects**: Stories about deleted or lost projects
- **AI-Mistakes**: Unexpected behavior and harmful suggestions
- **Other**: Uncategorized items

## Customization

### Adding Search Terms

Edit the `search_terms` list in the `AIContentScraper` class:

```python
self.search_terms = [
    "AI deleting project",
    "Your custom search term",
    # ... more terms
]
```

### Changing Subreddits

Modify the default subreddit list in the `search_reddit` method:

```python
subreddits = ['technology', 'programming', 'YourSubreddit']
```

### Adjusting Results Per Term

Change the `max_per_term` parameter when running:

```python
results = scraper.scrape_all(max_per_term=10)  # Get 10 results per search term
```

## API Rate Limits

The scraper includes built-in rate limiting:
- 1 second delay between different search sources
- 2 seconds delay between Reddit subreddit searches
- Respects API terms of service

## Data Sources

### Hacker News
Uses the official Algolia HN Search API. No authentication required.

### Reddit
Uses Reddit's public JSON API. No authentication required for public posts.

### Google News (Optional)
Basic HTML scraping. May be blocked by some networks. Disabled by default.

## Output Example

### JSON Format
```json
{
  "scrape_date": "2025-11-18T00:00:00",
  "total_results": 150,
  "results": [
    {
      "title": "Article Title",
      "url": "https://example.com/article",
      "source": "Hacker News",
      "points": 250,
      "num_comments": 45,
      "search_term": "AI deleting project",
      "date_found": "2025-11-18T00:00:00"
    }
  ]
}
```

### Markdown Format
```markdown
## Hacker News

### Article Title

- **URL**: https://example.com/article
- **Search term**: AI deleting project
- **Points**: 250
- **Comments**: 45
- **Found on**: 2025-11-18T00:00:00
```

## Troubleshooting

### Connection Errors
- Check your internet connection
- Some APIs may be blocked by corporate firewalls
- Try increasing timeout values

### No Results
- Terms may not have recent matches
- Try different search terms
- Check if APIs are accessible from your network

### Rate Limiting
- If you get 429 errors, increase delay times
- Reduce `max_per_term` parameter
- Run scraper less frequently

## Contributing

To add new data sources:
1. Create a new search method (e.g., `search_medium`)
2. Add it to the `scrape_all` method
3. Update the README with the new source

## License

See repository LICENSE file.

## Ethical Use

This scraper is designed for research and documentation purposes. Please:
- Respect robots.txt files
- Follow API terms of service
- Don't overload servers with requests
- Use data responsibly
