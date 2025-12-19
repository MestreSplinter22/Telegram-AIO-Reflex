"""Generic table state for data management."""

import reflex as rx
import csv
import os
from typing import Any, Dict
from pydantic import BaseModel

class Item(BaseModel):
    """Generic item for table state."""
    id: str
    name: str
    description: str
    price: float
    category: str
    status: str


class TableState(rx.State):
    """Generic table state for data management."""
    
    # Data
    items: list[Item] = []
    
    # Search and filters
    search_value: str = ""
    sort_column: str = "name"
    sort_direction: str = "asc"
    
    # Pagination
    current_page: int = 1
    items_per_page: int = 10
    
    # Loading
    loading: bool = False
    
    async def load_data(self):
        """Load data from CSV file."""
        self.loading = True
        yield
        
        try:
            csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "items.csv")
            if os.path.exists(csv_path):
                with open(csv_path, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    self.items = [
                        Item(
                            id=row["id"],
                            name=row["name"],
                            description=row["description"],
                            price=float(row["price"]),
                            category=row["category"],
                            status=row["status"]
                        )
                        for row in reader
                    ]
            else:
                # Sample data if CSV doesn't exist
                self.items = [
                    Item(id="1", name="Item 1", description="Description 1", price=10.0, category="A", status="active"),
                    Item(id="2", name="Item 2", description="Description 2", price=20.0, category="B", status="active"),
                    Item(id="3", name="Item 3", description="Description 3", price=30.0, category="A", status="inactive")
                ]
        except Exception as e:
            # Fallback to sample data
            self.items = [
                Item(id="1", name="Sample 1", description="Sample item 1", price=10.0, category="A", status="active"),
                Item(id="2", name="Sample 2", description="Sample item 2", price=20.0, category="B", status="active")
            ]
        
        self.loading = False
    
    @rx.var
    def filtered_items(self) -> list[Item]:
        """Get filtered items based on search."""
        filtered = self.items
        
        if self.search_value:
            search_lower = self.search_value.lower()
            filtered = [
                item for item in filtered
                if (search_lower in item.name.lower() or
                    search_lower in item.description.lower() or
                    search_lower in item.category.lower())
            ]
        
        # Sort
        reverse = self.sort_direction == "desc"
        filtered.sort(key=lambda x: getattr(x, self.sort_column), reverse=reverse)
        
        return filtered
    
    @rx.var
    def paginated_items(self) -> list[Item]:
        """Get paginated items."""
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_items[start:end]
    
    @rx.var
    def total_pages(self) -> int:
        """Get total pages."""
        return max(1, (len(self.filtered_items) + self.items_per_page - 1) // self.items_per_page)
    
    def set_search_value(self, value: str):
        """Set search value."""
        self.search_value = value
        self.current_page = 1
    
    def set_sort_column(self, column: str):
        """Set sort column."""
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
    
    def prev_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
    
    def go_to_page(self, page: int):
        """Go to specific page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page