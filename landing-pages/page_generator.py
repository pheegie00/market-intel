#!/usr/bin/env python3
"""
Landing Page Generator
Creates high-converting landing pages from offers
"""

import os
import json
from pathlib import Path
from datetime import datetime


def generate_landing_page_html(offer: dict) -> str:
    """
    Generate a complete landing page HTML from an offer.
    Uses direct response principles and clean design.
    """
    
    # Extract offer details
    name = offer.get("name", "The Program")
    tagline = offer.get("tagline", "Transform your results")
    target = offer.get("target_audience", "ambitious professionals")
    price = offer.get("price", 2997)
    anchor_value = offer.get("anchor_value", price * 3)
    urgency = offer.get("urgency", "Limited spots available")
    scarcity = offer.get("scarcity", "Enrollment closes soon")
    
    dream = offer.get("dream_outcome", {})
    problems = offer.get("problems", [])
    solutions = offer.get("solutions", [])
    bonuses = offer.get("bonuses", [])
    guarantee = offer.get("guarantee", {})
    
    # Calculate bonus total
    bonus_total = sum(b.get("value", 0) for b in bonuses)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | {tagline}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a1a2e;
            background: #fff;
        }}
        
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 20px; }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            padding: 80px 20px;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 2.5rem;
            margin-bottom: 20px;
            line-height: 1.2;
        }}
        
        .hero .tagline {{
            font-size: 1.3rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }}
        
        .hero .target {{
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 30px;
            display: inline-block;
            font-size: 0.9rem;
        }}
        
        /* CTA Button */
        .cta-btn {{
            display: inline-block;
            background: #f97316;
            color: #fff;
            padding: 18px 40px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            margin: 20px 0;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .cta-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(249, 115, 22, 0.3);
        }}
        
        /* Sections */
        section {{
            padding: 60px 20px;
        }}
        
        section h2 {{
            font-size: 2rem;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        /* Problem Section */
        .problems {{
            background: #f8f9fa;
        }}
        
        .problem-card {{
            background: #fff;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border-left: 4px solid #ef4444;
        }}
        
        .problem-card h3 {{
            color: #ef4444;
            margin-bottom: 10px;
        }}
        
        /* Solution Section */
        .solution-card {{
            background: #f0fdf4;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border-left: 4px solid #22c55e;
        }}
        
        .solution-card h3 {{
            color: #16a34a;
            margin-bottom: 10px;
        }}
        
        /* Bonuses */
        .bonuses {{
            background: #fef3c7;
        }}
        
        .bonus-card {{
            background: #fff;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 2px dashed #f59e0b;
        }}
        
        .bonus-value {{
            color: #f59e0b;
            font-weight: 700;
            font-size: 1.2rem;
        }}
        
        /* Guarantee */
        .guarantee {{
            background: #16213e;
            color: #fff;
            text-align: center;
        }}
        
        .guarantee-badge {{
            background: #22c55e;
            display: inline-block;
            padding: 15px 30px;
            border-radius: 50px;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        
        /* Pricing */
        .pricing {{
            text-align: center;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
        }}
        
        .price-anchor {{
            font-size: 1.5rem;
            text-decoration: line-through;
            opacity: 0.6;
        }}
        
        .price-actual {{
            font-size: 4rem;
            font-weight: 700;
            margin: 20px 0;
        }}
        
        .urgency {{
            background: #ef4444;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        /* Footer */
        footer {{
            background: #1a1a2e;
            color: rgba(255,255,255,0.6);
            padding: 30px 20px;
            text-align: center;
            font-size: 0.9rem;
        }}
        
        @media (max-width: 600px) {{
            .hero h1 {{ font-size: 1.8rem; }}
            .price-actual {{ font-size: 3rem; }}
        }}
    </style>
</head>
<body>
    <!-- Hero -->
    <section class="hero">
        <div class="container">
            <div class="target">For {target}</div>
            <h1>{name}</h1>
            <p class="tagline">{tagline}</p>
            <a href="#pricing" class="cta-btn">Yes! I Want This →</a>
        </div>
    </section>
    
    <!-- Dream Outcome -->
    <section class="dream">
        <div class="container">
            <h2>Imagine If You Could...</h2>
            <p style="font-size: 1.3rem; text-align: center; max-width: 600px; margin: 0 auto;">
                <strong>{dream.get("primary_desire", "Achieve your biggest goals")}</strong>
            </p>
            <p style="text-align: center; margin-top: 20px; color: #666;">
                {dream.get("emotional_driver", "")}
            </p>
        </div>
    </section>
    
    <!-- Problems -->
    <section class="problems">
        <div class="container">
            <h2>Sound Familiar?</h2>
'''
    
    for prob in problems[:3]:
        html += f'''
            <div class="problem-card">
                <h3>❌ {prob.get("problem", "")}</h3>
                <p>{prob.get("why_current_fails", "")}</p>
            </div>
'''
    
    html += '''
            <p style="text-align: center; margin-top: 30px; font-size: 1.2rem;">
                <strong>There's a better way...</strong>
            </p>
        </div>
    </section>
    
    <!-- Solutions -->
    <section class="solutions">
        <div class="container">
            <h2>What You Get</h2>
'''
    
    for sol in solutions:
        html += f'''
            <div class="solution-card">
                <h3>✅ {sol.get("solution", "")}</h3>
                <p><strong>Solves:</strong> {sol.get("problem_solved", "")}</p>
                <p><strong>Delivered via:</strong> {sol.get("delivery_method", "")}</p>
                <p><strong>Results:</strong> {sol.get("time_to_result", "")}</p>
            </div>
'''
    
    html += '''
        </div>
    </section>
    
    <!-- Bonuses -->
    <section class="bonuses">
        <div class="container">
            <h2>🎁 Plus These Bonuses</h2>
'''
    
    for bonus in bonuses:
        html += f'''
            <div class="bonus-card">
                <h3>{bonus.get("name", "")}</h3>
                <p>{bonus.get("description", "")}</p>
                <p class="bonus-value">Value: ${bonus.get("value", 0):,}</p>
            </div>
'''
    
    html += f'''
            <p style="text-align: center; font-size: 1.3rem; margin-top: 20px;">
                <strong>Total Bonus Value: ${bonus_total:,}</strong>
            </p>
        </div>
    </section>
    
    <!-- Guarantee -->
    <section class="guarantee">
        <div class="container">
            <div class="guarantee-badge">✓ {guarantee.get("type", "100% Guarantee")}</div>
            <h2>Zero Risk</h2>
            <p style="max-width: 600px; margin: 0 auto;">
                {guarantee.get("terms", "If you're not satisfied, we'll refund your investment.")}
            </p>
            <p style="margin-top: 10px; opacity: 0.8;">
                {guarantee.get("duration", "30 days")} guarantee
            </p>
        </div>
    </section>
    
    <!-- Pricing -->
    <section class="pricing" id="pricing">
        <div class="container">
            <h2>Your Investment</h2>
            <p class="price-anchor">Total Value: ${anchor_value + bonus_total:,}</p>
            <p class="price-actual">${price:,}</p>
            
            <div class="urgency">
                ⏰ {urgency}<br>
                🔒 {scarcity}
            </div>
            
            <a href="#" class="cta-btn">Get Instant Access →</a>
            
            <p style="margin-top: 30px; opacity: 0.8; font-size: 0.9rem;">
                Secure payment • Instant access • {guarantee.get("duration", "30-day")} guarantee
            </p>
        </div>
    </section>
    
    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} {name}. All rights reserved.</p>
            <p style="margin-top: 10px;">
                <a href="#" style="color: inherit;">Privacy Policy</a> | 
                <a href="#" style="color: inherit;">Terms of Service</a>
            </p>
        </div>
    </footer>
</body>
</html>'''
    
    return html


def save_landing_page(html: str, name: str, output_dir: str = None) -> str:
    """Save landing page HTML to file."""
    if output_dir is None:
        output_dir = Path(__file__).parent / "output"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize name for filename
    safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in name.lower())
    filename = f"{safe_name}.html"
    filepath = output_dir / filename
    
    with open(filepath, "w") as f:
        f.write(html)
    
    return str(filepath)


def deploy_to_netlify(html_path: str, site_name: str = None) -> dict:
    """
    Deploy landing page to Netlify.
    Requires NETLIFY_AUTH_TOKEN environment variable.
    """
    import subprocess
    
    token = os.getenv("NETLIFY_AUTH_TOKEN")
    if not token:
        return {"error": "NETLIFY_AUTH_TOKEN not set"}
    
    # Get directory containing the HTML
    html_dir = Path(html_path).parent
    
    # Deploy using Netlify CLI
    cmd = f"NETLIFY_AUTH_TOKEN={token} netlify deploy --prod --dir={html_dir}"
    if site_name:
        cmd += f" --site={site_name}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Parse URL from output
        for line in result.stdout.split("\n"):
            if "Website URL:" in line or "Deployed to" in line:
                url = line.split()[-1]
                return {"success": True, "url": url}
        
        return {"success": True, "output": result.stdout}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Example usage
    sample_offer = {
        "name": "Email Marketing Accelerator",
        "tagline": "Turn your email list into a revenue machine",
        "target_audience": "Online coaches who want more sales",
        "price": 2997,
        "anchor_value": 8991,
        "urgency": "Enrollment closes Friday at midnight",
        "scarcity": "Only 10 spots available",
        "dream_outcome": {
            "primary_desire": "Convert subscribers into buyers on autopilot",
            "emotional_driver": "Feel confident every email will generate revenue"
        },
        "problems": [
            {"problem": "Low open rates", "why_current_fails": "Generic subject lines don't stand out"},
            {"problem": "Nobody clicks", "why_current_fails": "Boring content that doesn't drive action"},
            {"problem": "No sales from emails", "why_current_fails": "No strategy to convert readers to buyers"}
        ],
        "solutions": [
            {"solution": "Subject Line Swipe File", "problem_solved": "Low open rates", "delivery_method": "500+ proven templates", "time_to_result": "Instant"},
            {"solution": "Email Sales Framework", "problem_solved": "No sales", "delivery_method": "Step-by-step video training", "time_to_result": "7 days"},
            {"solution": "Weekly Coaching Calls", "problem_solved": "Getting stuck", "delivery_method": "Live Zoom Q&A", "time_to_result": "Ongoing"}
        ],
        "bonuses": [
            {"name": "Automation Templates", "description": "Done-for-you email sequences", "value": 997},
            {"name": "Private Community", "description": "24/7 support from peers", "value": 497}
        ],
        "guarantee": {
            "type": "90-Day Money Back Guarantee",
            "terms": "If you don't see results, get a full refund",
            "duration": "90 days"
        }
    }
    
    html = generate_landing_page_html(sample_offer)
    path = save_landing_page(html, sample_offer["name"])
    print(f"Landing page saved to: {path}")
