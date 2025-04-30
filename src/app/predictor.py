import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import BayesianRidge

class CyclePredictor:
    def __init__(self, cycle_data):
        self.model = BayesianRidge()
        self.train_model(cycle_data)
    
    def train_model(self, data):
        X = np.array(range(len(data))).reshape(-1, 1)
        y = np.array(data)
        self.model.fit(X, y)
    
    def predict_next(self, last_date, n_periods=3):
        next_dates = []
        current_pred = len(self.model.predict([[0]]))
        
        for i in range(1, n_periods + 1):
            pred_days = self.model.predict([[current_pred + i]])[0]
            next_dates.append(last_date + timedelta(days=pred_days))
        
        return next_dates