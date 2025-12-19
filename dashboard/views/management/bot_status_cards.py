"""Bot status cards component."""

import reflex as rx
from ...components.ui.card import card
from ...backend.states.bot import BotState


def bot_status_card(title: str, value: str, status: str = "default") -> rx.Component:
    """Create a single bot status card.
    
    Args:
        title: The card title
        value: The card value
        status: The status color (green, red, yellow, default)
    
    Returns:
        A bot status card component
    """
    status_colors = {
        "green": "text-green-500",
        "red": "text-red-500",
        "yellow": "text-yellow-500",
        "default": "text-foreground"
    }
    
    status_color = status_colors.get(status, "text-foreground")
    
    return card(
        rx.vstack(
            rx.hstack(
                rx.icon("circle", size=16, class_name=status_color),
                rx.text(title, class_name="text-sm text-muted-foreground"),
                class_name="items-center space-x-2",
            ),
            rx.text(value, class_name=f"text-lg font-bold {status_color}"),
            class_name="space-y-1",
        ),
        class_name="p-4",
    )


def bot_status_cards() -> rx.Component:
    """Bot status overview cards with real API data."""
    return rx.grid(
        rx.card(
            rx.vstack(
                rx.text("Status", class_name="text-sm text-muted-foreground"),
                rx.text(
                    rx.cond(BotState.bot_running, "Online", "Offline"),
                    class_name="text-lg font-bold text-green-500"
                ),
                class_name="space-y-1",
            ),
            class_name="p-4",
        ),
        rx.card(
            rx.vstack(
                rx.text("Usuários Ativos", class_name="text-sm text-muted-foreground"),
                rx.text(
                    BotState.bot_active_users,
                    class_name="text-lg font-bold text-foreground"
                ),
                class_name="space-y-1",
            ),
            class_name="p-4",
        ),
        rx.card(
            rx.vstack(
                rx.text("Mensagens/Hoje", class_name="text-sm text-muted-foreground"),
                rx.text(
                    BotState.bot_messages_today,
                    class_name="text-lg font-bold text-foreground"
                ),
                class_name="space-y-1",
            ),
            class_name="p-4",
        ),
        rx.card(
            rx.vstack(
                rx.text("Tempo Resposta", class_name="text-sm text-muted-foreground"),
                rx.text(
                    BotState.bot_response_time,
                    class_name="text-lg font-bold text-foreground"
                ),
                class_name="space-y-1",
            ),
            class_name="p-4",
        ),
        class_name="grid grid-cols-2 md:grid-cols-4 gap-4 w-full",
    )