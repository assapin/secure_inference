import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score



dataset_url = 'https://raw.githubusercontent.com/suvoooo/Machine_Learning/master/winequality-red.csv'
data = pd.read_csv(dataset_url, sep=';')


y = data.quality
X = data.drop('quality', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=123,
                                                    stratify=y)


pipeline = make_pipeline(preprocessing.StandardScaler(),
                         RandomForestRegressor(n_estimators=100))

hyperparameters = { 'randomforestregressor__max_features' : ['auto', 'sqrt', 'log2'],
                    'randomforestregressor__max_depth': [None, 5, 3, 1]}


clf = GridSearchCV(pipeline, hyperparameters, cv=10)

clf.fit(X_train, y_train)

pred = clf.predict(X_test)
print(r2_score(y_test, pred))
print(mean_squared_error(y_test, pred))

#joblib.dump(clf, '../model/rf_regressor.pkl')
# To load: clf2 = joblib.load('rf_regressor.pkl')