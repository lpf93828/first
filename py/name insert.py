print ('enter 5 names')
names=[]

for i in range(5):
    name=input()
    names.append(name)
print ('the name are ',names)

print ('replace one name.which one?(1-5):')
nember=int(input())-1
del names[nember]
print ('new names')
names.insert(nember,input())
print ('the name are ',names)
