from pathlib import Path
from typing import Dict

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "ParcelPilot_Assessment_Data.xlsx"

EXPECTED_SHEETS = {"README", "accounts", "orders", "tickets"}


class ParcelPilotData:
    """Loads and provides controlled access to ParcelPilot operational data."""

    def __init__(self, file_path: Path = DATA_FILE):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"ParcelPilot data file not found: {self.file_path}"
            )

        self._load_data()

    def _load_data(self) -> None:
        workbook = pd.ExcelFile(self.file_path)

        missing_sheets = EXPECTED_SHEETS - set(workbook.sheet_names)

        if missing_sheets:
            raise ValueError(
                f"Missing expected sheets: {sorted(missing_sheets)}"
            )

        self.readme = pd.read_excel(workbook, sheet_name="README")
        self.accounts = pd.read_excel(workbook, sheet_name="accounts")
        self.orders = pd.read_excel(workbook, sheet_name="orders")
        self.tickets = pd.read_excel(workbook, sheet_name="tickets")

    def get_account(self, account_id: str) -> pd.DataFrame:
        """Return account information for a specific account."""
        return self.accounts[
            self.accounts["account_id"].astype(str) == str(account_id)
        ].copy()

    def get_order(self, order_id: str) -> pd.DataFrame:
        """Return order information for a specific order."""
        return self.orders[
            self.orders["order_id"].astype(str) == str(order_id)
        ].copy()

    def get_orders_for_account(self, account_id: str) -> pd.DataFrame:
        """Return orders belonging to a specific account."""
        return self.orders[
            self.orders["account_id"].astype(str) == str(account_id)
        ].copy()

    def get_ticket(self, ticket_id: str) -> pd.DataFrame:
        """Return ticket information for a specific ticket."""
        return self.tickets[
            self.tickets["ticket_id"].astype(str) == str(ticket_id)
        ].copy()

    def get_tickets_for_account(self, account_id: str) -> pd.DataFrame:
        """Return tickets belonging to a specific account."""
        return self.tickets[
            self.tickets["account_id"].astype(str) == str(account_id)
        ].copy()

    def search_accounts(self, query: str) -> pd.DataFrame:
        """Search account names and IDs."""
        query = str(query).lower()

        mask = (
            self.accounts["account_id"]
            .astype(str)
            .str.lower()
            .str.contains(query, na=False)
            | self.accounts["customer_name"]
            .astype(str)
            .str.lower()
            .str.contains(query, na=False)
        )

        return self.accounts[mask].copy()

    def search_orders(self, query: str) -> pd.DataFrame:
        """Search order IDs, account IDs, carriers, and statuses."""
        query = str(query).lower()

        searchable_columns = [
            "order_id",
            "account_id",
            "carrier",
            "status",
        ]

        mask = pd.Series(False, index=self.orders.index)

        for column in searchable_columns:
            if column in self.orders.columns:
                mask |= (
                    self.orders[column]
                    .astype(str)
                    .str.lower()
                    .str.contains(query, na=False)
                )

        return self.orders[mask].copy()

    def search_tickets(self, query: str) -> pd.DataFrame:
        """Search ticket IDs, account IDs, subjects, and status."""
        query = str(query).lower()

        searchable_columns = [
            "ticket_id",
            "account_id",
            "subject",
            "status",
        ]

        mask = pd.Series(False, index=self.tickets.index)

        for column in searchable_columns:
            if column in self.tickets.columns:
                mask |= (
                    self.tickets[column]
                    .astype(str)
                    .str.lower()
                    .str.contains(query, na=False)
                )

        return self.tickets[mask].copy()

    def summary(self) -> Dict[str, int]:
        """Return basic dataset counts."""
        return {
            "accounts": len(self.accounts),
            "orders": len(self.orders),
            "tickets": len(self.tickets),
        }