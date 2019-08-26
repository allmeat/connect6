import numpy as np

aa = np.ones((21,21))

def np2board(x):
    if x==0:
        out=" "
    elif x==1:
        out="O"
    elif x==2:
        out="X"
    return out

def drawboard():

    alphabet = "a b c d e f g h i j k l m n o p q r s t u".split(" ")
    bar =
    rowIndex = " ".join(list(map(lambda y : y, alphabet)))
    a1 = list(map(lambda y: " ".join([np2board(x) for i, x in enumerate(y)]), aa))
    a2 = rowIndex + "\n" + "\n".join(a1)
    return a2

bb= "".join([np2board(x) for x in aa[0]])

bb= drawboard()
print(bb)