from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

products = [
    {
        'id': 1,
        'title': 'Microsoft Surface Laptop',
        'price': 1249,
        'quantity': 2
    },
    {
        'id': 2,
        'title': 'Dell XPS 13',
        'price': 1000,
        'quantity': 1
    }
]

# READ

@app.route('/')
def show_products():
    return render_template('index.html', products=products)

#UPDATE
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = None

    for item in products:
        if item['id'] == product_id:
            product = item
            break

    if product is None:
            return "User not found", 404

    if request.method == 'POST':
        product["title"] = request.form.get("title")
        product["price"] = request.form.get("price")
        product["quantity"] = request.form.get("quantity")

        return redirect(url_for("show_products"))

    return render_template("edit_product.html", product=product)


# CREATE
@app.route('/product/create/', methods=['POST', 'GET'])
def create_product():
    if request.method == 'POST':
        title = request.form.get("title")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        new_product = {
            "id": len(products) + 1,
            "title": title,
            "price": price,
            "quantity": quantity,
        }
        products.append(new_product)

        return redirect(url_for("show_products"))
    return render_template("create_product.html")

if __name__ == '__main__':
    app.run(debug=True)
