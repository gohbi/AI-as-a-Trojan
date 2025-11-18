#!/usr/bin/env python3
"""
Unit tests for AI Content Scraper
Tests internal functionality without requiring internet access
"""

import unittest
import sys
import os

# Add the scraper directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from ai_content_scraper import AIContentScraper


class TestAIContentScraper(unittest.TestCase):
    """Test cases for AIContentScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = AIContentScraper()
    
    def test_initialization(self):
        """Test that scraper initializes correctly."""
        self.assertIsInstance(self.scraper.search_terms, list)
        self.assertGreater(len(self.scraper.search_terms), 0)
        self.assertIsInstance(self.scraper.results, list)
        self.assertEqual(len(self.scraper.results), 0)
    
    def test_search_terms(self):
        """Test that search terms are properly configured."""
        expected_terms = [
            "AI deleting project",
            "AI overstepping boundaries",
            "AI data harvesting",
        ]
        for term in expected_terms:
            self.assertIn(term, self.scraper.search_terms)
    
    def test_filter_duplicates(self):
        """Test duplicate URL filtering."""
        # Add test results with duplicates
        self.scraper.results = [
            {'title': 'Article 1', 'url': 'https://example.com/1'},
            {'title': 'Article 2', 'url': 'https://example.com/2'},
            {'title': 'Article 1 Duplicate', 'url': 'https://example.com/1'},
            {'title': 'Article 3', 'url': 'https://example.com/3'},
        ]
        
        filtered = self.scraper.filter_duplicates()
        
        self.assertEqual(len(filtered), 3)
        urls = [r['url'] for r in filtered]
        self.assertEqual(len(urls), len(set(urls)))  # All URLs should be unique
    
    def test_categorization(self):
        """Test categorization of results."""
        # Add test results
        self.scraper.results = [
            {'title': 'Microsoft Copilot Issue', 'url': 'https://example.com/1', 
             'search_term': 'copilot privacy'},
            {'title': 'ChatGPT Problem', 'url': 'https://example.com/2', 
             'search_term': 'chatgpt deleting'},
            {'title': 'Google Bard Issue', 'url': 'https://example.com/3', 
             'search_term': 'google ai privacy'},
            {'title': 'Random AI Issue', 'url': 'https://example.com/4', 
             'search_term': 'ai unexpected'},
        ]
        
        categorized = self.scraper.generate_categorized_structure()
        
        self.assertIsInstance(categorized, dict)
        self.assertIn('Microsoft', categorized)
        self.assertIn('OpenAI', categorized)
        self.assertIn('Google', categorized)
    
    def test_save_to_json(self):
        """Test JSON output generation."""
        import tempfile
        import json
        
        # Add test results
        self.scraper.results = [
            {'title': 'Test Article', 'url': 'https://example.com/test'},
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            self.scraper.save_to_json(temp_file)
            
            # Verify the file was created and contains valid JSON
            self.assertTrue(os.path.exists(temp_file))
            
            with open(temp_file, 'r') as f:
                data = json.load(f)
            
            self.assertIn('scrape_date', data)
            self.assertIn('total_results', data)
            self.assertIn('results', data)
            self.assertEqual(data['total_results'], 1)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_save_to_markdown(self):
        """Test Markdown output generation."""
        import tempfile
        
        # Add test results
        self.scraper.results = [
            {
                'title': 'Test Article',
                'url': 'https://example.com/test',
                'source': 'Test Source',
                'search_term': 'test term'
            },
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            temp_file = f.name
        
        try:
            self.scraper.save_to_markdown(temp_file)
            
            # Verify the file was created and contains expected content
            self.assertTrue(os.path.exists(temp_file))
            
            with open(temp_file, 'r') as f:
                content = f.read()
            
            self.assertIn('AI-as-a-Trojan', content)
            self.assertIn('Test Article', content)
            self.assertIn('https://example.com/test', content)
            self.assertIn('Test Source', content)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAIContentScraper)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
