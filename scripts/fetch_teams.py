#!/usr/bin/env python3
"""
Fetch FRC team data from The Blue Alliance API.
Outputs team data to src/lib/teams.json
"""

import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests python-dotenv")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Constants
TBA_BASE_URL = "https://www.thebluealliance.com/api/v3"
OUTPUT_PATH = Path(__file__).parent.parent / "src" / "lib" / "teams.json"
RATE_LIMIT_DELAY = 0.05  # seconds between requests to avoid rate limiting


def get_api_key():
    """Get TBA API key from environment variable."""
    api_key = os.getenv("TBA_API_KEY")
    if not api_key:
        print("Error: TBA_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key:")
        print("  TBA_API_KEY=your_api_key_here")
        sys.exit(1)
    return api_key


def make_request(endpoint, api_key, retries=3):
    """Make a request to the TBA API with proper headers."""
    headers = {
        "X-TBA-Auth-Key": api_key,
        "Accept": "application/json"
    }
    url = f"{TBA_BASE_URL}{endpoint}"

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 60 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            elif e.response.status_code == 404:
                return []  # No data found is not an error
            raise
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                print(f"Request error for {endpoint}, retrying...")
                time.sleep(5)
                continue
            print(f"Request error for {endpoint}: {e}")
            return None

    return None


def fetch_all_teams(api_key):
    """Fetch all FRC teams from TBA API."""
    all_teams = []
    page = 0

    print("Fetching teams from TBA API...")

    while True:
        print(f"  Fetching page {page}...", end=" ", flush=True)
        teams = make_request(f"/teams/{page}", api_key)

        if teams is None:
            print("error, skipping")
            page += 1
            if page > 20:  # Safety limit
                break
            continue

        if not teams:  # Empty list means no more pages
            print("done (no more pages)")
            break

        print(f"got {len(teams)} teams")
        all_teams.extend(teams)
        page += 1
        time.sleep(RATE_LIMIT_DELAY)

    print(f"  Found {len(all_teams)} teams total")
    return all_teams


def main():
    """Main function to fetch team data and output to JSON."""
    api_key = get_api_key()

    # Fetch all teams
    teams = fetch_all_teams(api_key)

    if not teams:
        print("Error: No teams fetched from API")
        sys.exit(1)

    # Build team data dictionary
    print("\nBuilding team data...")
    team_data = {}

    for team in teams:
        team_number = team.get("team_number")
        team_name = team.get("nickname", team.get("name", "Unknown"))

        if team_number is None:
            continue

        team_data[str(team_number)] = {"name": team_name}

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write to JSON file (minified)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(team_data, f, separators=(",", ":"), ensure_ascii=False)

    print(f"\nDone! Team data saved to {OUTPUT_PATH}")
    print(f"Total teams: {len(team_data)}")


if __name__ == "__main__":
    main()
