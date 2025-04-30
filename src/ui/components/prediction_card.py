from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class PredictionCard(BoxLayout):
    title = StringProperty('')
    date = StringProperty('')
    confidence = StringProperty('')