"""Bot control buttons component."""

import reflex as rx
from ...backend.states.bot import BotState


def bot_controls() -> rx.Component:
    """Bot control buttons with API integration."""
    return rx.vstack(
        rx.hstack(
            rx.button(
                "Iniciar Bot",
                class_name="bg-green-500 text-green-900 hover:bg-green-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=BotState.start_bot,
                loading=BotState.bot_status_loading,
                disabled=rx.cond(BotState.bot_running, True, False),
            ),
            rx.button(
                "Parar Bot",
                class_name="bg-red-500 text-red-900 hover:bg-red-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=BotState.stop_bot,
                loading=BotState.bot_status_loading,
                disabled=rx.cond(BotState.bot_running, False, True),
            ),
            rx.button(
                "Status",
                class_name="bg-blue-500 text-blue-900 hover:bg-blue-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=BotState.get_bot_status,
                loading=BotState.bot_status_loading,
            ),
            rx.button(
                "Testar",
                class_name="bg-purple-500 text-purple-900 hover:bg-purple-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=BotState.test_bot,
                loading=BotState.bot_status_loading,
            ),
            class_name="items-center space-x-2",
        ),
        rx.hstack(
            rx.button(
                "Reiniciar Bot",
                class_name="bg-yellow-500 text-yellow-900 hover:bg-yellow-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=BotState.restart_bot,
                loading=BotState.bot_status_loading,
            ),
            rx.button(
                "Limpar Logs",
                class_name="bg-orange-500 text-orange-900 hover:bg-orange-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=BotState.clear_logs,
            ),
            rx.button(
                "Exportar Logs",
                class_name="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium",
                on_click=rx.download(
                    data="bot_logs",
                    filename="logs_telegram_bot.json"
                ),
            ),
            class_name="items-center space-x-2 mt-2",
        ),
        class_name="space-y-2",
    )