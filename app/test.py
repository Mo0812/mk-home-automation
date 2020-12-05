import pickle
import xgboost as xgb

with open("app/model/gb-model.prev.bin", "rb") as f_in:
    om, od = pickle.load(f_in)

with open("app/model/gb-model.bin", "rb") as f_in:
    nm, nd = pickle.load(f_in)

data = {
    "instanceid": 65537,
    "type": 2,
    "weekday": "Tuesday",
    "time": "20:30"
}

X_data = od.transform([data])
ddata = xgb.DMatrix(X_data, feature_names=od.feature_names_)
prediction = om.predict(ddata)
print("old:", prediction[0], prediction[0] >= 0.5)

X_data = nd.transform([data])
ddata = xgb.DMatrix(X_data, feature_names=nd.feature_names_)
prediction = nm.predict(ddata)
print("old:", prediction[0], prediction[0] >= 0.5)
