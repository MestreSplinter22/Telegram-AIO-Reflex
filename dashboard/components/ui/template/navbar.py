"""Navbar component for the app."""

import reflex as rx


def menu_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=20)


def menu_item(text: str, url: str) -> rx.Component:
    """Menu item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The menu item component.

    """
    # Whether the item is active.
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & text == "Overview"
    )

    return rx.link(
        rx.hstack(
            rx.match(
                text,
                ("Overview", menu_item_icon("home")),
                ("Users", menu_item_icon("users")),
                ("Transactions", menu_item_icon("credit-card")),
                ("Gift Cards", menu_item_icon("gift")),
                ("Bot Management", menu_item_icon("bot")),
                ("Settings", menu_item_icon("settings")),
                menu_item_icon("layout-dashboard"),
            ),
            rx.text(text, size="4", weight="regular"),
            class_name=rx.cond(
                active,
                "text-primary",
                "text-foreground",
            ),
            opacity=rx.cond(
                active,
                "1",
                "0.95",
            ),
            align="center",
            border_radius="md",
            width="100%",
            spacing="2",
            padding="0.35em",
            transition="all 0.2s",
            _hover={
                "background_color": rx.cond(
                    active,
                    "var(--accent)",
                    "var(--muted)",
                ),
                "background_opacity": "0.5",
            },
        ),
        underline="none",
        href=url,
        width="100%",
    )


def navbar_footer() -> rx.Component:
    """Navbar footer.

    Returns:
        The navbar footer component.

    """
    return rx.hstack(
        rx.link(
            rx.text("Docs", size="3"),
            href="https://reflex.dev/docs/getting-started/introduction/",
            class_name="text-muted-foreground hover:text-foreground",
            underline="none",
        ),
        rx.link(
            rx.text("Blog", size="3"),
            href="https://reflex.dev/blog/",
            class_name="text-muted-foreground hover:text-foreground",
            underline="none",
        ),
        rx.spacer(),
        rx.color_mode.button(class_name="opacity-80 scale-95"),
        justify="start",
        align="center",
        width="100%",
        padding="0.35em",
    )


def menu_button() -> rx.Component:
    from reflex.page import DECORATED_PAGES

    ordered_page_routes = [
        "/",
        "/users",
        "/transactions",
        "/products",
        "/bot-management",
        "/flows",
        "/settings",
    ]

    pages = [
        page_dict
        for page_list in DECORATED_PAGES.values()
        for _, page_dict in page_list
    ]

    ordered_pages = sorted(
        pages,
        key=lambda page: (
            ordered_page_routes.index(page["route"])
            if page["route"] in ordered_page_routes
            else len(ordered_page_routes)
        ),
    )

    return rx.drawer.root(
        rx.drawer.trigger(
            rx.icon("align-justify"),
        ),
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                    rx.vstack(
                        rx.hstack(
                            rx.spacer(),
                            rx.drawer.close(rx.icon(tag="x")),
                            justify="end",
                            width="100%",
                        ),
                        rx.divider(),
                        *[
                            menu_item(
                                text=page.get(
                                    "title", page["route"].strip("/").capitalize()
                                ),
                                url=page["route"],
                            )
                            for page in ordered_pages
                        ],
                        rx.spacer(),
                        navbar_footer(),
                        spacing="4",
                        width="100%",
                        class_name="bg-navbar",
                    ),
                    top="auto",
                    left="auto",
                    height="100%",
                    width="20em",
                    padding="1em",
                    class_name="bg-navbar border-l border-border",
                ),
            width="100%",
        ),
        direction="right",
    )


def navbar() -> rx.Component:
    """The navbar.

    Returns:
        The navbar component.

    """
    return rx.el.nav(
        rx.hstack(
            # The logo.
            rx.color_mode_cond(
                rx.image(src="/reflex_black.svg", height="1em"),
                rx.image(src="/reflex_white.svg", height="1em"),
            ),
            rx.spacer(),
            menu_button(),
            align="center",
            width="100%",
            padding_y="1.25em",
            padding_x=["1em", "1em", "2em"],
        ),
        display=["block", "block", "block", "block", "block", "none"],
        position="sticky",
        class_name="bg-navbar border-b border-border",
        top="0px",
        z_index="5",
    )
