"""
this package is for the use of chatzy user interface.
the intent is to "listen" in the web and invoke some functions on any new chat.
save the history and at least now do some very simple answering like hi or something.
later on the intend is to join this lib with the AI lib to obtain better NLP.

Assumptions:
 1. is that chatzy is opened in the background (can simply switch via the start menu) and it's the current tab
on chrome.
 2. chatzy is already opened and signed in, in full screen view in the chrome. (login to pass the computer is too

"""
import pyautogui

# TODO list:
# add option to record every action done by the API.
# add option to just record every action the user do.


def experiments():
    return


def get_latest_main_window_chat(lines=None):
    raise NotImplementedError


def type_in_main_window(msg):
    raise NotImplementedError


def get_all_new_chats():
    raise NotImplementedError


def answer_chat(user, msg):
    return type_in_main_window("\\pm \"" + user + "\" " + msg)


def start_record_user_actions(time=0):
    raise NotImplementedError


def switch_to_chrome():
    pass


if __name__ == "__main__":
    type_in_main_window("hi")
