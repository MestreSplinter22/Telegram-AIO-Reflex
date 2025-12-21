import reflex as rx
from dashboard.components.ui.template.navbar import navbar
from dashboard.components.ui.template.sidebar import sidebar
from dashboard.backend.states.flow_state import FlowState
from dashboard.components.flow_editor import flow_editor_component

# IMPORTAMOS O COMPONENTE QUE CRIAMOS ACIMA
# (Certifique-se que o caminho do import esteja correto base na sua estrutura)
from dashboard.components.zoom import ZoomPanPinch, ZoomContent

# --- COMPONENTE DE NÓ (CARD) ---
def render_node(node: dict):
    bg_color = rx.cond(
        FlowState.selected_screen_key == node["id"], 
        "#1e293b", 
        rx.cond(node["missing"], "#fef2f2", "#ffffff")
    )
    
    text_color = rx.cond(
        FlowState.selected_screen_key == node["id"], 
        "white", 
        rx.cond(node["missing"], "#b91c1c", "black")
    )
    
    border_color = rx.cond(
        FlowState.selected_screen_key == node["id"], 
        "#3b82f6", 
        rx.cond(node["missing"], "#ef4444", "#e2e8f0")
    )

    return rx.box(
        rx.vstack(
            rx.text(node["label"], font_weight="bold", font_size="14px", is_truncated=True, width="100%"),
            rx.text(node["id"], font_size="10px", opacity=0.7),
            rx.cond(node["missing"], rx.text("⚠️ Link Quebrado", font_size="10px", color="red")),
            spacing="1",
            align_items="start",
            width="100%"
        ),
        position="absolute",
        left=f"{node['x']}px",
        top=f"{node['y']}px",
        width="220px",
        height="100px",
        bg=bg_color,
        color=text_color,
        border="2px solid",
        border_color=border_color,
        border_radius="lg",
        shadow="lg",
        padding="4",
        cursor="pointer",
        # Importante: on_click aqui funciona nativamente sem hacks
        on_click=lambda: FlowState.select_screen(node["id"]),
        z_index="10",
        _hover={"transform": "scale(1.02)", "transition": "0.1s"}
    )

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
                                rx.badge("Zoom & Pan Ativos", color_scheme="green"),
                                rx.icon_button("rotate-cw", on_click=FlowState.calculate_interactive_layout, variant="ghost", size="1")
                            ),
                            rx.divider(my="2"),
                            
                            # --- AQUI ESTÁ A MÁGICA ---
                            # O componente React vai gerenciar todo o Drag e Zoom
                            rx.box(
                                ZoomPanPinch.create(
                                    ZoomContent.create(
                                        # O CONTEÚDO GIGANTE
                                        rx.box(
                                            # Grid de fundo (agora parte do conteúdo, move junto)
                                            rx.box(
                                                width="5000px", height="5000px",
                                                background_image="radial-gradient(#94a3b8 1px, transparent 1px)",
                                                background_size="20px 20px",
                                                opacity="0.4",
                                                position="absolute", top="-1000px", left="-1000px",
                                                pointer_events="none"
                                            ),
                                            
                                            # Linhas SVG
                                            rx.html(FlowState.svg_content),
                                            
                                            # Nós
                                            rx.foreach(FlowState.graph_nodes, render_node),
                                            
                                            # Tamanho da área "clicável" interna
                                            width="100%", 
                                            height=FlowState.canvas_height,
                                            position="relative",
                                        ),
                                    ),
                                    # Props do Wrapper
                                    initial_scale=1.0,
                                    min_scale=0.1,
                                    max_scale=4.0,
                                    limit_to_bounds=False, # Importante para Canvas Infinito
                                    # Estilo do container PAI (a janela visível)
                                    style={
                                        "width": "100%", 
                                        "height": "100%", 
                                        "cursor": "grab",
                                        "background": "#f8fafc"
                                    }
                                ),
                                # O box container precisa ter tamanho definido para o plugin funcionar
                                width="100%",
                                height="100%",
                                overflow="hidden",
                                border_radius="md",
                                border="1px solid #e2e8f0"
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