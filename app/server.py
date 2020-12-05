import ml as model
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask('mkha')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    prediction, onoff = model.predict(data)

    result = {
        'onoff_probability': float(prediction),
        'onoff': bool(onoff)
    }

    return jsonify(result)


@app.route('/fit', methods=['POST'])
def fit():
    csv = request.files["file"]
    try:
        model.refit(csv)
        result = {
            "success": True
        }
        return jsonify(result)
    except Exception as e:
        print(e)
        abort(500, e)


if __name__ == '__main__':
    debugging = bool(os.getenv("DEBUGGING") == "True")
    app.run(debug=debugging, host='0.0.0.0', port=9090)
