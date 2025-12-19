"""Revenue chart component for gift card dashboard."""

import reflex as rx
from ...backend.states.dashboard import DashboardState


def revenue_chart() -> rx.Component:
    """Revenue chart showing daily performance."""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("trending-up", size=22, style={"color": "var(--icon-tertiary)"}),
            rx.text("Performance Financeira", class_name="text-xl font-semibold text-foreground"),
            class_name="justify-center items-center gap-2",
        ),
        rx.box(class_name="border-b border-border w-full my-2"),

        # Chart container
        rx.box(
            rx.recharts.line_chart(
                rx.recharts.line(
                    data_key="revenue",
                    stroke=rx.color("yellow", 9),
                    stroke_width=2,
                    dot=False,
                ),
                rx.recharts.x_axis(
                    data_key="day",
                    stroke=rx.color("gray", 8),
                    font_size=12,
                ),
                rx.recharts.y_axis(
                    stroke=rx.color("gray", 8),
                    font_size=12,
                    tick_formatter="R${value}"
                ),
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    stroke=rx.color("gray", 5),
                ),
                rx.recharts.tooltip(
                    content_style={
                        "backgroundColor": rx.color("gray", 1),
                        "borderRadius": "var(--radius-2)",
                        "border": f"1px solid {rx.color('gray', 5)}",
                    },
                    formatter="R${value}"
                ),
                data=[
                    {"day": "Seg", "revenue": 1250},
                    {"day": "Ter", "revenue": 1890},
                    {"day": "Qua", "revenue": 2340},
                    {"day": "Qui", "revenue": 1980},
                    {"day": "Sex", "revenue": 2890},
                    {"day": "Sáb", "revenue": 3200},
                    {"day": "Dom", "revenue": 2780},
                ],
                width="100%",
                height=300,
            ),
            class_name="w-full max-w-3xl mx-auto",
        ),
        spacing="3",
        class_name="w-full h-full p-4 md:p-6",
    )