import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from .models import TrafficData

def train_model():
    # Load data from Django model
    qs = TrafficData.objects.all().values("vehicle_count", "intersection")
    df = pd.DataFrame(list(qs))

    # Features and target
    X = df[["vehicle_count"]]
    y = df["intersection"]

    # Train–test split (70/30)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print("Validation Accuracy:", accuracy)

    # Save model
    joblib.dump(model, "signals/ml_model.pkl")