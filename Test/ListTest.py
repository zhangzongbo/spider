myTuple = ('a', 'b', 'c', 'd')
print(myTuple[0])
myList = list(range(0, 120000))
print(len(myList))

myList = myList[0:11000] + myList[100000:]
print(len(myList))
