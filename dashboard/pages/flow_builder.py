import reflex as rx
from dashboard.components.ui.template.navbar import navbar
from dashboard.components.ui.template.sidebar import sidebar
from dashboard.backend.states.flow_state import FlowState
from dashboard.components.flow_editor import flow_editor_component

# Importamos do nosso wrapper local criado no passo anterior
from dashboard.components.react_flow_wrapper import ReactFlow, Background, Controls, MiniMap

@rx.page(route="/flows", title="Bot Flow Builder")
def flow_builder_page() -> rx.Component:
    return rx.box(
        rx.flex(
            sidebar(),
            rx.box(
                navbar(),
                rx.box(
                    rx.grid(
                        # === COLUNA 1: FLUXO INTERATIVO ===
                        rx.card(
                            rx.hstack(
                                rx.heading("Fluxo Interativo", size="3"),
                                rx.spacer(),
                                rx.badge("React Flow", color_scheme="blue"),
                                rx.icon_button("rotate-cw", on_click=FlowState.calculate_interactive_layout, variant="ghost", size="1")
                            ),
                            rx.divider(my="2"),
                            
                            # --- CORREÇÃO AQUI ---
                            rx.box(
                                ReactFlow.create(
                                    # 1. Filhos passados como argumentos posicionais (sem children=)
                                    Background.create(variant="dots", gap=20, size=1, color="#cbd5e1"),
                                    Controls.create(),
                                    MiniMap.create(),
                                    
                                    # 2. Props passadas como argumentos nomeados
                                    nodes=FlowState.nodes,
                                    edges=FlowState.edges,
                                    on_node_click=FlowState.on_node_click,
                                    fit_view=True,
                                ),
                                # Estilos do container
                                width="100%",
                                height="600px", 
                                border_radius="md",
                                border="1px solid #e2e8f0",
                                overflow="hidden",
                                bg="#f8fafc"
                            ),
                            
                            # Input inferior
                            rx.hstack(
                                rx.input(
                                    placeholder="Nova tela...", 
                                    value=FlowState.new_screen_name, 
                                    on_change=FlowState.set_new_screen_name,
                                    size="2", width="60%"
                                ),
                                rx.button("Criar", on_click=FlowState.add_new_screen, size="2", width="40%"),
                                mt="4", width="100%"
                            ),
                            height="100%",
                            max_height="90vh",
                            overflow="hidden",
                            display="flex",
                            flex_direction="column"
                        ),
                        
                        # === COLUNA 2: EDITOR ===
                        rx.card(
                            rx.flex(
                                rx.heading(f"Editando: {FlowState.selected_screen_key}", size="3"),
                                rx.spacer(),
                                rx.hstack(
                                    rx.text("Visual", font_size="2"),
                                    rx.switch(
                                        is_checked=FlowState.visual_editor_mode,
                                        on_change=FlowState.toggle_editor_mode
                                    ),
                                    align="center"
                                ),
                                width="100%",
                                align="center",
                                mb="4"
                            ),
                            rx.divider(mb="4"),
                            
                            rx.box(
                                rx.cond(
                                    FlowState.visual_editor_mode,
                                    flow_editor_component(),
                                    rx.text_area(
                                        value=FlowState.current_screen_content,
                                        on_change=FlowState.update_content,
                                        height="600px",
                                        font_family="monospace",
                                        bg="#0f172a", color="#e2e8f0"
                                    )
                                ),
                                flex="1", overflow_y="auto", width="100%"
                            ),
                            
                            rx.box(
                                rx.divider(my="4"),
                                rx.button(
                                    "SALVAR ALTERAÇÕES", 
                                    color_scheme="green", width="100%",
                                    on_click=FlowState.save_current_screen
                                ),
                                width="100%", mt="auto"
                            ),
                            height="85vh",
                            display="flex", flex_direction="column"
                        ),
                        
                        columns="2fr 1fr",
                        gap="4",
                        width="100%",
                        height="85vh"
                    ),
                    p="6", width="100%", min_height="100vh", bg="gray.2",
                ),
                width="100%", display="flex", flex_direction="column",
            ),
            width="100%", display="flex",
        ),
        on_mount=FlowState.load_flow
    )