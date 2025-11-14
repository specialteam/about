#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ArzDigital Cryptocurrency Scraper
A professional web scraper for extracting cryptocurrency data from arzdigital.com
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import random
from pathlib import Path


class ArzDigitalScraper:
    """Professional scraper for arzdigital.com cryptocurrency data"""

    def __init__(self, output_dir: str = "data", log_dir: str = "logs"):
        """
        Initialize the scraper

        Args:
            output_dir: Directory to save output files
            log_dir: Directory to save log files
        """
        self.base_url = "https://arzdigital.com/coins/"
        self.output_dir = Path(output_dir)
        self.log_dir = Path(log_dir)

        # Create directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

        # User-Agent rotation for better simulation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        ]

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })

        self.all_coins = []

    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.log_dir / f'scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _get_random_user_agent(self) -> str:
        """Get a random user agent for request simulation"""
        return random.choice(self.user_agents)

    def _make_request(self, url: str, retry_count: int = 3) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic and user simulation

        Args:
            url: URL to fetch
            retry_count: Number of retries on failure

        Returns:
            Response object or None on failure
        """
        for attempt in range(retry_count):
            try:
                # Update user agent for each request
                self.session.headers.update({
                    'User-Agent': self._get_random_user_agent()
                })

                # Add random delay to simulate human behavior (1-3 seconds)
                time.sleep(random.uniform(1, 3))

                self.logger.info(f"Fetching: {url} (Attempt {attempt + 1}/{retry_count})")

                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                self.logger.info(f"Successfully fetched: {url}")
                return response

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching {url} (Attempt {attempt + 1}): {e}")
                if attempt < retry_count - 1:
                    wait_time = (attempt + 1) * 2
                    self.logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Failed to fetch {url} after {retry_count} attempts")
                    return None

        return None

    def _parse_coin_data(self, coin_element) -> Optional[Dict]:
        """
        Parse individual coin data from HTML element

        Args:
            coin_element: BeautifulSoup element containing coin data

        Returns:
            Dictionary with coin data or None on parse error
        """
        try:
            coin_data = {}

            # Extract coin name and symbol
            name_elem = coin_element.find('a', class_='coin-name')
            if name_elem:
                coin_data['name'] = name_elem.get_text(strip=True)
                coin_data['url'] = name_elem.get('href', '')

            symbol_elem = coin_element.find('span', class_='coin-symbol')
            if symbol_elem:
                coin_data['symbol'] = symbol_elem.get_text(strip=True)

            # Extract price
            price_elem = coin_element.find('span', class_='price')
            if price_elem:
                coin_data['price_irr'] = price_elem.get_text(strip=True)

            # Extract price in USD
            usd_price_elem = coin_element.find('span', class_='price-usd')
            if usd_price_elem:
                coin_data['price_usd'] = usd_price_elem.get_text(strip=True)

            # Extract 24h change
            change_elem = coin_element.find('span', class_='change')
            if change_elem:
                coin_data['change_24h'] = change_elem.get_text(strip=True)
                coin_data['change_direction'] = 'up' if 'up' in change_elem.get('class', []) else 'down'

            # Extract market cap
            market_cap_elem = coin_element.find('td', class_='market-cap')
            if market_cap_elem:
                coin_data['market_cap'] = market_cap_elem.get_text(strip=True)

            # Extract volume
            volume_elem = coin_element.find('td', class_='volume')
            if volume_elem:
                coin_data['volume_24h'] = volume_elem.get_text(strip=True)

            # Extract rank
            rank_elem = coin_element.find('td', class_='rank')
            if rank_elem:
                coin_data['rank'] = rank_elem.get_text(strip=True)

            # Add timestamp
            coin_data['scraped_at'] = datetime.now().isoformat()

            return coin_data if coin_data else None

        except Exception as e:
            self.logger.error(f"Error parsing coin data: {e}")
            return None

    def scrape_page(self, page_number: int = 1) -> List[Dict]:
        """
        Scrape a single page of cryptocurrency data

        Args:
            page_number: Page number to scrape (1-based)

        Returns:
            List of coin data dictionaries
        """
        # Construct URL
        if page_number == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}page-{page_number}/"

        # Fetch page
        response = self._make_request(url)
        if not response:
            return []

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find coin table/list
        coins_data = []

        # Try different selectors to find coins
        coin_elements = soup.find_all('tr', class_='coin-row')
        if not coin_elements:
            coin_elements = soup.find_all('div', class_='coin-item')
        if not coin_elements:
            # Try to find table rows
            table = soup.find('table', class_='coins-table')
            if table:
                coin_elements = table.find_all('tr')[1:]  # Skip header

        self.logger.info(f"Found {len(coin_elements)} coin elements on page {page_number}")

        # Parse each coin
        for coin_elem in coin_elements:
            coin_data = self._parse_coin_data(coin_elem)
            if coin_data:
                coins_data.append(coin_data)

        # If no data found with specific selectors, try generic approach
        if not coins_data:
            self.logger.warning(f"No coins found with specific selectors on page {page_number}")
            coins_data = self._generic_parse(soup)

        self.logger.info(f"Successfully parsed {len(coins_data)} coins from page {page_number}")
        return coins_data

    def _generic_parse(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Generic parser when specific selectors don't work

        Args:
            soup: BeautifulSoup object of the page

        Returns:
            List of coin data dictionaries
        """
        coins_data = []

        # Try to find all links that might be coins
        links = soup.find_all('a', href=True)

        for link in links:
            href = link.get('href', '')
            # Check if this looks like a coin page
            if '/coins/' in href and href.count('/') >= 4:
                coin_data = {
                    'name': link.get_text(strip=True),
                    'url': href,
                    'scraped_at': datetime.now().isoformat()
                }
                # Try to find price nearby
                parent = link.find_parent('tr') or link.find_parent('div')
                if parent:
                    # Extract any numbers that might be prices
                    text = parent.get_text()
                    coin_data['raw_text'] = text.strip()

                if coin_data['name']:
                    coins_data.append(coin_data)

        return coins_data

    def scrape_multiple_pages(self, start_page: int = 1, end_page: int = 5) -> List[Dict]:
        """
        Scrape multiple pages

        Args:
            start_page: Starting page number
            end_page: Ending page number (inclusive)

        Returns:
            List of all coins data
        """
        self.logger.info(f"Starting scrape from page {start_page} to {end_page}")

        for page in range(start_page, end_page + 1):
            self.logger.info(f"Scraping page {page}/{end_page}")
            coins = self.scrape_page(page)
            self.all_coins.extend(coins)

            self.logger.info(f"Total coins collected so far: {len(self.all_coins)}")

        self.logger.info(f"Scraping completed! Total coins: {len(self.all_coins)}")
        return self.all_coins

    def save_to_json(self, filename: Optional[str] = None) -> str:
        """
        Save scraped data to JSON file

        Args:
            filename: Custom filename (optional)

        Returns:
            Path to saved file
        """
        if not filename:
            filename = f"arzdigital_coins_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.all_coins, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Data saved to JSON: {filepath}")
        return str(filepath)

    def save_to_csv(self, filename: Optional[str] = None) -> str:
        """
        Save scraped data to CSV file

        Args:
            filename: Custom filename (optional)

        Returns:
            Path to saved file
        """
        if not self.all_coins:
            self.logger.warning("No data to save to CSV")
            return ""

        if not filename:
            filename = f"arzdigital_coins_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        filepath = self.output_dir / filename

        # Get all unique keys from all coins
        all_keys = set()
        for coin in self.all_coins:
            all_keys.update(coin.keys())

        fieldnames = sorted(all_keys)

        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.all_coins)

        self.logger.info(f"Data saved to CSV: {filepath}")
        return str(filepath)

    def get_summary(self) -> Dict:
        """Get summary statistics of scraped data"""
        return {
            'total_coins': len(self.all_coins),
            'scrape_time': datetime.now().isoformat(),
            'unique_symbols': len(set(coin.get('symbol', '') for coin in self.all_coins if coin.get('symbol'))),
        }


def main():
    """Main execution function"""
    print("=" * 60)
    print("ArzDigital Cryptocurrency Scraper")
    print("=" * 60)
    print()

    # Initialize scraper
    scraper = ArzDigitalScraper()

    # Scrape pages 1-5
    print("Starting scraping process...")
    print("This will scrape pages 1-5 from arzdigital.com/coins/")
    print()

    scraper.scrape_multiple_pages(start_page=1, end_page=5)

    # Display summary
    summary = scraper.get_summary()
    print()
    print("=" * 60)
    print("Scraping Summary:")
    print("=" * 60)
    print(f"Total Coins Collected: {summary['total_coins']}")
    print(f"Unique Symbols: {summary['unique_symbols']}")
    print(f"Scrape Time: {summary['scrape_time']}")
    print()

    # Save data
    print("Saving data...")
    json_file = scraper.save_to_json()
    csv_file = scraper.save_to_csv()

    print()
    print("=" * 60)
    print("Files saved successfully:")
    print(f"  - JSON: {json_file}")
    print(f"  - CSV: {csv_file}")
    print("=" * 60)
    print()
    print("Scraping completed successfully!")


if __name__ == "__main__":
    main()
