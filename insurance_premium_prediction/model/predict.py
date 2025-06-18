import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl','rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.0.0' # For now we made it manually but it is automatically tracked and updated using "MLFlow"

# Get class labels from model (important for matching probabilities to class names) - For showing confidence scores
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    input_df = pd.DataFrame([user_input])

    # Predict the class
    predict_class = model.predict(input_df)[0]

    # Get probabilites for all classes - Easy in RF as it gives confidence score as well
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    # Create mapping: {class_name, probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        'predicted_category': predict_class,
        'confidence': round(confidence, 4),
        'class_probabilities': class_probs
    }