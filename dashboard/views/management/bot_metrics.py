"""Bot metrics component."""

import reflex as rx
from ...components.ui.card import card


def bot_metrics() -> rx.Component:
    """Bot metrics charts card."""
    return card(
        rx.vstack(
            rx.text("Métricas do Bot", class_name="text-lg font-medium text-foreground"),
            rx.text("Gráficos de uso e performance", class_name="text-sm text-muted-foreground"),
            class_name="space-y-2",
        ),
        class_name="p-4 w-full",
    )