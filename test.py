from pastebin import PastebinAPI

api_dev_key = ''
username = 'cheesepoop9870'
password = 'Ilovestarwars321?'

my_key = PastebinAPI.generate_user_key("aBxmsmmYtoEP3qOh1sZmMS4LVQvj7AsB", "cheesepoop9870","Ilovestarwars321?")
print(my_key)

try:
  with open('app.log', 'r') as file:
    for line in file:
      print(line.strip())
except FileNotFoundError:
  print("Error: The file 'your_file.txt' was not found.")
except Exception as e:
  print(f"An error occurred: {e}")