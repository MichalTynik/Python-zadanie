import json

class Data:
    def __init__(self, path):
        self.path = path
    
            
    def save_info(self, data:list):
        """Ulozi informacie o letaku do json suboru

        Args:
            data (list): Zoznam s informaciami  
        """
        try: 
            with open(self.path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data boli zapisane do suboru {self.path}")
        except Exception as e:
            print(f"Chyba pri zapise: {e}")
        
    