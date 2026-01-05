import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# File path for data
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- ROUTES ---

@app.route('/')
def index():
    items = load_data()
    # Get search query from the search bar
    search_query = request.args.get('search', '').lower()
    if search_query:
        items = [i for i in items if search_query in i['name'].lower()]
    return render_template('index.html', items=items)

@app.route('/admin')
def admin():
    items = load_data()
    return render_template('admin.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    price = request.form.get('price')
    if name and price:
        items = load_data()
        items.append({'name': name, 'price': price})
        save_data(items)
    return redirect(url_for('admin'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    items = load_data()
    if 0 <= item_id < len(items):
        items.pop(item_id)
        save_data(items)
    return redirect(url_for('admin'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
