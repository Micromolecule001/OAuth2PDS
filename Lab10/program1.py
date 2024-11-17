def check_serial(serial):
    correct_serial = "ABC-123-DEF"
    return serial == correct_serial

# Введення ключа
user_input = input("Введіть серійний ключ: ")

if check_serial(user_input):
    print("Серійний ключ правильний!")
else:
    print("Серійний ключ невірний!")

