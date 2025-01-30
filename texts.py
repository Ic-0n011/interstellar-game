MAIN_MENU = [
    "Начать новую игру",
    "Что нужно делать",
    "Об авторе",
    "Выход"
]

INSTRUCTIONS = [
    "Цель игры: добраться до базы (O),",
    "за кратчайшее время, следите за показателем топлива!",
    "избегая чёрных дыр (B) и обломков материи (X).",
    "Белые дыры (W) отбросят вас в случайном направлении.",
    "",
    "",
    "Управление:",
    "Стрелка влево/вправо - Поворот корабля.",
    "Стрелка вверх - Ускорение, стрелка вниз - тормоз",
    "",
    "",
    "Нажмите любую клавишу, чтобы вернуться в меню."
]

AUTHOR_INFO = [
    "Автор игры: Ic-0n.",
    "Версия: 1.0.",
    "",
    "Нажмите любую клавишу, чтобы вернуться в меню."
]

ASCII_TITLE = '''
▄▄████▄█████████▄▄███████████████▄███▄▄▄⌐▌
█▌  ▐██         ██         ██   "██▌  ▐█U▌
█▌  ▐██   ███▄▄▄██   ███   ██     █▌  ▐█U▌
█▌  ▐██   ████████   ███   ██   µ  ▌  ▐█U▌
█▌  ▐██   ███▀▀▀██  L███]  ██   ▌█▄   ▐█U▌
█▌  ▐██         ██         ██   ██▄▓  ▐█U▌
██▓▄▄█▀█████████▀▀█████████████████▄▄▄▐█U▌
▀▀▀█▄∞╧═^^ⁿ""""▀▀███████▄""""ⁿⁿ^══∞▄█▀▀▀─▌
                 ═▀███▌`
                   ⁿ▀
'''

ASCII_SHIP_WIN = """
                                                                      ,,,╓╓┐
                                                      ,,,╓╥╦g@@@Ñ▓╩╩╨╜╙"``╟▓
                                     ,,,╓╓╥m╦@@@Ñ╩╩╨╜╙""`         ,,  ╔╦, ╘▒
                     ,,╓╓╥╦╦@@@Ñ▓╩╩╨╙""`         ,,, ╓╦╦@  ╙╬▓╢@  ▐   ╣▒▓  ▒r
    ,,,╓╓╥m@@@ÑÑ╩╩╨╜╙"``        ,,,     Φ@▓▓  ▒▓  ▓   ▒▒▒   ╓╚▒▒▒╗ L   ▓L  ▓▓
  ▓╣""`           ,┐<╦,  '╫▓╢▓   ▓       ╣▒▒╗]▒▒▓ L   ▒▒▒   ]  ▓▒▒▓,   ╘   ]▒
  ]▒  #@@▓[ "▒` ╓▓▒  ╟▒╢╕ ]▒▒▒   ]        ╣▒▒L╟▒▒@    ╟▒▒[   [  ╙╬▒▒   ▓▒[  ▒
   ▒   ╙▒▒▒╖╒`  ╣▒▒L  ▒▒▒  ▒▒▒    L        ▒▒▒ ▓▒▒    ]▒▒╣, √▓H   ╙"        ╢[
   ▒L    ▓▒▒╗   ╟▒▒▓  ▒▒▒  ▓▒▒L  ▒╛        ╘▓╛  ╜╙          ,,,╓╓╥╦æ@@@Ñ╩╩╝╜╙"
   ╟▓     ▒▒▒    ╚▒▒  ║▓`   ╙╩╩═└`          ,,,╓╥╦m@@@Ñ▓╩╩╨╜╙"``
   j▒    ╓Ñ▓▓M      `      ,,,╓╓╥m@@@ÑÑ╩╩╨╜╙""`
    ▒L    ,,,╓╓╥╦╦@@@Ñ╩╩╝╜╜""`
    ╫▓╩╩╨╜╙"``
"""

ASCII_SHIP_LOSE = """
██████████████████████████████████████████████████████████████████████████████
 █████ ████████████████████████████████████████████████████████████████████████
  ████████████████████████████████████ ██████████████████████████ █████████████
██████████████████████████████████████████████████████████████████████████████
██████████████ ████████████▀▀▀▀▀▀█████▀▀▀▀▀▀▀█████▀▀▀▀▀████████████████████████
 █████████ ██████████████▓▓▀     ▓▓▓▓╜'       ]▒▒▓╝   ,║▓▓█████████████████████
███████████████████████▓▓     ▓▓▓▓▓╥═══╧▓∞═══╣╬╬W⌐⌐  ╬▓▓████████████ ██████████
██████████████████████▓▓     ║▓▓▓▓▓╣⌐⌐⌐⌐╫▓⌐⌐ ⌐╫▓⌐⌐⌐⌐╢▓▓▓███████████████████████
 ███ █████████████▓▓▓▓▓▓     ▒▓  ░░╢╕  ░░║░   ╫Ü     ▓▓█   ▓█████████████████
████████ █████████████▓▓╦══ ═  ════╬╥~~~╩╣░~~~╬m╧══╧══════╩▓▓▓▓████████████████
 ████████████████████▓▓▓▓▄▄╖╖╖    ╓╠[    ╙    ║▓╖╖╖╖┐    ╖╫▓▓██████████████████
██████████████████████████▓▓m  ═╦▓▓▓╦╤════╦@▓████▓▓════╬▓▓█████████ ███████████
██████████████████████████████████████████████████████████████████████████████
 █████████████████████████████████████████████████████████████████ ████████████
█████████████ █████████████████████████████████████████████████████████████████
███████████████████████████████▐▌████▒█▓██████▌███║███████████████████████████
"""
