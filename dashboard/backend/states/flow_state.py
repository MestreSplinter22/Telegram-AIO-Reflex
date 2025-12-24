import reflex as rx
import json
import os
from typing import Dict, List, Any

FLOW_FILE_PATH = "dashboard/backend/telegram/flows/start_flow.json"

class FlowState(rx.State):
    full_flow: Dict[str, Any] = {}
    screen_keys: List[str] = []
    selected_screen_key: str = ""
    
    # Editor Mode
    visual_editor_mode: bool = True
    editor_blocks: List[Dict[str, Any]] = [] 
    original_data_type: str = "dict"
    
    # Input Badge
    temp_badge_url: str = ""
    
    current_screen_content: str = ""
    new_screen_name: str = ""
    status_message: str = ""
    
    # --- REACT FLOW STATES ---
    # Substituímos graph_nodes e svg_content por estas listas
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    def set_temp_badge_url(self, value: str):
        self.temp_badge_url = value

    # --- CARREGAMENTO ---
    def load_flow(self):
        if os.path.exists(FLOW_FILE_PATH):
            try:
                with open(FLOW_FILE_PATH, "r", encoding="utf-8") as f:
                    self.full_flow = json.load(f)
                if "screens" in self.full_flow:
                    self.screen_keys = sorted(list(self.full_flow["screens"].keys()))
                
                if not self.selected_screen_key:
                    initial = self.full_flow.get("initial_screen", "")
                    if initial and initial in self.screen_keys:
                        self.select_screen(initial)
                    elif self.screen_keys:
                        self.select_screen(self.screen_keys[0])
                
                self.calculate_interactive_layout()
            except Exception as e:
                self.status_message = f"Erro Load: {str(e)}"
                print(e)

    def select_screen(self, key: str):
        self.selected_screen_key = key
        
        # Recupera dados ou cria padrão
        data = self.full_flow.get("screens", {}).get(key, {"text": "Nova Tela", "buttons": []})
        
        self.current_screen_content = json.dumps(data, indent=2, ensure_ascii=False)
        
        if isinstance(data, list):
            self.editor_blocks = data
            self.original_data_type = "list"
        else:
            self.editor_blocks = [data]
            self.original_data_type = "dict"
            
        # Recalcula o layout para atualizar o estilo do nó selecionado
        self.calculate_interactive_layout()

    # Evento de clique no Nó do ReactFlow
    def on_node_click(self, node_id: str):
        # Removemos a lógica de extração .get("id"), pois já é a string
        print(f"DEBUG: Clique no nó recebido: {node_id}") # Para você ver no terminal
        if node_id:
            self.select_screen(node_id)

    def add_new_screen(self):
        key = self.new_screen_name.strip()
        if not key: return
        self.select_screen(key)
        self.save_current_screen()
        self.new_screen_name = ""

    # --- EDITOR VISUAL (Mantido igual) ---
    def set_editor_mode(self, mode):
        # Converte a string "visual" ou "json" para booleano
        self.visual_editor_mode = (mode == "visual")
        
        # Se mudou para visual, carrega os blocos a partir do JSON atual
        if self.visual_editor_mode:
            try:
                data = json.loads(self.current_screen_content)
                if isinstance(data, list):
                    self.editor_blocks = data
                    self.original_data_type = "list"
                else:
                    self.editor_blocks = [data]
                    self.original_data_type = "dict"
            except:
                pass

    def add_block(self):
        self.editor_blocks.append({"text": "Nova mensagem...", "buttons": []})
        self.original_data_type = "list"

    def remove_block(self, index: int):
        if 0 <= index < len(self.editor_blocks):
            self.editor_blocks.pop(index)

    def update_block_text(self, index: int, text: str):
        if 0 <= index < len(self.editor_blocks):
            self.editor_blocks[index]["text"] = text

    def set_media_type(self, index: int, type: str):
        if 0 <= index < len(self.editor_blocks):
            block = self.editor_blocks[index]
            if "image_url" in block: del block["image_url"]
            if "video_url" in block: del block["video_url"]
            if type == "image": block["image_url"] = "https://..."
            elif type == "video": block["video_url"] = "https://..."
            self.editor_blocks[index] = block

    def update_media_url(self, index: int, key: str, value: str):
        if 0 <= index < len(self.editor_blocks):
            self.editor_blocks[index][key] = value

    def insert_badge(self, index: int):
        if not self.temp_badge_url: return
        if 0 <= index < len(self.editor_blocks):
            current_text = self.editor_blocks[index].get("text", "")
            badge_html = f"<a href='{self.temp_badge_url}'>&#8205;</a>"
            self.editor_blocks[index]["text"] = badge_html + current_text
            self.temp_badge_url = ""

    def add_button_row(self, block_index: int):
        if 0 <= block_index < len(self.editor_blocks):
            block = self.editor_blocks[block_index]
            if "buttons" not in block: block["buttons"] = []
            block["buttons"].append([{"text": "Novo Botão", "callback": "goto_..."}])
            self.editor_blocks[block_index] = block

    def add_button_to_row(self, block_index: int, row_index: int):
        if 0 <= block_index < len(self.editor_blocks):
            buttons = self.editor_blocks[block_index].get("buttons", [])
            if 0 <= row_index < len(buttons):
                buttons[row_index].append({"text": "Novo Botão", "callback": "goto_..."})

    def remove_button(self, block_index: int, row_index: int, btn_index: int):
        if 0 <= block_index < len(self.editor_blocks):
            buttons = self.editor_blocks[block_index].get("buttons", [])
            if 0 <= row_index < len(buttons):
                if 0 <= btn_index < len(buttons[row_index]):
                    buttons[row_index].pop(btn_index)
                    if not buttons[row_index]:
                        buttons.pop(row_index)

    def update_button(self, block_idx: int, row_idx: int, btn_idx: int, field: str, value: str):
        if 0 <= block_idx < len(self.editor_blocks):
            btn = self.editor_blocks[block_idx]["buttons"][row_idx][btn_idx]
            if field == "type":
                if value == "url":
                    if "callback" in btn: del btn["callback"]
                    btn["url"] = "https://..."
                else:
                    if "url" in btn: del btn["url"]
                    btn["callback"] = "goto_..."
            else:
                btn[field] = value
            self.editor_blocks[block_idx]["buttons"][row_idx][btn_idx] = btn

    def save_visual_changes(self):
        final_data = self.editor_blocks
        if len(self.editor_blocks) == 1 and self.original_data_type == "dict":
            final_data = self.editor_blocks[0]
        self.current_screen_content = json.dumps(final_data, indent=2, ensure_ascii=False)
        self.save_current_screen()

    def update_content(self, new_content: str):
        self.current_screen_content = new_content

    def set_new_screen_name(self, value: str):
        self.new_screen_name = value

    def save_current_screen(self):
        # --- CORREÇÃO: Sincronização do Modo Visual ---
        # Se estiver no modo visual, atualizamos o texto JSON (current_screen_content)
        # com base nos blocos editados (editor_blocks) antes de prosseguir.
        if self.visual_editor_mode:
            final_data = self.editor_blocks
            # Se originalmente era um dicionário único e continua com 1 bloco, salva como dict
            if len(self.editor_blocks) == 1 and self.original_data_type == "dict":
                final_data = self.editor_blocks[0]
            
            self.current_screen_content = json.dumps(final_data, indent=2, ensure_ascii=False)
        # -----------------------------------------------

        try:
            # Agora o current_screen_content está atualizado, independente do modo
            new_data = json.loads(self.current_screen_content)
            
            if "screens" not in self.full_flow: self.full_flow["screens"] = {}
            self.full_flow["screens"][self.selected_screen_key] = new_data
            
            with open(FLOW_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.full_flow, f, indent=2, ensure_ascii=False)
                
            self.status_message = "✅ Salvo com sucesso!"
            self.screen_keys = sorted(list(self.full_flow["screens"].keys()))
            self.calculate_interactive_layout()
            
            # Se salvou via modo texto, atualiza os blocos visuais para não quebrar se trocar de aba
            if not self.visual_editor_mode:
                if isinstance(new_data, list):
                    self.editor_blocks = new_data
                    self.original_data_type = "list"
                else:
                    self.editor_blocks = [new_data]
                    self.original_data_type = "dict"

        except json.JSONDecodeError:
            self.status_message = "❌ JSON Inválido. Corrija o texto antes de salvar."
        except Exception as e:
            self.status_message = f"❌ Erro ao salvar: {e}"
            print(f"Erro Save: {e}")

    # --- NOVO LAYOUT PARA REACT FLOW ---
    def calculate_interactive_layout(self):
        """
        Calcula nós e arestas compatíveis com a estrutura do React Flow.
        Mantém a lógica de BFS para distribuir as posições X e Y.
        """
        screens_raw = self.full_flow.get("screens", {})
        if not screens_raw: 
            self.nodes = []
            self.edges = []
            return

        screens = {str(k).strip(): v for k, v in screens_raw.items()}

        # Dimensões para cálculo de posição (Grid)
        NODE_WIDTH = 250
        NODE_HEIGHT = 150 
        GAP_X = 50
        GAP_Y = 100
        START_X = 100
        START_Y = 50

        # Listas temporárias
        temp_edges = []
        adjacency = {} 
        all_nodes_set = set(screens.keys())
        
        # 1. Identificar Conexões (Edges)
        for screen_id, content in screens.items():
            if screen_id not in adjacency: adjacency[screen_id] = []
            
            found_buttons = []
            stack = [content]
            
            # Varredura profunda por botões
            while stack:
                curr = stack.pop()
                if isinstance(curr, dict):
                    if "callback" in curr and isinstance(curr["callback"], str) and curr["callback"].startswith("goto_"):
                        found_buttons.append(curr)
                    for v in curr.values():
                        if isinstance(v, (dict, list)): stack.append(v)
                elif isinstance(curr, list):
                    for item in curr: stack.append(item)
            
            # Criar Edges
            for i, btn in enumerate(found_buttons):
                raw_target = btn["callback"].replace("goto_", "").strip()
                target = raw_target.split()[0] if raw_target else raw_target
                label = btn.get("text", "Próximo").strip()
                
                # Edge ID único
                edge_id = f"e-{screen_id}-{target}-{i}"
                
                # Verifica se o target existe (Link Quebrado)
                is_broken = target not in screens
                
                temp_edges.append({
                    "id": edge_id,
                    "source": screen_id,
                    "target": target,
                    "label": label,
                    "animated": True,
                    "style": {"stroke": "#ef4444", "strokeWidth": 2} if is_broken else {"stroke": "#94a3b8"},
                    "labelStyle": {"fill": "#ef4444", "fontWeight": 700} if is_broken else {"fill": "#64748b"},
                })
                
                adjacency[screen_id].append(target)
                if target not in all_nodes_set:
                    all_nodes_set.add(target)

        # 2. Algoritmo BFS para Níveis (Layout Hierárquico)
        start_node = self.full_flow.get("initial_screen", "").strip()
        if start_node not in screens and screens: start_node = next(iter(screens))

        levels = {}
        queue = [(start_node, 0)]
        visited = set()

        while queue:
            current, level = queue.pop(0)
            if current in visited: continue
            visited.add(current)
            levels[current] = level
            for child in adjacency.get(current, []): queue.append((child, level + 1))

        # Adicionar nós órfãos no nível 1
        for node in all_nodes_set:
            if node not in visited: levels[node] = 1

        nodes_by_level = {}
        for node, level in levels.items():
            if level not in nodes_by_level: nodes_by_level[level] = []
            nodes_by_level[level].append(node)

        # 3. Construir Nós do ReactFlow
        final_rf_nodes = []
        
        for level, level_nodes in nodes_by_level.items():
            # Centralizar a linha horizontalmente
            row_width = len(level_nodes) * (NODE_WIDTH + GAP_X)
            start_x_level = START_X # Você pode centralizar dinamicamente se quiser
            
            for i, node_id in enumerate(level_nodes):
                x = start_x_level + (i * (NODE_WIDTH + GAP_X))
                y = START_Y + (level * (NODE_HEIGHT + GAP_Y))
                
                is_selected = node_id == self.selected_screen_key
                is_missing = node_id not in screens
                
                # Estilização baseada em estado
                bg_color = "#1e293b" if is_selected else ("#fef2f2" if is_missing else "#ffffff")
                text_color = "white" if is_selected else ("#b91c1c" if is_missing else "black")
                border_color = "#3b82f6" if is_selected else ("#ef4444" if is_missing else "#cbd5e1")
                
                # Label com indicador
                label_text = f"🚫 {node_id}" if is_missing else node_id
                
                final_rf_nodes.append({
                    "id": node_id,
                    "data": {"label": label_text},
                    "position": {"x": x, "y": y},
                    "draggable": True,
                    "style": {
                        "background": bg_color,
                        "color": text_color,
                        "border": f"2px solid {border_color}",
                        "borderRadius": "8px",
                        "width": "200px",
                        "padding": "10px",
                        "fontSize": "12px",
                        "fontWeight": "bold",
                        "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)"
                    }
                })

        self.nodes = final_rf_nodes
        self.edges = temp_edges