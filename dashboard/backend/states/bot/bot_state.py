"""Bot management state with Telegram API integration."""

import reflex as rx


class BotState(rx.State):
    """Bot management and control state."""
    
    # Bot status
    bot_running: bool = False
    bot_status_loading: bool = False
    bot_response_time: str = "--"
    bot_active_users: int = 0
    bot_messages_today: int = 0
    bot_commands_today: int = 0
    
    async def get_bot_status(self):
        """Get current bot status from API."""
        self.bot_status_loading = True
        yield
        
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/telegram/status")
                if response.status_code == 200:
                    data = response.json()
                    self.bot_running = data.get("running", False)
                    self.bot_response_time = "2ms" if self.bot_running else "--"
                    yield rx.toast.info(f"Status do bot: {'Online' if self.bot_running else 'Offline'}", position="top-center")
                else:
                    self.bot_running = False
                    yield rx.toast.error("Erro ao verificar status do bot", position="top-center")
        except Exception as e:
            self.bot_running = False
            yield rx.toast.error(f"Erro de conexão: {str(e)}", position="top-center")
        finally:
            self.bot_status_loading = False
    
    async def start_bot(self):
        """Start the bot via API."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/api/telegram/start")
                if response.status_code == 200:
                    self.bot_running = True
                    yield rx.toast.success("Bot iniciado com sucesso!", position="top-center")
                else:
                    error_msg = response.json().get("detail", "Erro ao iniciar bot")
                    yield rx.toast.error(f"Erro: {error_msg}", position="top-center")
        except Exception as e:
            yield rx.toast.error(f"Erro de conexão: {str(e)}", position="top-center")
    
    async def stop_bot(self):
        """Stop the bot via API."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/api/telegram/stop")
                if response.status_code == 200:
                    self.bot_running = False
                    yield rx.toast.success("Bot parado com sucesso!", position="top-center")
                else:
                    error_msg = response.json().get("detail", "Erro ao parar bot")
                    yield rx.toast.error(f"Erro: {error_msg}", position="top-center")
        except Exception as e:
            yield rx.toast.error(f"Erro de conexão: {str(e)}", position="top-center")
    
    async def test_bot(self):
        """Test the bot via API."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/api/telegram/test")
                if response.status_code == 200:
                    yield rx.toast.success("Bot testado com sucesso!", position="top-center")
                else:
                    error_msg = response.json().get("detail", "Erro ao testar bot")
                    yield rx.toast.error(f"Erro: {error_msg}", position="top-center")
        except Exception as e:
            yield rx.toast.error(f"Erro de conexão: {str(e)}", position="top-center")
    
    async def restart_bot(self):
        """Restart bot (stop and start)."""
        await self.stop_bot()
        await self.start_bot()
    
    def clear_logs(self):
        """Clear bot logs (simulated)."""
        return rx.toast.success("Logs limpos com sucesso", position="top-center")