# Volkorp 12/05/2022
import enum
import random


class BossRoster(enum.Enum):
    MALIGATOR = 1
    WORSELIGATOR = 2
    WORSTLIGATOR = 3
    NOTTHATBADGATOR = 4


class Actions(enum.Enum):
    ATTACK = 1
    DEFEND = 2
    AVOID = 3


class BossStats:

    def __init__(self, health=0, strength=0, haste=0, name=""):
        self._health = health
        self._strength = strength
        self._haste = haste
        self._name = name

    def get_health(self):
        return self._health

    def get_strength(self):
        return self._strength

    def get_haste(self):
        return self._haste

    def set_health(self, new_value):
        self._health = new_value

    def get_name(self):
        return self._name


class NotSoHeroic:
    def __init__(self, health=0, defense=0):
        self._health = health
        self._defense = defense

    def get_health(self):
        return self._health

    def set_health(self, new_value):
        self._health = new_value

    def get_defense(self):
        return self._defense


def game_setter():
    boss_name = BossRoster(random.randint(1, 4)).name
    print('You are about to fight', boss_name, '! Prepare to die...')
    boss = set_boss_stats(boss_name)
    player = NotSoHeroic(random.randint(50, 80), random.randint(1, 7))

    print('''
    ----------------------
    --- {name}'s stats
    ----------------------
    --- Health:{health} 
    --- Strength:{strength}
    --- Haste:{haste}
    --------------------            
    
    Fight!!
    '''.format(name=boss_name, health=boss.get_health(), strength=boss.get_strength(), haste=boss.get_haste()))

    game_loop(player, boss)


def set_boss_stats(boss_name):
    if boss_name == BossRoster.MALIGATOR.name:
        boss = BossStats(50, 10, 3, boss_name)
    if boss_name == BossRoster.WORSELIGATOR.name:
        boss = BossStats(65, 15, 5, boss_name)
    if boss_name == BossRoster.WORSTLIGATOR.name:
        boss = BossStats(100, 19, 7, boss_name)
    if boss_name == BossRoster.NOTTHATBADGATOR.name:
        boss = BossStats(60, 5, 1, boss_name)
    return boss


def game_loop(player, boss):
    while boss.get_health() > 0 and player.get_health() > 0:
        print('''
    What would you like to do?
    1. Attack (Try to hit enemy)
    2. Defend (Try to mitigate enemie's hit)
    3. Avoid (Try to avoid enemie's attack)
        ''')
        option = input("Your option: ")

        # Little validation
        while str(option) not in ['1', '2', '3']:
            option = input("Your option: ")

        player_action = Actions(int(option)).value
        boss_action = chose_action()
        execute_action(player_action, boss_action, player, boss)
        print('''
    ----------------------
    {boss_name} health: {boss_health}
    None-mighty hero health: {player_health}
    ----------------------
        '''.format(boss_health=boss.get_health(), boss_name=boss.get_name(), player_health=player.get_health()))

    if boss.get_health() == 0:
        print('''
        Congratulations! You defeated {boss_name}!
        You earn {coins} golden coins and {exp} EXP!
        ''')
    else:
        print('''Well... Kind of end as expected. Good luck next time!''')


def chose_action():
    return Actions(random.randint(1, 3)).value


def execute_action(player_action, boss_action, player, boss):
    player_dmg = random.randint(1, boss.get_strength())
    player_def = random.randint(1, player.get_defense())
    boss_dmg = random.randint(1, 10)
    boss_def = random.randint(0, boss.get_haste())

    # Player attacking
    if player_action == boss_action and player_action == Actions.ATTACK.value:
        print('''
        Both of you try to hit each other causing {player_dmg} dmg to YOU and {boss_dmg} dmg to {boss_name}!'''.format(player_dmg=player_dmg, boss_dmg=boss_dmg, boss_name=boss.get_name())
              )

        player.set_health(player.get_health()-player_dmg)
        boss.set_health(boss.get_health()-boss_dmg)

    if player_action == Actions.ATTACK.value and boss_action == Actions.DEFEND.value:
        final_dmg = boss_dmg-boss_def

        if final_dmg <= 0:
            final_dmg = 0

        print('''
    You attempt to blow your enemies chest but {boss_name} partially parry your strike!
    He weaken your hit of {boss_dmg} by {boss_defense} and got {final_dmg} of damage.'''.format(boss_name=boss.get_name(), boss_dmg=boss_dmg, boss_defense=boss_def, final_dmg=final_dmg)
              )

        boss.set_health(boss.get_health()-final_dmg)

    if player_action == Actions.ATTACK.value and boss_action == Actions.AVOID.value:
        avoids = random.randint(1, 100)

        if avoids < 45:
            print(boss.get_name(), 'tries to avoid your attack and... Succeds! You fail on your attempt of hitting him.')
        else:
            print(boss.get_name(), 'tries to avoid your attack but fails miserably... You strike him right in the face dealing him {boss_dmg} dmg.'.format(boss_dmg=boss_dmg))
            boss.set_health(boss.get_health() - boss_dmg)

    # Player defending
    if player_action == Actions.DEFEND.value and boss_action != Actions.ATTACK.value:
        print("You accomplish your commitment of defending! But no one is trying to hit you this time... It's kind of ridiculous. ")

    if player_action == Actions.DEFEND.value and boss_action == Actions.ATTACK.value:
        final_dmg = player_dmg - player_def

        if final_dmg <= 0:
            final_dmg = 0

        print('You parry enemies hit ({player_dmg}) and parry {player_def} of damage. You get hurt by {final_dmg}.'.format(player_dmg=player_dmg, player_def=player_def, final_dmg=final_dmg))
        player.set_health(player.get_health()-(player_dmg-player_def))

    # Player avoiding
    if player_action == Actions.AVOID.value and boss_action != Actions.ATTACK.value:
        print('You two try to avoid each other... You may want to see other people?')

    if player_action == Actions.AVOID.value and boss_action == Actions.ATTACK.value:
        avoids = random.randint(1, 100)
        if avoids < 30:
            print("You dance as a leaf on the wind and succeed on avoiding", boss.get_name())
        else:
            print(boss.get_name(), 'hits you with {player_dmg} anyway. No matter how hard you try to roll on the floor.'.format(player_dmg=player_dmg))
            player.set_health(player.get_health() - player_dmg)


if __name__ == '__main__':
    game_setter()
