# Base Character class
import random


class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health
        self.dodge_chance = 0.0

    def attack(self, opponent):
        opponent.take_damage(self.attack_power)
        print(f"{self.name} attacks {opponent.name} for {self.attack_power} damage!")

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def special_ability(self, opponent):
        raise NotImplementedError("This class does not have a special ability.")

    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")


# Warrior class
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)

    def shield_block(self):
        print(f"{self.name} uses Shield Block! 30% chance to dodge the next attack.")
        self.dodge_chance = 0.3

    def heal(self):
        heal_amount = 20
        self.health = min(self.health + heal_amount, self.max_health)
        print(f"{self.name} heals for {heal_amount}! Current health: {self.health}")

    def attack(self, opponent):
        super().attack(opponent)

    def special_ability(self, opponent):
        self.shield_block()


# Mage class
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

    def cast_spell(self, opponent):
        spell_damage = self.attack_power + 10
        opponent.take_damage(spell_damage)
        print(f"{self.name} casts a powerful spell on {opponent.name} for {spell_damage} damage!")

    def heal(self):
        heal_amount = 15
        self.health = min(self.health + heal_amount, self.max_health)
        print(f"{self.name} heals for {heal_amount}! Current health: {self.health}")

    def attack(self, opponent):
        self.cast_spell(opponent)

    def illusion(self):
        print(f"{self.name} creates an illusion! 40% chance to dodge the next attack.")
        self.dodge_chance = 0.4

    def special_ability(self, opponent):
        self.illusion()


# Evil Wizard class
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)

    def cast_dark_spell(self, opponent):
        spell_damage = self.attack_power + 5
        opponent.take_damage(spell_damage)
        print(f"{self.name} casts a dark spell on {opponent.name} for {spell_damage} damage!")

    def summon_minions(self, opponent):
        minion_damage = 10 * random.randint(1, 5)
        print(f"{self.name} summons minions! They deal {minion_damage} damage!")
        opponent.take_damage(minion_damage)

    def invisible_attack(self, opponent):
        damage = self.attack_power * 2
        print(f"{self.name} becomes invisible and strikes for {damage} damage!")
        opponent.take_damage(damage)

    def regenerate(self):
        regen = random.randint(1, 5)
        self.health = min(self.health + regen, self.max_health)
        print(f"{self.name} regenerates {regen} health! Current health: {self.health}")


# Archer class
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30)

    def double_shot(self, opponent):
        damage = self.attack_power * 2
        print(f"{self.name} uses Double Shot for {damage} total damage!")
        opponent.take_damage(damage)

    def heal(self):
        heal_amount = 10
        self.health = min(self.health + heal_amount, self.max_health)
        print(f"{self.name} heals for {heal_amount}! Current health: {self.health}")

    def attack(self, opponent):
        self.double_shot(opponent)

    def evade(self):
        print(f"{self.name} uses Evade! 50% chance to dodge the next attack.")
        self.dodge_chance = 0.5

    def special_ability(self, opponent):
        self.evade()


# Paladin class
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=20)

    def divine_shield(self):
        print(f"{self.name} uses Divine Shield! 25% chance to dodge the next attack.")
        self.dodge_chance = 0.25

    def attack(self, opponent):
        strike_damage = self.attack_power + random.randint(5, 15)
        opponent.take_damage(strike_damage)
        print(f"{self.name} uses Divine Strike for {strike_damage} damage!")

    def heal(self):
        heal_amount = 18
        self.health = min(self.health + heal_amount, self.max_health)
        print(f"{self.name} heals for {heal_amount}! Current health: {self.health}")

    def special_ability(self, opponent):
        self.divine_shield()


# Game functions
def welcome_message():
    print("Welcome, hero, to the kingdom of Shadows!")
    print("Defeat the Evil Wizard and save the land!")
    print("Choose your character wisely.\n")


def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nInput ended. Exiting game.")
        return None


def create_character():
    while True:
        print("Choose your class:")
        print("1. Warrior")
        print("2. Mage")
        print("3. Archer")
        print("4. Paladin")

        class_choice = safe_input("Enter your choice: ")
        if class_choice is None:
            return None

        name = safe_input("Enter your character's name: ")
        if name is None:
            return None

        if class_choice == '1':
            return Warrior(name)
        elif class_choice == '2':
            return Mage(name)
        elif class_choice == '3':
            return Archer(name)
        elif class_choice == '4':
            return Paladin(name)

        print("Invalid choice. Try again.\n")


def battle(player, wizard):

    def wizard_attack_with_dodge(attack_function):
        if random.random() < player.dodge_chance:
            print(f"{player.name} dodges the attack!")
            player.dodge_chance = 0.0
            return
        attack_function()
        player.dodge_chance = 0.0

    def default_wizard_action():
        action = random.choice(['attack', 'cast_dark_spell', 'summon_minions', 'invisible_attack'])

        if action == 'attack':
            wizard_attack_with_dodge(lambda: super(EvilWizard, wizard).attack(player))
        elif action == 'cast_dark_spell':
            wizard_attack_with_dodge(lambda: wizard.cast_dark_spell(player))
        elif action == 'summon_minions':
            wizard_attack_with_dodge(lambda: wizard.summon_minions(player))
        elif action == 'invisible_attack':
            wizard_attack_with_dodge(lambda: wizard.invisible_attack(player))

        wizard.regenerate()

    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Special Ability")
        print("3. Heal")
        print("4. View Stats")

        choice = safe_input("Choose an action: ")

        if choice == '1':
            player.attack(wizard)

        elif choice == '2':
            player.special_ability(wizard)

        elif choice == '3':
            player.heal()

        elif choice == '4':
            player.display_stats()
            continue

        else:
            print("Invalid choice.")
            continue

        if wizard.health > 0:
            default_wizard_action()

        if player.health <= 0:
            print(f"\n{player.name} has fallen! The Dark Wizard reigns supreme!\nGame Over.")
            return

    print(f"\n{wizard.name} has been defeated! {player.name} saves the kingdom!")


def main():
    welcome_message()
    player = create_character()
    if not player:
        print("Goodbye!")
        return

    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)


if __name__ == "__main__":
    main()
