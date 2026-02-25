"""
RSS Feed Loader from OPML
Loads RSS feeds from an OPML subscription file and outputs to TXT or JSON format.
Manual refresh required - set run frequency as needed.
"""

import xml.etree.ElementTree as ET
import json
import feedparser
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse
import sys


class OPMLRSSLoader:
    """Load RSS feeds from OPML file and process them."""
    
    def __init__(self, opml_file: str):
        """
        Initialize the OPML RSS loader.
        
        Args:
            opml_file: Path to the OPML subscription file
        """
        self.opml_file = opml_file
        self.feeds_urls: List[str] = []
        self.feed_data: List[Dict[str, Any]] = []
        
    def parse_opml(self) -> bool:
        """
        Parse OPML file and extract RSS feed URLs.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            tree = ET.parse(self.opml_file)
            root = tree.getroot()
            
            # Find all outline elements with type="rss"
            for outline in root.findall(".//outline[@type='rss']"):
                xml_url = outline.get('xmlUrl')
                if xml_url:
                    self.feeds_urls.append(xml_url)
            
            print(f"✓ Successfully parsed OPML file")
            print(f"✓ Found {len(self.feeds_urls)} RSS feed(s)")
            return True
            
        except FileNotFoundError:
            print(f"✗ Error: OPML file not found: {self.opml_file}")
            return False
        except ET.ParseError as e:
            print(f"✗ Error parsing OPML file: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    def fetch_feeds(self, timeout: int = 10) -> None:
        """
        Fetch all RSS feeds from the URLs.
        
        Args:
            timeout: Timeout in seconds for feed requests
        """
        print(f"\nFetching feeds (timeout: {timeout}s)...")
        
        for idx, feed_url in enumerate(self.feeds_urls, 1):
            print(f"  [{idx}/{len(self.feeds_urls)}] Fetching: {feed_url}")
            
            try:
                feed = feedparser.parse(feed_url, timeout=timeout)
                
                if feed.bozo:
                    print(f"    ⚠ Warning: Feed parsing had issues")
                
                feed_title = feed.feed.get('title', 'Unknown Feed')
                entries = feed.entries[:10]  # Limit to 10 most recent entries per feed
                
                articles = []
                for entry in entries:
                    article = {
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', '')[:200]  # Limit summary length
                    }
                    articles.append(article)
                
                feed_data = {
                    'feed_url': feed_url,
                    'feed_title': feed_title,
                    'article_count': len(articles),
                    'articles': articles,
                    'fetched_at': datetime.now().isoformat()
                }
                
                self.feed_data.append(feed_data)
                print(f"    ✓ Successfully fetched {len(articles)} article(s)")
                
            except Exception as e:
                print(f"    ✗ Failed to fetch: {str(e)}")
                self.feed_data.append({
                    'feed_url': feed_url,
                    'error': str(e),
                    'fetched_at': datetime.now().isoformat()
                })
    
    def save_as_txt(self, output_file: str) -> bool:
        """
        Save feed data to a text file.
        
        Args:
            output_file: Path to output text file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("RSS FEEDS SUMMARY\n")
                f.write("=" * 80 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total feeds: {len(self.feed_data)}\n\n")
                
                for feed in self.feed_data:
                    f.write("-" * 80 + "\n")
                    f.write(f"Feed: {feed.get('feed_title', 'Unknown')}\n")
                    f.write(f"URL: {feed.get('feed_url', 'N/A')}\n")
                    f.write(f"Fetched: {feed.get('fetched_at', 'N/A')}\n")
                    
                    if 'error' in feed:
                        f.write(f"Error: {feed['error']}\n")
                    else:
                        f.write(f"Articles: {feed.get('article_count', 0)}\n\n")
                        
                        for article in feed.get('articles', []):
                            f.write(f"\n  Title: {article['title']}\n")
                            f.write(f"  Link: {article['link']}\n")
                            f.write(f"  Published: {article['published']}\n")
                            if article['summary']:
                                f.write(f"  Summary: {article['summary']}\n")
                    
                    f.write("\n")
                
                f.write("=" * 80 + "\n")
            
            print(f"✓ Successfully saved to TXT: {output_file}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving TXT file: {e}")
            return False
    
    def save_as_json(self, output_file: str) -> bool:
        """
        Save feed data to a JSON file.
        
        Args:
            output_file: Path to output JSON file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            output_data = {
                'generated_at': datetime.now().isoformat(),
                'total_feeds': len(self.feed_data),
                'feeds': self.feed_data
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Successfully saved to JSON: {output_file}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving JSON file: {e}")
            return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Load RSS feeds from OPML file and export to TXT or JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python load_rss_feeds.py subscriptions.opml --txt output.txt
  python load_rss_feeds.py subscriptions.opml --json output.json
  python load_rss_feeds.py subscriptions.opml --both output
        """
    )
    
    parser.add_argument('opml_file', help='Path to OPML subscription file')
    parser.add_argument('--txt', metavar='FILE', help='Output file for TXT format')
    parser.add_argument('--json', metavar='FILE', help='Output file for JSON format')
    parser.add_argument('--both', metavar='PREFIX', 
                       help='Save both formats with given prefix (.txt and .json will be added)')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Timeout in seconds for feed requests (default: 10)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.txt and not args.json and not args.both:
        parser.print_help()
        print("\n✗ Error: Please specify at least one output format (--txt, --json, or --both)")
        sys.exit(1)
    
    # Check if OPML file exists
    if not Path(args.opml_file).exists():
        print(f"✗ Error: OPML file not found: {args.opml_file}")
        sys.exit(1)
    
    # Initialize loader and parse OPML
    loader = OPMLRSSLoader(args.opml_file)
    if not loader.parse_opml():
        sys.exit(1)
    
    # Fetch feeds
    loader.fetch_feeds(timeout=args.timeout)
    
    # Save output
    success = True
    
    if args.both:
        txt_file = f"{args.both}.txt"
        json_file = f"{args.both}.json"
        success &= loader.save_as_txt(txt_file)
        success &= loader.save_as_json(json_file)
    else:
        if args.txt:
            success &= loader.save_as_txt(args.txt)
        if args.json:
            success &= loader.save_as_json(args.json)
    
    print("\n" + "=" * 80)
    if success:
        print("✓ Feed loading completed successfully!")
    else:
        print("⚠ Feed loading completed with some errors")
    print("=" * 80)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()load
