import torch
from pandas import read_csv
from numpy import array

class PostureDataset(torch.utils.data.Dataset):
    def __init__(self, path):
        posData = read_csv(path, header=None)
        # first 66 elements as inputs
        self.X = posData.values[:, :-1]
        # last element as output
        self.y = posData.values[:, -1]
        # ensure input data is floats
        self.X = self.X.astype('float32')
        # reshape y
        self.y = array(self.y)
        self.y = self.y.astype('float32')
        self.y = self.y.reshape((len(self.y), 1))

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        return [self.X[index], self.y[index]]

    # get indexes for train and test rows
    def get_splits(self, trainsetRatio=0.8):
        # determine sizes
        train = round(trainsetRatio * len(self.X))
        test = len(self.X) - train
        # calculate the split
        return torch.utils.data.random_split(self, [train, test])
