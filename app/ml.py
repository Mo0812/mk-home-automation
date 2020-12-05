import pickle
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import os

with open("app/model/gb-model.bin", "rb") as f_in:
    model, dv = pickle.load(f_in)


def predict(data):
    X_data = dv.transform([data])
    ddata = xgb.DMatrix(X_data, feature_names=dv.feature_names_)
    prediction = model.predict(ddata)
    return prediction[0], prediction[0] >= 0.5


def load_model(filename):
    with open("app/model/" + filename, "rb") as f_in:
        model, dv = pickle.load(f_in)


def save_model(filename, model, dv):
    with open("app/model/" + filename, "wb") as f_out:
        pickle.dump((model, dv), f_out)


def _prepare_data(df):
    df.columns = df.columns.str.lower()
    df.protocoltime = pd.to_datetime(df.protocoltime)
    df.protocoltime = df.protocoltime.round('15min')

    devices = df.instanceid.unique()

    absolute_min_date = df.protocoltime.min(axis=0)
    absolute_max_date = df.protocoltime.max(axis=0)
    print("absolute_min_date=%s, absolute_max_date=%s" %
          (absolute_min_date, absolute_max_date))

    complete_time_data = pd.date_range(
        absolute_min_date, absolute_max_date, freq="15min")
    complete_time_data = complete_time_data.tz_localize(None)

    complete_arr = []

    for device in devices:
        single_device = df[df["instanceid"] == device]
        single_device["protocoltime"] = pd.to_datetime(
            single_device["protocoltime"]).apply(lambda x: x.replace(tzinfo=None))
        last_state = single_device.iloc[0]
        last_state["onoff"] = 0
        for time_data in complete_time_data.values:
            if time_data in single_device.protocoltime.values:
                # TODO edge case for multiple events in one time slot
                device_row = single_device[single_device["protocoltime"] == time_data]
                complete_arr.append(device_row.values[0])
                last_state = device_row.iloc[0]
            else:
                current_state = last_state.copy()
                current_state["protocoltime"] = time_data
                complete_arr.append(current_state.values)

    df = pd.DataFrame(complete_arr, columns=df.columns)
    df = df.sort_values(by=["instanceid", "protocoltime"])

    df.color[df.color == 0] = "f1e0b5"
    df["weekday"] = df.protocoltime.dt.day_name()
    df["weekofyear"] = df.protocoltime.dt.weekofyear
    df["year"] = df.protocoltime.dt.year
    df["month"] = df.protocoltime.dt.month
    df["day"] = df.protocoltime.dt.day
    df["time"] = df.protocoltime.dt.strftime("%H:%M")

    if "id" in df.columns:
        del df["id"]
    if "lastseen" in df.columns:
        del df["lastseen"]
    if "protocoltime" in df.columns:
        del df["protocoltime"]
    del df["weekofyear"]
    del df["year"]
    del df["month"]
    del df["day"]
    del df["color"]
    del df["dimmer"]

    return df


def fit(csv):
    df = pd.read_csv(csv)
    df = _prepare_data(df)
    df_train_full, df_test = train_test_split(
        df, test_size=0.2, random_state=11)
    y_train_full_onoff = (df_train_full.onoff == 1).values
    del df_train_full["onoff"]

    dv_full = DictVectorizer(sparse=False)
    dict_train_full_onoff = df_train_full.to_dict(orient="records")
    X_train_full_onoff = dv_full.fit_transform(dict_train_full_onoff)

    dtrain_full_onoff = xgb.DMatrix(
        X_train_full_onoff, label=y_train_full_onoff, feature_names=dv_full.feature_names_)

    xgb_params = {
        'eta': 0.3,
        'max_depth': 3,
        'min_child_weight': 1,
        'colsample_bytree': 0.5,
        'subsampling': 0.5,
        'objective': 'binary:logistic',
        'nthread': 8,
        'seed': 1
    }

    model = xgb.train(xgb_params, dtrain_full_onoff, num_boost_round=490)

    return model, dv_full


def refit(csv):
    new_model, new_dv = fit(csv)
    os.rename("app/model/gb-model.bin", "app/model/gb-model.prev.bin")
    save_model("gb-model.bin", new_model, new_dv)
    load_model("gb-model.bin")
