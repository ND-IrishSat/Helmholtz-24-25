import time

def calculateOffsets(xAvg, yAvg, zAvg):
    offsets = [0, 0, 0]
    
    offsets[0] = sum(xAvg) / len(xAvg)
    offsets[1] = sum(yAvg) / len(yAvg)
    offsets[2] = sum(zAvg) / len(zAvg)
    
    print("Offsets calculated -------")
    print()

    time.sleep(2)

    return offsets


def processStrings(magX, magY, magZ):

    values = [str(magX), str(magY), str(magZ)]

    results = [0, 0, 0]

    for i, v in enumerate(values):
        loc = v.index('.')
        if(len(v) - (loc + 1) < 2):
            v += "0"
        results[i] = v

    return results

# millis() function from arduino
def millis():
    return int(round(time.time() * 1000))

