from flask import Flask, request, make_response, jsonify
from DialogControl import DialogControl

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    dialog_control = DialogControl(req)
    dialog_control.handleRequest()
    response = dialog_control.getResponse()
    return make_response(jsonify(response))


if __name__ == '__main__':
    app.run()
