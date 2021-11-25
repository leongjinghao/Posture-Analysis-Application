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
from model_training.posture_dataset import PostureDataset
from torch.nn.init import kaiming_uniform_
from torch.nn.init import xavier_uniform_

# CUDA for PyTorch
device = torch.device("cuda")
torch.backends.cudnn.benchmark = True

# file path configuration
logFilePath = 'posture_log_file/landmark_data_dangerzone.txt'
modelFilePath = 'danger_zone_model.pth'

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
def trainModel(trainset, model):
    # optimisation configuration
    criterion = BCELoss()
    optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9)
    # enumerate epochs
    for epoch in range(100):
        for i, (inputs, targets) in enumerate(trainset):
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

        # print loss value for every 10 epochs (iteration)
        if epoch % 10 == 0:
            print('Epoch %d, Loss %f' % (epoch, float(loss)))

# evaluate the model using the test dataset
def evaluateModel(testset, model):
    predictions, actuals = list(), list()
    for i, (inputs, targets) in enumerate(testset):
        # evaluate the model on the test set
        yhat = model(inputs)
        # retrieve numpy array
        yhat = yhat.detach().numpy()
        actual = targets.numpy()
        actual = actual.reshape((len(actual), 1))
        # round to class values
        yhat = yhat.round()
        # consolidate all predicted class result using model
        predictions.append(yhat)
        # consolidate all actual class specified in dataset
        actuals.append(actual)

    # compare predicted class with actual class for all test dataset rows
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
    # initialise dataset
    postureDataset = PostureDataset(logFilePath)
    # retrieve random split for train and test dataset with specified ratio
    train, test = postureDataset.get_splits(trainsetRatio=0.8)

    # shuffle dataset within train and test dataset to optimise training result
    trainset = torch.utils.data.DataLoader(train, batch_size=32, shuffle=True)
    testset = torch.utils.data.DataLoader(test, batch_size=32, shuffle=True)

    # define the network
    model = MLP(66)
    # train the model
    trainModel(trainset, model)
    # evaluate the model
    acc = evaluateModel(testset, model)
    print('Accuracy: ' + str(acc))

    # save model in file path specified
    torch.save(model, modelFilePath)

    # load model for testing
    # model = torch.load(modelFilePath)
    # test prediction
    #testPos = [0.16322052478790283, 0.20188267529010773, 0.1494094580411911, 0.16965267062187195, 0.15959948301315308, 0.16072151064872742, 0.17120979726314545, 0.15098832547664642, 0.12733812630176544, 0.1836937814950943, 0.12096775323152542, 0.18620331585407257, 0.11519597470760345, 0.18821512162685394, 0.2192263901233673, 0.1300543248653412, 0.1465030163526535, 0.18267247080802917, 0.22254161536693573, 0.2064748853445053, 0.1977376490831375, 0.21932828426361084, 0.5268067121505737, 0.18645499646663666, 0.3194773197174072, 0.2781173586845398, 0.659105122089386, 0.41527730226516724, 0.44448214769363403, 0.42445412278175354, 0.46359387040138245, 0.5784137845039368, 0.36645272374153137, 0.577373743057251, 0.4044857621192932, 0.6266431212425232, 0.3218962848186493, 0.6196287870407104, 0.3537106215953827, 0.6036081910133362, 0.2859669029712677, 0.6092814803123474, 0.3689813017845154, 0.5865845084190369, 0.3065603971481323, 0.5911139845848083, 0.9043545126914978, 0.3549425005912781, 0.7570645213127136, 0.4017811417579651, 0.769014835357666, 0.6128551959991455, 0.6675293445587158, 0.6162047982215881, 0.7458033561706543, 0.9150148034095764, 0.693140983581543, 0.8860371112823486, 0.8450685143470764, 0.9527906775474548, 0.7642031311988831, 0.9214527606964111, 0.6435437798500061, 1.0069913864135742, 0.5086897611618042, 0.9511421918869019]
    # testPos = [0.4835713803768158, 0.24056236445903778, 0.5306033492088318, 0.19630596041679382, 0.5638108849525452, 0.19369162619113922, 0.5940192341804504, 0.1916925311088562, 0.4550308287143707, 0.1940644532442093, 0.43270552158355713, 0.19041068851947784, 0.4111633002758026, 0.18702110648155212, 0.6429838538169861, 0.19446295499801636, 0.40538933873176575, 0.18599393963813782, 0.5305572748184204, 0.2744101881980896, 0.45262131094932556, 0.27215978503227234, 0.8415300846099854, 0.36304184794425964, 0.265718936920166, 0.34421053528785706, 0.823294460773468, 0.6427538990974426, 0.20364953577518463, 0.6061266660690308, 0.6415218114852905, 0.8362496495246887, 0.31572097539901733, 0.8268066644668579, 0.6186655759811401, 0.9127404689788818, 0.32402318716049194, 0.9001800417900085, 0.5346417427062988, 0.8940770626068115, 0.39707332849502563, 0.8832436203956604, 0.5268311500549316, 0.8690509796142578, 0.40433624386787415, 0.858551561832428, 0.7035560011863708, 0.7194310426712036, 0.3920583128929138, 0.6997008323669434, 0.8900101780891418, 0.8890723586082458, -0.026458740234375, 0.788112998008728, 0.2304142564535141, 0.9069898128509521, 0.5178309082984924, 0.9283669590950012, 0.1547926515340805, 0.8549576997756958, 0.5901385545730591, 0.8973225951194763, -0.08521083742380142, 0.9663792252540588, 0.7185410857200623, 1.036260962486267]
    # yhat = format(float(predict(testPos, model)), 'f')
    # print('Predicted: ' + str(yhat))
