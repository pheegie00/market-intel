# Market Intelligence Suite 🎯

Your personal marketing AI superpower. Research niches, create high-ticket offers using the Hormozi framework, and generate landing pages — all from the command line.

*Like Cook.ai, but free and yours forever.*

## Features

- **🔍 Niche Research** — Analyze competitors, scrape Meta Ad Library, find keywords
- **💡 Offer Architect** — Create offers using Hormozi's Value Equation framework
- **🌐 Landing Page Generator** — Auto-generate high-converting pages
- **🚀 Netlify Deploy** — One-command deployment

## Quick Start

```bash
# Research a niche
python3 intel.py research "business coaching"

# Create an offer
python3 intel.py offer "fitness coaching" \
  --target "Busy professionals" \
  --problem "No time to exercise" \
  --result "Get fit in 20 minutes a day" \
  --price 1997

# Generate landing page
python3 intel.py landing -f output/offer-fitness-coaching.json

# Full pipeline (research → offer → landing page)
python3 intel.py full "email marketing" \
  --target "Online coaches" \
  --problem "Low email conversions" \
  --result "Turn your list into revenue" \
  --deploy
```

## The Hormozi Value Equation

```
Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort)
```

This tool optimizes all four variables:
- **Dream Outcome** — Clearly define what they want
- **Perceived Likelihood** — Stack proof and guarantees
- **Time Delay** — Promise fast results
- **Effort** — Make it done-for-you

## Output Files

All generated files are saved to `output/`:
- `research-{niche}.md` — Research reports
- `offer-{niche}.json` — Offer data (can be edited)
- `{offer-name}.html` — Landing pages

## Directory Structure

```
market-intel/
├── intel.py              # Main CLI
├── research/
│   └── ad_research.py    # Competitor research tools
├── offers/
│   └── offer_architect.py # Hormozi offer builder
├── landing-pages/
│   └── page_generator.py # HTML page generator
└── output/               # Generated files
```

## Requirements

```bash
pip install requests
```

For Netlify deployment:
```bash
npm install -g netlify-cli
export NETLIFY_AUTH_TOKEN=your_token
```

## Coming Soon

- [ ] Ad copy generator
- [ ] VSL script builder
- [ ] Email sequence generator
- [ ] Market intelligence dashboard
- [ ] Browser automation for ad scraping

---

Built for Phedra by their AI assistant 🤖
