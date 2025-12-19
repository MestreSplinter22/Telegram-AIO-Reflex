"""Products summary cards component for gift card dashboard."""

import reflex as rx
from ...backend.states.giftcards import GiftCardProductState
from ...components.ui.card import card


def products_summary_card(title: str, value: str, subtitle: str = None) -> rx.Component:
    """Individual products summary card component."""
    return card(
        rx.vstack(
            rx.text(title, class_name="text-sm text-muted-foreground"),
            rx.text(value, class_name="text-xl font-bold text-foreground"),
            rx.cond(
                subtitle,
                rx.text(subtitle, class_name="text-xs text-muted-foreground"),
                rx.text("", class_name="text-xs text-muted-foreground"),
            ),
            class_name="space-y-1 items-start",
        ),
        class_name="p-4",
    )


def products_summary() -> rx.Component:
    """Products summary cards component."""
    return rx.grid(
        products_summary_card(
            "Total de Produtos",
            GiftCardProductState.filtered_gift_cards.length(),
            "produtos cadastrados"
        ),
        products_summary_card(
            "Vendas Totais",
            "156",
            "vendas realizadas"
        ),
        products_summary_card(
            "Lucro Estimado",
            "R$ 12,450.00",
            "margem de lucro"
        ),
        products_summary_card(
            "Estoque Total",
            "1,247",
            "unidades disponíveis"
        ),
        class_name="grid grid-cols-2 md:grid-cols-4 gap-4 w-full",
    )