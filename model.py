import pandas as pd
from sklearn.feature_selection import chi2
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

bundas_train = pd.read_csv("bundas_train.csv")
bundas_train['Store_Size'] = bundas_train.Store_Size.fillna('Unknown')

weight = bundas_train[['Weight']]
bundas_train[['Weight']] = bundas_train.Weight.fillna(float(weight.mean()))

bundas_train.FatContent.replace('low fat', 'Low Fat', inplace=True)
bundas_train.FatContent.replace('LF', 'Low Fat', inplace=True)
bundas_train.FatContent.replace('reg', 'Regular', inplace=True)

X_train = bundas_train.drop(['Item_ID', 'Weight', 'Store_Establishment_Year', 'Store_ID', 'Item_Store_Sales'], axis=1)
y_train = bundas_train['Item_Store_Sales']

X_train_features = pd.get_dummies(X_train)

X_train_final, X_validation, y_train_final, y_validation = train_test_split(X_train_features, y_train, test_size=0.3)

model = linear_model.LinearRegression()
model.fit(X=X_train_final, y=y_train_final)
y_pred = model.predict(X_validation)
print(r2_score(y_validation, y_pred))


def preprocess_input(user_item_details):
    data = pd.DataFrame(user_item_details)
    encoded_data = pd.get_dummies(data)
    missing_cols = set(X_train_final.columns) - set(encoded_data.columns)
    print(data.dtypes)
    print(X_train_final.columns)
    print(encoded_data.columns)
    print(missing_cols)

    for column in missing_cols:
        encoded_data[column] = 0
    encoded_data = encoded_data[X_train_final.columns]
    return encoded_data


def model_predict(encoded_item_data):
    item_sales_pred = model.predict(encoded_item_data)
    return item_sales_pred
