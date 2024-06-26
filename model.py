import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initialize the neural network with one hidden layer.

        Args:
            input_size (int): The number of input features.
            hidden_size (int): The number of neurons in the hidden layer.
            output_size (int): The number of output features.
        """
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        Define the forward pass of the network. Uses ReLU activation function (f(x) = max(0, u)).

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor after passing through the network.
        """
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        """
        Save the model parameters to a file.

        Args:
            file_name (str): The name of the file to save the model parameters. Default is 'model.pth'.
        """
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        """
        Initialize the Q-learning trainer.

        Args:
            model (Linear_QNet): The neural network model to be trained.
            lr (float): The learning rate for the optimizer.
            gamma (float): The discount factor for future rewards.
        """
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        # MSE is a mean squared error function, measures the difference between predicted and actual Q-values
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        """
        Perform a single training step on the given batch of experience.

        Args:
            state (np.array): The current state.
            action (np.array): The action taken.
            reward (np.array): The reward received.
            next_state (np.array): The next state.
            done (bool): Whether the episode is done.

        This method calculates the predicted Q-values, the target Q-values using the Bellman equation,
        computes the loss, and updates the model parameters.
        """
        # Conversion to the PyTorch tensors.
        # (n, x)
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # Reshape the inputs to be batches of size 1 if they are single examples
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Predicted Q values with the current state
        pred = self.model(state)

        target = pred.clone()
        # Updating Q value for every move
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                # Bellman equation
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # Zero the parameter gradients
        self.optimizer.zero_grad()
        # Compute the loss
        loss = self.criterion(target, pred)
        # Backpropagation
        loss.backward()
        # Perform a single optimization step (parameter update)
        self.optimizer.step()
