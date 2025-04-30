from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from database.manager import DatabaseManager
from ui.screens import MainScreen, PredictionScreen

class CycleTrackerApp(App):
    def build(self):
        self.db = DatabaseManager()
        self.sm = ScreenManager()
        
        # Cargar interfaz
        Builder.load_file('src/ui/screens.kv')
        
        # Añadir pantallas
        self.sm.add_widget(MainScreen(name='main', db=self.db))
        self.sm.add_widget(PredictionScreen(name='predictions', db=self.db))
        
        return self.sm

if __name__ == '__main__':
    CycleTrackerApp().run()