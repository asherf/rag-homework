CONTEXT_PROMPT = (
    "You are a helpful assistant that answers questions based on the provided context."
)

EVAL_PROMPT_1 = (
    """
Given the user's question will retrieving data from the Tesla Owners Manual help provide an answer to the user's question. 
response with either 'yes' or 'no'.""",
)

CLAUDE_EVAL_PROMPT_2 = """
# RAG Query Evaluation Prompt

You are an intelligent query evaluator tasked with determining whether a given user query requires data retrieval through Retrieval-Augmented Generation (RAG) to provide an accurate and comprehensive response.

## Evaluation Criteria

Determine if the query needs data retrieval by assessing the following dimensions:

1. **Specificity and Domain Knowledge**
   - Does the query require specific, up-to-date, or detailed information beyond general knowledge?
   - Are there domain-specific details that cannot be confidently answered from pre-trained knowledge?

2. **Information Currency**
   - Is the query about recent events, current statistics, or time-sensitive information?
   - Does the query reference specific documents, reports, or sources that would require external data?

3. **Contextual Depth**
   - Does the query ask for detailed explanations that would benefit from referenced sources?
   - Is additional context or supporting evidence necessary to provide a comprehensive answer?

## Decision Framework

Classify the query into one of these categories:

- **Definite RAG Needed**: 
  - Queries requiring specific, verifiable information
  - Questions about recent events or current data
  - Requests for detailed explanations with source references
  - Technical or specialized domain inquiries

- **Potential RAG Needed**:
  - Queries with some specificity that might benefit from additional context
  - Questions where pre-trained knowledge seems insufficient
  - Requests that could be enhanced by supplementary information

- **No RAG Required**:
  - General knowledge questions
  - Broad conceptual inquiries
  - Simple explanations or definitions
  - Conversational or open-ended queries

## Evaluation Process

1. Analyze the query's language, intent, and required depth of information
2. Assess the complexity and specificity of the query
3. Determine the likelihood of finding relevant, authoritative sources
4. Make a clear recommendation for data retrieval

## Output Format

Provide a structured response:
```json
{
  "rag_needed": true/false,
  "confidence_level": "high"/"medium"/"low",
  "retrieval_rationale": "Explanation of why RAG is or isn't needed",
  "recommended_action": "retrieve_data"/"use_general_knowledge"
}
```

## Example Scenarios

### Scenario 1: RAG Needed
**Query**: "What were Acme Corp's quarterly earnings in Q2 2024?"
- **Rationale**: Requires specific, current financial data not in general knowledge

### Scenario 2: No RAG Needed
**Query**: "Explain the concept of machine learning"
- **Rationale**: General explanation possible from pre-trained knowledge

### Scenario 3: Potential RAG
**Query**: "What are the latest trends in renewable energy technology?"
- **Rationale**: Might benefit from recent sources and specific details
"""


CLAUDE_EVAL_PROMPT_3 = """
# Tesla Owner's Manual RAG Query Evaluation Prompt

## Purpose
Determine whether a user query can be effectively answered using the Tesla owner's manual through Retrieval-Augmented Generation (RAG).

## Evaluation Criteria

### Primary Decision Factors
1. **Manual Relevance**
   - Is the query directly related to vehicle operation, features, or maintenance?
   - Could the answer be reasonably found in an official Tesla owner's manual?

2. **Query Specificity**
   - Is the question specific enough to be addressed by technical documentation?
   - Does the query relate to:
     * Vehicle controls and interfaces
     * Charging procedures
     * Safety features
     * Maintenance instructions
     * Specific vehicle systems (autopilot, climate control, etc.)

3. **Exclusion Criteria
   Avoid RAG retrieval for:
   - General automotive knowledge
   - Highly speculative questions
   - Queries about future updates or unreleased features
   - Personal opinion or experience-based questions

## Decision Matrix

### Strongly Recommend RAG
- Explicit questions about Tesla vehicle operation
- Specific feature inquiries
- Maintenance and care instructions
- Troubleshooting guidance
- Technical specifications

### Potentially Use RAG
- Somewhat technical queries about vehicle functionality
- Queries that might have partial manual coverage
- Questions requiring nuanced technical explanation

### Do Not Use RAG
- Broad conceptual questions
- Comparative analyses
- Pricing or sales-related inquiries
- Personal experience or opinion requests

## Output Format

```json
{
  "rag_recommended": true/false,
  "confidence_level": "high"/"medium"/"low",
  "retrieval_rationale": "Explanation of RAG suitability",
  "recommended_action": "retrieve_manual_data"/"use_general_knowledge"
}
```

## Example Scenarios

### Scenario 1: Definite RAG Use
**Query**: "How do I activate Sentry Mode on my Tesla?"
- **Rationale**: Specific operational instruction likely in owner's manual

### Scenario 2: No RAG Needed
**Query**: "Are electric vehicles the future of transportation?"
- **Rationale**: Broad conceptual question beyond manual scope

### Scenario 3: Potential RAG
**Query**: "What does a yellow warning light on the dashboard mean?"
- **Rationale**: Likely covered in manual, but might require context
"""

CLAUDE_EVAL_PROMPT_3a_JSON = """
# Tesla Owner's Manual RAG Query Evaluation Prompt

## Purpose
Determine whether a user query can be effectively answered using the Tesla owner's manual through Retrieval-Augmented Generation (RAG).

## Evaluation Criteria

### Primary Decision Factors
1. **Manual Relevance**
   - Is the query directly related to vehicle operation, features, or maintenance?
   - Could the answer be reasonably found in an official Tesla owner's manual?

2. **Query Specificity**
   - Is the question specific enough to be addressed by technical documentation?
   - Does the query relate to:
     * Vehicle controls and interfaces
     * Charging procedures
     * Safety features
     * Maintenance instructions
     * Specific vehicle systems (autopilot, climate control, etc.)

3. **Exclusion Criteria
   Avoid RAG retrieval for:
   - General automotive knowledge
   - Highly speculative questions
   - Queries about future updates or unreleased features
   - Personal opinion or experience-based questions

## Decision Matrix

### Strongly Recommend RAG
- Explicit questions about Tesla vehicle operation
- Specific feature inquiries
- Maintenance and care instructions
- Troubleshooting guidance
- Technical specifications

### Potentially Use RAG
- Somewhat technical queries about vehicle functionality
- Queries that might have partial manual coverage
- Questions requiring nuanced technical explanation

### Do Not Use RAG
- Broad conceptual questions
- Comparative analyses
- Pricing or sales-related inquiries
- Personal experience or opinion requests

## Output Format

{
  "rag_recommended": true/false,
  "confidence_level": "high"/"medium"/"low",
  "retrieval_rationale": "Explanation of RAG suitability",
  "recommended_action": "retrieve_manual_data"/"use_general_knowledge"
}

## Example Scenarios

### Scenario 1: Definite RAG Use
**Query**: "How do I activate Sentry Mode on my Tesla?"
- **Rationale**: Specific operational instruction likely in owner's manual

### Scenario 2: No RAG Needed
**Query**: "Are electric vehicles the future of transportation?"
- **Rationale**: Broad conceptual question beyond manual scope

### Scenario 3: Potential RAG
**Query**: "What does a yellow warning light on the dashboard mean?"
- **Rationale**: Likely covered in manual, but might require context
"""

FACTUAL_PROMPT = """Generate 2-3 questions that real Cybertruck owners would actually type into a search bar or ask in an owners' forum. These should feel completely natural and conversational.

Write questions as if they were being typed into a search bar or asked in a forum. For example:

Instead of:
- "How do I activate the climate control system?"
- "What should I do if the touchscreen becomes unresponsive?"
- "How does one optimize range in cold weather?"

Write:
- "how to turn on AC in cybertruck"
- "screen frozen - what now?"
- "battery draining fast in cold weather"

Make questions feel real by:
1. Using natural search patterns
   - "how to..."
   - "why is my..."
   - "help with..."
2. Including context and emotion
   - "stuck at supercharger"
   - "help! frunk won't open"
   - "confused about ride height settings"
3. Writing like real people
   - Use contractions (I'm, won't, can't)
   - OK to use incomplete sentences
   - Include emotional context ("Help!", "Confused about...", "Worried about...")
4. Adding situational details
   - "in rain"
   - "with kids"
   - "while camping"

For each question, evaluate its real-world relevance:
- "common": Everyday, urgent needs:
  * "trunk won't close"
  * "phone key not working"
  * "what's this warning light mean"

- "rare": Occasional situations:
  * "winterizing cybertruck"
  * "car wash settings?"
  * "towing setup help"

- "unlikely": Technical/administrative:
  * Manual details
  * Specifications
  * Legal info

Text: {text}

Provide your response in the following JSON format:
{{
    "questions": [
        {{
            "question": "Natural, search-like question",
            "answer": "Clear, helpful answer",
            "supporting_text": "Relevant excerpt from source text",
            "question_type": "factual",
            "relevance_level": "common|rare|unlikely",
            "relevance_reasoning": "Brief explanation of why this question fits the chosen relevance level"
        }}
    ]
}}"""

REASONING_PROMPT = """Generate 2-3 questions that real Cybertruck owners would ask when trying to understand how features work together or make decisions about using their vehicle. These should feel like real forum posts or search queries.

Write questions as if they were being posted in an owners' forum. For example:

Instead of:
- "What is the optimal charging strategy?"
- "How does ambient temperature affect range?"
- "What are the considerations for child safety?"

Write:
- "best way to charge for long road trip?"
- "losing tons of range in cold - what helps?"
- "safest seats for car seats?"

Make questions feel real by:
1. Using natural patterns
   - "better to..."
   - "best way to..."
   - "tips for..."
2. Including context and emotion
   - "worried about range"
   - "confused about charging"
   - "need advice on settings"
3. Writing like real people
   - Use contractions (I'm, won't, can't)
   - OK to use incomplete sentences
   - Include emotional context ("Help!", "Confused about...", "Worried about...")
4. Adding situational details
   - "for camping"
   - "in winter"
   - "with full family"

For each question, evaluate its real-world relevance:
- "common": Everyday decisions:
  * "faster charging vs battery life?"
  * "seat heaters or cabin heat?"
  * "best settings for commute"

- "rare": Occasional planning:
  * "road trip planning help"
  * "winter driving tips"
  * "towing affects on range?"

- "unlikely": Technical/theoretical:
  * System details
  * Technical specs
  * Legal considerations

Text: {text}

Provide your response in the following JSON format:
{{
    "questions": [
        {{
            "question": "Natural, forum-style question",
            "answer": "Practical, helpful answer",
            "supporting_text": "Relevant excerpt from source text",
            "question_type": "reasoning",
            "relevance_level": "common|rare|unlikely",
            "relevance_reasoning": "Brief explanation of why this question fits the chosen relevance level"
        }}
    ]
}}"""


# From Claude.ai - given:
# You are an LLM expert. given 3 pieces of input:
# 1. questions
# 2. Answer
# 3. Expected answer
# Create a prompt that will act as a LLM-as-a-judge evaluator that will take the questions & answer (1 & 2) and will rate the answer from 1 to 10 based on how accurate and comprehensive it is given the expected answer (item 3)
LLM_JUDGE_EVAL_PROMPT = """You are an expert AI judge tasked with evaluating the quality and accuracy of answers against a ground truth expected answer. Your evaluation will be precise, objective, and nuanced.

Evaluation Criteria:
1. Comprehensive Quality Score (1-10):
   - Assess the overall quality of the answer across multiple dimensions:
     a) Accuracy of information
     b) Completeness of coverage
     c) Relevance to the original question
     d) Depth of explanation
     e) Precision of language

Scoring Guidelines:
10 - Perfect Answer
- Completely matches the expected answer
- Covers all key points comprehensively
- No factual errors
- Provides deep, insightful explanation

9 - Excellent Answer
- Almost fully matches expected answer
- Minor, negligible omissions
- Extremely high-quality explanation

7-8 - Very Good Answer
- Covers most key points
- Some minor gaps or slight imprecisions
- Solid overall understanding

5-6 - Adequate Answer
- Captures core information
- Several important points missing
- Moderate level of detail

3-4 - Partial Answer
- Significant gaps in information
- Misses critical components
- Limited depth and understanding

1-2 - Poor Answer
- Minimal relevant information
- Major misunderstandings
- Fails to address core question

0 - Completely Incorrect
- No relevant information
- Totally misses the point of the question

Output Format:
{
  "quality_score": [0-10],
  "justification": "Detailed explanation of the score",
  "strengths": ["List of strengths"],
  "areas_for_improvement": ["List of gaps or weaknesses"]
}
"""
