# import pastebin2

# Read and display the file content
# with open("app.log", "r") as file:
#     content = file.read()
#     lines = content.split('\n')
#     for line in lines:
#         if line.strip():  # Only print non-empty lines
#             print(line.strip())

# Upload to pastebin
# user_key = pastebin2.generate_user_key(pastebin2.api_dev_key, pastebin2.username, pastebin2.password)
# result = pastebin2.upload_paste(pastebin2.api_dev_key, user_key, content.strip(), "test", "text", 0, "10M")
# print(f"Upload result: {result}")
# print("Upload completed")