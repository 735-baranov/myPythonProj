from keras.layers import *
from keras.optimizers import *
from keras.models import *
from keras.metrics import *
from sklearn.model_selection import KFold


import json
from FeedGen import *

def file_len(filename):
    lines = 0
    for i in open(filename):
        lines += 1

    return lines


def num_of_classes(labelfile):
    with open(labelfile) as fin:
        line = fin.readline()

        return len(line.split(','))


def Inception(layers_input):
    conv1x1 = Conv1D(64, 1, strides=1, padding='same', activation='relu')(layers_input)
    conv1x1 = Dropout(0.2)(conv1x1)
    conv3x3 = Conv1D(128, 3, strides=1, padding='same', activation='relu')(layers_input)
    conv3x3 = Dropout(0.2)(conv3x3)
    conv5x5 = Conv1D(256, 5, strides=1, padding='same', activation='relu')(layers_input)
    conv5x5 = Dropout(0.2)(conv5x5)

    layer = concatenate([conv1x1, conv3x3, conv5x5])

    return layer


def make_model(num_of_inputs=256, num_of_outputs=10):
    inputs = Input(shape=(None, num_of_inputs))
    model = Inception(inputs)
    model = Inception(model)
    model = Bidirectional(GRU(128, dropout=0.2, recurrent_dropout=0.2))(model)
    model = Dense(512, activation="relu")(model)
    model = Dropout(0.2)(model)
    model = Dense(512, activation="relu")(model)
    model = Dropout(0.2)(model)
    model = Dense(num_of_outputs, activation='softmax')(model)

    nnet = Model(inputs=inputs, outputs=model)
    nnet.compile(optimizer=Adadelta(), loss=categorical_crossentropy, metrics=[categorical_accuracy])
    nnet.summary()

    return nnet


def train_model(someModel, trainGen, testGen, repeats=10, epochs_per_step=50, modelfile='model', read='n', steps=10,
                val_steps=10):
    for i in range(repeats):
        history = someModel.fit_generator(generator=trainGen,
                                          validation_data=testGen,
                                          steps_per_epoch=steps,
                                          validation_steps=val_steps,
                                          epochs=epochs_per_step,
                                          shuffle=True)
        ser = json.dumps(history.history)
        with open('history_{0}_{1}.json'.format(modelfile, i), 'w') as fout:
            fout.write(ser)

        someModel.save('{0}_{1}'.format(modelfile, i))


def predict(modelfile, validata, outfile):
    model = load_model(modelfile)
    steps = file_len(validata)
    predicts = model.predict_generator(PredictGenerator(validata), steps=steps)

    np.savetxt(outfile, predicts, delimiter=',')

    return predicts


def main(repeats, epochs, folds):
    p_rep = int(repeats)
    p_epo = int(epochs)
    p_fol = int(folds)

    data = readData('data.csv')
    labels = readData('labels.csv')

    kf = KFold(n_splits=p_fol, shuffle=True)
    i = 0
    for tr, tst in kf.split(data):
        nnet = make_model(num_of_outputs=num_of_classes('labels.csv'))
        train_model(nnet, trainGen=CrossValidationGenerator(data, labels, tr),
                    testGen=CrossValidationGenerator(data, labels, tst), repeats=p_rep,
                    epochs_per_step=p_epo, modelfile='testModel' + str(i), steps=len(tr),
                    val_steps=len(tst))
        i += 1
