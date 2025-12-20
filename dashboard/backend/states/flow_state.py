import reflex as rx
import json
import os
from typing import Dict, List, Any

# Caminho do arquivo JSON
FLOW_FILE_PATH = "dashboard/backend/telegram/flows/start_flow.json"

class FlowState(rx.State):
    """Estado para gerenciar o editor de fluxos."""
    
    # O JSON completo
    full_flow: Dict[str, Any] = {}
    
    # Lista de chaves (nomes das telas) para a sidebar
    screen_keys: List[str] = []
    
    # A tela atualmente selecionada
    selected_screen_key: str = ""
    
    # O conteúdo da tela selecionada (para edição)
    current_screen_content: str = ""
    
    # Variável para o Input de Nova Tela (CORREÇÃO AQUI)
    new_screen_name: str = ""
    
    # Mensagem de status
    status_message: str = ""

    # Adicione isso dentro da classe FlowState
    def set_new_screen_name(self, value: str):
        self.new_screen_name = value
    
    def load_flow(self):
        """Lê o arquivo JSON do disco."""
        if os.path.exists(FLOW_FILE_PATH):
            try:
                with open(FLOW_FILE_PATH, "r", encoding="utf-8") as f:
                    self.full_flow = json.load(f)
                    
                if "screens" in self.full_flow:
                    self.screen_keys = list(self.full_flow["screens"].keys())
                    self.screen_keys.sort()
                
                if not self.selected_screen_key and self.screen_keys:
                    self.select_screen(self.screen_keys[0])
                    
            except Exception as e:
                self.status_message = f"Erro ao carregar JSON: {str(e)}"
        else:
            self.status_message = "Arquivo de fluxo não encontrado."

    def select_screen(self, key: str):
        self.selected_screen_key = key
        if key in self.full_flow.get("screens", {}):
            data = self.full_flow["screens"][key]
            self.current_screen_content = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            self.current_screen_content = "{}"

    def update_content(self, new_content: str):
        self.current_screen_content = new_content

    def save_current_screen(self):
        try:
            new_data = json.loads(self.current_screen_content)
            self.full_flow["screens"][self.selected_screen_key] = new_data
            
            with open(FLOW_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.full_flow, f, indent=2, ensure_ascii=False)
                
            self.status_message = "✅ Salvo com sucesso!"
            
        except json.JSONDecodeError as e:
            self.status_message = f"❌ Erro de Sintaxe JSON: {e}"
        except Exception as e:
            self.status_message = f"❌ Erro ao salvar: {e}"

    # MÉTODO ATUALIZADO
    def add_new_screen(self):
        """Cria uma nova tela usando o valor de new_screen_name."""
        key_name = self.new_screen_name.strip()
        
        if not key_name:
            return
            
        if "screens" not in self.full_flow:
            self.full_flow["screens"] = {}
            
        if key_name in self.full_flow["screens"]:
            self.status_message = "❌ Já existe uma tela com esse nome."
            return
            
        # Cria template
        self.full_flow["screens"][key_name] = {
            "text": "Nova tela...",
            "buttons": []
        }
        
        # Salva
        with open(FLOW_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.full_flow, f, indent=2, ensure_ascii=False)
            
        # Limpa o input e recarrega
        self.new_screen_name = ""
        self.load_flow()
        self.select_screen(key_name)
        self.status_message = f"Tela '{key_name}' criada."