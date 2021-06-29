import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")



@app.route("/")
@login_required
def index():
    """The index page"""

    # Pull the dict from db with chart data
    chart = db.execute(f"SELECT category, description, transacted, cost FROM tracking WHERE id = {session['user_id']} ORDER BY transacted DESC")

    totalspend = db.execute(f"SELECT sum(cost) FROM tracking where id = {session['user_id']}")

    for p in totalspend:
        tot = p['sum(cost)']



    return render_template("index.html", chart=chart, usd=usd, totalspend=totalspend, tot=tot)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirm password matches
        elif not request.form.get("confirmation"):
            return apology("Please Confirm Password", 403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords Do Not Match", 403)

        # Enter new user's info into the database
        username = request.form.get("username")

        password = generate_password_hash(request.form.get("password"))

        # generate_password_hash('password')

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=password)

        # Take user to Index/home page

        return render_template("login.html")

    # Show the page is requested via GET
    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    """Add a spending item"""

    # Set the current user as user_id
    user_id = session["user_id"]

    if request.method == "POST":

        # Error checking all three fields

        cat = request.form.get("category")
        if cat == None:
            return apology("Missing Cateogry", 403)

        descrip = request.form.get("description")
        if descrip == '':
            return apology("Missing Description", 403)

        cos = request.form.get("cost")
        if cos == '':
            return apology("Missing Cost", 403)

        # Upate tracking DB with all three values, along with id

        db.execute("INSERT INTO tracking (id, category, description, cost) VALUES (?, ?, ?, ?)", (user_id, cat, descrip, cos))

        # Redirect home
        return redirect("/")


    else:
        # Render the page if just visiting
        return render_template("add.html")



@app.route("/data", methods=["GET", "POST"])
@login_required
def data():

    # Set the current user as user_id
    user_id = session["user_id"]

    # Get Savings total
    savingsdict = db.execute("SELECT sum(cost) FROM tracking WHERE id=? AND category=?", (user_id, "Savings"))

    for p in savingsdict:
        savings = p['sum(cost)']

    if savings == None:
        savings = 0

    # Get Other total
    otherdict = db.execute("SELECT sum(cost) FROM tracking WHERE id=? AND category=?", (user_id, "Other"))

    for p in otherdict:
        other = p['sum(cost)']

    if other == None:
        other = 0

    # Get Bills total
    billsdict = db.execute("SELECT sum(cost) FROM tracking WHERE id=? AND category=?", (user_id, "Bills"))

    for p in billsdict:
        bills = p['sum(cost)']

    if bills == None:
        bills = 0

    # Get Entertainment total
    Entertainmentdict = db.execute("SELECT sum(cost) FROM tracking WHERE id=? AND category=?", (user_id, "Entertainment"))

    for p in Entertainmentdict:
        Entertainment = p['sum(cost)']

    if Entertainment == None:
        Entertainment = 0

    # Get Clothing total
    Clothingdict = db.execute("SELECT sum(cost) FROM tracking WHERE id=? AND category=?", (user_id, "Clothing"))

    for p in Clothingdict:
        Clothing = p['sum(cost)']

    if Clothing == None:
        Clothing = 0

    # Get Health total
    Healthdict = db.execute("SELECT sum(cost) FROM tracking WHERE id=? AND category=?", (user_id, "Health"))

    for p in Healthdict:
        Health = p['sum(cost)']

    if Health == None:
        Health = 0

    # Get Transportation total
    Transportationict = db.execute("SELECT sum(cost) FROM tracking WHERE id=? AND category=?", (user_id, "Transportation"))

    for p in Transportationict:
        Transportation = p['sum(cost)']

    if Transportation == None:
        Transportation = 0

    return render_template("data.html", savings=savings, other=other, usd=usd, bills=bills, Entertainment=Entertainment, Clothing=Clothing, Health=Health, Transportation=Transportation)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():

    # Set the current user as user_id
    user_id = session["user_id"]

    # Get nov avg
    novdict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-11-1' AND date <= '2020-11-31' AND id=?", (user_id))

    for p in novdict:
        nov = p['avg(cost)']

    if nov == None:
        nov = 0

    # Get jan avg
    jandict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-01-1' AND date <= '2020-01-31' AND id=?", (user_id))

    for p in jandict:
        jan = p['avg(cost)']

    if jan == None:
        jan = 0

    # Get feb avg
    febdict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-02-1' AND date <= '2020-02-31' AND id=?", (user_id))

    for p in febdict:
        feb = p['avg(cost)']

    if feb == None:
        feb = 0

    # Get mar avg
    mardict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-03-1' AND date <= '2020-03-31' AND id=?", (user_id))

    for p in mardict:
        mar = p['avg(cost)']

    if mar == None:
        mar = 0

    # Get apr avg
    aprdict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-04-1' AND date <= '2020-04-31' AND id=?", (user_id))

    for p in aprdict:
        apr = p['avg(cost)']

    if apr == None:
        apr = 0

    # Get may avg
    maydict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-05-1' AND date <= '2020-05-31' AND id=?", (user_id))

    for p in maydict:
        may = p['avg(cost)']

    if may == None:
        may = 0

    # Get jun avg
    jundict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-06-1' AND date <= '2020-06-31' AND id=?", (user_id))

    for p in jundict:
        jun = p['avg(cost)']

    if jun == None:
        jun = 0

    # Get jul avg
    juldict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-07-1' AND date <= '2020-07-31' AND id=?", (user_id))

    for p in juldict:
        jul = p['avg(cost)']

    if jul == None:
        jul = 0

    # Get aug avg
    augdict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-08-1' AND date <= '2020-08-31' AND id=?", (user_id))

    for p in augdict:
        aug = p['avg(cost)']

    if aug == None:
        aug = 0

    # Get sep avg
    sepdict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-09-1' AND date <= '2020-09-31' AND id=?", (user_id))

    for p in sepdict:
        sep = p['avg(cost)']

    if sep == None:
        sep = 0

    # Get octo avg
    octodict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-10-1' AND date <= '2020-10-31' AND id=?", (user_id))

    for p in octodict:
        octo = p['avg(cost)']

    if octo == None:
        octo = 0

    # Get dec avg
    decdict = db.execute("SELECT avg(cost) from tracking WHERE category <> 'Savings' AND date >= '2020-12-1' AND date <= '2020-12-31' AND id=?", (user_id))

    for p in decdict:
        dec = p['avg(cost)']

    if dec == None:
        dec = 0

    return render_template("history.html", usd=usd, jan=jan, feb=feb, mar=mar, apr=apr, may=may, jun=jun, jul=jul, aug=aug, sep=sep, octo=octo, nov=nov, dec=dec)



# -----------------------------------------------------------------------------------------
#Error handling below:

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
