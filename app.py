from flask import Flask, request, jsonify

app = Flask(__name__)

# POST Route 
@app.route("/add", methods=["POST"])
def add_data():
    data = request.get_json()

    name = data.get("name")
    age = data.get("age")

    return jsonify({
        "message": "Data received:",
        "name": name,
        "age": age
    })


# GET Route : Home
@app.route("/")
def home():
    return "<h1>Welcome page</h1>"

# GET Route : Hello
@app.route("/hello/<name>")
def hello(name):
    return f"<h2>Hello, {name}</h2>"


if __name__ == "__main__":
    app.run(debug=True)
