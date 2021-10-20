import torch
from torch import Tensor
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Sigmoid
from torch.optim import SGD
from torch.nn import BCELoss
from numpy import vstack
from sklearn.metrics import accuracy_score
from torch.nn import Module
from pytorch_neural_network.posture_dataset import PostureDataset
from torch.nn.init import kaiming_uniform_
from torch.nn.init import xavier_uniform_

# CUDA for PyTorch
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
torch.backends.cudnn.benchmark = True

# lm index used for training
lm_Use = [0] + [i for i in range(11, 33)]

class MLP(Module):
    # constructor to setup the neural network
    def __init__(self, inputCount):
        super(MLP, self).__init__()
        # first hidden layer
        # with input count given in the argument and 10 output nodes
        self.hiddenLayer1 = Linear(inputCount, 10)
        kaiming_uniform_(self.hiddenLayer1.weight, nonlinearity='relu')
        self.activationLayer1 = ReLU()
        # second hidden layer
        # with 10 input nodes and 8 output nodes
        self.hiddenLayer2 = Linear(10, 8)
        kaiming_uniform_(self.hiddenLayer2.weight, nonlinearity='relu')
        self.activationLayer2 = ReLU()
        # third hidden layer (output layer)
        # with 8 input nodes and 1 output nodes (final output)
        self.hiddenLayer3 = Linear(8, 1)
        xavier_uniform_(self.hiddenLayer3.weight)
        self.activationLayer3 = Sigmoid()

    # forward propagation
    def forward(self, X):
        # input to first hidden layer
        X = self.hiddenLayer1(X)
        X = self.activationLayer1(X)
        # input to second hidden layer
        X = self.hiddenLayer2(X)
        X = self.activationLayer2(X)
        # input to output layer
        X = self.hiddenLayer3(X)
        X = self.activationLayer3(X)
        # return final output
        return X

# model training
def trainModel(train, model):
    # optimisation configuration
    criterion = BCELoss()
    optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9)
    # enumerate epochs
    for epoch in range(100):
        for i, (inputs, targets) in enumerate(train):
            # clear the gradients on every new iteration
            optimizer.zero_grad()
            # compute the predicted model output
            yhat = model(inputs)
            # calculate loss
            loss = criterion(yhat, targets)
            # credit assignment
            loss.backward()
            # update model weights
            optimizer.step()

# evaluate the model
def evaluateModel(test_dl, model):
    predictions, actuals = list(), list()
    for i, (inputs, targets) in enumerate(test_dl):
        # evaluate the model on the test set
        yhat = model(inputs)
        # retrieve numpy array
        yhat = yhat.detach().numpy()
        actual = targets.numpy()
        actual = actual.reshape((len(actual), 1))
        # round to class values
        yhat = yhat.round()
        # store
        predictions.append(yhat)
        actuals.append(actual)
    predictions, actuals = vstack(predictions), vstack(actuals)
    # calculate accuracy
    acc = accuracy_score(actuals, predictions)
    return acc

# make a class prediction for one row of data
def predict(row, model):
    # convert row to data
    row = Tensor([row])
    # make prediction
    yhat = model(row)
    # retrieve numpy array
    yhat = yhat.detach().numpy()
    return yhat


if __name__ == "__main__":
    postureDataset = PostureDataset('posture_log_file/landmark_data.txt')
    train, test = postureDataset.get_splits(trainsetRatio=0.8)

    # print(len(train))
    # print(len(test))

    trainset = torch.utils.data.DataLoader(train, batch_size=32, shuffle=True)
    testset = torch.utils.data.DataLoader(test, batch_size=32, shuffle=True)

    # define the network
    model = MLP(66)
    # train the model
    trainModel(trainset, model)
    # evaluate the model
    acc = evaluateModel(testset, model)
    print('Accuracy: ' + str(acc))

    torch.save(model, 'model.pth')

    model = torch.load('model.pth')

    # test prediction
    #testPos = [0.16322052478790283, 0.20188267529010773, 0.1494094580411911, 0.16965267062187195, 0.15959948301315308, 0.16072151064872742, 0.17120979726314545, 0.15098832547664642, 0.12733812630176544, 0.1836937814950943, 0.12096775323152542, 0.18620331585407257, 0.11519597470760345, 0.18821512162685394, 0.2192263901233673, 0.1300543248653412, 0.1465030163526535, 0.18267247080802917, 0.22254161536693573, 0.2064748853445053, 0.1977376490831375, 0.21932828426361084, 0.5268067121505737, 0.18645499646663666, 0.3194773197174072, 0.2781173586845398, 0.659105122089386, 0.41527730226516724, 0.44448214769363403, 0.42445412278175354, 0.46359387040138245, 0.5784137845039368, 0.36645272374153137, 0.577373743057251, 0.4044857621192932, 0.6266431212425232, 0.3218962848186493, 0.6196287870407104, 0.3537106215953827, 0.6036081910133362, 0.2859669029712677, 0.6092814803123474, 0.3689813017845154, 0.5865845084190369, 0.3065603971481323, 0.5911139845848083, 0.9043545126914978, 0.3549425005912781, 0.7570645213127136, 0.4017811417579651, 0.769014835357666, 0.6128551959991455, 0.6675293445587158, 0.6162047982215881, 0.7458033561706543, 0.9150148034095764, 0.693140983581543, 0.8860371112823486, 0.8450685143470764, 0.9527906775474548, 0.7642031311988831, 0.9214527606964111, 0.6435437798500061, 1.0069913864135742, 0.5086897611618042, 0.9511421918869019]
    testPos = [0.6329419612884521, 0.06960634142160416, 0.6452106833457947, 0.054717376828193665, 0.6594734191894531, 0.055396128445863724, 0.6716297268867493, 0.05632355809211731, 0.5974088311195374, 0.055344466120004654, 0.5754019618034363, 0.05646770820021629, 0.5524349808692932, 0.05827890709042549, 0.6697685718536377, 0.0691617876291275, 0.5010343790054321, 0.07070774585008621, 0.6553561687469482, 0.0915093719959259, 0.5982327461242676, 0.09167630970478058, 0.7243713736534119, 0.21951492130756378, 0.39001989364624023, 0.19436566531658173, 0.7632220983505249, 0.3738771975040436, 0.28357839584350586, 0.33560892939567566, 0.8859770894050598, 0.5042827725410461, 0.3189079761505127, 0.46261054277420044, 0.9224521517753601, 0.5429456830024719, 0.3065861165523529, 0.5030102133750916, 0.9240829348564148, 0.5431572198867798, 0.3521716892719269, 0.4970020651817322, 0.9035631418228149, 0.5321313738822937, 0.36563530564308167, 0.48405832052230835, 0.6633861660957336, 0.5032718777656555, 0.4557473063468933, 0.4988206624984741, 0.778692364692688, 0.7301715612411499, 0.3794146776199341, 0.7440634965896606, 0.7544254660606384, 0.948817253112793, 0.0799778401851654, 0.9180174469947815, 0.7131903171539307, 0.9809756875038147, 0.0331912562251091, 0.9301522970199585, 0.926450788974762, 0.9917929172515869, 0.16817474365234375, 1.00942063331604]
    yhat = format(float(predict(testPos, model)), 'f')
    print('Predicted: ' + str(yhat))
