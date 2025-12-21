import reflex as rx
from dashboard.backend.states.flow_state import FlowState

def render_button_editor(block_idx: int, row_idx: int, btn_idx: int, btn_data: dict):
    """Renderiza a edição de um único botão."""
    
    # Casting de segurança para garantir que btn_data seja tratado como dict
    btn = btn_data.to(dict)
    is_url = btn.contains("url")
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Botão ", row_idx + 1, "-", btn_idx + 1, font_weight="bold", font_size="10px"),
                rx.spacer(),
                rx.icon_button(
                    "trash-2", 
                    size="1", 
                    variant="ghost", 
                    color_scheme="red",
                    on_click=lambda: FlowState.remove_button(block_idx, row_idx, btn_idx)
                )
            ),
            rx.input(
                value=btn["text"],
                placeholder="Texto do Botão",
                size="1",
                on_change=lambda val: FlowState.update_button(block_idx, row_idx, btn_idx, "text", val)
            ),
            rx.select(
                ["callback", "url"],
                value=rx.cond(is_url, "url", "callback"),
                size="1",
                on_change=lambda val: FlowState.update_button(block_idx, row_idx, btn_idx, "type", val)
            ),
            rx.cond(
                is_url,
                rx.input(
                    value=btn["url"],
                    placeholder="https://google.com",
                    size="1",
                    on_change=lambda val: FlowState.update_button(block_idx, row_idx, btn_idx, "url", val)
                ),
                rx.input(
                    value=btn["callback"],
                    placeholder="goto_nomedatela",
                    size="1",
                    on_change=lambda val: FlowState.update_button(block_idx, row_idx, btn_idx, "callback", val)
                )
            ),
            spacing="2",
            padding="2",
            bg="gray.1",
            border_radius="md",
            width="100%"
        ),
        width="140px"
    )

def render_block(index: int, block: dict):
    """Renderiza um bloco completo de mensagem (Lego Block)."""
    
    has_image = block.contains("image_url")
    has_video = block.contains("video_url")
    
    media_type = rx.cond(
        has_image, 
        "image", 
        rx.cond(has_video, "video", "none")
    )
    
    # CORREÇÃO CRÍTICA 1: Forçar o tipo para LISTA
    buttons_rows = block["buttons"].to(list)
    
    return rx.card(
        rx.vstack(
            # --- CABEÇALHO DO BLOCO ---
            rx.hstack(
                rx.badge(
                    rx.text("Mensagem #", index + 1), 
                    variant="solid", 
                    color_scheme="blue"
                ),
                rx.spacer(),
                rx.icon_button(
                    "trash", 
                    color_scheme="red", 
                    variant="ghost", 
                    size="2",
                    on_click=lambda: FlowState.remove_block(index)
                ),
                width="100%",
                align="center"
            ),
            
            rx.divider(),
            
            # --- MÍDIA (Imagem/Video) ---
            rx.text("Mídia / Anexo", font_size="10px", font_weight="bold", color="gray"),
            rx.select(
                ["none", "image", "video"],
                value=media_type,
                on_change=lambda val: FlowState.set_media_type(index, val),
                size="2"
            ),
            
            rx.cond(
                media_type == "image",
                rx.vstack(
                    rx.input(
                        value=block["image_url"],
                        placeholder="URL da Imagem (https://...)",
                        on_change=lambda val: FlowState.update_media_url(index, "image_url", val)
                    ),
                    rx.text("Enviado como Anexo (Imagem Grande)", font_size="10px", color="gray")
                )
            ),
            rx.cond(
                media_type == "video",
                rx.vstack(
                    rx.input(
                        value=block["video_url"],
                        placeholder="URL do Vídeo ou FileID",
                        on_change=lambda val: FlowState.update_media_url(index, "video_url", val)
                    ),
                    rx.text("Enviado como Vídeo", font_size="10px", color="gray")
                )
            ),
            
            # --- TEXTO ---
            rx.hstack(
                rx.text("Texto da Mensagem", font_size="10px", font_weight="bold", color="gray"),
                rx.spacer(),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.button("Badge 🖼️", size="1", variant="surface", color_scheme="teal")
                    ),
                    rx.popover.content(
                        rx.vstack(
                            rx.text("Inserir Badge (Imagem Pequena no Topo)", size="1", weight="bold"),
                            
                            rx.input(
                                placeholder="URL da Imagem",
                                on_change=FlowState.set_temp_badge_url
                            ),
                            rx.button(
                                "Inserir", 
                                size="1", 
                                on_click=lambda: FlowState.insert_badge(index)
                            ),
                            spacing="2"
                        )
                    )
                ),
                align="center",
                width="100%"
            ),
            rx.text_area(
                value=block["text"],
                on_change=lambda val: FlowState.update_block_text(index, val),
                height="150px",
                placeholder="Olá {name}..."
            ),
            
            # --- BOTÕES ---
            rx.divider(),
            rx.hstack(
                rx.text("Botões", font_size="10px", font_weight="bold", color="gray"),
                rx.spacer(),
                rx.button("+ Linha", size="1", variant="outline", on_click=lambda: FlowState.add_button_row(index)),
                width="100%"
            ),
            
            rx.vstack(
                rx.foreach(
                    buttons_rows,
                    lambda row, r_idx: rx.box(
                        rx.hstack(
                            rx.foreach(
                                # CORREÇÃO CRÍTICA 2: Forçar a linha (row) para LISTA também
                                row.to(list),
                                lambda btn, b_idx: render_button_editor(index, r_idx, b_idx, btn)
                            ),
                            rx.icon_button(
                                "plus", 
                                size="1", 
                                variant="soft", 
                                on_click=lambda: FlowState.add_button_to_row(index, r_idx)
                            ),
                            align="start",
                            wrap="wrap",
                            spacing="2"
                        ),
                        border="1px dashed #475569",
                        padding="2",
                        border_radius="md",
                        width="100%"
                    )
                ),
                spacing="2",
                width="100%"
            ),
            
            spacing="3",
            align_items="start",
            width="100%"
        ),
        width="100%",
        bg="#1e293b",
        border="1px solid #334155"
    )

def flow_editor_component():
    """Componente Principal do Editor."""
    return rx.vstack(
        rx.foreach(
            FlowState.editor_blocks,
            lambda block, idx: render_block(idx, block)
        ),
        
        rx.button(
            "+ Adicionar Mensagem (Sequência)", 
            on_click=FlowState.add_block,
            width="100%",
            variant="outline",
            border_style="dashed",
            height="50px"
        ),
        
        spacing="4",
        width="100%",
        padding_bottom="100px" 
    )