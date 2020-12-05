import model
from flask import Flask, request, jsonify

app = Flask('mkha')


@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    prediction, onoff = model.predict(customer)

    result = {
        'onoff_probability': float(prediction),
        'onoff': bool(onoff)
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)