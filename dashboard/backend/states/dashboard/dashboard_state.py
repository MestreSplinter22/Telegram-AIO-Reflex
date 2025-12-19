"""Main dashboard state combining all metrics."""

import reflex as rx
from datetime import datetime
from ..models.base import BotMetrics


class DashboardState(rx.State):
    """Main dashboard state for overall metrics."""
    
    # Dashboard metrics
    total_revenue: float = 0.0
    total_profit: float = 0.0
    total_users: int = 0
    total_transactions: int = 0
    total_gift_cards_sold: int = 0
    
    # Bot metrics
    bot_metrics: list[BotMetrics] = []
    
    # Loading states
    dashboard_loading: bool = False
    
    # Date filters
    date_range: str = "today"
    custom_start_date: str = ""
    custom_end_date: str = ""
    
    async def load_dashboard_data(self):
        """Load all dashboard data."""
        self.dashboard_loading = True
        yield
        
        # Load sample data - replace with actual API calls
        self.total_revenue = 1250.75
        self.total_profit = 187.50
        self.total_users = 45
        self.total_transactions = 128
        self.total_gift_cards_sold = 89
        
        # Sample bot metrics
        self.bot_metrics = [
            BotMetrics(
                id="metrics_1",
                date=datetime.now(),
                active_users=12,
                total_messages=156,
                commands_executed=89,
                response_time_avg=1.2,
                uptime_percentage=99.8,
                errors_count=2
            )
        ]
        
        self.dashboard_loading = False
    
    def refresh_dashboard(self):
        """Refresh all dashboard data."""
        return self.load_dashboard_data()
    
    @rx.var
    def daily_revenue(self) -> float:
        """Get daily revenue."""
        return self.total_revenue / 30  # Simplified calculation
    
    @rx.var
    def daily_profit(self) -> float:
        """Get daily profit."""
        return self.total_profit / 30  # Simplified calculation
    
    @rx.var
    def conversion_rate(self) -> float:
        """Get conversion rate (transactions/users)."""
        if self.total_users > 0:
            return (self.total_transactions / self.total_users) * 100
        return 0.0
    
    @rx.var
    def average_order_value(self) -> float:
        """Get average order value."""
        if self.total_transactions > 0:
            return self.total_revenue / self.total_transactions
        return 0.0