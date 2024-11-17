def check_serial_obfuscated(serial):
    # Реструктурування даних: ключ розділений на частини
    correct_parts = ["A", "B", "C", "1", "2", "3", "D", "E", "F"]
    input_parts = [char for char in serial if char != "-"]

    # Логічна обфускація: перевірка у кілька етапів
    if len(input_parts) != len(correct_parts):
        return False

    for i in range(len(correct_parts)):
        if correct_parts[i] != input_parts[i]:
            return False
    return True

# Введення ключа
user_input = input("Введіть серійний ключ: ")

if check_serial_obfuscated(user_input):
    print("Серійний ключ правильний!")
else:
    print("Серійний ключ невірний!")

