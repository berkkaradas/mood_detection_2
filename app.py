from flask import (
    Flask,
    render_template,
    request,
    flash,
    make_response,
    redirect,
    url_for,
)
from db_dao import (
    create_user,
    check_credentials,
    create_user_preferences,
    user_preference_is_existed,
)
from secrets import token_urlsafe
from utils import remove_file
from mood_detection import detect_mood, random_music_picker,music_artist_finder

PATH = "C:\\Users\\bear_s_computer\\Downloads"

# app object
app = Flask(__name__)
app.secret_key = token_urlsafe(15)


@app.route("/", methods=["POST", "GET"])
def welcome_page():
    """
    Sign-In & Sign-Up Page
    """
    # user send get request to http://127.0.0.1:5000/
    if request.method == "GET":
        return render_template("signin_signup/index.html")
    # user submitted signup btn
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
    # user submitted signin btn
    elif request.method == "POST" and request.form.get("signin_btn"):
        email = request.form.get("email")
        password = request.form.get("password")
        if check_credentials(email=email, password=password):
            response = make_response(redirect("/homepage"))
            response.set_cookie("email", email)
            return response
        else:
            flash("Please check your credentials")
            return render_template("signin_signup/index.html")


@app.route("/homepage", methods=["POST", "GET"])
def home_page():
    # clean previous images
    remove_file()
    active_user = request.cookies.get("email")
    # user send get request to http://127.0.0.1:5000/homepage
    try:
        if request.method == "GET":
            # clean previous images
            remove_file()
            return render_template("homepage/homepage.html")
        elif request.method == "POST":
            # clean previous images
            remove_file()
            if request.form.get("like_btn"):
                return render_template("homepage/homepage.html")
            # user did not like recommended music
            elif request.form.get("dont_like_btn"):
                if request.cookies.get("music_name") and request.cookies.get(
                    "label_number"
                ):
                    music_name = request.cookies.get("music_name")
                    label_number = request.cookies.get("label_number")
                else:
                    music_name = "I will rock you"
                    label_number = 1
                create_user_preferences(music_id=music_name, user_email=active_user)
                # generate new music
                music_name = random_music_picker(label_number=int(label_number),user_email=active_user)
                music_artist = music_artist_finder(music_name=music_name)
                if user_preference_is_existed(
                    music_id=music_name, user_email=active_user
                ):
                    music_name = random_music_picker(label_number=int(label_number),user_email=active_user)
                    music_artist=music_artist_finder(music_name=music_name)
                return render_template("homepage/homepage.html", music_name=music_name,music_artist=music_artist)
            # user take photo from camera
            else:
                # clean previous images
                remove_file()
                try:
                    detection_result = detect_mood(file_path=f"{PATH}\emotion_snapshot.png")
                    music_name = random_music_picker(
                        label_number=int(detection_result["label"]),user_email=active_user
                    )
                    person_mood=detection_result['mood']
                    music_artist = music_artist_finder(music_name=music_name)
                    response = make_response(
                        render_template("homepage/homepage.html", music_name=music_name,music_artist=music_artist,person_mood=person_mood)
                    )
                    # set cookies to access music name and label number later
                    response.set_cookie("music_name", music_name)
                    response.set_cookie("label_number", str(detection_result["label"]))
                    return response
                except Exception as error:
                    return render_template("homepage/homepage.html",music_name=error,music_artist="We will recommend you your music!",person_mood="Let's find your mood")
    except Exception as error:
        return render_template("homepage/homepage.html",music_name=error,music_artist="We will recommend you your music!",person_mood="Let's find your mood")


if __name__ == "__main__":
    app.run(debug=True)
