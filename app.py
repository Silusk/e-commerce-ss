from flask import Flask, render_template, request, redirect, session,url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")
products = {

    "silk-gown": {
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCl5xiv83dzci-tOgnnJfD-10WB8fq6O0qusFPVGvjvUJH_AWhi050tIbYZsrutrP4O6NXgj79rbfcglK5jRzx3J7LuaLyMVSTgX73FIr6cJgeDhuHCjeN5b6R_mI3U1YPfeo7wiBaPIbXgL2gzfD5XuapL4923b-xjpOOrEyQcbQqaCLfwdDVNzy8cYOROM4h7EGekvTvjqnRNu6zbFz-OkgUwJ3qBWOlHlwbkjqh6hoT2_4GPWGhlnMTa9rfxib5lti1nyhTZwkU",
        "price": 420
    },

    "cashmere-coat": {
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAUQBJ---KNqr0Bm9Q_nfCxDZZz2kjtaNWOTeN-sNCr4oirzNs9kPTqPnkNo9BUhKe4S_-PpopGMs97NMQKT5Gr7v0vvIg3w8-Z-5rFGdG7IS1ucXzNNJ7DqSl0faPGUsGESa9cJs2R8ky9jdaSNhsMw3AQorSWJijWo3QrJHHTOeYc_BNJ5dcpsYhlAXMQ5pIcFQ-2_EREzEAdUjEFLUPI9bY305swg36TpJGfcswAFSRnsQ8j-ltstKixCk3AdB4_vPeDLdWqcWU",
        "price": 850
    },

    "trousers": {
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAdwsCApGVKcKvdN28ciNw4TPuL8CnFvz_HDtNbxhmDa16Nhff-898Trwrzor0IA9G-i21-pg7OGEj4MbpCZmStg7IAkZ6jcL4s4zLIcT9AusKDH9-7OznMWiFucgcpFoG866IJULKQI77Uzf-CJE_3pGtJqdtaq-9_XUfa79Rk1mBeG47VkYyMavsrWEL7BhvYOjENTJf6QvcM9T5OsiT7zzlbW0TzyteYsBj3qnVFvAjEDI7pNVktoN71kn0bZRA0GANA5zsujUM",
        "price": 290
    },

    "blazer": {
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBatNb48hHetbyJ9YfkWxmdJ7w5hGxNxC7dUj3tpKnei_IsSEWb7AYqhktRRnR0pyefhpKAtXL3N_sm3w-q5lf9uQGuJSVoCwnPze10Qj1Be4opx5ffQlb4f8UGJ50zDCo5ucoEmUZeSXbYUgq_wXns9TjGef880dlZyMeFRQqsYU8LGuMLTm4OVvIonSWUa41m6rjN4MxxufIgVzrkAzfHzwEYuzddRlX9WhKRvDjy8BTC8nBUFqvoyuuGDLJE6f1gLubkIBARaCo",
        "price": 560
    },

    "polo": {
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuDDF4zEwJ7U-vMl5pUuQygZh-DleE4J0FhFjPDG6BKLcUfoiha5iO3cxkjrh_zU4AWn3atMdDJDPBa1shAwTA97RxmmXQw_MsFFKkqUDk8nho4v7zH7B84dlmL_4sqnXfPGt_sPmVlT2lSW_Ag6lmZotcyiMH704EYf2xRHvTWErShgH_LV6sF6stLiK5cPrcCf0HeVGoSFNe628_cg_-XFmwTP2Al7vJdlc0Xs5T9AJhp3zmw8dQ6__OfritpsdpX0loo0qtPDvkg",
        "price": 185
    },

    "denim": {
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAkjDbdDkiTq1aKskJpNddCRoZ26MCIXpUS0j1M_OBqIiIjLuVf59_coLHVXe88Gqlk5PYuANWEnaOQWDTGILiVkBe9TW2W2J-m9X2fUnhX60RczPhomcFWN9CHVBuvTQivH3odmVlk5E3epbFhXI1cj458XQK8gZh6zWeABqGUDG2L2W5gzeBmxpYZoJq2-yksnu0s05hkGlKynIwZpmCCO7VAqWwIIFFZREompf-sOphVL1AViBF21Vjfs-_F8-TzFasWgCDIwi0",
        "price": 210
    }

}

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def login_page():
    return render_template("home.html")
@app.route("/galary")
def galary():
    return render_template("galary.html")



# LOGIN
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()

    conn.close()

    if user:
        session["user"] = email
        return redirect("/home")
    else:
        return "Invalid email or password"

# REGISTER
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return "Email already exists"

    conn.close()

    return redirect("/")

# HOME PAGE
@app.route("/home")
def home():
        return render_template("home.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
@app.route("/collections")
def collections():
    return render_template("collections.html")

@app.route("/product/<name>")
def product(name):
    item = products.get(name)
    return render_template(
        "product.html",
        product=name,
        image=item["image"],
        price=item["price"]
    )
@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    return render_template("cart.html", cart=cart_items)
@app.route("/contactus")
def contact_page():
    return render_template("contact us.html")
@app.route("/reviews")
def contacts():
    return render_template("reviews.html")


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"]
    mobile = request.form["mobile"]
    email = request.form["email"]
    message = request.form["message"]

    sender_email = os.environ.get("email_id")
    password = os.environ.get("app_pass")
    receiver_email = "silus09032004@gmail.com"

    body = f"""
New Contact Request

Name: {name}
Mobile: {mobile}
Email: {email}
Message: {message}
"""

    msg = MIMEText(body)
    msg["Subject"] = "New Website Enquiry"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    return "Thank you! We will contact you soon."
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/refund")
def refund():
    return render_template("refund.html")

@app.route("/shipping")
def shipping():
    return render_template("shipping.html")

if __name__ == "__main__":
    app.run(debug=True)
    
