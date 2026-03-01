# Основні парадигми ООП у Python

## Мета роботи
Ознайомитись з ключовими поняттями об’єктно-орієнтованого програмування (ООП) у Python та навчитися реалізовувати їх у власних класах на прикладі ігрової симуляції.

---
1.

    class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            return amount
        else:
            return "Insufficient funds"

    def get_balance(self):
        return self.__balance



2.

    class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def display_info(self):
        return f"{self.brand} {self.model}"

    class Car(Vehicle):
    def __init__(self, brand, model, seats):
        super().__init__(brand, model)
        self.seats = seats

    def display_info(self):
        return f"{super().display_info()}, Seats: {self.seats}"

    def honk(self):
        return f"{self.brand} {self.model} сигналить: 'Beep beep!'"


3. 

    class Animal:
    def speak(self):
        pass

    class Dog(Animal):
    def speak(self):
        return "Woof!"

    class Cat(Animal):
    def speak(self):
        return "Meow!"

    class Fish(Animal):
    pass

    animals = [Dog(), Cat(), Fish()]
    for animal in animals:
    print(animal.speak())  # Woof!, Meow!, None



4.

    from abc import ABC, abstractmethod

    class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2


Код гри:

    from abc import ABC, abstractmethod
    from random import randint, choice

    class Item(ABC):
    def __init__(self, name:str, health=500):
        self.name = name
        self.health = health
    
    @abstractmethod
    def attack(self, another_item):
        pass

    class Sword(Item):
    def __init__(self, name, attack_power:int):
        super().__init__(name=name)
        self.__attack_power = attack_power
        self._sharp = 0
    
    def attack(self, another_item:Item):
        current_attack = self.__attack_power + self._sharp + randint(0, 10)
        another_item.health -= current_attack
        return f"{self.name} атакує мечем і наносить {current_attack} шкоди. Здоров'я {another_item.name}: {another_item.health}"
    
    def sharpening(self):
        self._sharp += 1
        return f"{self.name} наточив меч."

    class Axe(Item):
    def __init__(self, name, attack_power:int):
        super().__init__(name=name)
        self.__attack_power = attack_power
        self._sharp = 0
    
    def attack(self, another_item:Item):
        current_attack = self.__attack_power + randint(0, 20)
        another_item.health -= current_attack
        return f"{self.name} атакує сокирою і наносить {current_attack} шкоди. Здоров'я {another_item.name}: {another_item.health}"

    def sharpening(self):
        self._sharp += 1
        return f"{self.name} наточив сокиру."

    class Bow(Item):
    def __init__(self, name, attack_power:int, range_power:int=5):
        super().__init__(name=name)
        self.__attack_power = attack_power
        self.range_power = range_power
    
    def attack(self, another_item:Item):
        current_attack = self.__attack_power + randint(5, 15) + self.range_power
        another_item.health -= current_attack
        return f"{self.name} стріляє з лука і наносить {current_attack} шкоди. Здоров'я {another_item.name}: {another_item.health}"
    
    def reload(self):
        self.range_power += 1
        return f"{self.name} перезарядив лук. Дальність тепер: {self.range_power}"

    # --- Випадковий вибір зброї ---
    weapons = [
    Sword("Ескалібур", 100),
    Axe("Кратос", 95),
    Bow("Леголас", 80, 10)
    ]

    player = choice(weapons)
    enemy = choice([w for w in weapons if w != player])

    print(f"Гравець отримав зброю: {player.name}")
    print(f"Противник отримав зброю: {enemy.name}")

    # --- Покрокова гра ---
    round_num = 1
    while player.health > 0 and enemy.health > 0:
    print(f"\n--- Хід {round_num} ---")
    action = input("Оберіть дію (attack / boost): ").strip().lower()
    
    if action == "attack":
        print(player.attack(enemy))
    elif action == "boost":
        if isinstance(player, Sword) or isinstance(player, Axe):
            print(player.sharpening())
        elif isinstance(player, Bow):
            print(player.reload())
    else:
        print("Невідома дія. Пропуск ходу.")

    if enemy.health <= 0:
        print(f"Перемога! {enemy.name} переможений.")
        break

    print(enemy.attack(player))
    if player.health <= 0:
        print(f"Поразка! {player.name} загинув.")
        break

    round_num += 1

## Висновок

❓ **Що зроблено в роботі:**  
У роботі розглянуто основні парадигми ООП (інкапсуляція, наслідування, поліморфізм, абстракція) на прикладах у Python. Реалізовано ігрову симуляцію з трьома типами зброї (меч, сокира, лук), де кожен клас має власну поведінку та методи.

❓ **Чи досягнуто мети роботи:**  
Так, мета роботи досягнута — продемонстровано ключові принципи ООП у практичному застосуванні.

❓ **Які нові знання отримано:**  
- Як працює інкапсуляція через приватні атрибути.  
- Як наслідування дозволяє розширювати функціонал базових класів.  
- Як поліморфізм забезпечує різну поведінку одного методу для різних класів.  
- Як абстракція задає єдиний інтерфейс для групи об’єктів.  
- Як об’єднати всі парадигми у єдиній програмі (ігровій симуляції).

❓ **Чи вдалось відповісти на всі питання задані в ході роботи:**  
Так, усі питання були розглянуті та пояснені з прикладами.

❓ **Чи вдалося виконати всі завдання:**  
Так, виконано всі завдання: додано генератор випадкових чисел, нові методи у класах, створено клас без перевизначення методу, реалізовано абстрактний клас та ігрову симуляцію з трьома типами зброї.

❓ **Чи виникли складності у виконанні завдання:**  
Невеликі складності виникали при організації покрокової гри та інтерактивної взаємодії з користувачем, але вони були вирішені шляхом використання умовних операторів та перевірки типів зброї.

❓ **Чи подобається такий формат здачі роботи (Feedback):**  
Так, формат README.md є зручним, структурованим і дозволяє чітко представити як теоретичну, так і практичну частину.

❓ **Побажання для покращення (Suggestions):**  
Можна додати UML-діаграму класів для більш наочного представлення структури програми та взаємозв’язків між класами.

---
