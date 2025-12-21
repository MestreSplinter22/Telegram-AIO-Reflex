import reflex as rx
from typing import Any, Dict

class ReactFlow(rx.Component):
    library = "reactflow"
    tag = "ReactFlow"
    
    # Props
    nodes: rx.Var[list]
    edges: rx.Var[list]
    fit_view: rx.Var[bool]
    
    # Props para otimização
    nodeTypes: rx.Var[dict]
    edgeTypes: rx.Var[dict]
    
    # Eventos
    on_node_click: rx.EventHandler[lambda node_id: [node_id]]
    on_pane_click: rx.EventHandler[lambda: []]
    
    style: dict = {"width": "100%", "height": "100%"}

    def _get_custom_code(self) -> str:
        return """
        import 'reactflow/dist/style.css';
        
        // Constantes estáticas para evitar re-render desnecessário
        const memoizedNodeTypes = {};
        const memoizedEdgeTypes = {};
        """
    
    @classmethod
    def create(cls, *children, **props):
        """
        Sobrescreve a criação para injetar os tipos estáticos e aceitar filhos.
        """
        # 1. Injeta as variáveis JS estáticas se não forem passadas
        if "nodeTypes" not in props:
            props["nodeTypes"] = rx.Var("memoizedNodeTypes")
        
        if "edgeTypes" not in props:
            props["edgeTypes"] = rx.Var("memoizedEdgeTypes")
            
        # 2. Repassa *children (Background, Controls, etc) e **props para o pai
        return super().create(*children, **props)

    def get_event_triggers(self) -> Dict[str, Any]:
        return {
            "on_node_click": lambda e, node: [node.id],
            "on_pane_click": lambda e: [],
        }

# --- Plugins ---
class Background(rx.Component):
    library = "reactflow"
    tag = "Background"
    variant: rx.Var[str]
    gap: rx.Var[int]
    size: rx.Var[int]
    color: rx.Var[str]
    
    @classmethod
    def create(cls, **props):
        return super().create(**props)

class Controls(rx.Component):
    library = "reactflow"
    tag = "Controls"

class MiniMap(rx.Component):
    library = "reactflow"
    tag = "MiniMap"