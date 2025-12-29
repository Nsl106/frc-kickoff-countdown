# FRC 2026 Kickoff Countdown

A countdown timer for the FIRST Robotics Competition 2026 REBUILT kickoff on January 10th, 2026 at 12:00 PM EST.

Note that pretty much everything other than this line was done with Claude Code as an experiment.
## Features

- Real-time countdown timer (DD:HH:MM:SS format)
- Team spotlight: highlights the team number derived from MM:SS (e.g., 02:54 = Team 254)
- Displays team name and 2026 competition status
- FRC 2026 REBUILT brand colors
- Static site deployment for GitHub Pages

## Tech Stack

- SvelteKit with static adapter
- TailwindCSS
- Python for TBA API data fetching

## Development

### Prerequisites

- Node.js 18+
- Python 3.8+ (for team data fetching)

### Setup

1. Install Node dependencies:
```bash
npm install
```

2. Install Python dependencies (for team data script):
```bash
pip install requests python-dotenv
```

3. Create a `.env` file with your TBA API key:
```
TBA_API_KEY=your_api_key_here
```

Get your API key at: https://www.thebluealliance.com/account

### Fetch Team Data

Run the Python script to fetch team data from The Blue Alliance:

```bash
# Full fetch with 2026 competition status
python scripts/fetch_teams.py

# Quick fetch (skips 2026 status check)
python scripts/fetch_teams.py --quick
```

This creates/updates `src/lib/teams.json`.

### Run Development Server

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

The static site will be output to the `build/` directory.

### Preview Production Build

```bash
npm run preview
```

## Deployment to GitHub Pages

1. Build the project:
```bash
npm run build
```

2. Deploy the `build/` directory to GitHub Pages

### Automatic Deployment with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_ENV: production

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

## Configuration

### Base Path

If deploying to `username.github.io/repo-name`, the base path is automatically set in `svelte.config.js`.

To change the repo name, edit the `base` path in `svelte.config.js`:

```js
paths: {
  base: process.env.NODE_ENV === 'production' ? '/your-repo-name' : ''
}
```

For custom domains or root deployment, set base to an empty string.

## FRC 2026 REBUILT Colors

- Primary Orange: `#ea572e`
- Primary Gold: `#e5ae32`
- Primary Blue: `#598290`
- Accent Green: `#92dbac`
- Black: `#000000`
