"""
Neural network class that chains layers and handles training.
"""

import numpy as np
from layers import Layer
from losses import CrossEntropyLoss


class NeuralNetwork:
    """Sequential neural network model.
    
    This class chains multiple layers and handles forward/backward passes,
    as well as parameter updates.
    """
    
    def __init__(self, layers, loss_fn=None):
        """Initialize network with a list of layers.
        
        Args:
            layers: List of Layer objects
            loss_fn: Loss function object (default: CrossEntropyLoss)
        """
        self.layers = layers
        self.loss_fn = loss_fn if loss_fn is not None else CrossEntropyLoss()
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
    
    def forward(self, x):
        """Forward pass through all layers.
        
        Args:
            x: Input data of shape (batch_size, input_dim)
            
        Returns:
            Output of shape (batch_size, output_dim)
        """
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def backward(self, grad_output):
        """Backward pass through all layers in reverse order.
        
        Args:
            grad_output: Gradient from loss function
        """
        for layer in reversed(self.layers):
            grad_output = layer.backward(grad_output)
        return grad_output
    
    def update_parameters(self, learning_rate):
        """Update parameters in all layers.
        
        Args:
            learning_rate: Learning rate for gradient descent
        """
        for layer in self.layers:
            layer.update_parameters(learning_rate)
    
    def train_step(self, x_batch, y_batch, learning_rate):
        """Perform one training step (forward, backward, update).
        
        Args:
            x_batch: Input batch (batch_size, input_dim)
            y_batch: Target batch (batch_size, output_dim)
            learning_rate: Learning rate
            
        Returns:
            Loss value for this batch
        """
        # Forward pass
        predictions = self.forward(x_batch)
        
        # Compute loss
        loss = self.loss_fn.forward(predictions, y_batch)
        
        # Backward pass
        grad = self.loss_fn.backward(predictions, y_batch)
        self.backward(grad)
        
        # Update parameters
        self.update_parameters(learning_rate)
        
        return loss
    
    def predict(self, x):
        """Make predictions (forward pass without training).
        
        Args:
            x: Input data (batch_size, input_dim)
            
        Returns:
            Predictions (batch_size, output_dim)
        """
        return self.forward(x)
    
    def evaluate(self, x, y):
        """Evaluate network on given data.
        
        Args:
            x: Input data (n_samples, input_dim)
            y: True labels, one-hot encoded (n_samples, n_classes)
            
        Returns:
            Tuple of (loss, accuracy)
        """
        predictions = self.predict(x)
        loss = self.loss_fn.forward(predictions, y)
        
        # Compute accuracy
        pred_classes = np.argmax(predictions, axis=1)
        true_classes = np.argmax(y, axis=1)
        accuracy = np.mean(pred_classes == true_classes)
        
        return loss, accuracy
    
    def fit(self, x_train, y_train, x_val=None, y_val=None,
            epochs=100, learning_rate=0.01, batch_size=32, verbose=True):
        """Train the network.
        
        Args:
            x_train: Training data (n_samples, input_dim)
            y_train: Training labels, one-hot (n_samples, n_classes)
            x_val: Validation data (optional)
            y_val: Validation labels (optional)
            epochs: Number of training epochs
            learning_rate: Learning rate for gradient descent
            batch_size: Batch size for mini-batch gradient descent
            verbose: Whether to print progress
        """
        n_samples = x_train.shape[0]
        n_batches = (n_samples + batch_size - 1) // batch_size
        
        for epoch in range(epochs):
            # Shuffle training data
            indices = np.random.permutation(n_samples)
            x_shuffled = x_train[indices]
            y_shuffled = y_train[indices]
            
            # Mini-batch training
            epoch_losses = []
            for i in range(n_batches):
                start_idx = i * batch_size
                end_idx = min(start_idx + batch_size, n_samples)
                
                x_batch = x_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]
                
                loss = self.train_step(x_batch, y_batch, learning_rate)
                epoch_losses.append(loss)
            
            # Compute average epoch loss
            avg_loss = np.mean(epoch_losses)
            
            # Evaluate on training and validation sets
            train_loss, train_acc = self.evaluate(x_train, y_train)
            self.train_losses.append(train_loss)
            self.train_accuracies.append(train_acc)
            
            if x_val is not None and y_val is not None:
                val_loss, val_acc = self.evaluate(x_val, y_val)
                self.val_losses.append(val_loss)
                self.val_accuracies.append(val_acc)
            
            # Print progress
            if verbose and (epoch % 10 == 0 or epoch == epochs - 1):
                msg = f"Epoch {epoch+1}/{epochs} - Loss: {train_loss:.4f}, Acc: {train_acc:.4f}"
                if x_val is not None:
                    msg += f", Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}"
                print(msg)
    
    def get_layer_count(self):
        """Return number of layers in the network."""
        return len(self.layers)
    
    def get_parameter_count(self):
        """Count total number of trainable parameters."""
        total = 0
        for layer in self.layers:
            if hasattr(layer, 'W'):
                total += layer.W.size + layer.b.size
        return total
