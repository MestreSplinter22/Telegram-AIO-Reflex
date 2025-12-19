import reflex as rx
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)


def notification(icon: str, color: LiteralAccentColor, count: int) -> rx.Component:
    return rx.box(
        rx.icon_button(
            rx.icon(icon),
            class_name="p-2 rounded-full bg-muted text-muted-foreground",
            variant="soft",
            color_scheme=color,
            size="3",
        ),
        rx.badge(
            rx.text(count, size="1"),
            class_name="absolute -top-1 -right-1 rounded-full bg-destructive text-destructive-foreground",
            variant="solid",
            color_scheme=color,
        ),
        class_name="relative",
    )
