import numpy as np
from sklearn.linear_model import BayesianRidge
from datetime import datetime, timedelta

class CyclePredictor:
    def __init__(self, db_manager):
        self.db = db_manager
        self.model = BayesianRidge()
    
    def train_model(self):
        data = self.db.get_cycle_stats()
        if len(data) < 3:
            return None
        
        X = np.array(range(len(data))).reshape(-1, 1)
        y = np.array(data)
        self.model.fit(X, y)
        return self.model.score(X, y)
    
    def predict_next_periods(self, n_periods=3):
        data = self.db.get_cycle_stats()
        if len(data) < 3:
            return []
        
        last_date = self.db.get_all_periods()[0][0]
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        
        X_pred = np.array([[len(data) + i] for i in range(n_periods)])
        predictions = self.model.predict(X_pred)
        
        results = []
        current_date = last_date
        for days in predictions:
            current_date += timedelta(days=days)
            results.append(current_date.strftime('%Y-%m-%d'))
        
        return results
    
    def get_confidence_interval(self):
        data = self.db.get_cycle_stats()
        if len(data) < 3:
            return (0, 0)
        
        mean = np.mean(data)
        std = np.std(data)
        return (max(0, mean - 1.96*std), mean + 1.96*std)