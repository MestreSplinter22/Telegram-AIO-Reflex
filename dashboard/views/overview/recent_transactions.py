"""Recent transactions component for overview page."""

import reflex as rx
from ...backend.states.transactions import TransactionState
from ...components.ui.status_badge import status_badge





def recent_transactions() -> rx.Component:
    """Recent transactions list."""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("activity", size=22, style={"color": "var(--icon-secondary)"}),
            rx.text("Transações Recentes", class_name="text-xl font-semibold text-foreground"),
            class_name="justify-center items-center gap-2",
        ),
        rx.box(class_name="border-b border-border w-full my-2"),

        # List
        rx.box(
            rx.vstack(
                rx.foreach(
                    TransactionState.filtered_transactions[:5],
                    lambda transaction: rx.hstack(
                        rx.vstack(
                            rx.text(transaction.description, class_name="text-sm font-medium text-foreground"),
                            rx.text(f"R$ {transaction.amount:.2f}", class_name="text-xs text-muted-foreground"),
                            spacing="1",
                            align_items="start",
                        ),
                        rx.spacer(),
                        status_badge(transaction.status),
                        class_name="w-full items-center py-2",
                    )
                ),
                spacing="0",
                class_name="divide-y divide-border w-full",
            ),
            class_name="w-full",
        ),
        spacing="3",
        class_name="w-full h-full p-4 md:p-6",
    )