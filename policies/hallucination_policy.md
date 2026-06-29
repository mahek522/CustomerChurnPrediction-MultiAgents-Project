# Hallucination Policy

## Purpose
Prevent AI agents from generating false, unsupported, or misleading information (hallucinations).

## Definition
A hallucination occurs when an AI generates content that:
- Is not grounded in the provided data
- Contradicts known facts
- Makes claims without evidence
- Invents information not present in the context

## Prevention Strategies

### 1. Strict Grounding
- All claims must be backed by dataset records
- All statistics must be calculated from actual data
- All patterns must be observed in retrieved results
- No external knowledge unless explicitly provided

### 2. Evidence Requirements
- Every claim must have a source reference
- Statistical claims must show calculation method
- Pattern claims must show supporting examples
- Recommendations must reference similar successful cases

### 3. Confidence Thresholds
- Low confidence (<70%) triggers "Insufficient Evidence" response
- Medium confidence (70-89%) requires explicit caveats
- High confidence (90%+) requires full source attribution

### 4. Validation Layer
- Validation Agent checks all outputs for:
  - Source attribution
  - Statistical accuracy
  - Logical consistency
  - Evidence support

## Detection Methods

### 1. Keyword Detection
Flag responses containing:
- Terms not in dataset (e.g., "logistic regression", "credit score")
- Unsupported metrics (e.g., "balance level", "payment history")
- External concepts not in context

### 2. Statistical Verification
- Recalculate all statistics using Pandas
- Verify counts and percentages
- Check for impossible values
- Validate calculations

### 3. Cross-Reference
- Compare claims against dataset
- Verify customer IDs exist
- Check attribute values match
- Validate relationships

## Response Types

### Valid Response
- All claims have evidence
- Statistics are accurate
- Sources are cited
- Confidence is justified

### Hallucination Detected
- Response is rejected
- Agent is notified of specific issue
- Response is regenerated with proper grounding

### Insufficient Evidence
- Response indicates lack of data
- Suggests additional information needed
- Does not make unsupported claims

## Agent Responsibilities

### Query Agent
- Only format retrieved data
- Do not add interpretations
- Do not infer beyond records

### Data Analyst Agent
- Only analyze provided data
- Do not extrapolate beyond dataset
- Show calculation methods

### Prediction Agent
- Base predictions on patterns in data
- Provide confidence scores
- Explain prediction rationale

### Recommendation Agent
- Base recommendations on evidence
- Reference similar successful cases
- Provide alternatives

### Validation Agent
- Check all claims for evidence
- Verify all statistics
- Flag any unsupported content
- Enforce grounding policy

## Mitigation

### When Hallucination Detected
1. Identify specific hallucinated content
2. Trace to source agent
3. Provide feedback to agent
4. Regenerate response with constraints
5. Log incident for monitoring

### Continuous Improvement
- Track hallucination incidents
- Identify common patterns
- Update prompts to prevent recurrence
- Adjust confidence thresholds
- Improve validation rules
