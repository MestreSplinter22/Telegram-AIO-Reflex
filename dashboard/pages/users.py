"""Users management page for gift card dashboard."""

import reflex as rx
from ..backend.states.users import UserState
from ..backend.states.models.base import User
from ..templates import template
from ..views.users.users_table import users_table



@template(route="/users", title="Gestão de Usuários", on_load=UserState.load_users)
def users() -> rx.Component:
    """Users management page.

    Returns:
        The UI for the users page.
    """
    return rx.vstack(
        rx.heading("Gestão de Usuários", class_name="text-2xl font-bold text-foreground"),
        rx.text("Gerencie usuários do bot Telegram e suas carteiras", class_name="text-base text-muted-foreground"),
        
        # Filters and search
        rx.hstack(
            rx.input(
                rx.input.slot(rx.icon("search"), class_name="pl-0"),
                placeholder="Buscar por nome, username ou email...",
                class_name="w-72 bg-background border border-input rounded-md px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring",
                on_change=UserState.set_user_search,
                    value=UserState.user_search,
            ),
            rx.select(
                ["all", "active", "suspended", "banned"],
                placeholder="Status",
                class_name="w-36 bg-background border border-input rounded-md px-3 py-2 text-sm",
                on_change=UserState.set_user_status_filter,
                    value=UserState.user_status_filter,
            ),
            rx.button(
                "Exportar CSV",
                class_name="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium",
                on_click=rx.download(
                    data="users_data",
                    filename="usuarios_telegram.csv"
                ),
            ),
            class_name="items-center space-x-4",
        ),
        
        # Users table
        users_table(),
        
        class_name="space-y-6 w-full",
    )