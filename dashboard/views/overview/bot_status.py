"""Bot status card component."""

import reflex as rx


def bot_status_card() -> rx.Component:
    """Bot status monitoring card."""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("bot", size=22, style={"color": "var(--icon)"}),
            rx.text("Status do Bot", class_name="text-xl font-semibold text-foreground"),
            class_name="justify-center items-center gap-2",
        ),
        rx.box(class_name="border-b border-border w-full my-2"),

        # Monitoring items list
        rx.box(
            rx.vstack(
                # Bot Status
                rx.hstack(
                    rx.vstack(
                        rx.text("Status do Sistema", class_name="text-sm font-medium text-foreground"),
                        rx.text("Bot Online", class_name="text-xs text-muted-foreground"),
                        spacing="1",
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.icon("circle", size=12, class_name="text-green-500"),
                        rx.text("2ms", class_name="text-xs text-muted-foreground"),
                        spacing="1",
                        align_items="center",
                    ),
                    class_name="w-full items-center py-2",
                ),
                
                # Active Users
                rx.hstack(
                    rx.vstack(
                        rx.text("Usuários Ativos", class_name="text-sm font-medium text-foreground"),
                        rx.text("Total de usuários conectados", class_name="text-xs text-muted-foreground"),
                        spacing="1",
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.text("342", class_name="text-base font-medium text-foreground"),
                    class_name="w-full items-center py-2",
                ),
                
                # Messages Today
                rx.hstack(
                    rx.vstack(
                        rx.text("Mensagens Hoje", class_name="text-sm font-medium text-foreground"),
                        rx.text("Total de mensagens processadas", class_name="text-xs text-muted-foreground"),
                        spacing="1",
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.text("1.2K", class_name="text-base font-medium text-foreground"),
                    class_name="w-full items-center py-2",
                ),
                
                # Commands Executed
                rx.hstack(
                    rx.vstack(
                        rx.text("Comandos Executados", class_name="text-sm font-medium text-foreground"),
                        rx.text("Total de comandos processados", class_name="text-xs text-muted-foreground"),
                        spacing="1",
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.text("847", class_name="text-base font-medium text-foreground"),
                    class_name="w-full items-center py-2",
                ),
                
                spacing="0",
                class_name="divide-y divide-border w-full",
            ),
            class_name="w-full",
        ),
        spacing="3",
        class_name="w-full h-full p-4 md:p-6",
    )