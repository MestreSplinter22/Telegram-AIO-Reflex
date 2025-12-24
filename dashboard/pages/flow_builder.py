import reflex as rx
from dashboard.components.ui.template.navbar import navbar
from dashboard.components.ui.template.sidebar import sidebar
from dashboard.backend.states.flow_state import FlowState
from dashboard.components.flow_editor import flow_editor_component

# Importamos do nosso wrapper local
from dashboard.components.react_flow_wrapper import ReactFlow, Background, Controls, MiniMap

# --- DESIGN SYSTEM COMPARTILHADO ---
THEME = {
    "app_bg": rx.color("gray", 1),          # Fundo geral da aplicação
    "panel_bg": rx.color("gray", 2),        # Fundo dos painéis (Canvas/Editor)
    "header_bg": rx.color("gray", 2),       # Fundo dos headers (Toolbars)
    "border_subtle": rx.color("gray", 4),   # Bordas divisórias
    "border_strong": rx.color("gray", 6),   # Bordas de destaque
    "text_primary": rx.color("gray", 12),   # Texto principal
    "text_secondary": rx.color("gray", 10), # Labels e instruções
    "accent": rx.color("indigo", 9),        # Ação principal (Botões/Destaques)
    "input_bg": rx.color("gray", 3),        # Inputs
}

# Estilos de Texto Utilitários
LABEL_STYLE = {
    "font_size": "10px",
    "font_weight": "bold",
    "color": THEME["text_secondary"],
    "letter_spacing": "0.05em",
    "text_transform": "uppercase",
}

@rx.page(route="/flows", title="Bot Flow Builder")
def flow_builder_page() -> rx.Component:
    return rx.box(
        rx.flex(
            sidebar(),
            rx.box(
                navbar(),
                rx.box(
                    rx.grid(
                        # =========================================
                        # === COLUNA 1: FLUXO INTERATIVO (CANVAS) ===
                        # =========================================
                        rx.box(
                            # 1. Header (Toolbar)
                            rx.hstack(
                                rx.box(
                                    rx.text("VISUALIZAÇÃO", **LABEL_STYLE),
                                    rx.heading("Fluxo Interativo", size="3", color=THEME["text_primary"]),
                                    line_height="1.2"
                                ),
                                rx.spacer(),
                                # Controles do Header
                                rx.hstack(
                                    rx.badge("React Flow", color_scheme="indigo", variant="surface"),
                                    rx.tooltip(
                                        rx.icon_button(
                                            "rotate-cw", 
                                            on_click=FlowState.calculate_interactive_layout, 
                                            variant="soft", color_scheme="gray", size="2"
                                        ),
                                        content="Reorganizar Layout Automaticamente"
                                    ),
                                    spacing="3"
                                ),
                                width="100%",
                                align="center",
                                padding="16px",
                                border_bottom=f"1px solid {THEME['border_subtle']}",
                                bg=THEME["header_bg"],
                                height="70px"
                            ),
                            
                            # 2. Área do Canvas (React Flow)
                            rx.box(
                                ReactFlow.create(
                                    # Plugins visuais
                                    Background.create(
                                        variant="dots", 
                                        gap=24, 
                                        size=1, 
                                        # CORREÇÃO 1: Convertendo cor para string
                                        # Alterado para cinza claro para melhor design do canvas
                                        color=str(rx.color("white", 3)) 
                                    ),
                                    
                                    # Props Lógicas
                                    nodes=FlowState.nodes,
                                    edges=FlowState.edges,
                                    on_node_click=FlowState.on_node_click,
                                    fit_view=True,
                                ),
                                width="100%",
                                flex="1", 
                                bg=THEME["panel_bg"], 
                                overflow="hidden"
                            ),
                            
                            # 3. Footer de Ação
                            rx.box(
                                rx.hstack(
                                    rx.icon("plus-square", size=18, color=THEME["text_secondary"]),
                                    rx.input(
                                        placeholder="Nome da nova tela (ID único)...", 
                                        value=FlowState.new_screen_name, 
                                        on_change=FlowState.set_new_screen_name,
                                        size="2", 
                                        variant="soft", 
                                        bg=THEME["input_bg"],
                                        color_scheme="gray",
                                        width="100%",
                                        border=f"1px solid {THEME['border_subtle']}",
                                        _focus={"border_color": THEME["accent"]}
                                    ),
                                    rx.button(
                                        "Criar Tela", 
                                        icon="plus",
                                        on_click=FlowState.add_new_screen, 
                                        size="2", 
                                        variant="solid",
                                        color_scheme="indigo",
                                        cursor="pointer"
                                    ),
                                    width="100%",
                                    align="center",
                                    spacing="3"
                                ),
                                padding="12px 16px",
                                border_top=f"1px solid {THEME['border_subtle']}",
                                bg=THEME["header_bg"]
                            ),
                            
                            # Estilos Container Coluna 1
                            height="85vh",
                            display="flex",
                            flex_direction="column",
                            bg=THEME["panel_bg"],
                            border=f"1px solid {THEME['border_subtle']}",
                            border_radius="lg",
                            overflow="hidden",
                            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
                        ),
                        
                        # =========================================
                        # === COLUNA 2: EDITOR VISUAL ===
                        # =========================================
                        rx.box(
                            # 1. Header Fixo
                            rx.hstack(
                                rx.box(
                                    rx.text("PROPRIEDADES", **LABEL_STYLE),
                                    rx.heading(FlowState.selected_screen_key, size="3", color="white", truncate=True),
                                    line_height="1.2"
                                ),
                                rx.spacer(),
                                rx.segmented_control.root(
                                    rx.segmented_control.item(
                                        rx.icon("layout-list", size=16), 
                                        value="visual",
                                        padding_x="2"
                                    ), 
                                    rx.segmented_control.item(
                                        rx.icon("code", size=16), 
                                        value="json",
                                        padding_x="2"
                                    ),
                                    value=rx.cond(FlowState.visual_editor_mode, "visual", "json"),
                                    on_change=FlowState.set_editor_mode,
                                    size="1",
                                    variant="surface"
                                ),
                                width="100%",
                                align="center",
                                padding="16px",
                                border_bottom=f"1px solid {THEME['border_subtle']}",
                                bg=THEME["header_bg"],
                                height="70px"
                            ),
                            
                            # 2. Área de Conteúdo
                            rx.box(
                                rx.cond(
                                    FlowState.visual_editor_mode,
                                    flow_editor_component(), 
                                    rx.box(
                                        rx.text_area(
                                            value=FlowState.current_screen_content,
                                            on_change=FlowState.update_content,
                                            height="100%",
                                            font_family="'Fira Code', monospace",
                                            font_size="12px",
                                            bg=rx.color("gray", 1), 
                                            color="#cbd5e1",
                                            border="none",
                                            padding="16px",
                                            _focus={"outline": "none"}
                                        ),
                                        height="100%",
                                        width="100%"
                                    )
                                ),
                                flex="1",
                                overflow="hidden",
                                position="relative"
                            ),
                            
                            # 3. Footer de Ação
                            rx.box(
                                rx.hstack(
                                    rx.hstack(
                                        # CORREÇÃO 2: Removi o spinner que dependia de 'is_saving'
                                        # Se quiser reativar depois, adicione is_saving: bool = False ao FlowState
                                        rx.icon("check-circle", size=16, color="green"), 
                                        rx.text(FlowState.status_message, font_size="11px", color=THEME["text_secondary"]),
                                        spacing="2",
                                        align="center"
                                    ),
                                    rx.spacer(),
                                    rx.button(
                                        "Salvar Alterações",
                                        icon="save",
                                        color_scheme="indigo", 
                                        variant="surface",
                                        on_click=FlowState.save_current_screen,
                                        size="2",
                                        cursor="pointer"
                                    ),
                                    width="100%",
                                    align="center"
                                ),
                                padding="12px 16px",
                                border_top=f"1px solid {THEME['border_subtle']}",
                                bg=THEME["header_bg"]
                            ),
                            
                            # Estilos Container Coluna 2
                            bg=THEME["panel_bg"],
                            border=f"1px solid {THEME['border_subtle']}",
                            border_radius="lg",
                            height="85vh",
                            display="flex", 
                            flex_direction="column",
                            overflow="hidden",
                            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)"
                        ),
                        
                        columns="2fr 1fr",
                        gap="4",
                        width="100%",
                        height="85vh"
                    ),
                    padding="24px", 
                    width="100%", 
                    min_height="100vh", 
                    bg=THEME["app_bg"]
                ),
                width="100%", display="flex", flex_direction="column",
            ),
            width="100%", display="flex",
        ),
        on_mount=FlowState.load_flow
    )