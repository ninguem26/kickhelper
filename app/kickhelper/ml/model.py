import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from joblib import load, dump


dir_path = os.path.dirname(os.path.realpath(__file__))

DATA_PATH = './ks-projects-201801.csv'
MODEL_PATH = os.path.join(dir_path, 'xgb-150k-v1.model')
ENCODER_PATH = os.path.join(dir_path, 'onehot-150k.joblib')

SEED = 42


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


def load_kickstarter(path, samples=150000, seed=SEED):
    ks = pd.read_csv(path)
    ks = ks.sample(samples, random_state=seed).reset_index().drop('index', axis=1)
    return ks


def preprocess(ks):
    
    data = ks.copy()
    
    # State
    data = data.loc[data.state.isin(['failed', 'successful'])]
    data['state'] = data.state.map({'failed' : 0, 'successful': 1})
    print("State phase OK.")
    
    # Dates
    data['launched'] = pd.to_datetime(data.launched)
    data['deadline'] = pd.to_datetime(data.deadline)
    data = data.assign(day=data.launched.dt.day,
                       month=data.launched.dt.month).drop('launched', axis=1)
    print("Dates phase OK.")
    
    # Drops columns
    cols2drop = ['ID', 'name', 'deadline', 'pledged', 'backers', 'goal', 'usd pledged', 'usd_pledged_real']
    data.drop(cols2drop, axis=1, inplace=True)  # drop some columns 
    print("Drops phase OK.")

    # Drop rows with values
    data = data[(data.country != 'N,0"')]
    print("Drops rows phase OK.")
    
    # Reset index
    data.reset_index(drop=True, inplace=True)
    print("Reset phase OK.")
    
    # Encode categorical
    encoder = OneHotEncoder(sparse=False)
    cols2enc = ['category', 'main_category', 'currency', 'country']
    encoder.fit(data[cols2enc])
    encoded_categoricals = pd.DataFrame(encoder.transform(data[cols2enc]))
    data = data.drop(cols2enc, axis=1)
    data = data.join(encoded_categoricals)
    print("Encode phase OK.")
    
    # Well, I don't know yet why there are missing values 
    data.dropna(inplace=True, axis=0)
    
    return encoder, data


def build():
    
    data = load_kickstarter(DATA_PATH)
    encoder, data = preprocess(data)
    
    x_train, x_test, y_train, y_test = train_test_split(data.drop(['state'], axis=1), data.state, test_size=0.2, random_state=SEED)
    
    clf = XGBClassifier(n_jobs=6, random_state=SEED)
    clf.fit(x_train, y_train, verbose=True)
    
    dump(encoder, 'onehot-150k.joblib')
    clf.save_model('xgb-150k-v1.model')
    
    