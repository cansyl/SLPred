fastaDict={}
MIN_SEQUENCE_LENGTH = 0
def readFasta(fileName):
    with open(fileName) as fp:
        protId = ''
        sequence = ''
        for line in fp:
            if line[0] == '>':
                if len(sequence) > MIN_SEQUENCE_LENGTH:
                    if sequence.find('U') != -1:
                        sequence = sequence.replace("U", "C")
                    fastaDict[protId] = sequence
                sequence = ''
                protId = line[1:].strip()
                
                continue
            line = line.strip()
            sequence = sequence + line
        if len(sequence) > MIN_SEQUENCE_LENGTH:
            fastaDict[protId] = sequence
    fp.close()
    return (fastaDict)
