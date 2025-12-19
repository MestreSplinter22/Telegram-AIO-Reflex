"""Styles for the app using Tailwind CSS classes."""
import reflex as rx

# Tailwind CSS utility classes for consistent styling
border_radius = "rounded-lg"
border = "border border-border"
text_color = "text-foreground"
gray_color = "text-muted-foreground"
gray_bg_color = "bg-muted"
accent_text_color = "text-accent"
accent_color = "bg-accent"
accent_bg_color = "bg-accent/10"
hover_accent_color = "hover:text-accent"
hover_accent_bg = "hover:bg-accent/20"
content_width_vw = "w-[90vw]"
sidebar_width = "w-[32em]"
sidebar_content_width = "w-[16em]"
max_width = "max-w-[1480px]"
color_box_size = ["w-[2.25rem] h-[2.25rem]", "w-[2.25rem] h-[2.25rem]", "w-[2.5rem] h-[2.5rem]"]

# Template styling using Tailwind classes
template_page_style = {
    "class_name": "pt-4 md:pt-8 px-auto md:px-8",
}

template_content_style = {
    "class_name": "p-4 mb-8 min-h-[90vh]",
}

link_style = {
    "class_name": "text-foreground no-underline hover:text-accent",
}

overlapping_button_style = {
    "class_name": "bg-white rounded-lg",
}

markdown_style = {
    "code": lambda text: rx.code(text, class_name="text-sm"),
    "codeblock": lambda text, **props: rx.code_block(text, **props, class_name="my-4"),
    "a": lambda text, **props: rx.link(
        text,
        **props,
        class_name="font-bold underline decoration-accent hover:decoration-accent/80",
    ),
}

notification_badge_style = {
    "class_name": "w-5 h-5 flex items-center justify-center absolute -right-1 -top-1",
}

ghost_input_style = {
    "class_name": "bg-transparent border-transparent focus:border-transparent focus:ring-0",
}

box_shadow_style = "shadow-md"

color_picker_style = {
    "class_name": "rounded-full shadow-md cursor-pointer flex items-center justify-center transition-transform active:scale-95 active:translate-y-0.5",
}

base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    "styles.css",
]

base_style = {
    "class_name": "font-sans",
}
