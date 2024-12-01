
import numpy as np


import torch

from Backend.Simple_NN import config

from Backend.Simple_NN.Network import Network
from Backend.Simple_NN.config import eval_every_x_epochs


def simple_avg_loss(state, new_boarders):

    #minimze fehler ...
    #overall duration
    sum_duration = torch.sum(state[0])
    sum_mistakes = torch.sum(state[1])

    return sum_duration +sum_mistakes


def state_to_tensor(environment, instance=None):
    tensor_MAXLOW = torch.from_numpy(environment.MAXLOW_pertask)
    tensor_MAXMED = torch.from_numpy(environment.MAXMEDIUM_pertask)

    tensor_duration_avg = torch.tensor(environment.person_to_levels[0]) #todo for some reasons the last one is 0, not right
    tensor_fai_avg = torch.tensor(environment.person_to_levels[1])

    #these are kind of the same, use first row if boarder variationn on
    tensor_boarders_used = torch.tensor(environment.person_to_levels[2])
    failures_tensor = torch.tensor([environment.failure_easy, environment.failure_middle, environment.failure_hard])



    desired_shape = (13,)
    new_tensor = torch.zeros(desired_shape)
    new_tensor[:failures_tensor.shape[0]] = failures_tensor

    result = torch.cat((tensor_MAXLOW.unsqueeze(0), tensor_MAXMED.unsqueeze(0), tensor_duration_avg.unsqueeze(0),
                        tensor_fai_avg.unsqueeze(0), new_tensor.unsqueeze(0)), dim=0).float()


    return result

def run_one_epoch(epoch, optimizer, environment, model, type ):
    all_losses = []
    optimizer.zero_grad()

    state = state_to_tensor(environment)
    new_boarders = model(state.view(-1))

    loss = simple_avg_loss(state, new_boarders)
    environment.update_enviroment(new_boarders)
    # TODO update environment
    if type == "Train":
        loss.backward()
        optimizer.step()
        # Store loss and metrics
    all_losses.append(loss.detach().cpu().numpy())
    print(f"{type} epoch {epoch} loss: ", np.array(all_losses).mean())

    #if type == "TEST":
        #TODO test performance






def train( assistance):

    environment = assistance.score_calulator
    state = state_to_tensor(environment).view(-1)
    model = Network(state.shape[0])
    #to run via SimpleNN/train.py
    model.load_network("networks/savedModels/net_100.pth")
    #if online system
  #  model.load_network("../../Simple_NN/networks/savedModels/net_100.pth")


    mps_device = torch.device("cpu")
    model.to(mps_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    all_losses = []


    for epoch in range(1, config.n_episodes + 1):

        model.train()
        run_one_epoch(epoch, optimizer, environment, model, type ="TRAIN")
        # Reset gradients
        if epoch % eval_every_x_epochs == 0 and epoch > 0:
            model.eval()
            val_loss = run_one_epoch(epoch, optimizer, environment, model, type ="TEST")





    model.save_network("../../Simple_NN/networks/", config.n_episodes)
    assistance.db_connector.save_boarders(environment)
    #  if epoch % 100 == 0 and epoch > 0:
    #     print("Start test epoch...")
    # save network
    #    model.eval()
    #   run_one_epoch(test_loader, test_dataset, type="Test", epoch=epoch, kl_beta=config.KL_BETA)





