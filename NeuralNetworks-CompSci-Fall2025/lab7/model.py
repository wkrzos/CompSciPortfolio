"""
Model definitions for IMDB sentiment classification using recurrent networks.
Implements RNN and LSTM-based models with embedding layer.
"""

import torch
import torch.nn as nn


class RecurrentNet(nn.Module):
    """
    Recurrent Neural Network for text classification.

    Args:
        vocab_size (int): Size of vocabulary
        embedding_dim (int): Dimension of word embeddings
        hidden_dim (int): Dimension of recurrent layer
        num_classes (int): Number of output classes (2 for binary sentiment)
        rnn_type (str): Type of recurrent layer ('RNN' or 'LSTM')
        num_layers (int): Number of recurrent layers
        dropout (float): Dropout rate between layers
    """

    def __init__(self, vocab_size, embedding_dim=128, hidden_dim=128,
                 num_classes=2, rnn_type='LSTM', num_layers=1, dropout=0.5):
        super(RecurrentNet, self).__init__()

        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        self.rnn_type = rnn_type
        self.num_layers = num_layers

        # Embedding layer: converts word indices to dense vectors
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)

        # Recurrent layer
        if rnn_type == 'RNN':
            self.rnn = nn.RNN(
                embedding_dim,
                hidden_dim,
                num_layers=num_layers,
                batch_first=True,
                dropout=dropout if num_layers > 1 else 0
            )
        elif rnn_type == 'LSTM':
            self.rnn = nn.LSTM(
                embedding_dim,
                hidden_dim,
                num_layers=num_layers,
                batch_first=True,
                dropout=dropout if num_layers > 1 else 0
            )
        else:
            raise ValueError(f"Unknown RNN type: {rnn_type}. Use 'RNN' or 'LSTM'.")

        # Dropout layer
        self.dropout = nn.Dropout(dropout)

        # Fully connected output layer
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        """
        Forward pass through the network.

        Args:
            x: Input tensor of shape (batch_size, seq_len) containing word indices

        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        # Embed word indices: (batch, seq_len) -> (batch, seq_len, embedding_dim)
        embedded = self.embedding(x)

        # Pass through recurrent layer: (batch, seq_len, embedding_dim) -> (batch, seq_len, hidden_dim)
        # For LSTM, output is (output, (h_n, c_n)); for RNN, output is (output, h_n)
        if self.rnn_type == 'LSTM':
            rnn_out, (hidden, cell) = self.rnn(embedded)
        else:
            rnn_out, hidden = self.rnn(embedded)

        # Take the last hidden state from the last layer
        # hidden shape: (num_layers, batch, hidden_dim)
        last_hidden = hidden[-1]  # (batch, hidden_dim)

        # Apply dropout
        out = self.dropout(last_hidden)

        # Pass through fully connected layer
        out = self.fc(out)  # (batch, num_classes)

        return out


class BidirectionalRecurrentNet(nn.Module):
    """
    Bidirectional Recurrent Neural Network for text classification.

    Args:
        vocab_size (int): Size of vocabulary
        embedding_dim (int): Dimension of word embeddings
        hidden_dim (int): Dimension of recurrent layer
        num_classes (int): Number of output classes (2 for binary sentiment)
        rnn_type (str): Type of recurrent layer ('RNN' or 'LSTM')
        num_layers (int): Number of recurrent layers
        dropout (float): Dropout rate between layers
    """

    def __init__(self, vocab_size, embedding_dim=128, hidden_dim=128,
                 num_classes=2, rnn_type='LSTM', num_layers=1, dropout=0.5):
        super(BidirectionalRecurrentNet, self).__init__()

        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        self.rnn_type = rnn_type
        self.num_layers = num_layers

        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)

        # Bidirectional recurrent layer
        if rnn_type == 'RNN':
            self.rnn = nn.RNN(
                embedding_dim,
                hidden_dim,
                num_layers=num_layers,
                batch_first=True,
                bidirectional=True,
                dropout=dropout if num_layers > 1 else 0
            )
        elif rnn_type == 'LSTM':
            self.rnn = nn.LSTM(
                embedding_dim,
                hidden_dim,
                num_layers=num_layers,
                batch_first=True,
                bidirectional=True,
                dropout=dropout if num_layers > 1 else 0
            )
        else:
            raise ValueError(f"Unknown RNN type: {rnn_type}. Use 'RNN' or 'LSTM'.")

        # Dropout layer
        self.dropout = nn.Dropout(dropout)

        # Fully connected output layer (hidden_dim * 2 because bidirectional)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        """
        Forward pass through the network.

        Args:
            x: Input tensor of shape (batch_size, seq_len) containing word indices

        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        # Embed word indices
        embedded = self.embedding(x)

        # Pass through bidirectional recurrent layer
        if self.rnn_type == 'LSTM':
            rnn_out, (hidden, cell) = self.rnn(embedded)
        else:
            rnn_out, hidden = self.rnn(embedded)

        # Concatenate forward and backward hidden states from last layer
        # hidden shape: (num_layers * 2, batch, hidden_dim) for bidirectional
        # We want the last layer's forward and backward states
        forward_hidden = hidden[-2]  # (batch, hidden_dim)
        backward_hidden = hidden[-1]  # (batch, hidden_dim)
        last_hidden = torch.cat([forward_hidden, backward_hidden], dim=1)  # (batch, hidden_dim*2)

        # Apply dropout
        out = self.dropout(last_hidden)

        # Pass through fully connected layer
        out = self.fc(out)

        return out


def count_parameters(model):
    """Count the number of trainable parameters in a model."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
