#!/usr/bin/env python3
"""
Helper script to organize scraped articles into the repository structure
Creates category folders and ReadMe files similar to Microsoft/Copilot-in-Word
"""

import json
import os
from pathlib import Path
from datetime import datetime


def load_scraped_data(json_file='scraped_content.json'):
    """Load scraped data from JSON file."""
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        print("Please run ai_content_scraper.py first.")
        return None
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('results', [])


def categorize_article(article):
    """Determine the category for an article."""
    title = article.get('title', '').lower()
    search_term = article.get('search_term', '').lower()
    combined = f"{title} {search_term}"
    
    categories = {
        'Microsoft': ['microsoft', 'copilot', 'bing', 'azure', 'windows'],
        'OpenAI': ['openai', 'chatgpt', 'gpt-3', 'gpt-4', 'gpt'],
        'Google': ['google', 'bard', 'gemini', 'deepmind'],
        'GitHub': ['github'],
        'Privacy-Concerns': ['privacy', 'data harvesting', 'opt-out', 'data collection', 'tracking'],
        'Deleted-Projects': ['delet', 'lost project', 'wiped', 'removed', 'erased'],
        'AI-Mistakes': ['mistake', 'wrong', 'harmful', 'dangerous', 'unexpected', 'accident'],
        'Training-Data': ['training data', 'training on', 'model training', 'dataset'],
    }
    
    for category, keywords in categories.items():
        if any(keyword in combined for keyword in keywords):
            return category
    
    return 'Other'


def create_category_structure(articles, base_path='..'):
    """Create folder structure and ReadMe files for categorized articles."""
    base_path = Path(base_path).resolve()
    
    # Group articles by category
    by_category = {}
    for article in articles:
        category = categorize_article(article)
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(article)
    
    print(f"\nOrganizing {len(articles)} articles into {len(by_category)} categories...\n")
    
    # Create folders and files for each category
    for category, cat_articles in sorted(by_category.items()):
        category_path = base_path / category
        category_path.mkdir(exist_ok=True)
        
        print(f"Category: {category} ({len(cat_articles)} articles)")
        
        # Group by topic/source within category
        for i, article in enumerate(cat_articles[:10], 1):  # Limit to top 10 per category
            # Create a sanitized folder name from the title
            title = article.get('title', f'Article-{i}')
            # Remove invalid filename characters
            folder_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in title)
            folder_name = folder_name.strip()[:50]  # Limit length
            
            if not folder_name:
                folder_name = f'Article-{i}'
            
            article_path = category_path / folder_name
            article_path.mkdir(exist_ok=True)
            
            # Create ReadMe.md for the article
            readme_path = article_path / 'ReadMe.md'
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {article.get('title', 'No title')}\n\n")
                f.write(f"**Source**: {article.get('source', 'Unknown')}\n\n")
                f.write(f"**URL**: [{article.get('url', 'N/A')}]({article.get('url', '#')})\n\n")
                
                if 'points' in article:
                    f.write(f"**Points**: {article['points']}\n\n")
                if 'score' in article:
                    f.write(f"**Score**: {article['score']}\n\n")
                if 'num_comments' in article:
                    f.write(f"**Comments**: {article['num_comments']}\n\n")
                
                f.write(f"**Search term**: {article.get('search_term', 'N/A')}\n\n")
                f.write(f"**Found on**: {article.get('date_found', 'N/A')}\n\n")
                
                f.write("## Summary\n\n")
                f.write("*Add a brief summary of the article content here.*\n\n")
                
                f.write("## Key Points\n\n")
                f.write("- *Add key points from the article*\n")
                f.write("- *What AI tool/company is involved?*\n")
                f.write("- *What was the issue or problem?*\n")
                f.write("- *What was the outcome or impact?*\n\n")
            
            print(f"  ✓ Created {category}/{folder_name}/ReadMe.md")
    
    print(f"\n✓ Organization complete!")
    print(f"\nFolders created in: {base_path}")
    print("\nYou can now review and edit the ReadMe.md files to add summaries")
    print("and commit the relevant ones to the repository.")


def update_main_readme(base_path='..'):
    """Update the main README.md with links to all categories."""
    base_path = Path(base_path).resolve()
    readme_path = base_path / 'README.md'
    
    # Get all category directories (excluding .git and scraper)
    categories = [d for d in base_path.iterdir() 
                  if d.is_dir() 
                  and d.name not in ['.git', 'scraper', '.github']
                  and not d.name.startswith('.')]
    
    if not categories:
        print("No category folders found to add to README.")
        return
    
    print("\nCategory folders found:")
    for cat in sorted(categories):
        print(f"  - {cat.name}")
    
    print(f"\nTo update the main README, add these categories to the Contents section.")


def main():
    """Main entry point."""
    print("=" * 60)
    print("AI-as-a-Trojan Content Organizer")
    print("=" * 60)
    
    # Load scraped data
    articles = load_scraped_data()
    
    if not articles:
        print("\nNo articles found. Run the scraper first:")
        print("  python ai_content_scraper.py")
        return
    
    print(f"\nLoaded {len(articles)} articles from scraped_content.json")
    
    # Organize articles
    create_category_structure(articles)
    
    # Suggest README updates
    update_main_readme()
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
