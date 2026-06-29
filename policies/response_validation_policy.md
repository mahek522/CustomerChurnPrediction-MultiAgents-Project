# Response Validation Policy

## Purpose
Ensure all AI responses meet quality standards, are safe for business use, and comply with all policies.

## Validation Criteria

### 1. Grounding Validation
- All claims must be backed by data sources
- Source references must be provided
- Statistics must be verifiable
- No unsupported assertions

### 2. Confidence Validation
- Confidence scores must be justified
- Low confidence responses must have caveats
- Insufficient evidence must be explicitly stated
- Confidence calculation must be explained

### 3. PII Validation
- No personally identifiable information
- Customer IDs used instead of names
- Contact information redacted
- Sensitive data masked

### 4. Toxicity Validation
- No offensive language
- No discriminatory content
- No harmful recommendations
- Professional tone maintained

### 5. Hallucination Validation
- No invented information
- No external knowledge not in context
- No contradictory statements
- No unsupported metrics

## Validation Process

### Step 1: Pre-Response Validation
Before generating response:
- Check query for malicious intent
- Verify sufficient data available
- Assess confidence level
- Determine appropriate response type

### Step 2: Post-Response Validation
After generating response:
- Scan for PII patterns
- Check for hallucination indicators
- Verify statistical accuracy
- Validate source attribution
- Assess confidence justification

### Step 3: Final Approval
Response approved only if:
- All validation checks pass
- Confidence score is justified
- No policy violations
- Quality standards met

## Response Types

### Type 1: High Confidence Response
**Characteristics:**
- Direct data retrieval
- Verified statistics
- Clear source attribution
- Confidence 90%+

**Validation:**
- Verify data sources
- Recalculate statistics
- Check source references
- Confirm confidence

### Type 2: Medium Confidence Response
**Characteristics:**
- Pattern analysis
- Statistical inference
- Partial evidence
- Confidence 70-89%

**Validation:**
- Verify pattern strength
- Check sample size
- Validate inference logic
- Confirm confidence justification
- Ensure caveats present

### Type 3: Low Confidence Response
**Characteristics:**
- Limited data
- Weak evidence
- Confidence 50-69%

**Validation:**
- Verify data limitations
- Check for alternative approaches
- Ensure strong disclaimers
- Confirm "Insufficient Evidence" if appropriate

### Type 4: Insufficient Evidence Response
**Characteristics:**
- No matching data
- No relevant retrieval
- Confidence <50%

**Validation:**
- Confirm no data available
- Verify retrieval attempts
- Ensure no unsupported claims
- Check for helpful suggestions

## Quality Standards

### Accuracy
- All statistics must be correct
- All claims must be verifiable
- All sources must be accurate
- All calculations must be valid

### Clarity
- Language must be clear
- Explanations must be understandable
- Recommendations must be actionable
- Caveats must be explicit

### Completeness
- All relevant factors considered
- All alternatives presented
- All limitations stated
- All sources cited

### Consistency
- Internal logic consistent
- External data consistent
- Previous responses consistent
- Business rules consistent

## Rejection Criteria

Response is rejected if:
- Contains PII
- Contains hallucinations
- Has unjustified confidence
- Lacks source attribution
- Contains toxic content
- Has statistical errors
- Violates business rules
- Exceeds scope of authority

## Remediation

### When Response Rejected
1. Identify specific violation
2. Notify generating agent
3. Provide specific feedback
4. Regenerate with constraints
5. Re-validate new response

### Common Issues and Fixes

**Issue: Missing Source Attribution**
- Fix: Add dataset references
- Fix: Cite Chroma retrieval results
- Fix: Reference business rules

**Issue: Unjustified Confidence**
- Fix: Provide evidence
- Fix: Lower confidence score
- Fix: Add caveats

**Issue: Statistical Error**
- Fix: Recalculate using Pandas
- Fix: Verify with SQL
- Fix: Check calculation method

**Issue: Hallucination**
- Fix: Remove unsupported claims
- Fix: Add evidence
- Fix: Regenerate with grounding

## Monitoring

### Metrics Tracked
- Validation pass rate
- Rejection reasons
- Common violations
- Agent performance
- Response quality trends

### Continuous Improvement
- Analyze rejection patterns
- Update validation rules
- Improve agent prompts
- Adjust confidence thresholds
- Enhance guardrail patterns

## Agent Responsibilities

### All Agents
- Follow all policies
- Provide source attribution
- Justify confidence scores
- Include appropriate caveats
- Maintain professional tone

### Validation Agent (Specific)
- Validate all outputs
- Check all policies
- Verify all statistics
- Flag all violations
- Provide specific feedback
- Ensure quality standards
