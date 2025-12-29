# FRC Kickoff Countdown Timer

Build a single-page countdown timer for the FIRST Robotics Competition 2026 kickoff on January 10th, 2026 at 12:00 PM EST.

## Tech Stack
- SvelteKit (static adapter for GitHub Pages)
- TailwindCSS for styling
- Python script for TBA API data fetching

## Project Structure
```
frc-countdown/
├── src/
│   ├── routes/
│   │   └── +page.svelte          # Main countdown page
│   ├── lib/
│   │   └── teams.json             # Generated team data
│   └── app.html
├── static/
│   └── .nojekyll                  # For GitHub Pages
├── scripts/
│   └── fetch_teams.py             # TBA API script
├── .env                           # API key (gitignored)
├── svelte.config.js
├── tailwind.config.js
├── package.json
└── README.md
```

## Requirements

### 1. Python Script (`scripts/fetch_teams.py`)
- Load TBA API key from `.env` file (key: `TBA_API_KEY`)
- Fetch all FRC teams from The Blue Alliance API
- For each team, get:
    - Team number
    - Team name
    - Whether they're competing in 2026 (check events/status)
- Output to `src/lib/teams.json` as:
  ```json
  {
    "254": {"name": "The Cheesy Poofs", "competing2026": true},
    "1": {"name": "The Juggernauts", "competing2026": false},
    ...
  }
  ```
- Handle API rate limits appropriately
- Include error handling

### 2. SvelteKit App Configuration
- Use `@sveltejs/adapter-static` for GitHub Pages
- Configure `svelte.config.js` for static site generation
- Set base path handling for GitHub Pages deployment
- Include `.nojekyll` file in static folder

### 3. Countdown Timer UI (`src/routes/+page.svelte`)

#### Layout
- Full viewport height, centered content
- Single focus: the countdown timer
- Clean, minimal design with FRC 2026 REBUILT branding

#### Timer Display
- Format: `DD:HH:MM:SS` (always 2 digits per segment with zero padding)
- Update every second
- Countdown to: January 10, 2026, 12:00 PM EST
- When complete: Display "FIRST Robotics Competition 2026 Kickoff Has Started!"

#### Team Number Highlighting
- Extract last 4 digits from timer (rightmost MM:SS)
- Highlight only the non-zero leading digits and the digits themselves
- Example: `01:10:02:54` → highlight `2:54` (team 254)
- Example: `05:03:47:23` → highlight `47:23` (team 4723)
- Example: `00:00:00:09` → highlight `9` (team 9)
- Display the team name and number below the timer
- If team doesn't exist in data, show "Team #[number] not found"
- If team isn't competing in 2026, indicate this visually (dimmed or different color)

#### Official FRC 2026 REBUILT Color Palette
Use these exact colors from the style guide:
- Primary Orange: `#ea572e` (RGB: 234, 87, 46)
- Primary Gold: `#e5ae32` (RGB: 229, 174, 50)
- Primary Blue: `#598290` (RGB: 89, 130, 144)
- Accent Green: `#92dbac` (RGB: 146, 219, 172)
- Black: `#000000`

Design suggestions:
- Use orange/gold for highlighted timer digits
- Use blue for regular timer digits
- Use green accent for team name display
- Dark background (black or very dark gray)

### 4. TailwindCSS Configuration
- Add the FRC brand colors to the Tailwind config
- Use appropriate font sizing for timer (large, bold, monospace)
- Responsive design (though desktop-focused is fine)

### 5. GitHub Pages Deployment
- Include build script that generates static site
- Configure for deployment to GitHub Pages
- Handle routing properly for SPA on GitHub Pages
- Include deployment instructions in README

## Development Workflow
1. Run `python scripts/fetch_teams.py` to generate team data
2. Run `npm run dev` for local development
3. Run `npm run build` to generate static site for deployment
4. Deploy `build/` directory to GitHub Pages

## Additional Notes
- Timer calculation should account for timezone (EST)
- Handle edge cases (team 0, team 10000+, etc.)
- Smooth transitions for timer updates
- Consider adding a subtle animation or glow effect to highlighted digits
- The app should work entirely client-side after build (no server required)

## Dependencies to Install
- SvelteKit
- @sveltejs/adapter-static
- TailwindCSS
- Python: requests, python-dotenv

## Example .env File
```
TBA_API_KEY=your_api_key_here
```