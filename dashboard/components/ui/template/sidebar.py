"""Sidebar component for the app."""

import reflex as rx


def sidebar_header() -> rx.Component:
    """Sidebar header.

    Returns:
        The sidebar header component.

    """
    return rx.hstack(
        # The logo.
        rx.color_mode_cond(
            rx.image(src="/reflex_black.svg", height="1.5em"),
            rx.image(src="/reflex_white.svg", height="1.5em"),
        ),
        rx.spacer(),
        align="center",
        width="100%",
        class_name="p-1.5 mb-4",
    )


def sidebar_footer() -> rx.Component:
    """Sidebar footer.

    Returns:
        The sidebar footer component.

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
        class_name="p-1.5",
    )


def sidebar_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=18)


def sidebar_item(text: str, url: str) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.

    """
    # Whether the item is active.
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & text == "Overview"
    )

    return rx.link(
        rx.hstack(
            rx.match(
                text,
                ("Overview", sidebar_item_icon("home")),
                ("Users", sidebar_item_icon("users")),
                ("Transactions", sidebar_item_icon("credit-card")),
                ("Gift Cards", sidebar_item_icon("gift")),
                ("Bot Management", sidebar_item_icon("bot")),
                ("Settings", sidebar_item_icon("settings")),
                ("Bot Flow Builder", sidebar_item_icon("git-merge")),
                sidebar_item_icon("layout-dashboard"),
            ),
            rx.text(text, size="3", weight="regular"),
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


def sidebar() -> rx.Component:
    """The sidebar.

    Returns:
        The sidebar component.
    """
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

    return rx.flex(
        rx.vstack(
            sidebar_header(),
            rx.vstack(
                *[
                    sidebar_item(
                        text=page.get("title", page["route"].strip("/").capitalize()),
                        url=page["route"],
                    )
                    for page in ordered_pages
                ],
                spacing="1",
                width="100%",
            ),
            rx.spacer(),
            sidebar_footer(),
            justify="end",
            align="end",
            width="100%",
            height="100dvh",
            class_name="p-4 bg-navbar",
        ),
        display=["none", "none", "none", "none", "none", "flex"],
        max_width="250px",
        width="auto",
        height="100%",
        position="sticky",
        justify="end",
        top="0px",
        left="0px",
        flex="1",
        class_name="bg-navbar",
    )
