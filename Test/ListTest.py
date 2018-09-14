myTuple = ('a', 'b', 'c', 'd')
print(myTuple[0])


cList = []
print(type(cList))
cList.append(1)
cList.append(2)
print(cList)
total = 0
myList = list(range(0, 5))
print(myList)
del myList[0]

myList.append(8)
for i in myList:

    total = total + i
print(total)
print(myList)
