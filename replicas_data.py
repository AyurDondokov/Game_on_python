from reader_dialog import *
import logging as log

# список с персонажами
r_c = {
    "Ar": "Аюр:",
    "H": "Ты:"
}
check = ReadingLocations('dialog/proba.txt')
check.dia_loc('caravan_lider__1')

test_npc = check.conversation
print(test_npc)
check.dia_loc('caravan_lider__2')
test_npc2 = check.conversation

# test_npc = [f"{r_c['Ar']}Hello",
#             f"{r_c['Ar']}My name is Ayur",
#             f"{r_c['Ar']}Its first dialog in game",
#             f"{r_c['H']}Hello!",
#             f"{r_c['Ar']}Do you want to fight?",
#             f"{r_c['H']}*Здесь должен быть выбор*",
#             f"{r_c['Ar']}Зайди на красный квадрат",
#             ]
#
