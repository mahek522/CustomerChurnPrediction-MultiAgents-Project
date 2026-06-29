# PII (Personally Identifiable Information) Policy

## Purpose
Protect customer privacy by preventing exposure of personally identifiable information in AI responses.

## PII Definition
Personally Identifiable Information includes:
- Full names
- Email addresses
- Phone numbers
- Social Security Numbers (SSN)
- Credit card numbers
- Bank account numbers
- Physical addresses
- Dates of birth
- Government IDs

## Data Handling Rules

### 1. Data Ingestion
- PII is stored in secure PostgreSQL database
- Access requires authentication
- Data is encrypted at rest
- Audit logs track all access

### 2. Data Retrieval
- Only retrieve necessary customer attributes
- Mask sensitive identifiers in responses
- Use customer IDs instead of names
- Limit exposed information to business-relevant fields

### 3. Response Generation
- Never include full names in responses
- Never include contact information
- Never include government IDs
- Use anonymized identifiers (e.g., "Customer 123")
- Aggregate data when possible

### 4. Output Validation
- Output guardrails scan for PII patterns
- Detected PII triggers response rejection
- Sensitive data is automatically redacted
- Validation agent checks for PII leakage

## Allowed Data

### Business-Relevant Attributes (Safe to Share)
- Customer ID (anonymized)
- Age (not DOB)
- Tenure (months)
- Monthly charges
- Contract type
- Internet service type
- Support ticket count
- Churn status (0/1)
- Risk category

### Sensitive Attributes (Never Share)
- Full name
- Email address
- Phone number
- SSN
- Credit card number
- Bank account
- Full address
- DOB
- Government ID

## Redaction Rules

### Automatic Redaction
The system automatically redacts:
- Email addresses: `***@***.***`
- Phone numbers: `***-***-****`
- SSN: `***-**-****`
- Credit card: `****-****-****-****`

### Manual Redaction
Agents must manually redact:
- Names: Use "Customer {ID}"
- Addresses: Use "Location {Region}"
- DOB: Use "Age: {years}"

## Enforcement

### Input Guardrails
- Block queries requesting PII
- Flag attempts to extract personal data
- Reject bulk data export requests

### Output Guardrails
- Scan responses for PII patterns
- Redact detected PII automatically
- Reject responses with unredacted PII
- Log PII detection incidents

### Validation Agent
- Check all outputs for PII
- Verify redaction completeness
- Ensure anonymization consistency
- Flag potential PII leakage

## Compliance

### GDPR Compliance
- Data minimization: Only collect necessary data
- Purpose limitation: Use data only for stated purposes
- Storage limitation: Retain data only as needed
- Right to erasure: Support data deletion requests

### Data Protection
- Encryption at rest
- Encryption in transit
- Access controls
- Audit logging
- Regular security reviews

## Incident Response

### PII Exposure Detected
1. Immediately stop response generation
2. Log incident with details
3. Notify security team
4. Review and fix guardrail rules
5. Retrain affected agents
6. Audit similar responses

### Prevention Measures
- Regular PII pattern updates
- Enhanced validation rules
- Agent prompt improvements
- Continuous monitoring
- User feedback integration
