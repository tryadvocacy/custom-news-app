
import pytest
from load_rss_feeds import OPMLRSSLoader
import os

def test_load_opml():
    # Create a dummy OPML file for testing
    opml_content = """<opml version="1.0">
        <head>
            <title>Test Subscriptions</title>
        </head>
        <body>
            <outline text="Feed 1" type="rss" xmlUrl="http://example.com/feed1.xml" />
            <outline text="Feed 2" type="rss" xmlUrl="http://example.com/feed2.xml" />
        </body>
    </opml>"""
    opml_file = "test_subscriptions.opml"
    with open(opml_file, "w") as f:
        f.write(opml_content)

    loader = OPMLRSSLoader(opml_file)
    loader.parse_opml()
    assert len(loader.feeds_urls) == 2
    assert loader.feeds_urls[0] == "http://example.com/feed1.xml"
    assert loader.feeds_urls[1] == "http://example.com/feed2.xml"

    # Clean up the dummy OPML file
    os.remove(opml_file)
