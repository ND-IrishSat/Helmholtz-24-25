
def processStrings(magX, magY, magZ):

    values = [str(magX), str(magY), str(magZ)]

    results = [0, 0, 0]

    for i, v in enumerate(values):
        loc = v.index('.')
        if(len(v) - (loc + 1) < 2):
            v += "0"
        results[i] = v

    return results



