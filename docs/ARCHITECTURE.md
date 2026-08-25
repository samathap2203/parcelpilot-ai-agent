# Architecture Note — ParcelPilot AI Support Agent

## 1. Agent Design

ParcelPilot AI Support Agent is designed as a tool-using support workflow exposed through a Streamlit interface. The agent receives a natural-language support request and can use the appropriate tools to investigate the request using operational data and business documents.

The architecture separates agent orchestration from data access, document retrieval, reliability logic, and state-changing actions.

The main flow is:

**User → Streamlit Interface → ParcelPilot Agent → Tools / Retrieval / Reliability / Actions**

The agent supports multi-step investigation when a question requires information from more than one source. For example, a cancellation question may require looking up an order, identifying the associated account, checking the customer agreement, and applying the current cancellation policy before preparing an action.

## 2. Tool Design

The implementation provides separate tools for the major support operations:

* **Document Search Tool** — searches supplied policies, SOPs, product documentation, and customer agreements.
* **Operational Data Tool** — retrieves account and order information from the structured ParcelPilot data.
* **Action Tool** — prepares and executes supported state-changing actions such as cancellation.
* **Access Control** — checks whether the current support context is authorized to access an account.

State-changing actions are deliberately separated from read-only operations. A cancellation is first prepared as a pending action and requires explicit confirmation before execution. A pending action can also be cancelled before confirmation.

This follows the assessment requirement that consequential actions require explicit user confirmation.

## 3. Document and Structured-Data Handling

The supplied business documents are processed through a document-ingestion workflow. PDF content is split into searchable chunks and stored for document retrieval.

The structured ParcelPilot data is handled separately from document retrieval. Account and order information is loaded through the data layer and exposed through the operational-data tool.

This separation prevents the system from treating structured operational records and unstructured business documents as the same type of source.

The assessment data pack contains current and deprecated policies, cancellation/service-credit documentation, product documentation, customer agreements, and structured account, order, and ticket data.

## 4. Source Reliability and Conflict Handling

A key design decision is that sources are not treated as equally authoritative.

The implementation prioritizes:

**Customer Agreement → Current Policy / Applicable SOP → Historical Ticket Context**

Customer-specific agreements can override general ParcelPilot rules. Current policies and SOPs are preferred over deprecated material, while historical ticket resolutions are treated as supporting context rather than authoritative policy.

For example, the Northstar agreement explicitly allows cancellation of a BOOKED shipment without a cancellation fee, overriding the general rule for that customer.

Similarly, the LumenWorks agreement defines a customer-specific failed-pickup credit that replaces the default SOP threshold and amount.

This approach directly addresses the assessment's requirement to handle outdated documents, customer-specific overrides, conflicting information, and potentially incorrect historical ticket guidance.

## 5. Major Technical Trade-offs

### Rule-based reliability over unrestricted retrieval

I chose explicit source-priority rules instead of allowing retrieval similarity alone to determine which source is authoritative. This makes the behavior easier to reason about and safer for a support workflow where incorrect policy interpretation can affect customers.

### Local structured-data access

The assessment data is loaded locally through a dedicated data layer rather than introducing a production database. This keeps the assessment implementation simple and reproducible while still demonstrating the required structured-data workflow.

### Lightweight retrieval architecture

The document retrieval implementation uses local ingestion and search rather than introducing a production-scale vector database. This reduces deployment complexity while being sufficient for the supplied assessment document set.

### Confirmation before consequential actions

The action workflow intentionally adds an extra confirmation step. This slightly increases interaction time but reduces the risk of an accidental state change.

### Streamlit for the interface

Streamlit was selected because it provides a simple way to demonstrate the complete support workflow, including chat, document search, operational lookup, and confirmation-based actions without adding unnecessary frontend complexity.
