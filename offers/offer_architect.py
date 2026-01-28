#!/usr/bin/env python3
"""
Offer Architect - Hormozi Value Equation Framework
Creates high-ticket offers using the $100M Offers methodology
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class DreamOutcome:
    """What the customer ultimately wants"""
    primary_desire: str          # The main thing they want
    emotional_driver: str        # The feeling behind it
    status_outcome: str          # How they want to be perceived
    tangible_result: str         # Measurable outcome


@dataclass
class Problem:
    """Problems that prevent the dream outcome"""
    problem: str
    pain_level: int              # 1-10
    current_solution: str        # What they're doing now
    why_current_fails: str       # Why it doesn't work


@dataclass
class Solution:
    """Solutions we provide"""
    problem_solved: str
    solution: str
    delivery_method: str         # How we deliver it
    time_to_result: str          # How long until they see results


@dataclass
class Bonus:
    """Value-adding bonuses"""
    name: str
    description: str
    value: int                   # Dollar value
    solves: str                  # What objection/problem it addresses


@dataclass
class Guarantee:
    """Risk reversal"""
    type: str                    # Money-back, results-based, etc.
    terms: str
    duration: str


@dataclass 
class Offer:
    """Complete offer package"""
    name: str
    tagline: str
    target_audience: str
    dream_outcome: DreamOutcome
    problems: List[Problem]
    solutions: List[Solution]
    bonuses: List[Bonus]
    guarantee: Guarantee
    price: int
    anchor_value: int            # Total value of everything
    urgency: str
    scarcity: str


def calculate_value_equation(offer: Offer) -> dict:
    """
    Calculate the Hormozi Value Equation:
    Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort)
    """
    # Score components (simplified for calculation)
    dream_score = 10  # Assumed high if properly defined
    likelihood_score = len(offer.solutions) + len(offer.bonuses)  # More solutions = higher likelihood
    time_score = 1  # Lower is better
    effort_score = 1  # Lower is better
    
    # Adjust based on guarantee
    if offer.guarantee and "money back" in offer.guarantee.type.lower():
        likelihood_score += 3
    
    value_score = (dream_score * likelihood_score) / (time_score * effort_score)
    
    return {
        "value_score": round(value_score, 1),
        "dream_outcome": dream_score,
        "likelihood": likelihood_score,
        "time_delay": time_score,
        "effort": effort_score,
        "price_to_value_ratio": round(offer.anchor_value / offer.price, 1) if offer.price > 0 else 0
    }


def generate_offer_stack(offer: Offer) -> str:
    """Generate the offer stack presentation."""
    
    stack = f"""
# 🎯 {offer.name}
## "{offer.tagline}"

### For: {offer.target_audience}

---

## The Dream Outcome
**{offer.dream_outcome.primary_desire}**

- 💭 {offer.dream_outcome.emotional_driver}
- 🏆 {offer.dream_outcome.status_outcome}
- 📊 {offer.dream_outcome.tangible_result}

---

## What's Included

"""
    
    total_value = 0
    
    # Main solutions
    for i, sol in enumerate(offer.solutions, 1):
        stack += f"""### {i}. {sol.solution}
- Solves: {sol.problem_solved}
- Delivered via: {sol.delivery_method}
- Results in: {sol.time_to_result}

"""
    
    # Bonuses
    if offer.bonuses:
        stack += "---\n\n## 🎁 BONUSES\n\n"
        for bonus in offer.bonuses:
            total_value += bonus.value
            stack += f"""### BONUS: {bonus.name} (${bonus.value:,} Value)
{bonus.description}
*{bonus.solves}*

"""
    
    # Guarantee
    stack += f"""---

## ✅ GUARANTEE
**{offer.guarantee.type}**
{offer.guarantee.terms}
Duration: {offer.guarantee.duration}

---

## 💰 Investment

"""
    
    total_value += offer.anchor_value
    
    stack += f"""**Total Value: ${total_value:,}**

~~${offer.anchor_value:,}~~

### Your Investment: **${offer.price:,}**

That's {round(total_value / offer.price, 1)}x the value of your investment.

"""
    
    if offer.urgency:
        stack += f"""### ⏰ {offer.urgency}
"""
    
    if offer.scarcity:
        stack += f"""### 🔒 {offer.scarcity}
"""
    
    return stack


def create_offer_from_niche(
    niche: str,
    target: str,
    main_problem: str,
    dream_result: str,
    price: int = 2997
) -> Offer:
    """
    Quick offer generator from basic inputs.
    """
    
    # Generate dream outcome
    dream = DreamOutcome(
        primary_desire=dream_result,
        emotional_driver=f"Feel confident and in control of their {niche}",
        status_outcome=f"Be seen as successful in {niche}",
        tangible_result=f"Measurable improvement in {niche} within 90 days"
    )
    
    # Generate problems
    problems = [
        Problem(
            problem=main_problem,
            pain_level=8,
            current_solution="Trying to figure it out alone",
            why_current_fails="No proven system or accountability"
        ),
        Problem(
            problem=f"Don't know where to start with {niche}",
            pain_level=7,
            current_solution="Watching free YouTube videos",
            why_current_fails="Information overload, no clear path"
        ),
        Problem(
            problem="Lack of support and guidance",
            pain_level=7,
            current_solution="Asking friends or family",
            why_current_fails="They don't have expertise"
        )
    ]
    
    # Generate solutions
    solutions = [
        Solution(
            problem_solved=main_problem,
            solution=f"{niche.title()} Mastery System",
            delivery_method="Step-by-step video training + templates",
            time_to_result="See first results in 7-14 days"
        ),
        Solution(
            problem_solved="Don't know where to start",
            solution="Quick-Start Action Plan",
            delivery_method="Done-for-you roadmap + checklists",
            time_to_result="Get clarity immediately"
        ),
        Solution(
            problem_solved="Lack of support",
            solution="Weekly Group Coaching Calls",
            delivery_method="Live Zoom calls + Q&A",
            time_to_result="Get answers within 24-48 hours"
        )
    ]
    
    # Generate bonuses
    bonuses = [
        Bonus(
            name="Private Community Access",
            description="24/7 access to our private community of action-takers",
            value=997,
            solves="Feeling alone on the journey"
        ),
        Bonus(
            name="Done-For-You Templates",
            description=f"Copy-paste templates for every aspect of {niche}",
            value=497,
            solves="Don't have time to create from scratch"
        ),
        Bonus(
            name="1-on-1 Strategy Session",
            description="Personal 30-minute call to create your custom plan",
            value=500,
            solves="Need personalized guidance"
        )
    ]
    
    # Guarantee
    guarantee = Guarantee(
        type="100% Money-Back Guarantee",
        terms="If you follow the system and don't see results in 90 days, we'll refund every penny.",
        duration="90 days"
    )
    
    return Offer(
        name=f"{niche.title()} Accelerator",
        tagline=f"The proven system to {dream_result.lower()}",
        target_audience=target,
        dream_outcome=dream,
        problems=problems,
        solutions=solutions,
        bonuses=bonuses,
        guarantee=guarantee,
        price=price,
        anchor_value=price * 3,
        urgency="Enrollment closes Friday at midnight",
        scarcity="Only 10 spots available this month"
    )


def offer_to_dict(offer: Offer) -> dict:
    """Convert offer to dictionary for JSON storage."""
    return {
        "name": offer.name,
        "tagline": offer.tagline,
        "target_audience": offer.target_audience,
        "dream_outcome": asdict(offer.dream_outcome),
        "problems": [asdict(p) for p in offer.problems],
        "solutions": [asdict(s) for s in offer.solutions],
        "bonuses": [asdict(b) for b in offer.bonuses],
        "guarantee": asdict(offer.guarantee),
        "price": offer.price,
        "anchor_value": offer.anchor_value,
        "urgency": offer.urgency,
        "scarcity": offer.scarcity,
        "value_equation": calculate_value_equation(offer)
    }


if __name__ == "__main__":
    # Example usage
    offer = create_offer_from_niche(
        niche="email marketing",
        target="Online coaches who want more sales",
        main_problem="Not converting email subscribers into buyers",
        dream_result="Turn your email list into a revenue machine",
        price=2997
    )
    
    print(generate_offer_stack(offer))
    print("\n\n--- Value Equation ---")
    print(json.dumps(calculate_value_equation(offer), indent=2))
