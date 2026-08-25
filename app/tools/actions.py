from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PendingAction:
    """An action waiting for explicit user confirmation."""

    action_type: str
    target_id: str
    details: Dict[str, Any]
    confirmed: bool = False


class ActionTool:
    """
    Handles operational actions using a confirmation-first workflow.

    This demo implementation does not directly modify the supplied
    assessment workbook.
    """

    def __init__(self):
        self.pending_action: Optional[PendingAction] = None

    def prepare_action(
        self,
        action_type: str,
        target_id: str,
        details: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Prepare an action without executing it.
        """

        self.pending_action = PendingAction(
            action_type=action_type,
            target_id=target_id,
            details=details,
        )

        return {
            "status": "confirmation_required",
            "action_type": action_type,
            "target_id": target_id,
            "details": details,
            "message": (
                "This action has not been executed. "
                "Please confirm before proceeding."
            ),
        }

    def confirm_action(self) -> Dict[str, Any]:
        """
        Execute the pending action only after explicit confirmation.
        """

        if self.pending_action is None:
            return {
                "status": "no_pending_action",
                "message": "There is no action waiting for confirmation.",
            }

        self.pending_action.confirmed = True

        action = self.pending_action

        self.pending_action = None

        return {
            "status": "executed",
            "action_type": action.action_type,
            "target_id": action.target_id,
            "details": action.details,
            "message": "The confirmed action has been executed.",
        }

    def cancel_pending_action(self) -> Dict[str, Any]:
        """Cancel an action that is waiting for confirmation."""

        if self.pending_action is None:
            return {
                "status": "no_pending_action",
                "message": "There is no pending action.",
            }

        target_id = self.pending_action.target_id
        action_type = self.pending_action.action_type

        self.pending_action = None

        return {
            "status": "cancelled",
            "action_type": action_type,
            "target_id": target_id,
            "message": "The pending action was cancelled.",
        }