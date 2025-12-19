"""Bot management and monitoring page."""

import reflex as rx
from ..backend.states.bot import BotState
from ..backend.states.dashboard import DashboardState
from ..templates import template
from ..components.bot_profile_modal import bot_profile_modal
from ..views.management.bot_status_cards import bot_status_cards
from ..views.management.bot_controls import bot_controls
from ..views.management.bot_metrics import bot_metrics
from ..views.management.bot_commands import bot_commands
from ..views.management.bot_logs import bot_logs


@template(route="/bot-management", title="Gerenciamento do Bot")
def bot_management() -> rx.Component:
    """Bot management and monitoring page.

    Returns:
        The UI for the bot management page.
    """
    return rx.vstack(
        rx.fragment(on_mount=BotState.get_bot_status),
        rx.hstack(
            rx.vstack(
                rx.heading("Gerenciamento do Bot Telegram", class_name="text-2xl font-bold text-foreground"),
                rx.text("Monitoramento em tempo real do bot e análise de uso", class_name="text-base text-muted-foreground"),
                align_items="start"
            ),
            bot_profile_modal(),
            justify="between",
            align_items="center",
            class_name="w-full"
        ),
        
        # Bot status overview
        bot_status_cards(),
        
        # Control buttons
        bot_controls(),
        
        # Bot metrics charts
        bot_metrics(),
        
        # Bot commands usage
        bot_commands(),
        
        # Bot logs
        bot_logs(),
        
        class_name="space-y-6 w-full",
    )