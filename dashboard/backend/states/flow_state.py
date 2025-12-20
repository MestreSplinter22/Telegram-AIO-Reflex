import reflex as rx
import json
import os
from typing import Dict, List, Any

FLOW_FILE_PATH = "dashboard/backend/telegram/flows/start_flow.json"

class FlowState(rx.State):
    full_flow: Dict[str, Any] = {}
    screen_keys: List[str] = []
    selected_screen_key: str = ""
    current_screen_content: str = ""
    new_screen_name: str = ""
    status_message: str = ""
    
    # Dados para o Gráfico
    graph_nodes: List[Dict[str, Any]] = []
    svg_content: str = ""
    
    # Configurações do Canvas
    canvas_height: str = "2000px"

    def load_flow(self):
        if os.path.exists(FLOW_FILE_PATH):
            try:
                with open(FLOW_FILE_PATH, "r", encoding="utf-8") as f:
                    self.full_flow = json.load(f)
                    
                if "screens" in self.full_flow:
                    # Ordena as chaves para a lista ficar bonita
                    self.screen_keys = list(self.full_flow["screens"].keys())
                    self.screen_keys.sort()
                
                # Seleciona tela inicial
                if not self.selected_screen_key:
                    initial = self.full_flow.get("initial_screen", "")
                    if initial and initial in self.screen_keys:
                        self.select_screen(initial)
                    elif self.screen_keys:
                        self.select_screen(self.screen_keys[0])
                
                self.calculate_interactive_layout()
                    
            except Exception as e:
                self.status_message = f"Erro ao carregar: {str(e)}"
                print(f"Erro Load: {e}")
        else:
            self.status_message = "Arquivo não encontrado."

    def calculate_interactive_layout(self):
        """
        Algoritmo V3:
        - Encontra botões em qualquer lugar (recursivo).
        - Cria nós 'Fantasmas' (Vermelhos) para links quebrados.
        - Normaliza nomes (strip) para evitar erros de espaço.
        """
        screens_raw = self.full_flow.get("screens", {})
        if not screens_raw:
            return

        # Limpa chaves (remove espaços extras que causam bugs)
        screens = {k.strip(): v for k, v in screens_raw.items()}

        NODE_WIDTH = 220
        NODE_HEIGHT = 100
        GAP_X = 60
        GAP_Y = 160
        START_X = 600
        START_Y = 50

        connections = []
        adjacency = {} 
        all_nodes_set = set(screens.keys()) # Começa com as telas reais
        
        # --- 1. VARREDURA PROFUNDA (RECURSIVA) ---
        def find_buttons_recursive(data):
            found_buttons = []
            if isinstance(data, dict):
                if "callback" in data and isinstance(data["callback"], str) and data["callback"].startswith("goto_"):
                    found_buttons.append(data)
                for key, value in data.items():
                    found_buttons.extend(find_buttons_recursive(value))
            elif isinstance(data, list):
                for item in data:
                    found_buttons.extend(find_buttons_recursive(item))
            return found_buttons

        for screen_id, content in screens.items():
            if screen_id not in adjacency: adjacency[screen_id] = []
            
            # Busca todos os botões dentro desta tela
            buttons = find_buttons_recursive(content)
            
            for btn in buttons:
                target = btn["callback"].replace("goto_", "").strip()
                label = btn.get("text", "Próximo").strip()
                # Encurta texto longo
                label_short = label[:18] + "..." if len(label) > 18 else label

                connections.append({
                    "source": screen_id,
                    "target": target,
                    "label": label_short
                })
                
                adjacency[screen_id].append(target)
                
                # Se o alvo não existe nas telas, adiciona como nó fantasma
                if target not in all_nodes_set:
                    all_nodes_set.add(target)
                    if target not in adjacency: adjacency[target] = []

        # --- 2. CÁLCULO DE NÍVEIS (BFS) ---
        start_node = self.full_flow.get("initial_screen", "").strip()
        if start_node not in screens and screens:
            start_node = next(iter(screens))

        levels = {}
        queue = [(start_node, 0)]
        visited = set()

        while queue:
            current, level = queue.pop(0)
            if current in visited: continue
            visited.add(current)
            levels[current] = level
            
            # Adiciona filhos na fila
            children = adjacency.get(current, [])
            for child in children:
                queue.append((child, level + 1))

        # Trata nós isolados (que não foram conectados pelo início)
        for node in all_nodes_set:
            if node not in visited:
                levels[node] = 1

        # --- 3. COORDENADAS ---
        nodes_by_level = {}
        for node, level in levels.items():
            if level not in nodes_by_level: nodes_by_level[level] = []
            nodes_by_level[level].append(node)

        final_nodes = []
        node_coords = {}
        
        for level, level_nodes in nodes_by_level.items():
            row_width = len(level_nodes) * (NODE_WIDTH + GAP_X)
            start_x_level = START_X - (row_width / 2)
            
            for i, node_id in enumerate(level_nodes):
                x = start_x_level + (i * (NODE_WIDTH + GAP_X))
                y = START_Y + (level * (NODE_HEIGHT + GAP_Y))
                
                node_coords[node_id] = {"x": x, "y": y}
                
                # Verifica se é real ou quebrado (fantasma)
                is_missing = node_id not in screens
                
                final_nodes.append({
                    "id": node_id,
                    "label": f"🚫 {node_id}" if is_missing else node_id,
                    "x": x,
                    "y": y,
                    "missing": is_missing # Flag para o frontend pintar de vermelho
                })

        self.graph_nodes = final_nodes
        self.canvas_height = f"{max(900, (len(nodes_by_level) * 300))}px"

        # --- 4. GERAR SVG ---
        svg_parts = ["""
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
                </marker>
                <marker id="arrowhead-missing" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#ef4444" />
                </marker>
            </defs>
        """]

        for conn in connections:
            source, target = conn["source"], conn["target"]
            
            if source in node_coords and target in node_coords:
                start, end = node_coords[source], node_coords[target]
                
                x1 = start["x"] + (NODE_WIDTH / 2)
                y1 = start["y"] + NODE_HEIGHT
                x2 = end["x"] + (NODE_WIDTH / 2)
                y2 = end["y"]
                
                # Detecção de Ciclo (Seta voltando para cima)
                is_loop_back = y2 < y1
                
                if is_loop_back:
                    # Desenha curva pela lateral para não ficar feio
                    path_d = f"M {x1} {y1} C {x1} {y1+100}, {x2-100} {y2}, {x2} {y2+(NODE_HEIGHT/2)}"
                    # Ajusta ponto final para lateral do nó
                    marker = "marker-end='url(#arrowhead)'"
                else:
                    cp1_y = y1 + 50
                    cp2_y = y2 - 50
                    path_d = f"M {x1} {y1} C {x1} {cp1_y}, {x2} {cp2_y}, {x2} {y2}"
                    marker = "marker-end='url(#arrowhead)'"

                # Se o destino for fantasma, linha vermelha
                color = "#ef4444" if target not in screens else "#cbd5e1"
                if target not in screens: marker = "marker-end='url(#arrowhead-missing)'"

                svg_parts.append(f'<path d="{path_d}" stroke="{color}" stroke-width="2" fill="none" {marker} />')
                
                # Texto
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                text_len = len(conn["label"]) * 6 + 10
                svg_parts.append(f'<rect x="{mid_x - (text_len/2)}" y="{mid_y - 10}" width="{text_len}" height="20" fill="white" rx="4" opacity="0.9" />')
                svg_parts.append(f'<text x="{mid_x}" y="{mid_y + 4}" fill="#64748b" font-size="10" text-anchor="middle" font-family="sans-serif">{conn["label"]}</text>')

        self.svg_content = f'<svg width="100%" height="100%" style="position: absolute; top: 0; left: 0;">{"".join(svg_parts)}</svg>'

    def select_screen(self, key: str):
        self.selected_screen_key = key
        # Só carrega JSON se a tela existir de verdade
        if key in self.full_flow.get("screens", {}):
            data = self.full_flow["screens"][key]
            self.current_screen_content = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            # É uma tela fantasma/nova
            self.current_screen_content = "{\n  \"text\": \"Tela Nova...\",\n  \"buttons\": []\n}"
        
        # Recalcula para atualizar cores
        self.calculate_interactive_layout()

    def update_content(self, new_content: str):
        self.current_screen_content = new_content

    def set_new_screen_name(self, value: str):
        self.new_screen_name = value

    def save_current_screen(self):
        try:
            new_data = json.loads(self.current_screen_content)
            
            # Garante que 'screens' existe
            if "screens" not in self.full_flow: self.full_flow["screens"] = {}
            
            # Salva na chave selecionada
            self.full_flow["screens"][self.selected_screen_key] = new_data
            
            with open(FLOW_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.full_flow, f, indent=2, ensure_ascii=False)
                
            self.status_message = "✅ Salvo!"
            
            # Atualiza lista de chaves e gráfico
            self.screen_keys = list(self.full_flow["screens"].keys())
            self.screen_keys.sort()
            self.calculate_interactive_layout()
            
        except json.JSONDecodeError:
            self.status_message = "❌ JSON Inválido"
        except Exception as e:
            self.status_message = f"❌ Erro: {e}"

    def add_new_screen(self):
        key = self.new_screen_name.strip()
        if not key: return
        self.selected_screen_key = key
        self.save_current_screen() # Salva a tela padrão
        self.new_screen_name = ""