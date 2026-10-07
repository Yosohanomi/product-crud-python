from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)

# products = [
#     {
#         'id': 1,
#         'title': 'Microsoft Surface Laptop',
#         'price': 1249,
#         'quantity': 2
#     },
#     {
#         'id': 2,
#         'title': 'Dell XPS 13',
#         'price': 1000,
#         'quantity': 1
#     }
# ]

FILE_PATH = "data/products.json"

def load_products(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)

def save_products(products, file_path):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(products, file, indent=4, ensure_ascii=False)

# READ

@app.route('/')
def show_products():
    products = load_products(FILE_PATH)

    active_products = [product for product in products if product.get("is_active", 1) == 1]
    return render_template('index.html', products=active_products)

#UPDATE
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    products = load_products(FILE_PATH)
    product = None

    for item in products:
        if item['id'] == product_id:
            product = item
            break

    if product is None:
            return "User not found", 404

    if request.method == 'POST':
        product["title"] = request.form.get("title")
        product["price"] = float(request.form.get("price", 0))
        product["quantity"] = int(request.form.get("quantity", 0))

        save_products(products, FILE_PATH)
        return redirect(url_for("show_products"))

    return render_template("edit_product.html", product=product)


# CREATE
@app.route('/product/create/', methods=['POST', 'GET'])
def create_product():
    products = load_products(FILE_PATH)
    if request.method == 'POST':
        title = request.form.get("title")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        new_product = {
            "id": len(products) + 1,
            "title": title,
            "price": price,
            "quantity": quantity,
            "is_active": 1
        }
        products.append(new_product)

        save_products(products, FILE_PATH)
        return redirect(url_for("show_products"))
    return render_template("create_product.html")

#DELETE
@app.route('/product/delete/<int:product_id>/', methods=[ 'POST'])
def delete_product(product_id):
    product = None
    products = load_products(FILE_PATH)
    for item in products:
        if item['id'] == product_id:
            product = item
            break

    if product is None:
            return "product not found", 404

    product['is_active'] = 0
    save_products(products, FILE_PATH)

    return redirect(url_for("show_products"))

if __name__ == '__main__':
    app.run(debug=True)
