from pastebin import PastebinAPI

api_dev_key = 'aBxmsmmYtoEP3qOh1sZmMS4LVQvj7AsB'
username = 'cheesepoop9870'
password = 'Ilovestarwars321?'

my_key = PastebinAPI.generate_user_key(api_dev_key, username, password)
print(my_key)

try:
  with open('app.log', 'r') as file:
    for line in file:
      print(line.strip())
except FileNotFoundError:
  print("Error: The file 'your_file.txt' was not found.")
except Exception as e:
  print(f"An error occurred: {e}")