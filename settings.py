def init():
    global posDict
    global conjTag
    global conjBarTag
    global conjPTag
    global pointTag
    global pointList
    global removeTag
    global conjList
    global conjList2

    pointList = ['"', "'"]
    conjTag = 'CC'
    conjBarTag = '_CONJP_'
    conjPTag = 'CONJP'
    pointTag = 'PNT'
    removeTag = '_TOREMOVE_'
    posDict = {}
    conjList = []
    conjList2 = []