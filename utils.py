from os import remove, listdir, getlogin

PATH = f"C:\\Users\\{getlogin()}\\Downloads"


def remove_file():
    try:
        for file in listdir(f"{PATH}"):
            if file.endswith(".png"):
                remove(f"{PATH}\\{file}")
    except Exception as error:
        pass


if __name__ == "__main__":
    # print(f"C:\\Users\\{getlogin()}\\Downloads")
    remove_file()
