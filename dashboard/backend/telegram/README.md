# Bot Telegram com aiogram - TelegramaIO

## Descrição
Bot do Telegram integrado com Reflex framework, agora usando **aiogram** (versão 3.4.1) ao invés de python-telegram-bot.

## Comandos
- `/start` - Retorna "Hello World! Bot iniciado com sucesso!"
- `/help` - Lista os comandos disponíveis

## Configuração

### Token do Bot
O bot requer um token válido do Telegram. Configure através de:

1. **Variável de ambiente (recomendado):**
   ```bash
   export TELEGRAM_BOT_TOKEN="seu_token_aqui"
   ```

2. **Ou diretamente no código:**
   Edite `bot.py` e substitua `BOT_TOKEN` pelo seu token real.

### Obter Token do Telegram
1. Converse com [@BotFather](https://t.me/botfather) no Telegram
2. Use `/newbot` para criar um novo bot
3. Copie o token fornecido

### Instalação
```bash
pip install aiogram==3.4.1
pip uninstall python-telegram-bot -y
```

### Inicialização Manual
O bot **não** é inicializado automaticamente. Use os endpoints para controle manual.

## Estrutura de Arquivos
- `bot.py` - Lógica principal do bot (atualizado para aiogram)
- `routes.py` - Endpoints de API para status do bot
- `startup.py` - Funções de inicialização do bot
- `lifespan.py` - Gerenciamento do ciclo de vida do bot
- `events.py` - Eventos e mensagens de log
- `__init__.py` - Pacote Python

## Como Testar
1. Configure o token do bot (veja seção Configuração)
2. Instale as novas dependências: `pip install aiogram==3.4.1`
3. Execute o Reflex: `reflex run`
4. Inicie o bot manualmente:
   ```bash
   curl -X POST http://localhost:8000/api/telegram/start
   ```
5. Abra http://localhost:8000/api/telegram/status para verificar status
6. Envie `/start` para o bot no Telegram
7. Você receberá a mensagem "Hello World! Bot iniciado com sucesso!"

### Controle Manual do Bot

#### Endpoints de API:
```bash
# Verificar status do bot
curl http://localhost:8000/api/telegram/status

# Iniciar o bot manualmente
curl -X POST http://localhost:8000/api/telegram/start

# Parar o bot
curl -X POST http://localhost:8000/api/telegram/stop

# Testar funcionalidade
curl http://localhost:8000/api/telegram/test
```

#### Fluxo de Uso:
1. Inicie o servidor Reflex
2. Use o endpoint `/api/telegram/start` para iniciar o bot
3. Use o endpoint `/api/telegram/stop` para parar o bot quando necessário

## Mudanças da Migração

### Bibliotecas
- **Removida**: `python-telegram-bot==21.5`
- **Adicionada**: `aiogram==3.4.1`

### Arquivos Atualizados
- `bot.py`: Reescrito completamente para usar aiogram
- `routes.py`: Adicionada função `register_telegram_routes()` para compatibilidade
- `startup.py`: Atualizado para usar asyncio.Task
- `lifespan.py`: Atualizado para gerenciar o ciclo de vida do bot
- `events.py`: Mensagens de log atualizadas para indicar uso de aiogram