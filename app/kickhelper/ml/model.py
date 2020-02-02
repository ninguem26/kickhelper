import numpy as np
from xgboost import XGBClassifier
from joblib import load

MODEL_PATH = '/home/lativ/Study/ML/datascience/kickhelper/app/kickhelper/ml/xgb-150k-v1.model'
ENCODER_PATH = '/home/lativ/Study/ML/datascience/kickhelper/app/kickhelper/ml/onehot-150k.joblib'

def predict(inputs):

    main_category, category, goal, country, currency, today = inputs

    """ Encode inputs """
    encoder = load(ENCODER_PATH)
    inputs2enc = np.array([category, main_category, currency, country]).reshape(1, -1)
    inputs_encoded = encoder.transform(inputs2enc)

    """ Stack """
    numericals = np.array([goal, today.day, today.month]).reshape(1, -1)
    final_inputs = np.hstack([numericals, inputs_encoded]).astype(np.float32)

    """ Load model and predict """
    model = XGBClassifier(seed=42)
    model.load_model(MODEL_PATH)
    result = model.predict_proba(final_inputs)

    return result


