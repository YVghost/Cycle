import csv
from kivy.storage.jsonstore import JsonStore
from kivy.uix.filechooser import FileChooserListView
from kivymd.toast import toast

class DataExporter:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def export_to_csv(self, path):
        try:
            data = self.db.get_all_periods()
            with open(f"{path}/cycle_data.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Fecha Inicio', 'Duración Ciclo'])
                for row in data:
                    writer.writerow(row)
            toast("Datos exportados exitosamente")
            return True
        except Exception as e:
            toast(f"Error: {str(e)}")
            return False