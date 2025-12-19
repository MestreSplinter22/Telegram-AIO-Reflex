"""Transactions summary cards component for gift card dashboard."""

import reflex as rx
from ...backend.states.transactions import TransactionState
from ...components.ui.card import card


def transactions_summary_card(title: str, value: str, subtitle: str = None) -> rx.Component:
    """Individual summary card component."""
    return card(
        rx.vstack(
            rx.text(title, class_name="text-sm text-muted-foreground"),
            rx.text(value, class_name="text-xl font-bold text-foreground"),
            rx.cond(
                subtitle,
                rx.text(subtitle, class_name="text-xs text-muted-foreground"),
                rx.text("", class_name="text-xs text-muted-foreground"),
            ),
            class_name="space-y-1 items-start",
        ),
        class_name="p-4",
    )


def transactions_summary() -> rx.Component:
    """Transactions summary cards component."""
    return rx.grid(
        transactions_summary_card(
            "Total de Transações",
            TransactionState.total_transactions,
            "transações processadas"
        ),
        transactions_summary_card(
            "Receita Total",
            f"R$ {TransactionState.total_revenue:.2f}",
            "em vendas"
        ),
        transactions_summary_card(
            "PIX Processados",
            "247",
            "transações PIX"
        ),
        class_name="grid grid-cols-1 md:grid-cols-3 gap-4 w-full",
    )