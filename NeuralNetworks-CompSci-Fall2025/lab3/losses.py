"""
Loss functions with forward and backward implementations.
"""

import numpy as np


class CrossEntropyLoss:
    """Cross-entropy loss for classification.
    
    This is designed to work with softmax outputs (probabilities).
    Loss: L = -sum(y_true * log(y_pred))
    
    When combined with softmax, the gradient simplifies to: y_pred - y_true
    """
    
    def forward(self, y_pred, y_true):
        """Compute cross-entropy loss.
        
        Args:
            y_pred: Predicted probabilities (batch_size, n_classes)
            y_true: True labels, one-hot encoded (batch_size, n_classes)
            
        Returns:
            Scalar loss value
        """
        batch_size = y_pred.shape[0]
        
        # Clip predictions for numerical stability
        y_pred_clipped = np.clip(y_pred, 1e-12, 1 - 1e-12)
        
        # Compute cross-entropy
        loss = -np.sum(y_true * np.log(y_pred_clipped)) / batch_size
        
        return loss
    
    def backward(self, y_pred, y_true):
        """Compute gradient of cross-entropy w.r.t. predictions.
        
        When softmax is the final activation, this simplifies to:
        grad = (y_pred - y_true) / batch_size
        
        Args:
            y_pred: Predicted probabilities (batch_size, n_classes)
            y_true: True labels, one-hot encoded (batch_size, n_classes)
            
        Returns:
            Gradient w.r.t. predictions (batch_size, n_classes)
        """
        batch_size = y_pred.shape[0]
        
        # For softmax + cross-entropy, the gradient is simply:
        grad = (y_pred - y_true) / batch_size
        
        return grad


class MSELoss:
    """Mean Squared Error loss.
    
    Loss: L = mean((y_pred - y_true)^2)
    """
    
    def forward(self, y_pred, y_true):
        """Compute MSE loss.
        
        Args:
            y_pred: Predictions (batch_size, output_dim)
            y_true: True values (batch_size, output_dim)
            
        Returns:
            Scalar loss value
        """
        return np.mean((y_pred - y_true) ** 2)
    
    def backward(self, y_pred, y_true):
        """Compute gradient of MSE.
        
        grad = 2 * (y_pred - y_true) / n
        
        Args:
            y_pred: Predictions (batch_size, output_dim)
            y_true: True values (batch_size, output_dim)
            
        Returns:
            Gradient w.r.t. predictions (batch_size, output_dim)
        """
        batch_size = y_pred.shape[0]
        return 2 * (y_pred - y_true) / batch_size
