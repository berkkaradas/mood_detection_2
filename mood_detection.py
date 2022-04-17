from cProfile import label

from pandas import read_excel
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from numpy import argmax, expand_dims
from random import choice


MUSIC_DATA = read_excel("data/music_data.xlsx")

ACTUAL_DATA = MUSIC_DATA[["SONG", "ARTIST", "Label", "LINK"]]


def detect_mood(file_path: str) -> dict:
    """
    this method is used to detect mood of given image
    :param file_path:
    :return:
    """
    MOOD_DETECTION_MODEL = load_model("data/affectnet_efficient.h5")
    result = dict()
    img = image.load_img(
        file_path,
        target_size=(224, 224),
    )
    img_array = image.img_to_array(img)

    x = expand_dims(img_array, axis=0)
    img_data = preprocess_input(x)

    predictions = MOOD_DETECTION_MODEL.predict(x)
    predictions = argmax(predictions, axis=1)
    result["label"] = int(predictions)
    if predictions == 0:
        result["mood"] = "Neutral"
    elif predictions == 1:
        result["mood"] = "Happy"
    elif predictions == 2:
        result["mood"] = "Sad"
    elif predictions == 3:
        result["mood"] = "Energetic"

    return result


def random_music_picker(label_number: int, user_email: str) -> str:
    music_list = ACTUAL_DATA[ACTUAL_DATA["Label"] == label_number].SONG.to_list()
    return str(choice(music_list))


def music_artist_finder(music_name: str):
    try:
        music_name = ACTUAL_DATA[ACTUAL_DATA["SONG"] == music_name]
        return str(music_name["ARTIST"].values[0])
    except Exception as error:
        return "We will rock you"


if __name__ == "__main__":
    print(music_artist_finder(random_music_picker(1)))
