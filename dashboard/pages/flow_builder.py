import reflex as rx
from dashboard.components.ui.template.navbar import navbar
from dashboard.components.ui.template.sidebar import sidebar
from dashboard.backend.states.flow_state import FlowState

# --- COMPONENTE DE NÓ (CARD) ---
def render_node(node: dict):
    """Renderiza um único nó. Se for 'missing', fica vermelho."""
    
    # Cores condicionais
    # Se estiver selecionado: Azul Escuro
    # Se estiver faltando (missing): Vermelho Claro
    # Padrão: Branco
    bg_color = rx.cond(
        FlowState.selected_screen_key == node["id"], 
        "#1e293b", 
        rx.cond(node["missing"], "#fef2f2", "#ffffff")
    )
    
    border_color = rx.cond(
        FlowState.selected_screen_key == node["id"], 
        "#3b82f6", 
        rx.cond(node["missing"], "#ef4444", "#e2e8f0")
    )
    
    text_color = rx.cond(
        FlowState.selected_screen_key == node["id"], 
        "white", 
        rx.cond(node["missing"], "#b91c1c", "black")
    )

    return rx.box(
        rx.vstack(
            rx.text(node["label"], font_weight="bold", font_size="14px", is_truncated=True, width="100%"),
            rx.text("ID: ", node["id"], font_size="10px", opacity=0.7),
            
            # Aviso se for link quebrado
            rx.cond(
                node["missing"],
                rx.text("⚠️ Não Criado", font_size="10px", color="red", font_weight="bold")
            ),
            
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
        border=f"2px solid",
        border_color=border_color,
        border_radius="lg",
        shadow="lg",
        padding="4",
        cursor="pointer",
        on_click=lambda: FlowState.select_screen(node["id"]),
        z_index="10"
    )

# --- PÁGINA PRINCIPAL ---
@rx.page(route="/flows", title="Bot Flow Builder")
def flow_builder_page() -> rx.Component:
    return rx.box(
        rx.flex(
            sidebar(),
            rx.box(
                navbar(),
                rx.box(
                    # --- CONTEÚDO PRINCIPAL ---
                    rx.grid(
                        # COLUNA 1: CANVAS INTERATIVO
                        rx.card(
                            rx.hstack(
                                rx.heading("Fluxo Interativo", size="3"),
                                rx.spacer(),
                                rx.icon_button("rotate-cw", on_click=FlowState.calculate_interactive_layout, variant="ghost", size="1")
                            ),
                            rx.divider(my="2"),
                            
                            # O CANVAS
                            rx.box(
                                # --- CORREÇÃO: Renderiza o SVG gerado pelo Python ---
                                rx.html(FlowState.svg_content),
                                # ----------------------------------------------------

                                # Camada de Nós (Renderizados pelo Reflex)
                                rx.foreach(FlowState.graph_nodes, render_node),
                                
                                width="100%",
                                height="650px",
                                bg="#f8fafc",
                                border_radius="md",
                                position="relative",
                                overflow="scroll",
                                background_image="radial-gradient(#cbd5e1 1px, transparent 1px)",
                                background_size="20px 20px"
                            ),
                            
                            # Barra inferior
                            rx.hstack(
                                rx.input(
                                    placeholder="Nova tela (ex: menu_suporte)", 
                                    value=FlowState.new_screen_name, 
                                    on_change=FlowState.set_new_screen_name,
                                    size="2",
                                    width="60%"
                                ),
                                rx.button("Criar Tela", on_click=FlowState.add_new_screen, size="2", width="40%"),
                                mt="4",
                                width="100%"
                            ),
                            height="100%"
                        ),
                        
                        # COLUNA 2: EDITOR JSON
                        rx.card(
                            rx.flex(
                                rx.heading(f"Editando: {FlowState.selected_screen_key}", size="3"),
                                rx.spacer(),
                                rx.badge(FlowState.status_message, variant="outline"),
                                rx.button("SALVAR ALTERAÇÕES", color_scheme="green", on_click=FlowState.save_current_screen),
                                width="100%",
                                align="center",
                                mb="4"
                            ),
                            rx.text_area(
                                value=FlowState.current_screen_content,
                                on_change=FlowState.update_content,
                                height="650px",
                                font_family="monospace",
                                font_size="13px",
                                bg="#1e293b", 
                                color="#e2e8f0"
                            ),
                            rx.text(
                                "Dica: Use [...] para sequência de mensagens.",
                                size="1",
                                color="gray",
                                mt="2"
                            ),
                            height="100%"
                        ),
                        
                        columns="2fr 1fr",
                        gap="4",
                        width="100%",
                        height="85vh"
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