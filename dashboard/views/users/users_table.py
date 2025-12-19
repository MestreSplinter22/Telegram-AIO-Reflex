"""Users table component for gift card dashboard."""

import reflex as rx
from ...backend.states.users import UserState
from ...backend.states.models.base import User
from ...components.ui.card import card


def user_status_badge(status: str) -> rx.Component:
    """User status badge component."""
    color_map = {
        "active": ("green", "Ativo"),
        "suspended": ("yellow", "Suspenso"),
        "banned": ("red", "Banido")
    }
    color, text = color_map.get(status, ("gray", status))
    
    return rx.badge(
        text,
        color_scheme=color,
        variant="surface",
        class_name="text-xs px-2 py-1",
    )


def risk_score_badge(score: float) -> rx.Component:
    """Risk score badge component."""
    return rx.badge(
        f"{score:.0f}%",
        color_scheme=rx.cond(
            score < 30,
            "green",
            rx.cond(
                score < 70,
                "yellow",
                "red"
            )
        ),
        variant="surface",
        size="2",
    )


def users_table() -> rx.Component:
    """Users table component."""
    return card(
        rx.vstack(
            rx.hstack(
                rx.text("Usuários", class_name="text-lg font-medium text-foreground"),
                rx.spacer(),
                rx.text(f"Total: {UserState.users.length()} usuários", class_name="text-sm text-muted-foreground"),
                class_name="w-full",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Usuário", class_name="text-sm font-medium text-foreground"),
                        rx.table.column_header_cell("Telegram", class_name="text-sm font-medium text-foreground"),
                        rx.table.column_header_cell("Saldo", class_name="text-sm font-medium text-foreground"),
                        rx.table.column_header_cell("Gasto Total", class_name="text-sm font-medium text-foreground"),
                        rx.table.column_header_cell("Status", class_name="text-sm font-medium text-foreground"),
                        rx.table.column_header_cell("Risco", class_name="text-sm font-medium text-foreground"),
                        rx.table.column_header_cell("Ações", class_name="text-sm font-medium text-foreground"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        UserState.users,
                        lambda user: rx.table.row(
                            rx.table.cell(
                                rx.vstack(
                                    rx.text(user.name, class_name="text-sm font-medium text-foreground"),
                                    rx.text(user.email, class_name="text-xs text-muted-foreground"),
                                    class_name="space-y-1 items-start",
                                )
                            ),
                            rx.table.cell(
                                rx.vstack(
                                    rx.text(f"@{user.username}", class_name="text-sm text-foreground"),
                                    rx.text(user.telegram_id, class_name="text-xs text-muted-foreground"),
                                    class_name="space-y-1 items-start",
                                )
                            ),
                            rx.table.cell(
                                rx.text(f"R$ {user.balance:.2f}", class_name="text-sm font-medium text-foreground")
                            ),
                            rx.table.cell(
                                rx.text(f"R$ {user.total_spent:.2f}", class_name="text-sm text-foreground")
                            ),
                            rx.table.cell(
                                user_status_badge(user.status)
                            ),
                            rx.table.cell(
                                risk_score_badge(user.risk_score)
                            ),
                            rx.table.cell(
                                rx.hstack(
                                    rx.button(
                                        "Ver Detalhes",
                                        size="2",
                                        variant="ghost",
                                        on_click=UserState.set_selected_user(user),
                                        class_name="text-xs",
                                    ),
                                    rx.button(
                                        "Carteira",
                                        size="2",
                                        variant="ghost",
                                        color_scheme="blue",
                                        class_name="text-xs",
                                    ),
                                    class_name="space-x-2",
                                )
                            ),
                        )
                    )
                ),
                class_name="w-full",
            ),
            class_name="space-y-4",
        ),
        class_name="w-full p-6",
    )