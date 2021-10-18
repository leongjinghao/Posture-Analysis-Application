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
    print('Accuracy: %.3f' % acc)

    torch.save(model, 'model.pth')

    model = torch.load('model.pth')

    # test prediction
    testPos = [0.40465500950813293, 0.30729806423187256, 0.39920634031295776, 0.2775283753871918, 0.40185922384262085, 0.27067211270332336, 0.4050736129283905, 0.26221638917922974, 0.39394038915634155, 0.2904113531112671, 0.39280086755752563, 0.2927198112010956, 0.3916458785533905, 0.2950746715068817, 0.4215143620967865, 0.24422256648540497, 0.40267413854599, 0.28645163774490356, 0.421942800283432, 0.31036072969436646, 0.41614946722984314, 0.32054921984672546, 0.5135082602500916, 0.2850976586341858, 0.4559158682823181, 0.36824604868888855, 0.5555553436279297, 0.4776943027973175, 0.5013267397880554, 0.4939555525779724, 0.5006917715072632, 0.6175298094749451, 0.47705331444740295, 0.620148241519928, 0.48851659893989563, 0.6606314182281494, 0.4659281373023987, 0.6599661111831665, 0.47280067205429077, 0.6517767906188965, 0.4557916522026062, 0.652662992477417, 0.4768761396408081, 0.6353680491447449, 0.461587131023407, 0.6370322108268738, 0.6334103941917419, 0.4162602722644806, 0.5897025465965271, 0.4609770178794861, 0.5844500064849854, 0.6341816186904907, 0.5583183169364929, 0.6489982008934021, 0.5936256051063538, 0.9159660339355469, 0.5845736265182495, 0.8926661014556885, 0.6137014031410217, 0.9578613042831421, 0.6018709540367126, 0.9341383576393127, 0.550584077835083, 0.9841305017471313, 0.5366649627685547, 0.9545736908912659]
    yhat = model(Tensor(testPos))
    print('Predicted: %.3f (class=%d)' % (yhat, yhat.round()))
