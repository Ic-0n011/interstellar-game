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
    "Белые дыры (W) отбросят вас.",
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
    "Мой github: https://github.com/Ic-0n011/",
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
  ▒                             ╕   ▒
          ░                     ╟
                    `           █        ▒─
                              ,█-
  ,          ,┐         ┌,   ▄▀
                         ,▄═▀∞▄▄
                        ▐▌     ▐▌
                      ;P▀█▄▄▄▄▄█▄        ``
             █▀▀▀▀.-▀▐╗,⌐, ¬└ⁿ` ¿▀▄
  `         █""▀▀▀▀N▄▄▄▀╩┘▀██▄▄▄██▀▀▄
            █⌂▐▀▀$¥▄▄▄▄█▀▀██▀█▄▄█▀.╓█
        ▒   █, ,▀▀▀▀▀▀4▄███PA▄▄▌▄▓╝,█
        ▄▄▀└█Ñ▄▄▒▓▓▀▀MM▄▄▄▄▄▄▀▀█▀▄$▐▌▄,
       █`   █▄▄▄,,╓,▀▀▀▀Æ▄▄¿X/▐██▀¬▐ ,▄██▄▄▄   ,
      ▐█    ╙▀▄▄▄██▀▀▀▀▀▀▀▀▀▀▄█▄9▀▀▀▀▀▀▄▄▄██"
       ▀██▄,    ██ ~⌐∞═▄▄██▀▀▀▀▀▀▀▀▀▀▀▀███`
        `▀▀███▄▄▄██████▀▄;,,,,,▄▄▄▄▄███▀▀
             ╘▀▀▀███████████████▀▀▀▀▀
  ▒                     ╙┘         └┘
"""

ASCII_SHIP_LOSE = """
▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒╫▓▓▓▓▓▓▓▓▓▓▒╣╣▓▓╬▒▒
▒▒▒▒▒▒▒▒▒▀▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒╣╢╢▒▒╣╣╣▒╣▓▓▓▓▓▓▓▒▒▒╢╣║▒
▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒╣▒╫▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▌▒╣╢▓╣▒
▒▒▒▒▒▒▒▒▒▒▒▒▒██▄▒▒▒╣╫▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣▐▓▓▓▓▌▒╬╢╣╣▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███▄█▓▀▀▀▀▓▓████▓██▓▓▓▒▓▓▓▓▓╣╣▓╣▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒╣▒▓██▀░░░░░░░░░▀██▌██▓▓▓▓▓▓▓▓╬╣▓╣╢▒▒▒
▒▒▀▒▒▒▒▒▒▒▒╣▒▓▓█▀░░░░░░░░░░░▐████▓▓▓▓▓▓▓▓╬╣╣╢▒▒▒▒▒
▒▒▒▒▒▒▒▒▒╣▒▓▓▓▓█░░░░░░░░░░░▄████▓▓▓▓▓▓▓▓▒╬╣╢▒╣▒▒▒▒
▒▒▒▒▒▒▒╣╣▓▓▓▓▓▓█░░░░░░░░░░████▓▓▓▓▓▓▓▓▓▒╢╣╢╢╣▒▒▒▒▒
▒▒▒▒▒╣╢╫▓▓▓▓▓▓▓█▌░░░░░░▄████▓▓▓▓▓▓▓▓▓▒╣╢╣╫╢▒▒▒▒▒▒▒
▒▒▒▒▒▒▓▓▒▓▓▓▓▓▓███████████▓▓▓▓▓▓▓▓▓▒╣▒╣╫╣╣▒▒▒▒▒▒▒▒
▒▒▒▒╫▓▒▒▓▓▓▓▓███████████▓█▓▓▓▓▓▓▓▒╣▒╣╫▓╣╣▒▒▒▒▒▒▒▒▒
▒▒▒╣╣▒╣▓▓▓╫▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓██▌╣╬▓╣╣▒▒▒▒▒▒▒▒▒▒▒
▒▒╣╣╢▒▓▓▓▒▒▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒╣╢╢▓▄▒▒▒▒▒▒▒▒▒▒▀▒▒▒
▒▒▒╢╢╣▓▓▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒╢▒╣╣╫╬╣╣╣▒██▒▒▒▒▒▒▒▒▒▒▒▒▒
▒╣╬╬▒╢▓▓▓▓▓▒╢╢▒▒▒▒▒╣╢╢▒╢╣╬╬╬╣╣▒▒▒▒▒▒▒▀▌▒▒▒▒▒▒▒▒▒▒▒
▒▒╫▓╢▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▒╣╢╣╣╣▒▒▒▒╣▒▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒▒▒
▒▒╫╢▓╣╢╣╣▒╣╣╣▒╣╣╣▒▒▒╣▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▒▒▒▒▒
"""
