"""Gift cards catalog management page."""

import reflex as rx
from ..backend.states.giftcards import GiftCardProductState
from ..templates import template
from ..views.products.products_summary import products_summary
from ..views.products.giftcards_grid import giftcards_grid



@template(route="/products", title="Catálogo de Gift Cards", on_load=GiftCardProductState.load_gift_cards)
def products() -> rx.Component:
    """Gift cards catalog management page.

    Returns:
        The UI for the gift cards page.
    """
    return rx.vstack(
        rx.heading("Catálogo de Gift Cards", class_name="text-2xl font-bold text-foreground"),
        rx.text("Gerencie produtos, estoque e margens de lucro", class_name="text-base text-muted-foreground"),
        
        # Action buttons
        rx.hstack(
            rx.button(
                "Adicionar Novo Produto",
                class_name="bg-green-500 text-green-900 hover:bg-green-600 px-4 py-2 rounded-md text-sm font-medium",
                on_click=GiftCardProductState.toggle_add_product,
            ),
            rx.button(
                "Exportar Relatório",
                class_name="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md text-sm font-medium",
                on_click=rx.download(
                    data="giftcards_report",
                    filename="catalogo_giftcards.csv"
                ),
            ),
            class_name="items-center space-x-4",
        ),
        
        # Summary statistics
        products_summary(),
        
        # Gift cards grid
        giftcards_grid(),
        

        
        class_name="space-y-6 w-full",
    )