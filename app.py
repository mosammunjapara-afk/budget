from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

budget_data = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/transactions")
def get_transactions():
    return jsonify(budget_data)

@app.route("/api/add", methods=["POST"])
def add_transaction():
    data = request.get_json()

    try:
        amount = float(data.get("amount", 0))
    except:
        amount = 0.0

    budget_data.append({
        "name": data.get("name"),
        "type": data.get("type"),
        "amount": amount,
        "category": data.get("category") or "General",
        "date": data.get("date") or "-"
    })

    return jsonify({"success": True, "data": budget_data})

@app.route("/api/edit/<int:index>", methods=["POST"])
def edit_transaction(index):
    if 0 <= index < len(budget_data):
        data = request.get_json()
        t = budget_data[index]

        t["name"] = data.get("name")
        t["type"] = data.get("type")
        t["category"] = data.get("category") or "General"
        t["date"] = data.get("date") or "-"

        try:
            t["amount"] = float(data.get("amount", 0))
        except:
            t["amount"] = 0.0

        return jsonify({"success": True, "data": budget_data})

    return jsonify({"success": False, "error": "Invalid index"})

@app.route("/api/delete/<int:index>", methods=["POST"])
def delete_transaction(index):
    if 0 <= index < len(budget_data):
        budget_data.pop(index)
        return jsonify({"success": True, "data": budget_data})

    return jsonify({"success": False, "error": "Invalid index"})

if __name__ == "__main__":
    app.run(debug=True)
