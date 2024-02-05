import functools
import uuid
import datetime
from dataclasses import asdict

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    session,
    url_for,
    request,
)
from stockFind.forms import LoginForm, RegisterForm, StockForm, ExtendedStockForm
from stockFind.models import User, Stock
from stockFind.StockSentimentAnalysis import returnSentiment
from stockFind.Server.main import mainfunc

from passlib.hash import pbkdf2_sha256


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper

@pages.route("/analyze")
@login_required
def analyzeStock():
    # add code here, then send to render (do it like sentiment analyses)
    return render_template("analyzeStocks.html", stockdata='/static/stockData.png', optimalPort="/static/optimalPortfolio.png")


@pages.route("/get-sentiment-data")
@login_required
def get_sentiment_data():
    user_data = current_app.db.user.find_one({"email": session["email"]})
    if user_data is None:
        return jsonify({"error": "User data not found"}), 404

    user = User(**user_data)
    stock_data = current_app.db.stock.find({"_id": {"$in": user.stocks}})
    stocks = [Stock(**stock) for stock in stock_data]
    ids = [stock._id for stock in stocks]
    names = [stock.company for stock in stocks]
    tickers = [stock.ticker for stock in stocks]

    sentiment_data = returnSentiment(tickers, 10)
    newstocks = []

    for i in range(len(tickers)):
        newstocks.append((tickers[i], sentiment_data[i], ids[i], names[i]))

    return jsonify(newstocks)

@pages.route("/get-stock-data")
@login_required
def get_stock_data():
    user_data = current_app.db.user.find_one({"email": session["email"]})
    if user_data is None:
        return jsonify({"error": "User data not found"}), 404
    

    optPort, stats, stocks = mainfunc()
    optPort = [round(dec, 2) for dec in optPort]
    stats = [round(stat,2) for stat in stats]
    return jsonify((optPort, stats, stocks))

@pages.route("/")
@login_required
def index():
    user_data = current_app.db.user.find_one({"email": session["email"]})
    if user_data is None:
        # Handle the case where user data is not found
        flash("User data not found", "error")
        return redirect(url_for(".register"))
        
    user = User(**user_data)


    stock_data = current_app.db.stock.find({"_id": {"$in": user.stocks}})
    stocks = [Stock(**stock) for stock in stock_data]
    stock_len = len(stocks)
    return render_template(
        "index.html",
        title="stockFind",
        Stock_data=stocks,
        Len = stock_len
    )


@pages.route("/register", methods=["POST", "GET"])
def register():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )

        current_app.db.user.insert_one(asdict(user))

        flash("User registered successfully", "success")

        return redirect(url_for(".login"))

    return render_template(
        "register.html", title="Stocks Watchlist - Register", form=form
    )


@pages.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for(".index"))

    form = LoginForm()

    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": form.email.data})
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for(".login"))

        user = User(**user_data)

        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email

            return redirect(url_for(".index"))

        flash("Login credentials not correct", category="danger")

    return render_template("login.html", title="Stocks Watchlist - Login", form=form)


@pages.route("/logout")
def logout():
    current_theme = session.get("theme")
    session.clear()
    session["theme"] = current_theme

    return redirect(url_for(".login"))


@pages.route("/add_stock", methods=["GET", "POST"])
@login_required
def add_stock():
    form = StockForm()

    if form.validate_on_submit():
        stock = Stock(
            _id=uuid.uuid4().hex,
            ticker=form.ticker.data,
            company=form.company.data,
            amtInvested=form.amtInvested.data
        )

        current_app.db.stock.insert_one(asdict(stock))

        current_app.db.user.update_one(
            {"_id": session["user_id"]}, {"$push": {"stocks": stock._id}}
        )

        return redirect(url_for(".stock", _id=stock._id))
    
    return render_template(
        "new_stock.html", title="stockFind - Add Stock", form=form
    )


@pages.get("/stock/<string:_id>")
def stock(_id: str):
    stock = Stock(**current_app.db.stock.find_one({"_id": _id}))
    return render_template("stock_details.html", stock=stock)


@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
