import reflex as rx
import os

tailwind_config = {
    "plugins": ["@tailwindcss/typography"],
    "theme": {
        "extend": {
            "colors": {
                "background": "var(--background)",
                "navbar": "var(--navbar)",
                "foreground": "var(--foreground)",
                "card": {
                    "DEFAULT": "var(--card)",
                    "foreground": "var(--card-foreground)",
                },
                "popover": {
                    "DEFAULT": "var(--popover)",
                    "foreground": "var(--popover-foreground)",
                },
                "primary": {
                    "DEFAULT": "var(--primary)",
                    "foreground": "var(--primary-foreground)",
                },
                "secondary": {
                    "DEFAULT": "var(--secondary)",
                    "foreground": "var(--secondary-foreground)",
                },
                "accent": {
                    "DEFAULT": "var(--accent)",
                    "foreground": "var(--accent-foreground)",
                },
                "destructive": {
                    "DEFAULT": "var(--destructive)",
                    "foreground": "var(--destructive-foreground)",
                },
                "muted": {
                    "DEFAULT": "var(--muted)",
                    "foreground": "var(--muted-foreground)",
                },
                "border": "var(--border)",
                "input": "var(--input)",
                "ring": "var(--ring)",
            },
            "borderRadius": {
                "DEFAULT": "var(--radius)",
            },
        }
    },
}

###### CONFIGURAÇÃO DO BANCO DE DADOS PARA DESENVOLVIMENTO SEM HOT RELOAD

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "telegramaio.db")
###### FIM

config = rx.Config(
    app_name="dashboard",
    # Usa o caminho absoluto externo
    db_url=f"sqlite:///{DB_PATH}", #ALTERAR QUANDO NECESSARIO PARA PRODUÇÃO (ATUALMENTE BUSCANDO UMA PASTA ANTES DO PROJETO PARA EVITAR CONFLITO COM HOT RELOADING)
    plugins=[
        rx.plugins.TailwindV4Plugin(tailwind_config),
    ],
    disable_plugins=[
        "reflex.plugins.sitemap.SitemapPlugin"
    ],
)
