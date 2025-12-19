import reflex as rx

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

config = rx.Config(
    app_name="dashboard",
    db_url="sqlite:///telegramaio.db",
    plugins=[
        rx.plugins.TailwindV4Plugin(tailwind_config),
    ],
    disable_plugins=[
        "reflex.plugins.sitemap.SitemapPlugin"
    ],
)
