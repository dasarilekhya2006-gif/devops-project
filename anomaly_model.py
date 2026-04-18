from sklearn.ensemble import IsolationForest
import numpy as np

def train_model():
    X = np.random.rand(100, 1)
    model = IsolationForest(contamination=0.1)
    model.fit(X)
    return model