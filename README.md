# 📦 ParcelPilot AI Support Agent

ParcelPilot AI Support Agent is an AI-assisted customer support workflow designed to help support teams investigate customer requests using operational data and business documents.

The system combines operational-data access, document retrieval, access control, source-priority rules, reliability checks, and confirmation-based actions in a Streamlit interface.

> **Note:** The LLM integration is implemented and configured, but live LLM requests are currently disabled because the API account used during development has no remaining credits. The operational-data, document-retrieval, access-control, reliability, and confirmation workflows remain fully demonstrable.

---

## 🚀 Project Overview

ParcelPilot provides a support-agent workflow for handling parcel and order-related customer requests.

The application allows a support agent to:

- Search ParcelPilot business documents
- Retrieve order information
- Retrieve customer account information
- Enforce account-level access control
- Prioritize authoritative sources
- Prepare cancellation actions
- Require explicit confirmation before executing actions
- Cancel pending actions
- Monitor system component status
- Interact with the workflow through a Streamlit web interface

The project is designed with a focus on **reliable and controlled AI-assisted support operations**.

---

## ✨ Key Features

### 🔎 Document Retrieval

The system ingests PDF documents and creates searchable document chunks.

Users can search for topics such as:

- Cancellation fees
- Service credits
- Customer agreements
- Support policies
- Cancellation procedures

The retrieval workflow returns relevant documents together with relevance scores.

---

### 📋 Operational Data Access

The application provides access to operational data stored in the supplied ParcelPilot assessment dataset.

Supported operations include:

- Order lookup
- Account lookup

Example identifiers include:

```text
ORD-1001
ACCT-001
🔐 Access Control

Account-level access control is implemented to prevent unauthorized access to customer account information.

For example, a support user assigned to:

ACCT-001

can access that account but is denied access to:

ACCT-002

Unauthorized access raises a PermissionError.

🧭 Source Priority and Reliability

The system includes source-priority logic to help ensure that more authoritative sources are preferred over less authoritative sources.

The implemented source priority is:

Customer Agreement
        ↓
Current Policy
        ↓
Historical Ticket

This helps the support workflow prioritize customer-specific contractual information and current policies over historical information when resolving support questions.

⚠️ Confirmation-Based Actions

Potentially consequential actions are not executed immediately.

For example, cancelling an order follows this workflow:

Prepare Cancellation
        ↓
Confirmation Required
        ↓
Explicit Confirmation
        ↓
Action Executed

A pending action can also be cancelled before confirmation.

This design prevents accidental execution of consequential support actions.

💬 Streamlit Support Interface

The project includes a Streamlit-based interface for demonstrating the support workflow.

The interface provides:

System status
ParcelPilot support chat
Document search
Operational data lookup
Account lookup
Confirmation-based cancellation actions
LLM connection status
🏗️ Architecture

The project is organized into separate modules for data access, retrieval, tools, reliability, and agent orchestration.

User
 │
 ▼
Streamlit Application
 │
 ▼
ParcelPilot Agent
 │
 ├── Operational Data
 │     ├── Orders
 │     └── Accounts
 │
 ├── Document Retrieval
 │     ├── Document Ingestion
 │     └── Document Search
 │
 ├── Access Control
 │
 ├── Reliability / Source Priority
 │
 ├── Confirmation-Based Actions
 │
 └── LLM Integration
📁 Project Structure
parcelpilot-ai-agent/
│
├── app/
│   ├── agent/
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── access_control.py
│   │   └── loader.py
│   │
│   ├── reliability/
│   │   └── __init__.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   └── store.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── actions.py
│   │   ├── document_search.py
│   │   └── operational_data.py
│   │
│   ├── __init__.py
│   └── config.py
│
├── data/
│   └── ParcelPilot assessment data
│
├── docs/
│   └── Supporting business documents
│
├── scripts/
│   └── ingest_documents.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── streamlit_app.py
└── README.md
🛠️ Technologies Used
Python
Streamlit
Pandas
OpenPyXL
OpenAI API
PyPDF
Python-dotenv
JSON-based data processing
PDF document retrieval
Rule-based access control
Source-priority and reliability logic
💻 Requirements

Before running the project, make sure Python is installed.

The project was developed and tested using:

Python 3.13.2

A virtual environment is recommended.

⚙️ Installation
1. Clone or download the project

Place the project in a local directory.

Example:

C:\Users\<username>\OneDrive\Desktop\parcelpilot-ai-agent
2. Open the project directory

Open Command Prompt or the VS Code terminal inside the project directory.

Example:

cd C:\Users\<username>\OneDrive\Desktop\parcelpilot-ai-agent
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment

On Windows:

.venv\Scripts\activate

After activation, the terminal should show:

(.venv)
5. Install dependencies
pip install -r requirements.txt
6. Configure environment variables

Create a local .env file based on .env.example.

Example:

OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4.1-mini

Do not commit or share the .env file.

The API key must remain private.

📄 Document Ingestion

The project includes a document-ingestion workflow for processing the supplied business documents.

To run document ingestion:

python scripts/ingest_documents.py

The retrieval system can then be used to search the processed documents.

▶️ Running the Application

Activate the virtual environment:

.venv\Scripts\activate

Then start Streamlit:

streamlit run streamlit_app.py

Streamlit will provide a local address similar to:

http://localhost:8501

Open that address in a web browser.

🧪 Testing the Application
Document Search

Enter a query such as:

cancellation fee

The application should return relevant documents.

Example documents returned during testing included:

03_Cancellation_and_Service_Credit_SOP_v4.pdf
05_Northstar_Logistics_Enterprise_Agreement.pdf
06_LumenWorks_Service_Agreement.pdf
Operational Data Test

Use:

ORD-1001

to retrieve order information.

For account access, use:

ACCT-001
Access-Control Test

A user with access to:

ACCT-001

should be able to retrieve:

ACCT-001

but should receive an access-denied error when attempting to retrieve:

ACCT-002

This verifies account-level authorization.

Confirmation-Based Action Test

Use:

Action target:
ORD-1001

Reason:
Customer requested cancellation

Click:

Prepare Cancellation

The system should display:

This action has not been executed. Please confirm before proceeding.

Then click:

Confirm Pending Action

The action should return:

status: executed

A pending action can also be cancelled using:

Cancel Pending Action
🔒 Security Considerations

The project uses environment variables for sensitive API credentials.

The following files and directories should not be committed:

.env
.venv/
__pycache__/
*.pyc
.streamlit/

These are included in .gitignore.

Never place an API key directly inside Python source code.

⚠️ Current Limitations
LLM API Availability

The LLM integration is configured in the project, but live API requests cannot currently be demonstrated because the API account used during development has no remaining credits.

The application therefore reports:

LLM: not_connected

The following workflows remain available:

Operational data
Document retrieval
Access control
Reliability/source priority
Confirmation-based actions
Streamlit interface
Retrieval Approach

The current document retrieval workflow is designed for the supplied assessment documents and uses the implemented document ingestion and search logic.

It is not intended to replace a production-grade enterprise vector database.

Demo Access Context

The Streamlit application currently creates a demonstration support-agent context with access to:

ACCT-001

A production implementation would obtain authenticated user identity and authorization information from an enterprise identity and access-management system.

🔮 Future Improvements

Potential future improvements include:

Connect the application to a production LLM service
Add authentication and role-based authorization
Replace demonstration access context with enterprise identity management
Add a production vector database
Improve semantic document retrieval
Add conversation history
Add structured audit logging
Add more operational actions
Add automated evaluation tests
Add monitoring and observability
Add deployment configuration for cloud hosting
Add more comprehensive unit and integration tests
📊 Validation Performed

The project was tested for the following workflows:

✓ Python environment
✓ Virtual environment
✓ Dependency installation
✓ Excel dataset loading
✓ Document ingestion
✓ Document search
✓ Account access control
✓ Unauthorized account access rejection
✓ Source-priority ranking
✓ Action preparation
✓ Confirmation-required behavior
✓ Action confirmation
✓ Pending-action cancellation
✓ Streamlit application
✓ Operational data lookup
✓ Account lookup
✓ Support workflow interface
📌 Important Submission Note

The .env file contains a private API credential and must not be shared with the assessment evaluator or uploaded to GitHub.

Share the project source code and configuration template instead:

.env.example

The evaluator can configure their own API credentials if required.

👤 Author

Samatha P

ParcelPilot AI Support Agent — Assessment Project