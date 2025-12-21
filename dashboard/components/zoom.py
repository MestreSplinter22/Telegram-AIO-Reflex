import reflex as rx

# Wrapper para o componente TransformWrapper do React
class ZoomPanPinch(rx.Component):
    library = "react-zoom-pan-pinch"
    tag = "TransformWrapper"
    
    # Configurações padrão
    initial_scale: float = 1.0
    min_scale: float = 0.5
    max_scale: float = 4.0
    center_on_init: bool = False
    limit_to_bounds: bool = False # Permite arrastar infinitamente
    wheel: dict = {"step": 0.1}   # Configuração do Zoom no mouse
    panning: dict = {"velocityDisabled": False} # Configuração do Pan

    @classmethod
    def get_component(cls, **props):
        return super().get_component(**props)

# Wrapper para o componente TransformComponent do React
class ZoomContent(rx.Component):
    library = "react-zoom-pan-pinch"
    tag = "TransformComponent"
    
    # Estilização forçada para garantir que o wrapper ocupe tudo
    wrapper_style: dict = {
        "width": "100%",
        "height": "100%",
    }