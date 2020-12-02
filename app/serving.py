import pickle
import xgboost as xgb


def predict(data, model, dv):
    X_data = dv.transform([data])
    ddata = xgb.DMatrix(X_data, feature_names=dv.feature_names_)
    prediction = model.predict(ddata)
    return prediction[0]


with open("app/model/gb-model.bin", "rb") as f_in:
    model, dv = pickle.load(f_in)

######

example = {
    "instanceid": 65537,
    "type": 2,
    "weekday": "Tuesday",
    "time": "00:30"
}

prediction = predict(example, model, dv)

print("Prediciton: %.3f -> %s" % (prediction, (prediction >= 0.5)))
