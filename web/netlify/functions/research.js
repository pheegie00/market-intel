// Market Intelligence Research Function
// Uses OpenAI to power market research and analysis

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

async function callOpenAI(systemPrompt, userPrompt, model = "gpt-4o-mini") {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt }
      ],
      temperature: 0.7,
      max_tokens: 4000
    })
  });
  
  const data = await response.json();
  if (data.error) throw new Error(data.error.message);
  return data.choices[0].message.content;
}

// Research handlers for each type
const handlers = {
  
  // Audience Discovery
  async audience(query) {
    const systemPrompt = `You are a market research expert. Analyze the given niche/space and identify specific audience segments that could be served. For each segment provide:
- Segment name
- Who they are (demographics, job titles, characteristics)
- Psychographics (goals, fears, values)
- Estimated market size (small/medium/large)
- Underserved level (low/medium/high)

Return as JSON array with objects containing: name, who, psychographics, marketSize, underservedLevel, notes`;

    const result = await callOpenAI(systemPrompt, `Analyze this space and identify 5-7 distinct audience segments: "${query}"`);
    return { type: "audience", query, result: parseJSON(result) };
  },

  // Where They Hang Out
  async channels(query) {
    const systemPrompt = `You are a market research expert specializing in audience distribution channels. For the given audience, identify WHERE they spend time online and offline, AND what tools/software they use. Provide specific, actionable names.

Return as JSON object with these categories:
- reddit: array of specific subreddit names with subscriber estimates
- facebook: array of specific group names/types
- linkedin: array of relevant groups, hashtags, influencers
- discord: relevant servers or communities
- slack: relevant Slack communities/workspaces
- newsletters: specific newsletters they likely read
- podcasts: specific podcasts they likely listen to
- youtube: channels they follow
- events: conferences, meetups, communities
- influencers: specific people they follow (with platform)
- saasTools: array of SaaS products/tools this audience uses to solve related problems, each with:
  - name: tool name
  - url: website
  - whatItDoes: brief description
  - pricing: price range
  - gap: what it does NOT solve (opportunity for you)
- courses: existing courses/training programs serving this audience
- certifications: relevant certifications this audience pursues
- jobBoards: where they look for jobs/opportunities

Be SPECIFIC - give actual names, URLs, and details. Not generic descriptions.`;

    const result = await callOpenAI(systemPrompt, `Where does this audience hang out? Audience: "${query}"`);
    return { type: "channels", query, result: parseJSON(result) };
  },

  // Pain Point Mining
  async painpoints(query) {
    const systemPrompt = `You are a market research expert specializing in customer pain points and problems. For the given audience, identify their key struggles, frustrations, and unmet needs.

Return as JSON object with:
- urgent: array of urgent/burning problems they face RIGHT NOW
- chronic: array of ongoing frustrations they've learned to live with
- aspirational: array of goals they want to achieve but struggle with
- questions: common questions they ask (that indicate pain)
- failures: things they've tried that didn't work
- wishes: things they wish existed
- quotes: realistic quotes/statements they might say expressing pain

For each pain point, include: description, intensity (1-10), frequency (how often they face it), and willingness_to_pay (low/medium/high)`;

    const result = await callOpenAI(systemPrompt, `What are the pain points for this audience? "${query}"`);
    return { type: "painpoints", query, result: parseJSON(result) };
  },

  // Competitor Analysis
  async competitors(query) {
    const systemPrompt = `You are a competitive intelligence expert. For the given market/audience, identify existing competitors and analyze the landscape.

Return as JSON object with:
- direct: array of direct competitors (same audience, same solution type)
- indirect: array of indirect competitors (same audience, different approach)
- adjacent: array of adjacent players (could enter this market)

For each competitor include:
- name: company/product name
- url: website if known
- offering: what they sell
- pricing: price point if known
- positioning: how they position themselves
- strengths: what they do well
- weaknesses: gaps or complaints
- audience_size: estimated reach (small/medium/large)

Also include:
- gaps: array of opportunities/gaps in the market
- trends: what's changing in this space
- barriers: barriers to entry`;

    const result = await callOpenAI(systemPrompt, `Analyze the competitive landscape for: "${query}"`);
    return { type: "competitors", query, result: parseJSON(result) };
  },

  // Demand Validation
  async demand(query) {
    const systemPrompt = `You are a market analyst specializing in demand validation. For the given topic/niche, assess the market demand and trends.

Return as JSON object with:
- searchTerms: array of relevant search terms with estimated monthly volume (low/medium/high/very high)
- trendDirection: growing, stable, or declining
- trendReason: why it's trending that direction
- seasonality: any seasonal patterns
- relatedTopics: adjacent topics with demand
- marketSignals: signals indicating demand (or lack thereof)
- concerns: any red flags or concerns
- opportunities: timing or positioning opportunities
- demandScore: 1-10 overall demand rating
- competitionLevel: low/medium/high
- recommendation: brief recommendation on whether to pursue`;

    const result = await callOpenAI(systemPrompt, `Validate the demand for: "${query}"`);
    return { type: "demand", query, result: parseJSON(result) };
  },

  // Offer Ideation
  async offers(query) {
    const systemPrompt = `You are a growth hacker. Suggest 8 monetization strategies for the given audience. Mix of:
- AI tools (auto-generate/submit/analyze)
- Aggregation plays (curate content, sell ads)
- Viral mechanics (shareable outputs, referral loops)
- Products (courses, communities - but with distribution twist)

At least 5 must be tools/aggregation/viral, not just courses.

Return JSON:
{
  "offers": [8 items with: name, category (Tool/Aggregator/Viral/Product), type, description (1 sentence), distributionPlay (how it spreads), priceRange, effort (low/med/high)],
  "quickWin": {name, description},
  "aggregationPlay": {name, description},
  "viralMechanic": {name, description}
}

Be specific and creative. Think automation, not just content.`;

    const result = await callOpenAI(systemPrompt, `Monetization strategies for: "${query}"`);
    return { type: "offers", query, result: parseJSON(result) };
  },

  // Full Pipeline - comprehensive analysis
  async full(query) {
    const systemPrompt = `You are a comprehensive market intelligence analyst. Conduct a full market analysis for the given niche/audience.

Return as JSON object with ALL of the following sections:

1. "audience": Top 3 audience segments with: name, who, psychographics, underservedLevel

2. "channels": Where they hang out - top 3 for each: reddit, linkedin, newsletters, podcasts, influencers

3. "painpoints": 
   - top5Urgent: 5 most urgent pain points with intensity (1-10)
   - topQuestions: 5 questions they commonly ask

4. "competitors":
   - top5: 5 main competitors with name, offering, pricing, weakness
   - gaps: 3 market gaps/opportunities

5. "demand":
   - score: 1-10 demand rating
   - trend: growing/stable/declining
   - searchTerms: 5 key search terms

6. "offers":
   - recommended: top 3 offer ideas with name, type, priceRange, effort, distributionPlay
   - quickWin: the fastest/easiest offer with viral potential
   - bigOpportunity: the biggest revenue opportunity
   - aggregationPlay: best content aggregation/roll-up opportunity (pool overseas content, translate, sell ads)
   - viralMechanic: best viral loop (shareable output, referral leaderboard, auto-post to social)
   - toolIdea: best "AI does it for you" automation tool (like ListingBott - auto-submit to 50 platforms)

7. "verdict":
   - pursue: yes/maybe/no
   - reasoning: 2-3 sentence explanation
   - nextSteps: array of 3 concrete next steps

Be specific and actionable. This is for a solo creator evaluating whether to enter this market.`;

    const result = await callOpenAI(systemPrompt, `Full market intelligence analysis for: "${query}"`);
    return { type: "full", query, result: parseJSON(result) };
  }
};

function parseJSON(text) {
  // Try to extract JSON from the response
  try {
    // First try direct parse
    return JSON.parse(text);
  } catch (e) {
    // Try to find JSON in the text
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

exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json"
  };

  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers, body: "" };
  }

  if (event.httpMethod !== "POST") {
    return { 
      statusCode: 405, 
      headers,
      body: JSON.stringify({ error: "Method not allowed" }) 
    };
  }

  try {
    const { type, query } = JSON.parse(event.body);
    
    if (!type || !query) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: "Missing type or query" })
      };
    }

    if (!handlers[type]) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: `Unknown research type: ${type}` })
      };
    }

    const result = await handlers[type](query);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(result)
    };

  } catch (error) {
    console.error("Research error:", error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
// Updated Wed Jan 28 18:09:37 UTC 2026
