"""Bot commands usage component."""

import reflex as rx
from ...components.ui.card import card


def bot_commands() -> rx.Component:
    """Most used bot commands."""
    return card(
        rx.vstack(
            rx.text("Comandos Mais Usados", class_name="text-lg font-medium text-foreground"),
            rx.vstack(
                rx.hstack(
                    rx.text("/start", class_name="text-sm text-foreground"),
                    rx.spacer(),
                    rx.text("245 vezes", class_name="text-xs text-muted-foreground"),
                    class_name="w-full",
                ),
                rx.hstack(
                    rx.text("/comprar", class_name="text-sm text-foreground"),
                    rx.spacer(),
                    rx.text("189 vezes", class_name="text-xs text-muted-foreground"),
                    class_name="w-full",
                ),
                rx.hstack(
                    rx.text("/saldo", class_name="text-sm text-foreground"),
                    rx.spacer(),
                    rx.text("156 vezes", class_name="text-xs text-muted-foreground"),
                    class_name="w-full",
                ),
                class_name="space-y-2",
            ),
            class_name="space-y-3",
        ),
        class_name="p-4 w-full",
    )