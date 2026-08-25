from typing import Any, Dict

from app.data.access_control import AccessController, UserContext
from app.data.loader import ParcelPilotData


class OperationalDataTool:
    """Controlled interface to ParcelPilot operational data."""

    def __init__(self, user: UserContext):
        self.data = ParcelPilotData()
        self.access = AccessController(user)

    @staticmethod
    def _records(df) -> list[Dict[str, Any]]:
        """Convert a DataFrame into JSON-friendly records."""
        return df.where(df.notna(), None).to_dict(orient="records")

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get an account after authorization."""
        self.access.require_account_access(account_id)

        result = self.data.get_account(account_id)

        return {
            "account_id": account_id,
            "records": self._records(result),
        }

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get an order.

        Authorization is performed using the account_id
        associated with the order.
        """
        result = self.data.get_order(order_id)

        if result.empty:
            return {
                "order_id": order_id,
                "records": [],
            }

        account_id = str(result.iloc[0]["account_id"])

        self.access.require_account_access(account_id)

        return {
            "order_id": order_id,
            "records": self._records(result),
        }

    def get_orders_for_account(self, account_id: str) -> Dict[str, Any]:
        """Get all orders for an authorized account."""
        self.access.require_account_access(account_id)

        result = self.data.get_orders_for_account(account_id)

        return {
            "account_id": account_id,
            "records": self._records(result),
        }

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Get a ticket after checking its associated account."""
        result = self.data.get_ticket(ticket_id)

        if result.empty:
            return {
                "ticket_id": ticket_id,
                "records": [],
            }

        account_id = str(result.iloc[0]["account_id"])

        self.access.require_account_access(account_id)

        return {
            "ticket_id": ticket_id,
            "records": self._records(result),
        }

    def get_tickets_for_account(self, account_id: str) -> Dict[str, Any]:
        """Get all tickets for an authorized account."""
        self.access.require_account_access(account_id)

        result = self.data.get_tickets_for_account(account_id)

        return {
            "account_id": account_id,
            "records": self._records(result),
        }

    def search_accounts(self, query: str) -> Dict[str, Any]:
        """
        Search accounts.

        Only return accounts the current user is authorized
        to access.
        """
        results = self.data.search_accounts(query)

        authorized_records = []

        for _, row in results.iterrows():
            account_id = str(row["account_id"])

            if self.access.can_access_account(account_id):
                authorized_records.append(
                    row.where(row.notna(), None).to_dict()
                )

        return {
            "query": query,
            "records": authorized_records,
        }

    def search_orders(self, query: str) -> Dict[str, Any]:
        """
        Search orders while enforcing account-level access.
        """
        results = self.data.search_orders(query)

        authorized_records = []

        for _, row in results.iterrows():
            account_id = str(row["account_id"])

            if self.access.can_access_account(account_id):
                authorized_records.append(
                    row.where(row.notna(), None).to_dict()
                )

        return {
            "query": query,
            "records": authorized_records,
        }

    def search_tickets(self, query: str) -> Dict[str, Any]:
        """
        Search tickets while enforcing account-level access.
        """
        results = self.data.search_tickets(query)

        authorized_records = []

        for _, row in results.iterrows():
            account_id = str(row["account_id"])

            if self.access.can_access_account(account_id):
                authorized_records.append(
                    row.where(row.notna(), None).to_dict()
                )

        return {
            "query": query,
            "records": authorized_records,
        }