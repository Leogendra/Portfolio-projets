import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.linear_layer1 = nn.Linear(input_size, hidden_size)
        self.linear_layer2 = nn.Linear(hidden_size, output_size)
        # self.load()
        

    def forward(self, x):
        x = F.relu(self.linear_layer1(x))
        x = self.linear_layer2(x)
        return x
    

    def save(self, chemin_modele="model.pth"):
        dossier_modele = "./model"
        if not os.path.exists(dossier_modele):
            os.makedirs(dossier_modele)

        chemin_modele = os.path.join(dossier_modele, chemin_modele)
        torch.save(self.state_dict(), chemin_modele)


    # # fonction pour récupérer le modèle sauvegardé
    def load(self, chemin_modele="model.pth"):
        chemin_modele = os.path.join("./model", chemin_modele)
        if os.path.exists(chemin_modele):
            print("Chargement du modèle sauvegardé")
            self.model.load_state_dict(torch.load(chemin_modele))



class QTrainer:
    def __init__(self, model, learning_rate, gamma):
        self.lr = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        
        if len(state.shape) == 1:
            # (1, x) -> ajoute une dimension
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
            
        # 1: récupère les valeurs de la sortie du réseau de neurones
        prediction = self.model(state)

        target = prediction.clone()
        
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                # 2: Q_new = r + y * max(next_predicted Q value) -> on fais que ça si !done
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = Q_new
            
        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()
        
        self.optimizer.step()