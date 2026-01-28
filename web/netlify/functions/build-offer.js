// Build Offer - Generates complete Hormozi-style offer stack
// Auto-fills all fields based on the offer idea

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

async function callOpenAI(systemPrompt, userPrompt) {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt }
      ],
      temperature: 0.7,
      max_tokens: 2500
    })
  });
  
  const data = await response.json();
  if (data.error) throw new Error(data.error.message);
  return data.choices[0].message.content;
}

function parseJSON(text) {
  try {
    return JSON.parse(text);
  } catch (e) {
    const jsonMatch = text.match(/```json\n?([\s\S]*?)\n?```/) || 
                      text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      try {
        return JSON.parse(jsonMatch[1] || jsonMatch[0]);
      } catch (e2) {
        return null;
      }
    }
    return null;
  }
}

exports.handler = async (event, context) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json"
  };

  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers, body: "" };
  }

  if (event.httpMethod !== "POST") {
    return { statusCode: 405, headers, body: JSON.stringify({ error: "Method not allowed" }) };
  }

  try {
    const { offer, context: marketContext } = JSON.parse(event.body);
    
    if (!offer) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: "Missing offer data" }) };
    }

    const systemPrompt = `You are an expert at creating irresistible offers using Alex Hormozi's $100M Offers framework.

Given an offer idea, generate a COMPLETE offer stack with all the details needed to sell it.

The Value Equation: Value = (Dream Outcome × Perceived Likelihood) ÷ (Time Delay × Effort & Sacrifice)
- Maximize Dream Outcome and Perceived Likelihood
- Minimize Time Delay and Effort

Return JSON with:
{
  "offerName": "Catchy, benefit-driven name",
  "tagline": "One-line hook that grabs attention",
  "targetAudience": "Specific description of ideal customer",
  "dreamOutcome": "The transformation they REALLY want (be specific and emotional)",
  "likelihood": "Why THIS will work for them (proof, system, credentials)",
  "timeDelay": "How fast they'll see results",
  "effort": "How easy you make it (done-for-you aspects)",
  "price": 997,
  "pricingModel": "one-time or monthly",
  "coreOffer": {
    "name": "Name of the core program/product",
    "description": "What it includes",
    "value": "$X,XXX"
  },
  "bonuses": [
    {"name": "Bonus 1 Name", "description": "What it is", "value": "$XXX"},
    {"name": "Bonus 2 Name", "description": "What it is", "value": "$XXX"},
    {"name": "Bonus 3 Name", "description": "What it is", "value": "$XXX"}
  ],
  "guarantee": {
    "type": "money-back or results-based",
    "headline": "Guarantee headline",
    "details": "Full guarantee description"
  },
  "urgency": "Why they should act now (scarcity or bonus deadline)",
  "socialProof": "Credibility statement (results, testimonials placeholder)",
  "implementationSteps": [
    "Step 1: What to do first",
    "Step 2: Next action",
    "Step 3: Then what",
    "Step 4: Final step"
  ],
  "techStack": "Suggested tools to build this (e.g., Stripe, Teachable, Notion)",
  "launchPlan": "Quick 1-2 week launch plan"
}

Make it specific to the offer. Don't be generic. Use power words and emotional triggers.`;

    const userPrompt = `Build a complete Hormozi-style offer for:

OFFER IDEA: ${offer.name || 'Untitled Offer'}
DESCRIPTION: ${offer.description || 'No description provided'}
CATEGORY: ${offer.category || 'Product'}
TARGET MARKET: ${marketContext || 'General audience'}
${offer.distributionPlay ? `DISTRIBUTION: ${offer.distributionPlay}` : ''}
${offer.priceRange ? `PRICE RANGE: ${offer.priceRange}` : ''}

Generate a complete, ready-to-sell offer with all the Hormozi framework elements filled in.`;

    const result = await callOpenAI(systemPrompt, userPrompt);
    const parsed = parseJSON(result);
    
    if (!parsed) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: "Failed to parse offer generation", raw: result })
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        offer: parsed,
        originalIdea: offer
      })
    };

  } catch (error) {
    console.error("Build offer error:", error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
