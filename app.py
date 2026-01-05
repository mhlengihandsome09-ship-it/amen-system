from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_data():
    if not os.path.exists("data.json") or os.stat("data.json").st_size == 0:
        return {}
    with open("data.json", "r") as file:
        return json.load(file)

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/items")
def get_items():
    return jsonify(load_data())

@app.route("/admin", methods=["GET", "POST"])
def admin():
    data = load_data()
    if request.method == "POST":
        category = request.form.get("category").lower().strip()
        item_type = request.form.get("type").strip()
        size = request.form.get("size").strip()
        
        # Back to simple Integer
        try:
            price = int(request.form.get("price"))
        except:
            price = 0

        if category not in data: data[category] = {}
        if item_type not in data[category]: data[category][item_type] = {}
        
        data[category][item_type][size] = price
        save_data(data)
        return redirect(url_for("admin"))

    return render_template("admin.html", data=data)

@app.route("/delete/<cat>/<itype>/<size>")
def delete_item(cat, itype, size):
    data = load_data()
    if cat in data and itype in data[cat] and size in data[cat][itype]:
        del data[cat][itype][size]
        if not data[cat][itype]: del data[cat][itype]
        if not data[cat]: del data[cat]
        save_data(data)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)