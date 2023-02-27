import worker
import services
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    name = "Hello and Welcome"
    return render_template('hello.html', name=name)


@app.route('/<token>', methods=['GET', 'POST'])
def bot_requests(token=None):
    services_obj = services.services()

    if request.method == "POST" and token == services_obj.get_config()["post_secret"]:
        services_obj.logs(msg=request.json, file_name="flask_app")
        worker_obj = worker.worker(request.json, services_obj)
        worker_obj.start_worker()
        response = {"ok": True}
        return jsonify(**response)
    else:
        name = "Hello and Welcome"
        return render_template('hello.html', name=name)
