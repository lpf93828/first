import random,easygui

secret=random.randint(1,100)
guess=0
tries=0

easygui.msgbox("""hi!i am lee ,i have a secret!
it is a number from 1 to 99,i give you 6 tries""")

while guess != secret and tries <6:
      guess =easygui.integerbox("what's your guess  ")
      if not guess:break
      if int(guess) < secret:
          easygui.msgbox(str(guess)+' is too low,you can try '+str(5-tries)+' times')
      elif int(guess) > secret:
          easygui.msgbox(str(guess)+' is too high,you can try '+str(5-tries)+' times')
      tries =tries+1
if int(guess)==secret:
    easygui.msgbox('you did it ,number is '+str(secret))
else:
    easygui.msgbox('no more guesses,number is '+str(secret))
