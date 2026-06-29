# Confidence Policy

## Purpose
Define confidence thresholds for AI responses based on evidence quality and data availability.

## Confidence Levels

### High Confidence (90-100%)
**Criteria:**
- Direct data retrieval from dataset
- Exact matches in ChromaDB
- Verified statistical calculations
- Multiple corroborating sources

**Examples:**
- "Customer 123 has churned (directly from dataset)"
- "50 customers have Fiber internet (verified count)"
- "Average tenure is 35 months (calculated from dataset)"

**Action:** Provide response with full details and sources.

### Medium Confidence (70-89%)
**Criteria:**
- Pattern analysis with clear evidence
- Statistical inference with reasonable sample size
- Correlation analysis with supporting data
- Partial matches in retrieval

**Examples:**
- "Customers with Month-to-Month contracts show higher churn tendency (pattern observed in data)"
- "Higher monthly charges correlate with churn (statistical correlation found)"
- "Customers with 3+ support tickets are at elevated risk (pattern analysis)"

**Action:** Provide response with confidence level, evidence, and caveats.

### Low Confidence (50-69%)
**Criteria:**
- Limited data points
- Weak correlations
- Incomplete information
- Small sample sizes

**Examples:**
- "Customer 456 may be at risk based on limited similar cases"
- "Trend suggests possible churn but insufficient data"

**Action:** Return "Insufficient Evidence" or provide response with strong disclaimers and request more data.

### Insufficient Evidence (<50%)
**Criteria:**
- No matching data
- No relevant retrieval results
- Contradictory evidence
- Missing critical information

**Action:** Return "Insufficient Evidence - Cannot provide reliable analysis"

## Confidence Calculation

### For Predictions
```
Confidence = (Data Quality × Evidence Strength × Sample Size) / 100
```

- Data Quality: 0-100 (completeness, accuracy)
- Evidence Strength: 0-100 (directness, corroboration)
- Sample Size: 0-100 (statistical significance)

### For Recommendations
```
Confidence = (Pattern Strength × Historical Success × Context Relevance) / 100
```

## Enforcement

### Prediction Agent
- Must provide confidence score for each prediction
- Low confidence predictions must be flagged
- Must explain confidence calculation

### Recommendation Agent
- Must provide confidence for each recommendation
- Low confidence recommendations must include alternatives
- Must reference similar successful cases

### Validation Agent
- Must verify confidence scores
- Must flag unjustified high confidence
- Must request evidence for low confidence claims

## Overrides

### Manual Override
Business users can override low confidence with:
- Business justification
- Risk acceptance
- Additional context

### System Override
System can override confidence with:
- Urgent business need
- Regulatory requirement
- Safety concern
