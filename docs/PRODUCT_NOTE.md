# Product Note — ParcelPilot AI Support Agent

## 1. Additional Client Problem Chosen: Trust and Reliability

I chose **Trust and Reliability** as the additional ParcelPilot problem to address.

The assessment data intentionally contains outdated policies, customer-specific agreements that can override general rules, and historical ticket resolutions that may contain incorrect guidance. A support agent that simply retrieves the most similar document could therefore produce a confident but incorrect answer.

I addressed this by making source reliability an explicit part of the support workflow.

The system:

* Prioritizes customer-specific agreements when they contain applicable customer terms.
* Prefers current policies and applicable SOPs over deprecated policies.
* Treats historical ticket information as context rather than authoritative policy.
* Uses account-level access control before exposing customer information.
* Requires explicit confirmation before executing consequential actions.
* Separates action preparation from action execution.

This makes the system more deliberate when sources disagree and reduces the risk of incorrect answers or unintended actions.

## 2. What I Would Build Next for ParcelPilot

If development continued, I would prioritize the following:

### Proactive Issue Detection

I would build an internal operations dashboard that identifies recurring and urgent issues across support activity.

It could detect:

* Sudden increases in similar complaints.
* Multiple tickets associated with the same product issue.
* High-severity tickets approaching or exceeding SLA.
* Unusual patterns in orders or support activity.
* Issues affecting multiple customers.

This directly addresses ParcelPilot's second broader problem: moving from a purely reactive support assistant toward proactive operational intelligence.

### Production Authentication and Authorization

The current demonstration uses a controlled support context. A production system should integrate with ParcelPilot's identity and access-management system so that account and role permissions come from authenticated users rather than a demonstration context.

### Audit and Observability

I would add structured audit logs for tool calls, retrieved sources, decisions, confirmations, and executed actions. This would make the system easier to monitor and investigate.

### Evaluation and Monitoring

I would introduce a test set covering policy conflicts, customer-specific overrides, access-control failures, unsupported questions, and action-confirmation scenarios. Production monitoring could then track answer quality and escalation behavior over time.

## 3. What I Intentionally Left Out

I intentionally kept the submission focused on the core assessment workflow rather than attempting to build a complete production support platform.

The following were left out:

* Full enterprise authentication and identity management.
* Production-scale vector infrastructure.
* Production deployment infrastructure.
* Comprehensive audit and observability infrastructure.
* Automated proactive issue-detection dashboards.
* A large collection of production support actions.
* Extensive production-grade evaluation infrastructure.

The goal was to demonstrate the core agent, tool, retrieval, structured-data, reliability, access-control, and confirmation workflows clearly within the scope of the assessment.

The assessment explicitly allows candidates to make sensible technical and product trade-offs rather than requiring every production feature.

## 4. Product Usefulness Metric

The primary metric I would use is:

**Support Resolution Rate without Human Rework**

This measures the percentage of eligible support requests that the system resolves correctly without requiring a human agent to correct or redo the work.

I would track this together with safety signals such as incorrect answers, unauthorized data-access attempts, and unintended actions, because a high resolution rate is only valuable if the answers and actions are trustworthy.
