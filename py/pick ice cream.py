import easygui
flavor = easygui.choicebox('what is your favorite ice cream flavor?',
                           choices=['vanilla','chocolate','strawberry'])
easygui.msgbox('you picker '+flavor)
