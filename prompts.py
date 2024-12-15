EVAL_PROMPT_1 = """
Given the user's question will retrieving data from the Tesla Owners Manual help provide an answer to the user's question. 
response with either 'yes' or 'no'.""",

EVAL_PROMPT_2 = """
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


EVAL_PROMPT_3 ="""
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