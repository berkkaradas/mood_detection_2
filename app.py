from flask import Flask, render_template, request, flash
from db_dao import create_user, check_credentials,user_is_exist
from secrets import token_urlsafe

# app object
app = Flask(__name__)
app.secret_key = token_urlsafe(15)


@app.route("/", methods=["POST", "GET"])
def welcome_page():
    """
    Sign-In & Sign-Up Page
    """
    if request.method == "GET":
        return render_template("signin_signup/index.html")
    # sign-up user
    elif request.method == "POST" and request.form.get("signup_btn"):
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            if create_user(name=name, email=email, password=password):
                return render_template("signin_signup/index.html")
            else:
                flash("User already existed")
                return render_template("signin_signup/index.html")
        except Exception as error:
            flash("Server encountered with a problem. Please try again later...")
    # sign-in user
    elif request.method == "POST" and request.form.get("signin_btn"):
        email = request.form.get("email")
        password = request.form.get("password")
        if check_credentials(email=email, password=password):
            return render_template("homepage/homepage.html")
        else:
            flash("Please check your credentials")
            return render_template("signin_signup/index.html")


@app.route("/homepage", methods=["POST", "GET"])
def home_page():
    if request.method == "GET":
        return render_template("homepage/homepage.html")


if __name__ == "__main__":
    app.run(debug=True)
