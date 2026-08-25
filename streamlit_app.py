import streamlit as st

from app.agent.agent import ParcelPilotAgent
from app.data.access_control import UserContext


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="ParcelPilot AI Support Agent",
    page_icon="📦",
    layout="wide",
)


# ---------------------------------------------------------
# Agent creation
# ---------------------------------------------------------

def create_agent() -> ParcelPilotAgent:
    """Create the demo internal support-agent context."""

    user = UserContext(
        user_id="user-001",
        role="support_agent",
        allowed_accounts={"ACCT-001"},
    )

    return ParcelPilotAgent(user)


if "agent" not in st.session_state:
    st.session_state.agent = create_agent()

agent = st.session_state.agent


# ---------------------------------------------------------
# Helper: natural-language request handler
# ---------------------------------------------------------

def handle_chat_request(query: str):
    """
    Handle common ParcelPilot support requests using the
    existing local tools.

    This provides a natural-language workflow even when
    the external LLM is unavailable.
    """

    text = query.lower().strip()

    # -----------------------------------------------------
    # Cancellation / fee workflow
    # -----------------------------------------------------

    if (
        "cancel" in text
        and ("fee" in text or "cancellation" in text)
        and ("ord-" in text or "order" in text)
    ):
        # Find order ID
        order_id = None

        for word in query.replace(",", " ").replace("?", " ").split():
            cleaned = word.strip(".,!?()")
            if cleaned.upper().startswith("ORD-"):
                order_id = cleaned.upper()
                break

        if not order_id:
            return {
                "status": "needs_information",
                "message": (
                    "I can check the cancellation policy, but I need "
                    "the Order ID, for example ORD-1001."
                ),
            }

        try:
            # Step 1: structured operational lookup
            order = agent.get_order(order_id)

            # Step 2: identify account
            account_id = None

            if isinstance(order, dict):
                if "account_id" in order:
                    account_id = order["account_id"]

                elif "records" in order and order["records"]:
                    first_record = order["records"][0]
                    if isinstance(first_record, dict):
                        account_id = first_record.get("account_id")

            # Step 3: account lookup if available
            account = None

            if account_id:
                try:
                    account = agent.get_account(account_id)
                except PermissionError:
                    account = None

            # Step 4: document retrieval
            documents = agent.search_documents(
                "cancellation fee",
                top_k=5,
            )

            return {
                "status": "completed",
                "message": (
                    f"I investigated {order_id} using the available "
                    "operational data and cancellation documentation."
                ),
                "order": order,
                "account": account,
                "documents": documents,
            }

        except PermissionError as exc:
            return {
                "status": "access_denied",
                "message": str(exc),
            }

        except Exception as exc:
            return {
                "status": "error",
                "message": f"Unable to complete the request: {exc}",
            }

    # -----------------------------------------------------
    # Document / policy questions
    # -----------------------------------------------------

    if any(
        keyword in text
        for keyword in [
            "policy",
            "sop",
            "agreement",
            "fee",
            "service credit",
            "sla",
            "cancellation",
            "contract",
        ]
    ):
        try:
            result = agent.search_documents(query, top_k=5)

            return {
                "status": "completed",
                "message": (
                    f"I searched the ParcelPilot document sources "
                    f"for: {query}"
                ),
                "documents": result,
            }

        except Exception as exc:
            return {
                "status": "error",
                "message": f"Document search failed: {exc}",
            }

    # -----------------------------------------------------
    # Order lookup
    # -----------------------------------------------------

    if "ord-" in text or "order" in text:
        order_id = None

        for word in query.replace(",", " ").replace("?", " ").split():
            cleaned = word.strip(".,!?()")
            if cleaned.upper().startswith("ORD-"):
                order_id = cleaned.upper()
                break

        if not order_id:
            return {
                "status": "needs_information",
                "message": (
                    "Please provide an Order ID, for example ORD-1001."
                ),
            }

        try:
            result = agent.get_order(order_id)

            return {
                "status": "completed",
                "message": f"Operational data found for {order_id}.",
                "order": result,
            }

        except PermissionError as exc:
            return {
                "status": "access_denied",
                "message": str(exc),
            }

        except Exception as exc:
            return {
                "status": "error",
                "message": f"Unable to retrieve the order: {exc}",
            }

    # -----------------------------------------------------
    # Account lookup
    # -----------------------------------------------------

    if "acct-" in text or "account" in text:
        account_id = None

        for word in query.replace(",", " ").replace("?", " ").split():
            cleaned = word.strip(".,!?()")
            if cleaned.upper().startswith("ACCT-"):
                account_id = cleaned.upper()
                break

        if not account_id:
            return {
                "status": "needs_information",
                "message": (
                    "Please provide an Account ID, for example ACCT-001."
                ),
            }

        try:
            result = agent.get_account(account_id)

            return {
                "status": "completed",
                "message": f"Account information found for {account_id}.",
                "account": result,
            }

        except PermissionError as exc:
            return {
                "status": "access_denied",
                "message": str(exc),
            }

        except Exception as exc:
            return {
                "status": "error",
                "message": f"Unable to retrieve the account: {exc}",
            }

    # -----------------------------------------------------
    # Unknown request
    # -----------------------------------------------------

    return {
        "status": "needs_information",
        "message": (
            "I could not confidently determine which ParcelPilot "
            "workflow is required. Try asking about an order, "
            "account, cancellation, policy, service credit, SLA, "
            "or agreement."
        ),
    }


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("📦 ParcelPilot AI Support Agent")

st.caption(
    "AI-assisted support workflow with access control, "
    "document retrieval, reliability checks, and "
    "confirmation-based actions."
)


# ---------------------------------------------------------
# Sidebar status
# ---------------------------------------------------------

st.sidebar.header("System Status")

status = agent.health_check()

for component, state in status.items():
    st.sidebar.write(
        f"**{component.replace('_', ' ').title()}:** {state}"
    )


# ---------------------------------------------------------
# Natural-language chatbot
# ---------------------------------------------------------

st.divider()

st.subheader("💬 ParcelPilot Support Chat")

st.write(
    "Ask a natural-language support question. "
    "The system routes the request to the appropriate "
    "operational-data or document-retrieval workflow."
)

chat_query = st.text_area(
    "Your request",
    placeholder=(
        "Example: Can Northstar cancel ORD-1001 "
        "without a cancellation fee? Explain why."
    ),
    height=100,
)

if st.button("Send Request", type="primary"):

    if not chat_query.strip():
        st.warning("Please enter a request.")

    else:
        result = handle_chat_request(chat_query)

        if result["status"] == "completed":
            st.success(result["message"])

        elif result["status"] == "access_denied":
            st.error(result["message"])

        elif result["status"] == "needs_information":
            st.warning(result["message"])

        else:
            st.error(result["message"])

        # Show workflow evidence
        if "order" in result and result["order"] is not None:
            st.markdown("#### 📋 Operational Data")
            st.json(result["order"])

        if "account" in result and result["account"] is not None:
            st.markdown("#### 👤 Account Data")
            st.json(result["account"])

        if "documents" in result and result["documents"] is not None:
            st.markdown("#### 📚 Retrieved Documents")

            document_result = result["documents"]

            if document_result.get("result_count", 0) == 0:
                st.info("No relevant documents were found.")

            else:
                for item in document_result["results"]:
                    with st.expander(
                        f"{item['document']} — score {item['score']}"
                    ):
                        st.write(item["text"])


# ---------------------------------------------------------
# Document search
# ---------------------------------------------------------

st.divider()

st.subheader("🔎 Search ParcelPilot Documents")

query = st.text_input(
    "Enter a question or search phrase",
    placeholder="Example: cancellation fee",
)

if st.button("Search Documents"):

    if not query.strip():
        st.warning("Please enter a search query.")

    else:
        result = agent.search_documents(
            query,
            top_k=5,
        )

        if result["result_count"] == 0:
            st.info("No relevant documents were found.")

        else:
            st.success(
                f"Found {result['result_count']} relevant document(s)."
            )

            for item in result["results"]:
                with st.expander(
                    f"{item['document']} — score {item['score']}"
                ):
                    st.write(item["text"])


# ---------------------------------------------------------
# Operational Data
# ---------------------------------------------------------

st.divider()

st.subheader("📋 Operational Data")

order_id = st.text_input(
    "Order ID",
    placeholder="Example: ORD-1001",
)

if st.button("Get Order"):

    if not order_id.strip():
        st.warning("Please enter an order ID.")

    else:
        try:
            result = agent.get_order(order_id.strip())
            st.json(result)

        except PermissionError as exc:
            st.error(str(exc))

        except Exception as exc:
            st.error(
                f"Unable to retrieve order: {exc}"
            )


account_id = st.text_input(
    "Account ID",
    placeholder="Example: ACCT-001",
)

if st.button("Get Account"):

    if not account_id.strip():
        st.warning("Please enter an account ID.")

    else:
        try:
            result = agent.get_account(account_id.strip())
            st.json(result)

        except PermissionError as exc:
            st.error(str(exc))

        except Exception as exc:
            st.error(
                f"Unable to retrieve account: {exc}"
            )


# ---------------------------------------------------------
# Confirmation-Based Actions
# ---------------------------------------------------------

st.divider()

st.subheader("⚠️ Confirmation-Based Actions")

st.write(
    "Actions are prepared first and require explicit "
    "confirmation before execution."
)

action_target = st.text_input(
    "Action target",
    placeholder="Example: ORD-1001",
)

action_reason = st.text_input(
    "Reason",
    placeholder="Example: Customer requested cancellation",
)

col1, col2 = st.columns(2)

with col1:

    if st.button("Prepare Cancellation"):

        if not action_target.strip():
            st.warning("Enter an action target.")

        else:
            result = agent.prepare_action(
                action_type="cancel_order",
                target_id=action_target.strip(),
                details={
                    "reason": action_reason.strip(),
                },
            )

            st.warning(result["message"])
            st.json(result)


with col2:

    if st.button("Confirm Pending Action"):

        result = agent.confirm_action()

        if result["status"] == "executed":
            st.success(result["message"])

        else:
            st.info(result["message"])

        st.json(result)


if st.button("Cancel Pending Action"):

    result = agent.cancel_action()

    st.info(result["message"])
    st.json(result)


# ---------------------------------------------------------
# LLM status
# ---------------------------------------------------------

st.divider()

if status.get("llm") == "not_connected":

    st.info(
        "LLM connection is currently disabled because the "
        "API account has no remaining credits. The local "
        "retrieval, access-control, reliability, and "
        "confirmation workflows remain available for "
        "demonstration."
    )

else:

    st.success(
        "LLM connection is available."
    )