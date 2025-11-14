#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for ArzDigital scraper - only scrapes first page
"""

from scraper import ArzDigitalScraper

def test_scraper():
    """Test the scraper with just one page"""
    print("=" * 60)
    print("ArzDigital Scraper Test")
    print("=" * 60)
    print("\nTesting with page 1 only...\n")

    # Initialize scraper
    scraper = ArzDigitalScraper()

    # Scrape only first page
    coins = scraper.scrape_page(page_number=1)

    print(f"\nResults:")
    print(f"  - Coins found: {len(coins)}")

    if coins:
        print(f"\nFirst coin sample:")
        first_coin = coins[0]
        for key, value in first_coin.items():
            print(f"  - {key}: {value}")

    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_scraper()
