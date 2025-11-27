from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        orders = db.get_all_orders()
        if request.args.get('warning'):
            warning = request.args.get('warning')
            return render_template('form.html', orders=orders, warning=warning)
        return render_template('form.html', orders=orders)

# Part2: /product 路由
@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():
    if request.method == 'GET':
        category = request.args.get("category")
        product = request.args.get("product")

        if category:  # 查詢商品種類下的商品列表
            product_list = db.get_product_names_by_category(category)
            return jsonify({"product": product_list})

        elif product:  # 查詢商品價格
            price = db.get_product_price(product)
            return jsonify({"price": price})

        else:
            return jsonify({"error": "Missing parameters"}), 400

    elif request.method == 'POST':
        data = request.get_json()  # 前端送來的 JSON
        order_data = {
            "product_date": data.get("date"),
            "customer_name": data.get("customer"),
            "product_name": data.get("product"),
            "product_amount": int(data.get("quantity")),
            "product_total": float(data.get("price")) * int(data.get("quantity")),
            "product_status": data.get("status"),
            "product_note": data.get("note")
        }
        db.add_order(order_data)
        return jsonify({"message": "Order placed successfully"}), 200

    elif request.method == 'DELETE':
        order_id = request.args.get("order_id")
        if not order_id:
            return jsonify({"error": "Missing order_id"}), 400
        db.delete_order(order_id)
        return jsonify({"message": "Order deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)