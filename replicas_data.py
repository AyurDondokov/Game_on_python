from reader_dialog import *


check = ReadingLocations('dialog/proba.txt')
test_npc = check.dia_loc('caravan_lider__1')
test_npc2 = check.dia_loc('caravan_lider__2')
npc = check.dict_npc_loc
print(npc)

# # список с персонажами
# r_c = {
#     "Ar": "Аюр:",
#     "H": "Ты:"
# }
# test_npc = [f"{r_c['Ar']}Hello",
#             f"{r_c['Ar']}My name is Ayur",
#             f"{r_c['Ar']}Its first dialog in game",
#             f"{r_c['H']}Hello!",
#             f"{r_c['Ar']}Do you want to fight?",
#             f"{r_c['H']}*Здесь должен быть выбор*",
#             f"{r_c['Ar']}Зайди на красный квадрат",
#             ]
#
