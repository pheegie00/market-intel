#!/usr/bin/env python3
"""
Market Intelligence Suite - Main CLI
Your personal Cook.ai alternative
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project directories to path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "research"))
sys.path.insert(0, str(BASE_DIR / "offers"))
sys.path.insert(0, str(BASE_DIR / "landing-pages"))

from ad_research import research_niche, analyze_landing_page, format_research_report
from offer_architect import create_offer_from_niche, generate_offer_stack, offer_to_dict, calculate_value_equation
from page_generator import generate_landing_page_html, save_landing_page, deploy_to_netlify


def cmd_research(args):
    """Run niche research"""
    competitors = args.competitors.split(",") if args.competitors else []
    
    print(f"\n🔍 Researching: {args.niche}\n")
    results = research_niche(args.niche, competitors)
    
    report = format_research_report(results)
    print(report)
    
    # Save to file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = BASE_DIR / "output" / f"research-{args.niche.replace(' ', '-')}.md"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\n📄 Report saved to: {output_path}")


def cmd_offer(args):
    """Create an offer"""
    print(f"\n🎯 Creating offer for: {args.niche}\n")
    
    offer = create_offer_from_niche(
        niche=args.niche,
        target=args.target or f"People who want to master {args.niche}",
        main_problem=args.problem or f"Struggling with {args.niche}",
        dream_result=args.result or f"Master {args.niche} and achieve your goals",
        price=args.price
    )
    
    # Print offer stack
    stack = generate_offer_stack(offer)
    print(stack)
    
    # Print value equation
    ve = calculate_value_equation(offer)
    print("\n📊 Value Equation Score:", ve["value_score"])
    print(f"   Price-to-Value Ratio: {ve['price_to_value_ratio']}x")
    
    # Save to file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = BASE_DIR / "output" / f"offer-{args.niche.replace(' ', '-')}.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(offer_to_dict(offer), f, indent=2)
    print(f"\n📄 Offer saved to: {output_path}")
    
    return offer_to_dict(offer)


def cmd_landing(args):
    """Generate landing page"""
    # Load offer from file or create new one
    if args.offer_file:
        with open(args.offer_file) as f:
            offer = json.load(f)
    else:
        print("Creating offer first...")
        offer = cmd_offer(args)
    
    print(f"\n🌐 Generating landing page...\n")
    
    html = generate_landing_page_html(offer)
    path = save_landing_page(html, offer.get("name", "offer"), str(BASE_DIR / "output"))
    
    print(f"✅ Landing page saved to: {path}")
    
    if args.deploy:
        print("\n🚀 Deploying to Netlify...")
        result = deploy_to_netlify(path, args.site_name)
        if "error" in result:
            print(f"❌ Deploy failed: {result['error']}")
        else:
            print(f"✅ Deployed: {result.get('url', 'Check Netlify dashboard')}")
    
    return path


def cmd_full(args):
    """Full pipeline: Research → Offer → Landing Page"""
    print("=" * 60)
    print("🚀 FULL MARKET INTELLIGENCE PIPELINE")
    print("=" * 60)
    
    # Step 1: Research
    print("\n[1/3] RESEARCH")
    print("-" * 40)
    competitors = args.competitors.split(",") if args.competitors else []
    research = research_niche(args.niche, competitors)
    print(format_research_report(research))
    
    # Step 2: Offer
    print("\n[2/3] OFFER CREATION")
    print("-" * 40)
    offer = cmd_offer(args)
    
    # Step 3: Landing Page
    print("\n[3/3] LANDING PAGE")
    print("-" * 40)
    args.offer_file = None  # Use the offer we just created
    
    # Create landing page
    html = generate_landing_page_html(offer)
    path = save_landing_page(html, offer.get("name", "offer"), str(BASE_DIR / "output"))
    print(f"✅ Landing page: {path}")
    
    if args.deploy:
        print("\n🚀 Deploying to Netlify...")
        result = deploy_to_netlify(path)
        if "url" in result:
            print(f"✅ Live at: {result['url']}")
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE")
    print("=" * 60)
    print(f"""
Output files in: {BASE_DIR / 'output'}
- Research report
- Offer JSON
- Landing page HTML

Next steps:
1. Review and customize the landing page
2. Add your payment processor link
3. Set up your email sequence
4. Launch ads using the research keywords
""")


def main():
    parser = argparse.ArgumentParser(
        description="Market Intelligence Suite - Your personal marketing AI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Research command
    research_parser = subparsers.add_parser("research", help="Research a niche")
    research_parser.add_argument("niche", help="Niche to research")
    research_parser.add_argument("-c", "--competitors", help="Competitor URLs (comma-separated)")
    research_parser.add_argument("-o", "--output", help="Output file path")
    
    # Offer command
    offer_parser = subparsers.add_parser("offer", help="Create an offer")
    offer_parser.add_argument("niche", help="Niche/topic")
    offer_parser.add_argument("-t", "--target", help="Target audience")
    offer_parser.add_argument("-p", "--problem", help="Main problem to solve")
    offer_parser.add_argument("-r", "--result", help="Dream result")
    offer_parser.add_argument("--price", type=int, default=2997, help="Price (default: 2997)")
    offer_parser.add_argument("-o", "--output", help="Output file path")
    
    # Landing page command
    landing_parser = subparsers.add_parser("landing", help="Generate landing page")
    landing_parser.add_argument("-f", "--offer-file", help="Offer JSON file")
    landing_parser.add_argument("-n", "--niche", help="Niche (if creating new offer)")
    landing_parser.add_argument("-t", "--target", help="Target audience")
    landing_parser.add_argument("-p", "--problem", help="Main problem")
    landing_parser.add_argument("-r", "--result", help="Dream result")
    landing_parser.add_argument("--price", type=int, default=2997, help="Price")
    landing_parser.add_argument("-d", "--deploy", action="store_true", help="Deploy to Netlify")
    landing_parser.add_argument("-s", "--site-name", help="Netlify site name")
    
    # Full pipeline command
    full_parser = subparsers.add_parser("full", help="Full pipeline: research → offer → landing")
    full_parser.add_argument("niche", help="Niche to target")
    full_parser.add_argument("-t", "--target", help="Target audience")
    full_parser.add_argument("-p", "--problem", help="Main problem")
    full_parser.add_argument("-r", "--result", help="Dream result")
    full_parser.add_argument("--price", type=int, default=2997, help="Price")
    full_parser.add_argument("-c", "--competitors", help="Competitor URLs")
    full_parser.add_argument("-d", "--deploy", action="store_true", help="Deploy to Netlify")
    
    args = parser.parse_args()
    
    if args.command == "research":
        cmd_research(args)
    elif args.command == "offer":
        cmd_offer(args)
    elif args.command == "landing":
        cmd_landing(args)
    elif args.command == "full":
        cmd_full(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
