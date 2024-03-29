import torch
import numpy as np
import torch.nn as nn
from torch.nn import functional as F
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import skimage.io
import skimage
import os
import time
import pandas as pd
import random
import pickle
import sys

import ACGAN_model
import ACGAN_Dataset

random.seed(312)
torch.manual_seed(312)

def load_checkpoint(checkpoint_path, model):
    state = torch.load(checkpoint_path,map_location = "cuda")
    model.load_state_dict(state['state_dict'])
    print('model loaded from %s' % checkpoint_path)

def mkdir(path):

    path=path.strip()
    path=path.rstrip("\\")

    isExists=os.path.exists(path)

    if not isExists:
        print (path,"successful")
        os.makedirs(path)
        return True
    else:
        print("-"*10)
        print ("Directory already exists.Please remove it.")
        print("-"*10)
        return False

# fixed input for model eval
rand_inputs = Variable(torch.randn(10,100, 1, 1), volatile=True)
pair_inputs = torch.cat((rand_inputs,rand_inputs),0)
pair_labels = torch.cat((torch.zeros(10,1,1,1),torch.ones(10,1,1,1)),0)
rand_pair = torch.cat((pair_inputs,pair_labels),1)

path = sys.argv[1]
G_model = ACGAN_model.Generator()
G_model_path = sys.argv[2]
load_checkpoint(G_model_path,G_model)

G_model.eval()
test_output = G_model(rand_pair)
torchvision.utils.save_image(test_output.cpu().data,
                        os.path.join(path,'fig2_2.jpg'), nrow=10)
