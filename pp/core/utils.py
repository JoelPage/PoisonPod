# https://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python

def Contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

# if contains(myList, lambda x: x.n == 3)  # True if any element has .n==3
    # do stuff

def GetIndex(list, filter):
    for x in list:
        if filter(x):
            return list.index(x)
    return None

def GetElement(list, filter):
    for x in list:
        if filter(x):
            return x
    return None