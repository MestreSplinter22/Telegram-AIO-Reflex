"""Transactions management page for gift card dashboard."""

import reflex as rx
from ..backend.states.transactions import TransactionState
from ..backend.states.dashboard import DashboardState
from ..templates import template
from ..views.transactions.transactions_table import transactions_table
from ..views.transactions.transactions_summary import transactions_summary



@template(route="/transactions", title="Gestão de Transações", on_load=TransactionState.load_transactions)
def transactions() -> rx.Component:
    """Transactions management page.

    Returns:
        The UI for the transactions page.
    """
    return rx.vstack(
        rx.heading("Gestão de Transações", class_name="text-2xl font-bold text-foreground"),
        rx.text("Monitoramento de todas as operações financeiras PIX e compras", class_name="text-base text-muted-foreground"),
        
        # Advanced filters
        rx.hstack(
            rx.input(
                rx.input.slot(rx.icon("search"), class_name="pl-0"),
                placeholder="Buscar transações...",
                class_name="w-[250px] h-10 px-3 py-2 text-sm rounded-md border border-input bg-background",
                on_change=TransactionState.set_transaction_search,
                    value=TransactionState.transaction_search,
            ),
            rx.select(
                ["all", "deposit", "purchase", "refund", "manual_adjustment"],
                placeholder="Tipo",
                class_name="w-[150px] h-10 px-3 py-2 text-sm rounded-md border border-input bg-background",
                on_change=TransactionState.set_transaction_type_filter,
                    value=TransactionState.transaction_type_filter,
            ),
            rx.select(
                ["all", "pending", "completed", "failed", "refunded"],
                placeholder="Status",
                class_name="w-[150px] h-10 px-3 py-2 text-sm rounded-md border border-input bg-background",
                on_change=TransactionState.set_status_filter,
                    value=TransactionState.transaction_status_filter,
            ),
            rx.select(
                ["1d", "7d", "30d", "90d", "all"],
                placeholder="Período",
                class_name="w-[120px] h-10 px-3 py-2 text-sm rounded-md border border-input bg-background",
                on_change=TransactionState.set_date_range,
                    value=TransactionState.transaction_date_filter,
            ),
            rx.button(
                "Exportar Excel",
                class_name="bg-green-500 text-green-900 hover:bg-green-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=rx.download(
                    data="transactions_report",
                    filename="transacoes.xlsx"
                ),
            ),
            class_name="items-center space-x-4",
        ),
        
        # Summary cards
        transactions_summary(),
        
        # Transactions table
        transactions_table(),
        
        class_name="space-y-6 w-full",
    )