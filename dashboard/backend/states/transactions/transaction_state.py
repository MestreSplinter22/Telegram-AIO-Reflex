"""Transaction management state."""

import reflex as rx
from datetime import datetime
from ..models.base import Transaction


class TransactionState(rx.State):
    """Transaction management state."""
    
    # Transaction data
    transactions: list[Transaction] = []
    transactions_loading: bool = False
    
    # Filters
    transaction_type_filter: str = "all"
    transaction_status_filter: str = "all"
    transaction_date_filter: str = "all"
    transaction_search: str = ""
    
    # Selected transaction
    selected_transaction: Transaction | None = None
    
    async def load_transactions(self):
        """Load transactions from sample data."""
        self.transactions_loading = True
        yield
        
        # Sample data - replace with actual API calls
        self.transactions = [
            Transaction(
                id="txn_1",
                user_id="user_1",
                type="deposit",
                amount=100.00,
                status="completed",
                description="Depósito via PIX",
                pix_key="12345678900",
                pix_transaction_id="pix_123",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Transaction(
                id="txn_2",
                user_id="user_2",
                type="purchase",
                amount=50.00,
                status="completed",
                description="Compra de Gift Card Amazon",
                gift_card_id="gift_1",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        self.transactions_loading = False
    
    def get_filtered_transactions(self, user_id: str = None) -> list[Transaction]:
        """Get filtered transactions."""
        filtered = self.transactions
        
        if user_id:
            filtered = [txn for txn in filtered if txn.user_id == user_id]
        
        if self.transaction_type_filter != "all":
            filtered = [txn for txn in filtered if txn.type == self.transaction_type_filter]
        
        if self.transaction_status_filter != "all":
            filtered = [txn for txn in filtered if txn.status == self.transaction_status_filter]
        
        if self.transaction_search:
            search_lower = self.transaction_search.lower()
            filtered = [
                txn for txn in filtered
                if (search_lower in txn.description.lower() or
                    search_lower in txn.id.lower())
            ]
        
        return filtered
    
    @rx.var
    def filtered_transactions(self) -> list[Transaction]:
        """Get filtered transactions for current view."""
        return self.get_filtered_transactions()
    
    def set_selected_transaction(self, transaction: Transaction):
        """Set selected transaction for details view."""
        self.selected_transaction = transaction
    
    def clear_selected_transaction(self):
        """Clear selected transaction."""
        self.selected_transaction = None
    
    def set_transaction_search(self, value: str):
        """Set transaction search query."""
        self.transaction_search = value

    def set_transaction_type_filter(self, value: str):
        """Set transaction type filter."""
        self.transaction_type_filter = value

    def set_status_filter(self, value: str):
        """Set transaction status filter."""
        self.transaction_status_filter = value

    def set_date_range(self, value: str):
        """Set transaction date range filter."""
        self.transaction_date_filter = value

    @rx.var
    def total_transactions(self) -> int:
        """Get total number of transactions."""
        return len(self.transactions)

    @rx.var
    def total_revenue(self) -> float:
        """Get total revenue from transactions."""
        return sum(txn.amount for txn in self.transactions if txn.status == "completed")

    def update_transaction_status(self, transaction_id: str, new_status: str):
        """Update transaction status."""
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                transaction.status = new_status
                transaction.updated_at = datetime.now()
                yield rx.toast.success(f"Status da transação atualizado para {new_status}")
                break