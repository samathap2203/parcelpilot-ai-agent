from dataclasses import dataclass
from typing import Optional, Set


@dataclass
class UserContext:
    """Represents the authenticated internal user."""

    user_id: str
    role: str
    allowed_accounts: Optional[Set[str]] = None


class AccessController:
    """
    Enforces account-level access before operational data
    is returned to the agent.
    """

    def __init__(self, user: UserContext):
        self.user = user

    def can_access_account(self, account_id: str) -> bool:
        """Check whether the current user can access an account."""

        # Administrators and operations managers can access
        # all operational accounts.
        if self.user.role in {"admin", "operations_manager"}:
            return True

        # Users without an account allow-list cannot access
        # account-specific information.
        if not self.user.allowed_accounts:
            return False

        return str(account_id) in {
            str(account) for account in self.user.allowed_accounts
        }

    def require_account_access(self, account_id: str) -> None:
        """
        Raise an error when the user is not authorized
        to access the requested account.
        """

        if not self.can_access_account(account_id):
            raise PermissionError(
                f"Access denied for account: {account_id}"
            )

    def can_access_role(self, required_role: str) -> bool:
        """Check whether the user has the required role."""

        role_hierarchy = {
            "support_agent": 1,
            "support_manager": 2,
            "operations_manager": 3,
            "admin": 4,
        }

        current_level = role_hierarchy.get(self.user.role, 0)
        required_level = role_hierarchy.get(required_role, 999)

        return current_level >= required_level