import os

import torch
from torch import nn

import torch.nn.functional as F
class Network(nn.Module):

    def __init__(self, input_shape):
        super(Network, self).__init__()
      #  model = nn.Sequential(nn.Linear(n_input, n_hidden),
     #                         nn.ReLU(),
     #                         nn.Linear(n_hidden, n_out),
    #                          nn.Sigmoid())

        self.lin1 = nn.Linear(input_shape, 128)
        #3x12
        self.lin2 = nn.Linear(128, 39)




    def forward(self, x):
        """
        forward of both actor and critic
        """
        x = F.relu(self.lin1(x))
        x = F.relu(self.lin2(x))

        # actor: choses action to take from state s_t
        # by returning probability of each action
      #  action_prob = F.log_softmax(self.action_head(x), dim=-1)



        # return values for both actor and critic as a tuple of 2 values:
        # 1. a list with the probability of each action over the action space
        # 2. the value from state s_t
        return x

    def save_network(self, path, epoch_label):
        save_path = path + 'savedModels/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_filename = 'net_%s.pth' % epoch_label

        torch.save(self.state_dict(), save_path + save_filename)

    def load_network(self, path):
        state_dict = torch.load(path)
        self.load_state_dict(state_dict)
