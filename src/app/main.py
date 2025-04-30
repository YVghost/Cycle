from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from src.database.database_manager import DatabaseManager
from src.app.predictor import CyclePredictor
from src.ui.home_screen import HomeScreen
from src.ui.history_screen import HistoryScreen
from src.ui.settings_screen import SettingsScreen

class CycleTrackerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.predictor = CyclePredictor(self.db)
        self.sm = ScreenManager()
        
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.load_kv_files()
        self.setup_screens()
        return self.sm
    
    def load_kv_files(self):
        Builder.load_file("src/ui/home_screen.kv")
        Builder.load_file("src/ui/history_screen.kv")
        Builder.load_file("src/ui/settings_screen.kv")
    
    def setup_screens(self):
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(HistoryScreen(name='history'))
        self.sm.add_widget(SettingsScreen(name='settings'))

if __name__ == '__main__':
    CycleTrackerApp().run()