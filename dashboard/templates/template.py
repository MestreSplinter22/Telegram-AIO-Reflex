"""Common templates used between pages in the app."""

from __future__ import annotations

from typing import Callable

import reflex as rx

from .. import styles
from ..components.ui.template.navbar import navbar
from ..components.ui.template.sidebar import sidebar

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


def menu_item_link(text, href):
    return rx.menu.item(
        rx.link(
            text,
            href=href,
            width="100%",
            color="inherit",
        ),
        _hover={
            "color": styles.accent_color,
            "background_color": styles.accent_text_color,
        },
    )


class ThemeState(rx.State):
    """The state for the theme of the app."""

    accent_color: str = "crimson"

    gray_color: str = "gray"

    radius: str = "large"

    scaling: str = "100%"


ALL_PAGES = []


def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventType[()] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app.

    Args:
        route: The route to reach the page.
        title: The title of the page.
        description: The description of the page.
        meta: Additional meta to add to the page.
        on_load: The event handler(s) called when the page load.
        script_tags: Scripts to attach to the page.

    Returns:
        The template with the page content.

    """

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        """The template for each page of the app.

        Args:
            page_content: The content of the page.

        Returns:
            The template with the page content.

        """
        # Get the meta tags for the page.
        all_meta = [*default_meta, *(meta or [])]

        def templated_page():
            return rx.box(
                rx.box(
                    navbar(),
                    class_name="sticky top-0 z-50"
                ),
                rx.flex(
                    sidebar(),
                    rx.box(
                        rx.box(
                            class_name="absolute inset-0 bg-gradient-to-br from-background/90 via-[#0f0f0f]/80 to-[#1a1a1a]/90 dark:from-background/90 dark:via-[#0a0a0a]/80 dark:to-[#161616]/90 backdrop-blur-sm z-0"
                        ),
                        rx.box(
                            class_name="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/5 via-transparent to-transparent dark:from-primary/10 z-0"
                        ),
                        rx.box(
                            class_name="absolute inset-0 bg-[linear-gradient(to_right,#8882_1px,transparent_1px),linear-gradient(to_bottom,#8882_1px,transparent_1px)] bg-[size:20px_20px] dark:opacity-30 z-0"
                        ),
                        rx.box(
                            page_content(),
                            class_name="relative z-10 w-full p-4 md:p-6 lg:p-8",
                        ),
                        class_name="relative flex-1 min-h-[calc(100vh-64px)] bg-gradient-to-br from-background via-[#0f0f0f] to-[#1a1a1a] dark:from-background dark:via-[#0a0a0a] dark:to-[#161616] transition-all duration-500",
                    ),
                    class_name="flex flex-col md:flex-row"
                ),
                class_name="w-full min-h-screen"
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap():
            return rx.theme(
                templated_page(),
                has_background=True,
                accent_color=ThemeState.accent_color,
                gray_color=ThemeState.gray_color,
                radius=ThemeState.radius,
                scaling=ThemeState.scaling,
            )

        ALL_PAGES.append(
            {
                "route": route,
            }
            | ({"title": title} if title is not None else {})
        )

        return theme_wrap

    return decorator
