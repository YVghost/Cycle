from plyer import notification
from kivy.clock import Clock
from datetime import datetime

class NotificationManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.scheduled = False
    
    def schedule_daily_check(self):
        if not self.scheduled:
            Clock.schedule_interval(self.check_predictions, 3600)  # Cada hora
            self.scheduled = True
    
    def check_predictions(self, dt):
        predictions = self.db.get_predictions()
        today = datetime.today().date()
        
        for pred_date in predictions:
            if (pred_date - today).days == 3:
                self.send_notification(
                    title="Recordatorio de ciclo",
                    message="Tu período está por comenzar en 3 días"
                )
    
    def send_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="CycleTracker",
            timeout=10
        )