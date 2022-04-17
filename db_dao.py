import sqlite3 as sql


def create_user(name: str, email: str, password: str) -> bool:
    """
    This method is used to create a new user
    """
    if not user_is_exist(email):
        with sql.connect("user_data.sqlite3") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Users (name,email,password) VALUES (?,?,?)",
                (name, email, password),
            )
        return True
    else:
        return False


def create_user_preferences(music_id: str, user_email: str) -> bool:
    """
    This method is used to create a user preference
    """
    try:
        if not user_preference_is_existed(music_id=music_id, user_email=user_email):
            with sql.connect("user_data.sqlite3") as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO User_Selection (music_id,user_email) VALUES (?,?)",
                    (
                        music_id,
                        user_email,
                    ),
                )
            return True
        # preference already existed
        else:
            return False
    # server encountered with error
    except Exception as error:
        return False


def user_preference_is_existed(music_id: str, user_email: str) -> bool:
    """
    This method is used to check user preference existence
    """
    with sql.connect("user_data.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT music_id FROM User_Selection where music_id=? and user_email=?",
            (
                music_id,
                user_email,
            ),
        )
        user_preference = cursor.fetchall()
        if user_preference:
            return True
        else:
            return False


def user_is_exist(email: str) -> bool:
    """
    This method is used to check user existence
    """
    with sql.connect("user_data.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM Users where email=?", (email,))
        user = cursor.fetchall()
        if user:
            return True
        else:
            return False


def check_credentials(email: str, password: str) -> bool:
    """
    This method is used to check credentials
    User id start from
    """
    with sql.connect("user_data.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT email FROM Users WHERE email=? AND password=?", (email, password)
        )
        email = cursor.fetchall()
        if email:
            return True
        else:
            return False


if __name__ == "__main__":
    create_user_preferences(music_id="1", user_email="112")
