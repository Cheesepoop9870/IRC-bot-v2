import pastebin2
with open("app.log", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())
    # print(file.read().replace("\n", ""))
    pastebin2.upload_paste(pastebin2.api_dev_key,   pastebin2.generate_user_key(pastebin2.api_dev_key, pastebin2.username, pastebin2.password), file.read().strip(), "test", "text", 0, "10M")
    # print("uploaded", end="\n"))