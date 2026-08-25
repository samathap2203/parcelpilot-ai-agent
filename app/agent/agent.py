from typing import Any, Dict

from app.data.access_control import UserContext
from app.reliability.conflict_handler import detect_conflict
from app.tools.actions import ActionTool
from app.tools.document_search import DocumentSearchTool
from app.tools.operational_data import OperationalDataTool


class ParcelPilotAgent:
    """
    Core orchestration layer for the ParcelPilot support agent.

    The agent coordinates:
    - operational data
    - document retrieval
    - source/conflict handling
    - confirmation-based actions

    The actual LLM call is intentionally kept separate so the
    application can be developed and tested without API credits.
    """

    def __init__(self, user: UserContext):
        self.user = user

        self.operational_data = OperationalDataTool(user)
        self.document_search = DocumentSearchTool()
        self.actions = ActionTool()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Retrieve an order through the protected operational tool."""

        return self.operational_data.get_order(order_id)

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Retrieve an authorized account."""

        return self.operational_data.get_account(account_id)

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Retrieve an authorized support ticket."""

        return self.operational_data.get_ticket(ticket_id)

    def search_documents(
        self,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Search ParcelPilot documents."""

        return self.document_search.search(
            query=query,
            top_k=top_k,
        )

    def analyze_sources(
        self,
        sources: list[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze retrieved sources for authority and conflicts.
        """

        return detect_conflict(sources)

    def prepare_action(
        self,
        action_type: str,
        target_id: str,
        details: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Prepare an action.

        Nothing is executed until explicit confirmation.
        """

        return self.actions.prepare_action(
            action_type=action_type,
            target_id=target_id,
            details=details,
        )

    def confirm_action(self) -> Dict[str, Any]:
        """Execute the currently pending confirmed action."""

        return self.actions.confirm_action()

    def cancel_action(self) -> Dict[str, Any]:
        """Cancel the currently pending action."""

        return self.actions.cancel_pending_action()

    def health_check(self) -> Dict[str, Any]:
        """Return the status of the agent's internal components."""

        return {
            "agent": "ready",
            "operational_data": "ready",
            "document_search": "ready",
            "reliability": "ready",
            "actions": "ready",
            "llm": "not_connected",
        }