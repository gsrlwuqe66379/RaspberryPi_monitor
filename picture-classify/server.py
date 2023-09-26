from sanic import Sanic
from sanic.response import json
from sanic.response import text

app = Sanic(__name__)


@app.route("/data")
async def get_data(request):
    with open("data.json", "r") as f:
        data = f.read()
        print(data)
    return json(data)


@app.route("/")
async def hello_world(request):
    return text("Hello, world.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5391, debug=False)
