"""Dashboard stats cards component."""

import reflex as rx
from ...backend.states.dashboard import DashboardState
from ...components.ui.card import card


def stat_card(icon: str, title: str, value: rx.Var, subtitle: str, color: str = "blue") -> rx.Component:
    """Individual stat card component."""
    return card(
        rx.vstack(
            rx.hstack(
                rx.icon(icon, class_name=f"h-6 w-6 text-{color}-500"),
                rx.spacer(),
                rx.icon("trending-up", class_name="h-4 w-4 text-green-500"),
                class_name="w-full",
            ),
            rx.vstack(
                rx.text(value, class_name="text-2xl font-bold text-foreground"),
                rx.text(title, class_name="text-sm text-muted-foreground"),
                rx.text(subtitle, class_name="text-xs text-muted-foreground"),
                class_name="space-y-1 items-start",
            ),
            class_name="space-y-3 items-start",
        ),
        class_name="w-full p-6",
    )


def dashboard_stats() -> rx.Component:
    """Dashboard stats cards grid."""
    return rx.grid(
        stat_card(
            "dollar-sign",
            "Receita Total",
            "R$ " + DashboardState.total_revenue.to_string(),
            "+12% vs mês anterior",
            "green"
        ),
        stat_card(
            "users",
            "Usuários Totais",
            DashboardState.total_users.to_string(),
            f"12 ativos",
            "blue"
        ),
        stat_card(
            "credit-card",
            "PIX Processados",
            DashboardState.total_transactions.to_string(),
            "Hoje: 47 transações",
            "purple"
        ),
        stat_card(
            "gift",
            "Gift Cards Vendidos",
            DashboardState.total_gift_cards_sold.to_string(),
            "Este mês: 156 unidades",
            "orange"
        ),
        stat_card(
            "wallet",
            "Saldo Total",
            f"R$ 2,450.75",
            "Em carteiras de usuários",
            "cyan"
        ),
        stat_card(
            "bot",
            "Performance Bot",
            "99.8%",
            "Uptime - 2ms resposta",
            "teal"
        ),
        class_name="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 w-full",
    )