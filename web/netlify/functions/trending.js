// Trending Opportunities Function
// Surfaces top 10 trending niches/opportunities to create offers around

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

// Simple in-memory cache (resets on cold start, but helps with warm instances)
let cache = {
  data: null,
  timestamp: 0
};

const CACHE_DURATION = 4 * 60 * 60 * 1000; // 4 hours in ms

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
      temperature: 0.8,
      max_tokens: 3000
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
                      text.match(/```\n?([\s\S]*?)\n?```/) ||
                      text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      try {
        return JSON.parse(jsonMatch[1] || jsonMatch[0]);
      } catch (e2) {
        return { raw: text, parseError: true };
      }
    }
    return { raw: text, parseError: true };
  }
}

async function getTrendingOpportunities() {
  // Check cache first
  const now = Date.now();
  if (cache.data && (now - cache.timestamp) < CACHE_DURATION) {
    return cache.data;
  }

  const systemPrompt = `You are a market trends analyst specializing in identifying emerging business opportunities for solo creators and entrepreneurs.

Your job is to identify 10 TRENDING opportunities right now — niches, audiences, or problems that are:
- Growing in search volume or social mentions
- Underserved by existing solutions
- Viable for a solo creator to build a product/service around
- Ethical and legitimate (NO adult content, fraud, abuse, gambling, or anything harmful)

Think about:
- New technologies creating opportunities (AI tools, automation, etc.)
- Demographic shifts (aging population, remote work, etc.)
- Economic trends (side hustles, cost-cutting, etc.)
- Cultural moments (viral trends, new platforms, etc.)
- Regulatory changes creating new needs
- Problems that are getting worse and need solutions

For each opportunity, explain WHY it's trending now and what kind of offer could serve it.

Return as JSON object with:
- opportunities: array of exactly 10 items, each containing:
  - title: short catchy title (3-6 words) that can be used as a search query
  - category: one of [Tech & AI, Health & Wellness, Finance & Business, Career & Skills, Lifestyle, B2B Services]
  - whyTrending: 1-2 sentence explanation of why this is hot right now
  - trendStrength: "rising" | "viral" | "steady-growth"
  - audienceSize: "niche" | "medium" | "mass-market"
  - offerIdea: quick 1-sentence offer idea for this space
  - icon: single emoji that represents this opportunity

Focus on CURRENT trends as of early 2026. Be specific and actionable, not generic.`;

  const userPrompt = `What are the top 10 trending opportunities for solo creators and entrepreneurs right now? Focus on emerging trends, growing problems, and underserved markets. Make them specific enough to research and build offers around.`;

  const result = await callOpenAI(systemPrompt, userPrompt);
  const parsed = parseJSON(result);
  
  // Update cache
  cache.data = parsed;
  cache.timestamp = now;
  
  return parsed;
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

  try {
    const data = await getTrendingOpportunities();
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        cached: cache.timestamp < Date.now() - 1000, // was it from cache?
        ...data
      })
    };

  } catch (error) {
    console.error("Trending error:", error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
