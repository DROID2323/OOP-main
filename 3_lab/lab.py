class MyName:
    """Опис класу / Документація"""
    total_names = 0  # Змінна класу

    def __init__(self, name=None) -> None:
        """Ініціалізація об'єкта"""
        if name is None:
            name = self.anonymous_user().name
        if not name.isalpha():
            raise ValueError("Ім'я може містити лише літери!")
        self.name = name.capitalize()
        MyName.total_names += 1
        self.my_id = MyName.total_names

    @property
    def whoami(self) -> str:
        """Властивість: повертає ім'я"""
        return f"My name is {self.name}"

    @property
    def my_email(self) -> str:
        """Властивість: повертає email"""
        return self.create_email()

    def create_email(self, domain="itcollege.lviv.ua") -> str:
        """Метод: створює email з доменом"""
        return f"{self.name}@{domain}"

    def name_length(self) -> int:
        """Метод: рахує кількість букв у імені"""
        return len(self.name)

    @property
    def full_name(self) -> str:
        """Властивість: форматований рядок з ім'ям та email"""
        return f"User #{self.my_id}: {self.name} ({self.my_email})"

    @classmethod
    def anonymous_user(cls):
        """Метод класу: створює об'єкт Anonymous"""
        return cls("Anonymous")

    @staticmethod
    def say_hello(message="Hello to everyone!") -> str:
        """Статичний метод: повертає привітання"""
        return f"You say: {message}"

    def save_to_file(self, filename="users.txt") -> None:
        """Метод: зберігає дані у файл"""
        with open(filename, "a", encoding="utf-8") as f:
            f.write(self.full_name + "\n")


# --- Основна частина програми ---
print("Розпочинаємо створювати об’єкти!")

names = ("Bohdan", "Marta", None, "Dima")
all_names = {name: MyName(name) for name in names}

for name, me in all_names.items():
    print(f"""{">*<"*20}
This is object: {me}
This is object attribute: {me.name} / {me.my_id}
This is {type(MyName.whoami)}: {me.whoami} / {me.my_email}
This is {type(me.create_email)} call: {me.create_email("gmail.com")}
This is static {type(MyName.say_hello)} with custom message: {me.say_hello("Привіт, група!")}
This is class variable {type(MyName.total_names)}: from class {MyName.total_names} / from object {me.total_names}
Length of name: {me.name_length()}
Full name: {me.full_name}
Saving to file...
{"<*>"*20}""")
    me.save_to_file()

print(f"\n✅ Ми створили {MyName.total_names} об’єктів!")
