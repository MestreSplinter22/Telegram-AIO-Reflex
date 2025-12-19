"""Gift cards grid component for products catalog."""

import reflex as rx
from ...backend.states.giftcards import GiftCardProductState
from ...components.ui.card import card


def giftcard_item(giftcard) -> rx.Component:
    """Individual gift card item component."""
    return card(
        rx.vstack(
            rx.text(giftcard.name, class_name="font-medium text-foreground"),
            rx.text(giftcard.category, class_name="text-muted-foreground"),
            rx.text(f"R$ {giftcard.selling_price:.2f}", class_name="font-bold text-foreground"),
            rx.text(f"Estoque: {giftcard.stock}", class_name="text-xs text-muted-foreground"),
            rx.text(f"Vendas: {giftcard.sold_count}", class_name="text-xs text-muted-foreground"),
            class_name="space-y-2 items-start",
        ),
        class_name="w-full",
    )


def giftcards_grid() -> rx.Component:
    """Gift cards grid component."""
    return rx.grid(
        rx.foreach(
            GiftCardProductState.filtered_gift_cards,
            giftcard_item
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full",
    )