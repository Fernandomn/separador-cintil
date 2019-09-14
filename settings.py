def init():
    global posDict
    global conjTag
    global conjBarTag
    global conjPTag
    global pointTag
    global pointList
    global removeTag

    pointList = ['"', "'"]
    conjTag = 'CC'
    conjBarTag = '_CONJP_'
    conjPTag = 'CONJP'
    pointTag = 'PNT'
    removeTag = '_TOREMOVE_'
    posDict = {}
