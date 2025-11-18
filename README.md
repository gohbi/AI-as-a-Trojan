# AI-as-a-Trojan
A curated collection of articles, blog posts, and media documenting AI updates and applications that have malicious or problematic outcomes, including AI overstepping, deleting projects, data harvesting, and privacy concerns.

## About

This repository serves as a directory of real-world incidents where AI tools and applications have caused harm, whether through:
- Deleting entire projects or code
- Overstepping boundaries and taking unwanted actions
- Harvesting user data without clear consent
- Requiring opt-out rather than opt-in for privacy
- Making harmful or unexpected suggestions
- Other malicious or problematic outcomes

## Contents

### Microsoft
- [Copilot in Word](Microsoft/Copilot-in-Word/ReadMe.md) - How to disable AI Copilot in Microsoft Word

## Web Scraper

This repository includes an automated web scraper to continuously discover new AI-related incidents and articles.

### Quick Start

```bash
cd scraper
pip install -r requirements.txt
python ai_content_scraper.py
```

For detailed usage instructions, see [scraper/README.md](scraper/README.md).

### What the Scraper Finds

The scraper searches multiple sources (Hacker News, Reddit, etc.) for articles about:
- AI deleting projects
- AI overstepping boundaries
- AI data harvesting
- Privacy and opt-out concerns
- AI mistakes and unexpected behavior
- And more...

Results are automatically organized and saved in both JSON and Markdown formats.

## Contributing

Contributions are welcome! You can:
- Submit links to articles documenting AI issues
- Run the scraper and share interesting finds
- Improve the scraper functionality
- Add new categories or improve organization

## Purpose

This repository aims to document and raise awareness about the real-world risks and issues that can arise from AI tools and applications, helping users make informed decisions about AI adoption and usage.
