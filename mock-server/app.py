from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join("data", "customers.json")

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/customers")
def get_customers():
    data = load_data()

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit

    paginated = data[start:end]

    return jsonify({
        "data": paginated,
        "total": len(data),
        "page": page,
        "limit": limit
    })

@app.route("/api/customers/<customer_id>")
def get_customer(customer_id):
    data = load_data()

    for customer in data:
        if customer["customer_id"] == customer_id:
            return jsonify(customer)

    return jsonify({"error": "Customer not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)