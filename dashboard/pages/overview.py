"""Main overview page for gift card dashboard."""

import reflex as rx
from ..components.ui.card import card
from ..components.notification import notification
from ..backend.states.dashboard import DashboardState
from ..templates import template
from ..views.overview.dashboard_stats import dashboard_stats
from ..views.overview.revenue_chart import revenue_chart
from ..views.overview.recent_transactions import recent_transactions
from ..views.overview.bot_status import bot_status_card


@template(route="/", title="Overview", on_load=DashboardState.load_dashboard_data)
def overview() -> rx.Component:
    """The main overview page for gift card dashboard.

    Returns:
        The UI for the overview page.
    """
    return rx.vstack(
        rx.hstack(
            rx.icon("bar-chart-3", size=22, style={"color": "var(--icon)"}),
            rx.text("Métricas do Dashboard", class_name="text-xl font-semibold text-foreground"),
            class_name="justify-center items-center",
        ),
        rx.box(class_name="border-b border-border w-full my-2"),
        # Main dashboard stats
        dashboard_stats(),
        
        rx.grid(
            card(revenue_chart(), class_name="w-full"),
            card(bot_status_card(), class_name="w-full"),
            card(recent_transactions(), class_name="w-full"),
            class_name="gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 w-full",
        ),
        
        class_name="space-y-8 w-full",
    )