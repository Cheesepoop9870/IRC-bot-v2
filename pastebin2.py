import requests
# from pastebin import PastebinAPI
import logging as log
import os
api_dev_key = os.getenv("PASTEBIN_API_KEY")
username = 'cheesepoop9870'
password = os.getenv("MAIN_PASSWORD")

def generate_user_key(api_dev_key, username, password):
    """Generate a user key for Pastebin API.
    Args:
        api_dev_key (str): The API developer key.
        username (str): The Pastebin username.
        password (str): The Pastebin password.
    """
    log.info("Generating user key")
    login_url = "https://pastebin.com/api/api_login.php"
    login_payload = {
        "api_dev_key": api_dev_key,
        "api_user_name": username,
        "api_user_password": password
    }
    login_request = requests.post(login_url, login_payload)
    log.info(f"Login request status code: {login_request.status_code}")
    log.info(f"User key generated: {login_request.text}")
    return login_request.text

def upload_paste(api_dev_key, user_key, paste_code, paste_name, paste_format, paste_private, paste_expire_date):
    """Upload a paste to Pastebin.
    Args:
        api_dev_key (str): The API developer key.
        user_key (str): The user key.
        paste_code (str): The code to upload.
        paste_name (str): The name of the paste.
        paste_format (str): The format of the paste.
        paste_private (int): The privacy level of the paste.
        paste_expire_date (str): The expiration date of the paste.
        """
    response = requests.post("https://pastebin.com/api/api_post.php", data={"api_dev_key": api_dev_key, "api_option": "paste", "api_paste_code": paste_code, "api_paste_private": paste_private, "api_paste_name": paste_name, "api_paste_expire_date": paste_expire_date, "api_paste_format": paste_format, "api_user_key": user_key})
    return response.text
def get_paste(api_dev_key, user_key, paste_key):
    """Get a paste from Pastebin.
    Args:
        api_dev_key (str): The API developer key.
        user_key (str): The user key.
        paste_key (str): The paste key.
        """
    return requests.post("https://pastebin.com/api/api_post.php", data={"api_dev_key": api_dev_key, "api_option": "show_paste", "api_paste_key": paste_key, "api_user_key": user_key, })

def main():
    user_key = generate_user_key(api_dev_key, username, password)
    print(user_key)
    upload_paste(api_dev_key, user_key, "test", "test", "python", 0, "10M")

if __name__ == "__main__":
    main()
