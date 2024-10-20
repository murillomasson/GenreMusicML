from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import uuid

class MLModel:
    def __init__(self, track_crud):
        self.scaler = None
        self.encoder = LabelEncoder()
        self.model = RandomForestClassifier()
        self.track_crud = track_crud
        self.model_name = "RandomForestClassifier"
        self.accuracy = None
        self.precision = None
        self.recall = None
        self.f1 = None


    def train(self, df, spotify_ids, track_data):
        X = df.drop(['genre'], axis=1)
        y = df['genre']
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        y_encoded = self.encoder.fit_transform(y)

        X_train, X_test, y_train, y_test, ids_train, ids_test = train_test_split(
            X_scaled, y_encoded, spotify_ids, test_size=0.2, random_state=42
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)

        self.accuracy = accuracy_score(y_test, y_pred)
        self.precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        self.recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        self.f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        track_names = [track["name"] for track in track_data if track["spotify_id"] in ids_test]

        self.save_results(ids_test, y_test, 
                          y_train, y_pred, 
                          y_pred_proba, 
                          self.accuracy, 
                          self.precision, 
                          self.recall, 
                          self.f1,
                          track_names                          
                          )
        
        return self.accuracy, self.precision, self.recall, self.f1


    def predict(self, track_data):
        if not self.scaler:
            raise ValueError("Model has not been trained yet. Please train the model before prediction.")

        features = [[
            track_data["danceability"],
            track_data["energy"],
            track_data["tempo"],
            track_data["loudness"],
            track_data["valence"]
        ]]

        scaled_features = self.scaler.transform(features)

        predicted_label = self.model.predict(scaled_features)[0]
        predicted_proba = self.model.predict_proba(scaled_features)[0]

        predicted_genre = self.encoder.inverse_transform([predicted_label])[0]
        confidence_score = predicted_proba[predicted_label]

        return {
            "predicted_genre": predicted_genre,
            "confidence_score": confidence_score,
            "model_used": self.model_name,
            "test_data_id": str(uuid.uuid4()),
            "status": "success",
            "notes": None,
        }

    def save_results(self, ids_test, y_test, y_train, y_pred, y_pred_proba, accuracy, precision, recall, f1, track_names):

        ids_test_list = ids_test.to_list()
        y_pred_proba_value = y_pred_proba[:, 1]
        confidence_scores = y_pred_proba_value.tolist()
        prediction_data_list = [{
            "spotify_id": ids_test_list[i],
            "predicted_genre": int(y_pred[i]),
            "confidence_score": float(confidence_scores[i]),
            "model_used": self.model_name,
            "test_data_id": str(uuid.uuid4()),
            "status": "success",
            "notes": f"Gênero real: {y_test[i]}",
            "name": track_names
            
        } for i in range(len(ids_test_list))]

        for prediction_data in prediction_data_list:
            self.track_crud.insert_prediction_result(prediction_data)

            performance_metrics = {
            "model_used": self.model_name,
            "test_data_id": str(uuid.uuid4()),
            "trained_data_count": len(y_train),
            "tested_data_count": len(y_test),
            "accuracy": float(accuracy) if accuracy is not None else None,
            "precision": float(precision) if recall is not None else None,
            "recall": float(recall) if recall is not None else None,
            "f1_score": float(f1) if f1 is not None else None,
        }

            self.track_crud.insert_performance_metrics(
                performance_metrics["test_data_id"],
                performance_metrics["trained_data_count"],
                performance_metrics["tested_data_count"],
                performance_metrics["accuracy"],
                performance_metrics["precision"],
                performance_metrics["recall"],
                performance_metrics["f1_score"],
            )
