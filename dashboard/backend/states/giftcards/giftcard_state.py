"""Gift card management state."""

import reflex as rx
from datetime import datetime
from ..models.base import GiftCard


class GiftCardProductState(rx.State):
    """Gift card product management state."""
    
    # Gift card data
    gift_cards: list[GiftCard] = []
    gift_cards_loading: bool = False
    
    # Filters
    gift_card_category_filter: str = "all"
    gift_card_status_filter: str = "all"
    gift_card_search: str = ""
    
    # Selected gift card
    selected_gift_card: GiftCard | None = None
    
    # Modal states
    create_modal_open: bool = False
    edit_modal_open: bool = False
    
    # Form data for create/edit
    gift_card_form: dict = {}
    
    async def load_gift_cards(self):
        """Load gift cards from sample data."""
        self.gift_cards_loading = True
        yield
        
        # Sample data - replace with actual API calls
        self.gift_cards = [
            GiftCard(
                id="gift_1",
                name="Amazon Gift Card $50",
                category="amazon",
                value=50.00,
                cost_price=45.00,
                selling_price=47.50,
                profit_margin=5.26,
                stock=100,
                sold_count=250,
                status="active",
                created_at=datetime.now(),
                image_url="https://example.com/amazon50.jpg"
            ),
            GiftCard(
                id="gift_2",
                name="Netflix Gift Card $25",
                category="netflix",
                value=25.00,
                cost_price=22.50,
                selling_price=23.75,
                profit_margin=5.56,
                stock=50,
                sold_count=125,
                status="active",
                created_at=datetime.now(),
                image_url="https://example.com/netflix25.jpg"
            )
        ]
        self.gift_cards_loading = False
    
    @rx.var
    def filtered_gift_cards(self) -> list[GiftCard]:
        """Get filtered gift cards."""
        filtered = self.gift_cards
        
        if self.gift_card_category_filter != "all":
            filtered = [
                card for card in filtered
                if card.category == self.gift_card_category_filter
            ]
        
        if self.gift_card_status_filter != "all":
            filtered = [
                card for card in filtered
                if card.status == self.gift_card_status_filter
            ]
        
        if self.gift_card_search:
            search_lower = self.gift_card_search.lower()
            filtered = [
                card for card in filtered
                if (search_lower in card.name.lower() or
                    search_lower in card.category.lower())
            ]
        
        return filtered
    
    def set_selected_gift_card(self, gift_card: GiftCard):
        """Set selected gift card for details view."""
        self.selected_gift_card = gift_card
    
    def clear_selected_gift_card(self):
        """Clear selected gift card."""
        self.selected_gift_card = None
    
    def open_create_modal(self):
        """Open create gift card modal."""
        self.create_modal_open = True
        self.gift_card_form = {}
    
    def close_create_modal(self):
        """Close create gift card modal."""
        self.create_modal_open = False
        self.gift_card_form = {}
    
    def open_edit_modal(self, gift_card: GiftCard):
        """Open edit gift card modal."""
        self.edit_modal_open = True
        self.selected_gift_card = gift_card
        self.gift_card_form = {
            "name": gift_card.name,
            "category": gift_card.category,
            "value": gift_card.value,
            "cost_price": gift_card.cost_price,
            "selling_price": gift_card.selling_price,
            "stock": gift_card.stock,
            "status": gift_card.status
        }
    
    def close_edit_modal(self):
        """Close edit gift card modal."""
        self.edit_modal_open = False
        self.selected_gift_card = None
        self.gift_card_form = {}
    
    def create_gift_card(self):
        """Create new gift card."""
        # Implementation for creating gift card
        self.create_modal_open = False
        yield rx.toast.success("Gift card criado com sucesso!")
    
    def update_gift_card(self):
        """Update existing gift card."""
        # Implementation for updating gift card
        self.edit_modal_open = False
        yield rx.toast.success("Gift card atualizado com sucesso!")
    
    def set_gift_card_search(self, value: str):
        """Set gift card search query."""
        self.gift_card_search = value

    def set_gift_card_category_filter(self, value: str):
        """Set gift card category filter."""
        self.gift_card_category_filter = value

    def set_gift_card_status_filter(self, value: str):
        """Set gift card status filter."""
        self.gift_card_status_filter = value

    def toggle_add_product(self):
        """Toggle add product modal."""
        self.create_modal_open = not self.create_modal_open

    def delete_gift_card(self, gift_card_id: str):
        """Delete gift card."""
        self.gift_cards = [
            card for card in self.gift_cards
            if card.id != gift_card_id
        ]
        yield rx.toast.success("Gift card deletado com sucesso!")