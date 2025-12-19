import reflex as rx

from dashboard import styles


def card(*children, **props):
    """Card component with Tailwind CSS styling using theme variables."""
    # Merge provided class_name with default styling
    provided_class_name = props.pop('class_name', '')
    default_class_name = "bg-card text-card-foreground border border-border rounded-lg shadow-lg"
    combined_class_name = f"{default_class_name} {provided_class_name}".strip()
    
    return rx.card(
        *children,
        class_name=combined_class_name,
        **props,
    )
