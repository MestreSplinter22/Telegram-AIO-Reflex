import reflex as rx
from dashboard.components.ui.template.navbar import navbar
from dashboard.components.ui.template.sidebar import sidebar
from dashboard.backend.states.flow_state import FlowState

# --- ADICIONE ESTE DECORADOR ---
@rx.page(route="/flows", title="Bot Flow Builder")
def flow_builder_page() -> rx.Component:
    return rx.box(
        rx.flex(
            sidebar(),
            rx.box(
                navbar(),
                rx.box(
                    # --- CONTEÚDO PRINCIPAL ---
                    rx.flex(
                        # Coluna 1: Lista de Telas
                        rx.card(
                            rx.heading("Telas do Bot", size="3", mb="4"),
                            rx.scroll_area(
                                rx.vstack(
                                    rx.foreach(
                                        FlowState.screen_keys,
                                        lambda key: rx.button(
                                            key,
                                            variant="ghost",
                                            width="100%",
                                            justify_content="start",
                                            on_click=lambda: FlowState.select_screen(key),
                                            color_scheme=rx.cond(
                                                FlowState.selected_screen_key == key,
                                                "blue",
                                                "gray"
                                            )
                                        )
                                    ),
                                    spacing="2",
                                    align_items="stretch",
                                ),
                                h="600px",
                            ),
                            # Input para adicionar nova tela
                            rx.divider(my="4"),
                            rx.hstack(
                                rx.input(
                                    placeholder="Nome da nova tela (ex: menu_vip)",
                                    value=FlowState.new_screen_name,
                                    on_change=FlowState.set_new_screen_name
                                ),
                                rx.button("+", on_click=FlowState.add_new_screen)
                            ),
                            width="25%",
                            min_width="250px",
                            mr="4"
                        ),
                        
                        # Coluna 2: Editor JSON
                        rx.card(
                            rx.flex(
                                rx.heading(f"Editando: {FlowState.selected_screen_key}", size="3"),
                                rx.spacer(),
                                rx.text(FlowState.status_message, color="gray", size="2"),
                                rx.button("SALVAR ALTERAÇÕES", color_scheme="green", on_click=FlowState.save_current_screen),
                                width="100%",
                                align="center",
                                mb="4"
                            ),
                            rx.text_area(
                                value=FlowState.current_screen_content,
                                on_change=FlowState.update_content,
                                height="600px",
                                font_family="monospace",
                                font_size="14px",
                                bg="gray.5",
                            ),
                            rx.text(
                                "Dica: Você pode usar Listas [...] para mensagens sequenciais ou Objetos {...} para mensagem única.",
                                size="1",
                                color="gray",
                                mt="2"
                            ),
                            width="75%"
                        ),
                        width="100%",
                        align_items="start"
                    ),
                    p="6",
                    width="100%",
                    min_height="100vh",
                    bg="gray.2",
                ),
                width="100%",
                display="flex",
                flex_direction="column",
            ),
            width="100%",
            display="flex",
        ),
        on_mount=FlowState.load_flow
    )