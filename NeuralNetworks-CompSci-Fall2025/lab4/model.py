import torch
import torch.nn as nn


class HeartDiseaseNet(nn.Module):
    
    def __init__(self, input_dim=13, hidden_layers=[32], n_classes=2):
        super(HeartDiseaseNet, self).__init__()
        
        layers = []
        prev_size = input_dim
        
        for hidden_size in hidden_layers:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, n_classes))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)
