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
    
    # Variável temporária para o input de Badge
    temp_badge_url: str = ""
    
    current_screen_content: str = ""
    new_screen_name: str = ""
    status_message: str = ""
    
    # Layout Interativo
    graph_nodes: List[Dict[str, Any]] = []
    svg_content: str = ""
    canvas_height: str = "2000px"

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

    def select_screen(self, key: str):
        self.selected_screen_key = key
        # Se a tela não existir, cria um padrão na memória
        data = self.full_flow.get("screens", {}).get(key, {"text": "Nova Tela", "buttons": []})
        
        # Prepara conteúdo RAW
        self.current_screen_content = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Prepara conteúdo ESTRUTURADO (Visual)
        if isinstance(data, list):
            self.editor_blocks = data
            self.original_data_type = "list"
        else:
            self.editor_blocks = [data]
            self.original_data_type = "dict"
            
        self.calculate_interactive_layout()

    # --- AÇÃO FALTANTE: CRIAR NOVA TELA ---
    def add_new_screen(self):
        key = self.new_screen_name.strip()
        if not key: return
        
        # Seleciona a chave (isso vai carregar o default "Nova Tela" no editor)
        self.select_screen(key)
        
        # Salva imediatamente para persistir no arquivo
        self.save_current_screen()
        
        self.new_screen_name = ""

    # --- EDITOR VISUAL ---

    def toggle_editor_mode(self):
        self.visual_editor_mode = not self.visual_editor_mode
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

    # --- BADGES ---
    def insert_badge(self, index: int):
        """Insere o HTML da badge usando a variável temporária do estado."""
        if not self.temp_badge_url:
            return
            
        if 0 <= index < len(self.editor_blocks):
            current_text = self.editor_blocks[index].get("text", "")
            badge_html = f"<a href='{self.temp_badge_url}'>&#8205;</a>"
            self.editor_blocks[index]["text"] = badge_html + current_text
            self.temp_badge_url = ""

    # --- BOTÕES ---

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

    # --- SALVAMENTO ---

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
        try:
            new_data = json.loads(self.current_screen_content)
            if "screens" not in self.full_flow: self.full_flow["screens"] = {}
            self.full_flow["screens"][self.selected_screen_key] = new_data
            
            with open(FLOW_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.full_flow, f, indent=2, ensure_ascii=False)
                
            self.status_message = "✅ Salvo!"
            self.screen_keys = sorted(list(self.full_flow["screens"].keys()))
            self.calculate_interactive_layout()
            
            if not self.visual_editor_mode:
                if isinstance(new_data, list):
                    self.editor_blocks = new_data
                else:
                    self.editor_blocks = [new_data]

        except json.JSONDecodeError:
            self.status_message = "❌ JSON Inválido"
        except Exception as e:
            self.status_message = f"❌ Erro: {e}"

    # --- LAYOUT V5 (SCROLL CORRIGIDO) ---
    def calculate_interactive_layout(self):
        screens_raw = self.full_flow.get("screens", {})
        if not screens_raw: return

        screens = {str(k).strip(): v for k, v in screens_raw.items()}

        NODE_WIDTH = 220
        NODE_HEIGHT = 100
        GAP_X = 60
        GAP_Y = 160
        START_X = 600
        START_Y = 50

        connections = []
        adjacency = {} 
        all_nodes_set = set(screens.keys())
        
        for screen_id, content in screens.items():
            if screen_id not in adjacency: adjacency[screen_id] = []
            
            found_buttons = []
            stack = [content]
            
            while stack:
                curr = stack.pop()
                if isinstance(curr, dict):
                    if "callback" in curr and isinstance(curr["callback"], str) and curr["callback"].startswith("goto_"):
                        found_buttons.append(curr)
                    for v in curr.values():
                        if isinstance(v, (dict, list)): stack.append(v)
                elif isinstance(curr, list):
                    for item in curr: stack.append(item)
            
            for btn in found_buttons:
                raw_target = btn["callback"].replace("goto_", "").strip()
                target = raw_target.split()[0] if raw_target else raw_target
                label = btn.get("text", "Próximo").strip()
                label_short = label[:18] + "..." if len(label) > 18 else label

                connections.append({"source": screen_id, "target": target, "label": label_short})
                adjacency[screen_id].append(target)
                if target not in all_nodes_set:
                    all_nodes_set.add(target)
                    if target not in adjacency: adjacency[target] = []

        # BFS
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

        for node in all_nodes_set:
            if node not in visited: levels[node] = 1

        nodes_by_level = {}
        for node, level in levels.items():
            if level not in nodes_by_level: nodes_by_level[level] = []
            nodes_by_level[level].append(node)

        final_nodes = []
        node_coords = {}
        
        max_y = 0
        max_x = 0
        
        for level, level_nodes in nodes_by_level.items():
            row_width = len(level_nodes) * (NODE_WIDTH + GAP_X)
            start_x_level = START_X - (row_width / 2)
            
            for i, node_id in enumerate(level_nodes):
                x = start_x_level + (i * (NODE_WIDTH + GAP_X))
                y = START_Y + (level * (NODE_HEIGHT + GAP_Y))
                
                max_y = max(max_y, y + NODE_HEIGHT)
                max_x = max(max_x, x + NODE_WIDTH)
                
                node_coords[node_id] = {"x": x, "y": y}
                is_missing = node_id not in screens
                
                final_nodes.append({
                    "id": node_id,
                    "label": f"🚫 {node_id}" if is_missing else node_id,
                    "x": x,
                    "y": y,
                    "missing": is_missing
                })

        self.graph_nodes = final_nodes
        real_height = max(1000, max_y + 300) 
        real_width = max(1200, max_x + 300)
        self.canvas_height = f"{real_height}px"

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
                
                target_missing = target not in screens
                color = "#ef4444" if target_missing else "#94a3b8"
                marker = "marker-end='url(#arrowhead-missing)'" if target_missing else "marker-end='url(#arrowhead)'"
                
                if y2 < y1:
                    path_d = f"M {x1} {y1} C {x1} {y1+100}, {x2-100} {y2}, {x2} {y2+(NODE_HEIGHT/2)}"
                else:
                    cp1_y = y1 + 50
                    cp2_y = y2 - 50
                    path_d = f"M {x1} {y1} C {x1} {cp1_y}, {x2} {cp2_y}, {x2} {y2}"

                svg_parts.append(f'<path d="{path_d}" stroke="{color}" stroke-width="2" fill="none" {marker} />')
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                safe_label = conn["label"].replace("<", "").replace(">", "")
                text_len = len(safe_label) * 6 + 10
                svg_parts.append(f'<rect x="{mid_x - (text_len/2)}" y="{mid_y - 10}" width="{text_len}" height="20" fill="white" rx="4" opacity="0.9" />')
                svg_parts.append(f'<text x="{mid_x}" y="{mid_y + 4}" fill="#64748b" font-size="10" text-anchor="middle" font-family="sans-serif">{safe_label}</text>')

        self.svg_content = f'<svg width="{real_width}px" height="{real_height}px" style="position: absolute; top: 0; left: 0; pointer-events: none;">{"".join(svg_parts)}</svg>'