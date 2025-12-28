import reflex as rx
import os

# Caminho para o config do vite que o reflex gera
vite_conf_path = os.path.join(os.getcwd(), ".web", "vite.config.js")

if os.path.exists(vite_conf_path):
    with open(vite_conf_path, "r") as f:
        content = f.read()
    
    # Se já não tiver o patch, a gente adiciona
    if "allowedHosts" not in content:
        # Inserimos a regra de allowedHosts logo após a definição do port
        patched_content = content.replace(
            "port: process.env.PORT,",
            "port: process.env.PORT, allowedHosts: true,"
        )
        with open(vite_conf_path, "w") as f:
            f.write(patched_content)
        print("✅ Patch de segurança do Vite aplicado com sucesso!")

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
    cors_allowed_origins=["*"], 
    api_url="https://api.promosdiarias.shop", 
    deploy_url="https://front.promosdiarias.shop",
    db_url=f"sqlite:///{DB_PATH}",
    plugins=[
        rx.plugins.TailwindV4Plugin(tailwind_config),
    ],
    disable_plugins=[
        "reflex.plugins.sitemap.SitemapPlugin"
    ],
)
