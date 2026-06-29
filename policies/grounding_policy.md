# Grounding Policy

## Purpose
Ensure all AI responses are grounded in actual data from the dataset, retrieved vector chunks, or approved business rules.

## Rules

### 1. Data Sources
Responses must only be based on:
- Customer records from the dataset
- Retrieved vector chunks from ChromaDB
- Approved business rules and policies

### 2. Unsupported Claims
Agents must NOT:
- Make claims about data not present in the dataset
- Infer information that cannot be verified
- Use external knowledge not in the context
- Generate statistics without calculation

### 3. Source Attribution
Every response must provide:
- Dataset references (customer IDs, record counts)
- Chroma retrieval source (which documents were retrieved)
- Agent responsible for the claim

### 4. Confidence Thresholds
- High confidence (90%+): Direct data retrieval
- Medium confidence (70-89%): Pattern analysis with clear evidence
- Low confidence (<70%): Return "Insufficient Evidence"

### 5. Verification
All statistical claims must be verified using:
- Pandas operations on the dataset
- SQL queries on PostgreSQL
- ChromaDB retrieval results

## Enforcement
The Validation Agent enforces this policy by checking:
- Source attribution in responses
- Statistical calculations
- Evidence for claims
- Confidence scores

## Violations
If grounding policy is violated:
- Response is rejected
- Agent is notified
- Response is regenerated with proper grounding
