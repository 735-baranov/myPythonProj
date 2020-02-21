import numpy as np

def readData(dataFile):
    data = np.array([[float(j) for j in i.split(',')] for i in open(dataFile)])
    return data


def CrossValidationGenerator(data, labels, indices):
    while True:
        for i in indices:
            yield np.array(data[i]).reshape(1, -1, 256), np.array(labels[i]).reshape(1, -1)


def DataGenerator(dataFile, labelFile):
    findata = open(dataFile)
    finlabel = open(labelFile)

    while True:
        # label = [float(i) for i in finlabel.readline().split(',')]
        label = finlabel.readline()

        if len(label) < 10:
            findata = open(dataFile)
            finlabel = open(labelFile)
            label = finlabel.readline()

        label = [float(i) for i in label.split(',')]
        data = [float(i) for i in findata.readline().split(',')]

        yield np.array(data).reshape(1, -1, 256), np.array(label).reshape(1, -1)


def PredictGenerator(dataFile):
    findata = open(dataFile)

    while True:
        for i in open(dataFile):

            data = [float(j) for j in i.split(',')]

            if len(data) < 10:
                continue

            yield np.array(data).reshape(1, -1, 256)


if __name__ == '__main__':
    for i in DataGenerator('data.csv', 'labels.csv'):
        print(i[0].shape)
        print(i[1].shape)
