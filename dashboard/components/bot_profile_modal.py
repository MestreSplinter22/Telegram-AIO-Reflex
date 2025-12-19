"""Bot profile modal component for displaying bot information and API token management."""

import reflex as rx


class BotProfileModalState(rx.State):
    """State for bot profile modal."""
    
    is_open: bool = False
    bot_token: str = ""
    bot_info: dict = {}
    has_bot: bool = False
    loading: bool = False
    
    def set_is_open(self, value: bool):
        """Set modal open state."""
        self.is_open = value

    def set_bot_token(self, value: str):
        """Set bot token value."""
        self.bot_token = value

    def open_modal(self):
        """Open the modal."""
        self.is_open = True
        
    def close_modal(self):
        """Close the modal."""
        self.is_open = False
        
    async def save_token(self):
        """Save the bot token."""
        if self.bot_token:
            # Simulate API call to validate token
            self.loading = True
            yield
            
            # Mock bot info - in real app, call Telegram API
            self.bot_info = {
                "name": "GiftCard Bot",
                "username": "@giftcard_bot",
                "id": 123456789,
                "status": "ativo",
                "created_at": "2024-01-15",
                "commands_count": 15,
                "users_count": 1250,
                "description": "Bot para gerenciamento de cartões de presente"
            }
            self.has_bot = True
            self.loading = False
            
    def clear_token(self):
        """Clear the bot token."""
        self.bot_token = ""
        self.bot_info = {}
        self.has_bot = False


def bot_profile_modal() -> rx.Component:
    """Bot profile modal component."""
    
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Configurar Bot",
                class_name="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md"
            )
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Configuração do Bot Telegram",
                class_name="text-lg font-semibold text-foreground"
            ),
            rx.dialog.description(
                "Gerencie as configurações do seu bot Telegram",
                class_name="text-sm text-muted-foreground"
            ),
            rx.vstack(
                # Bot Profile Card (if bot exists)
                rx.cond(
                    BotProfileModalState.has_bot,
                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("bot", class_name="w-8 h-8 text-primary"),
                                rx.vstack(
                                    rx.text(
                                        BotProfileModalState.bot_info["name"],
                                        class_name="font-semibold text-lg"
                                    ),
                                    rx.text(
                                        BotProfileModalState.bot_info["username"],
                                        class_name="text-sm text-muted-foreground"
                                    ),
                                    align_items="start"
                                ),
                                class_name="w-full"
                            ),
                            rx.divider(),
                            rx.grid(
                                rx.vstack(
                                    rx.text("ID", class_name="text-xs text-muted-foreground"),
                                    rx.text(BotProfileModalState.bot_info["id"], class_name="text-sm font-medium")
                                ),
                                rx.vstack(
                                    rx.text("Status", class_name="text-xs text-muted-foreground"),
                                    rx.badge(
                                        BotProfileModalState.bot_info["status"],
                                        class_name="bg-green-100 text-green-800"
                                    )
                                ),
                                rx.vstack(
                                    rx.text("Comandos", class_name="text-xs text-muted-foreground"),
                                    rx.text(BotProfileModalState.bot_info["commands_count"], class_name="text-sm font-medium")
                                ),
                                rx.vstack(
                                    rx.text("Usuários", class_name="text-xs text-muted-foreground"),
                                    rx.text(BotProfileModalState.bot_info["users_count"], class_name="text-sm font-medium")
                                ),
                                columns="2",
                                class_name="w-full gap-4"
                            ),
                            rx.text(
                                BotProfileModalState.bot_info["description"],
                                class_name="text-sm text-muted-foreground"
                            ),
                            class_name="space-y-4"
                        ),
                        class_name="w-full"
                    ),
                    rx.text("Nenhum bot configurado", class_name="text-muted-foreground text-center py-8")
                ),
                
                # API Token Input
                rx.vstack(
                    rx.text("Token da API", class_name="text-sm font-medium"),
                    rx.input(
                        placeholder="Insira o token do seu bot Telegram",
                        value=BotProfileModalState.bot_token,
                        on_change=BotProfileModalState.set_bot_token,
                        type="password",
                        class_name="w-full"
                    ),
                    rx.text(
                        "O token será usado para conectar seu bot ao sistema",
                        class_name="text-xs text-muted-foreground"
                    ),
                    align_items="start",
                    class_name="w-full"
                ),
                
                # Action Buttons
                rx.hstack(
                    rx.cond(
                        BotProfileModalState.has_bot,
                        rx.button(
                            "Remover Token",
                            on_click=BotProfileModalState.clear_token,
                            class_name="bg-destructive text-destructive-foreground hover:bg-destructive/90 px-4 py-2 rounded-md"
                        )
                    ),
                    rx.button(
                        "Salvar Token",
                        on_click=BotProfileModalState.save_token,
                        loading=BotProfileModalState.loading,
                        class_name="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md"
                    ),
                    justify="between",
                    class_name="w-full"
                ),
                
                class_name="space-y-6 w-full"
            ),
            rx.dialog.close(
                rx.button(
                    "Fechar",
                    class_name="absolute top-2 right-2 text-muted-foreground hover:text-foreground"
                )
            ),
            class_name="sm:max-w-[425px]"
        ),
        open=BotProfileModalState.is_open,
        on_open_change=BotProfileModalState.set_is_open
    )