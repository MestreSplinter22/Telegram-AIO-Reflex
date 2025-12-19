"""Bot logs component."""

import reflex as rx
from ...components.ui.card import card


def bot_logs() -> rx.Component:
    """Bot activity logs."""
    return card(
        rx.vstack(
            rx.text("Logs do Bot", class_name="text-lg font-medium text-foreground"),
            rx.text("Últimas atividades do bot", class_name="text-sm text-muted-foreground"),
            rx.text(
                "2024-01-15 10:30:45 - Bot iniciado\n2024-01-15 10:31:12 - Novo usuário: @usuario123\n2024-01-15 10:32:01 - Compra realizada: R$ 50.00\n2024-01-15 10:33:28 - PIX confirmado",
                class_name="font-mono text-xs text-foreground whitespace-pre-wrap",
            ),
            class_name="space-y-2",
        ),
        class_name="p-4 w-full",
    )