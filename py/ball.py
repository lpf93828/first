class HotDog:
    def __init__(self):
        self.cooked_level=0
        self.cooked_string="Raw"
        self.condiments=[]

    def __str__(self):
        msg="hot dog"
        if len(self.condiments)>0:
            msg=msg+" with "
        for i in self.condiments:
            msg=msg+i+", "
        msg=msg.strip(", ")
        msg=self.cooked_string+" "+msg+"."
        return msg

    def cook(self,time):
        self.cooked_level +=time
        if self.cooked_level>8:
            self.cooked_string="charcoal"
        elif self.cooked_level>5:
            self.cooked_string="well-done"
        elif self.cooked_level>3:
            self.cooked_string="medium"
        else :
            self.cooked_string="raw"

    def addcondiment(self,condiment):
        self.condiments.append(condiment)

myDog=HotDog()
print (myDog)
print ("cooking 4 minutes..")
myDog.cook(4)
print (myDog)
print ("cooking 3 more minutes...")
myDog.cook(3)
print (myDog)
print ("if cook 10 minutes")
myDog.cook(10)
print (myDog)
print ("now,add some")
myDog.addcondiment("ketchup")
print (myDog)
