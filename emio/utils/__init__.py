
def getListFromArgs(args):
    if isinstance(args, list):
        return args
    if isinstance(args, str) and args:
        argsList = []
        for name in args.split(" "):
            argsList += [name]
        return argsList
    return None


class RGBAColor:
    red = [0.8, 0.1, 0.1, 1]
    blue = [0.15, 0.45, 0.75, 1]
    lightblue = [0.67, 0.84, 0.90, 1]
    green = [0.1, 0.5, 0.1, 1]
    yellow = [1, 0.8, 0, 1]
    grey = [0.5, 0.5, 0.5, 1]
    white = [1, 1, 1, 1]


def getColorFromFilename(filename):
    color = RGBAColor.white
    if "red" in filename:
        color = RGBAColor.red
    elif "blue" in filename:
        color = RGBAColor.blue
    elif "lightblue" in filename:
        color = RGBAColor.lightblue
    elif "green" in filename:
        color = RGBAColor.green
    elif "yellow" in filename:
        color = RGBAColor.yellow
    elif "grey" in filename:
        color = RGBAColor.grey
    return color


def addArticulationCenter(node, name,
                          parentIndex, childIndex,
                          posOnParent, posOnChild,
                          articulationProcess,
                          isTranslation, isRotation, axis,
                          articulationIndex):
    """
    Adds articulation center, compact form.
    Args:
        node:
        name:
        parentIndex:
        childIndex:
        posOnParent:
        posOnChild:
        articulationProcess:
        isTranslation:
        isRotation:
        axis:
        articulationIndex:

    Returns:

    """

    center = node.addChild(name)
    center.addObject('ArticulationCenter', parentIndex=parentIndex, childIndex=childIndex, posOnParent=posOnParent,
                     posOnChild=posOnChild, articulationProcess=articulationProcess)

    articulation = center.addChild('Articulation')
    articulation.addObject('Articulation', translation=isTranslation, rotation=isRotation, rotationAxis=axis,
                           articulationIndex=articulationIndex)

    return center
