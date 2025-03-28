from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.static_url_path = '/static'
app.static_folder = 'static'

class Shoppo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)   

@app.route('/favicon.ico')
def favicon():
    print("Favicon function called")
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')   

@app.route("/")
def home():
    shoppo_list = Shoppo.query.all()
    return render_template("base.html", shoppo_list=shoppo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    quantity = request.form.get("quantity")
    new_shoppo = Shoppo(title=title, complete=False)
    db.session.add(new_shoppo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:shoppo_id>")
def update(shoppo_id):
    shoppo = Shoppo.query.filter_by(id=shoppo_id).first()
    shoppo.complete = not shoppo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete_all", methods=["POST"])
def delete_all():
    db.session.query(Shoppo).delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:shoppo_id>")
def delete(shoppo_id):
    todo = Shoppo.query.filter_by(id=shoppo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete_selected", methods=["POST"])
def delete_selected():
    selected_items = request.form.getlist('selected_items')
    for shoppo_id in selected_items:
        shoppo = Shoppo.query.filter_by(id=shoppo_id).first()
        db.session.delete(shoppo)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='0.0.0.0')





    
