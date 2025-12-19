"""User management state."""

import reflex as rx
from datetime import datetime
from ..models.base import User


class UserState(rx.State):
    """User management state."""
    
    # User data
    users: list[User] = []
    users_loading: bool = False
    
    # Selected user for details
    selected_user: User | None = None
    user_transactions: list = []
    
    # Filters
    user_search: str = ""
    user_status_filter: str = "all"
    
    async def load_users(self):
        """Load users from sample data."""
        self.users_loading = True
        yield
        
        # Sample data - replace with actual API calls
        self.users = [
            User(
                id="user_1",
                telegram_id="123456789",
                username="@user1",
                name="João Silva",
                email="joao@example.com",
                balance=150.50,
                total_spent=500.00,
                total_orders=15,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                status="active",
                risk_score=5.0
            ),
            User(
                id="user_2",
                telegram_id="987654321",
                username="@user2",
                name="Maria Santos",
                email="maria@example.com",
                balance=75.25,
                total_spent=200.00,
                total_orders=8,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                status="active",
                risk_score=2.5
            )
        ]
        self.users_loading = False
    
    def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def set_selected_user(self, user: User):
        """Set selected user for details view."""
        self.selected_user = user
    
    def clear_selected_user(self):
        """Clear selected user."""
        self.selected_user = None
    
    @rx.var
    def filtered_users(self) -> list[User]:
        """Get filtered users based on search and status."""
        filtered = self.users
        
        if self.user_search:
            search_lower = self.user_search.lower()
            filtered = [
                user for user in filtered
                if (search_lower in user.name.lower() or
                    search_lower in user.username.lower() or
                    search_lower in user.email.lower())
            ]
        
        if self.user_status_filter != "all":
            filtered = [
                user for user in filtered
                if user.status == self.user_status_filter
            ]
        
        return filtered
    
    def set_user_search(self, value: str):
        """Set user search query."""
        self.user_search = value

    def set_user_status_filter(self, value: str):
        """Set user status filter."""
        self.user_status_filter = value

    def update_user_status(self, user_id: str, new_status: str):
        """Update user status."""
        for user in self.users:
            if user.id == user_id:
                user.status = new_status
                yield rx.toast.success(f"Status do usuário atualizado para {new_status}")
                break