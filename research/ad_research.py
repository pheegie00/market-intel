#!/usr/bin/env python3
"""
Competitor Ad Research Tool
Analyzes Meta Ad Library and competitor landing pages
"""

import json
import re
from datetime import datetime
from pathlib import Path
import requests
from urllib.parse import quote_plus

# Meta Ad Library search URL
META_AD_LIBRARY = "https://www.facebook.com/ads/library/"

def search_meta_ads(query: str, country: str = "US") -> dict:
    """
    Search Meta Ad Library for competitor ads.
    Returns structured data about active ads.
    """
    # Meta Ad Library API endpoint (public)
    api_url = f"https://www.facebook.com/ads/library/async/search_ads/"
    
    # For now, we'll use web scraping approach
    search_url = f"{META_AD_LIBRARY}?active_status=active&ad_type=all&country={country}&q={quote_plus(query)}&search_type=keyword_unordered"
    
    return {
        "query": query,
        "search_url": search_url,
        "note": "Open this URL in browser to view ads, or use browser automation for scraping"
    }


def analyze_landing_page(url: str) -> dict:
    """
    Analyze a competitor landing page for marketing elements.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        html = r.text.lower()
        
        analysis = {
            "url": url,
            "status": r.status_code,
            "elements": {}
        }
        
        # Check for common high-converting elements
        elements = {
            "headline": bool(re.search(r'<h1[^>]*>.*?</h1>', html)),
            "video": "youtube" in html or "vimeo" in html or "<video" in html or "wistia" in html,
            "testimonials": any(word in html for word in ["testimonial", "review", "what people say", "success stor"]),
            "social_proof": any(word in html for word in ["trusted by", "as seen", "featured in", "clients", "customers"]),
            "urgency": any(word in html for word in ["limited", "hurry", "now", "today only", "spots left", "deadline"]),
            "guarantee": any(word in html for word in ["guarantee", "money back", "risk-free", "refund"]),
            "cta_buttons": len(re.findall(r'<button|<a[^>]*class="[^"]*btn|type="submit"', html)),
            "form": "<form" in html,
            "price_anchoring": "$" in html and any(word in html for word in ["was", "normally", "value", "worth"]),
            "faq": "faq" in html or "frequently asked" in html,
            "bonuses": any(word in html for word in ["bonus", "free", "included", "extra"]),
        }
        
        analysis["elements"] = elements
        analysis["score"] = sum(elements.values())
        analysis["max_score"] = len(elements)
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', r.text, re.IGNORECASE | re.DOTALL)
        if title_match:
            analysis["title"] = title_match.group(1).strip()
        
        return analysis
        
    except Exception as e:
        return {"url": url, "error": str(e)}


def research_niche(niche: str, competitors: list = None) -> dict:
    """
    Comprehensive niche research.
    """
    results = {
        "niche": niche,
        "timestamp": datetime.now().isoformat(),
        "ad_library": search_meta_ads(niche),
        "competitor_analysis": [],
        "keywords": [],
        "opportunities": []
    }
    
    if competitors:
        for comp in competitors:
            if comp.startswith("http"):
                results["competitor_analysis"].append(analyze_landing_page(comp))
    
    # Generate keyword variations
    results["keywords"] = [
        f"{niche} course",
        f"{niche} coaching",
        f"{niche} consultant",
        f"{niche} agency",
        f"{niche} program",
        f"best {niche}",
        f"how to {niche}",
        f"{niche} for beginners",
        f"{niche} masterclass",
        f"learn {niche}",
    ]
    
    return results


def format_research_report(research: dict) -> str:
    """Format research into readable report."""
    report = f"""
# Market Research Report: {research['niche'].title()}
Generated: {research['timestamp']}

## 🔍 Ad Library Search
Search for active ads: {research['ad_library']['search_url']}

## 🎯 Keyword Opportunities
"""
    for kw in research['keywords']:
        report += f"- {kw}\n"
    
    if research['competitor_analysis']:
        report += "\n## 🏢 Competitor Analysis\n"
        for comp in research['competitor_analysis']:
            if 'error' in comp:
                report += f"\n### {comp['url']}\n❌ Error: {comp['error']}\n"
            else:
                report += f"\n### {comp.get('title', comp['url'])}\n"
                report += f"URL: {comp['url']}\n"
                report += f"Score: {comp['score']}/{comp['max_score']}\n\n"
                report += "**Elements Found:**\n"
                for elem, found in comp['elements'].items():
                    emoji = "✅" if found else "❌"
                    report += f"- {emoji} {elem.replace('_', ' ').title()}\n"
    
    return report


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        niche = " ".join(sys.argv[1:])
    else:
        niche = "business coaching"
    
    print(f"Researching: {niche}")
    results = research_niche(niche)
    print(format_research_report(results))
