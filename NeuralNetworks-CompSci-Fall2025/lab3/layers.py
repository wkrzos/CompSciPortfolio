"""
Neural network layers with forward and backward pass implementations.
All operations use pure matrix calculations.
"""

import numpy as np
from abc import ABC, abstractmethod


class Layer(ABC):
    """Abstract base class for all layers."""
    
    @abstractmethod
    def forward(self, x):
        """Forward pass through the layer.
        
        Args:
            x: Input array of shape (batch_size, input_dim)
            
        Returns:
            Output array of shape (batch_size, output_dim)
        """
        pass
    
    @abstractmethod
    def backward(self, grad_output):
        """Backward pass through the layer.
        
        Args:
            grad_output: Gradient of loss w.r.t. layer output
                        Shape: (batch_size, output_dim)
        
        Returns:
            Gradient of loss w.r.t. layer input
            Shape: (batch_size, input_dim)
        """
        pass
    
    def update_parameters(self, learning_rate):
        """Update layer parameters using computed gradients.
        
        Default implementation does nothing (for layers without parameters).
        """
        pass


class Linear(Layer):
    """Fully connected linear layer: y = Wx + b
    
    Convention: x is (batch_size, n_in), weights W is (n_in, n_out)
    """
    
    def __init__(self, n_in, n_out, weight_std=0.01):
        """Initialize linear layer.
        
        Args:
            n_in: Number of input features
            n_out: Number of output features
            weight_std: Standard deviation for weight initialization
        """
        self.n_in = n_in
        self.n_out = n_out
        
        # Initialize weights and bias with proper dtype
        self.W = np.random.randn(n_in, n_out).astype(np.float64) * weight_std
        self.b = np.zeros((1, n_out), dtype=np.float64)
        
        # Cache for backward pass
        self.x_cache = None
        
        # Gradients
        self.grad_W = None
        self.grad_b = None
    
    def forward(self, x):
        """Forward pass: y = xW + b
        
        Args:
            x: Input of shape (batch_size, n_in)
            
        Returns:
            Output of shape (batch_size, n_out)
        """
        x = np.asarray(x, dtype=np.float64)
        self.x_cache = x
        return x @ self.W + self.b
    
    def backward(self, grad_output):
        """Backward pass using chain rule.
        
        Given dL/dy (grad_output), compute:
        - dL/dW = x^T @ dL/dy
        - dL/db = sum(dL/dy, axis=0)
        - dL/dx = dL/dy @ W^T
        
        Args:
            grad_output: Gradient of shape (batch_size, n_out)
            
        Returns:
            Gradient w.r.t. input of shape (batch_size, n_in)
        """
        grad_output = np.asarray(grad_output, dtype=np.float64)
        batch_size = self.x_cache.shape[0]
        
        # Compute gradients for parameters
        self.grad_W = (self.x_cache.T @ grad_output) / batch_size
        self.grad_b = np.sum(grad_output, axis=0, keepdims=True) / batch_size
        
        # Compute gradient w.r.t. input
        grad_input = grad_output @ self.W.T
        
        return grad_input
    
    def update_parameters(self, learning_rate):
        """Update weights and bias using gradient descent."""
        self.W -= learning_rate * self.grad_W
        self.b -= learning_rate * self.grad_b


class Activation(Layer):
    """Wrapper for activation functions.
    
    This delegates to activation function objects that implement
    forward and backward methods.
    """
    
    def __init__(self, activation_fn):
        """Initialize with an activation function object.
        
        Args:
            activation_fn: Object with forward() and backward() methods
        """
        self.activation_fn = activation_fn
        self.input_cache = None
        self.output_cache = None
    
    def forward(self, x):
        """Apply activation function."""
        self.input_cache = x
        output = self.activation_fn.forward(x)
        self.output_cache = output
        return output
    
    def backward(self, grad_output):
        """Backpropagate through activation function."""
        return self.activation_fn.backward(grad_output, self.input_cache, self.output_cache)
