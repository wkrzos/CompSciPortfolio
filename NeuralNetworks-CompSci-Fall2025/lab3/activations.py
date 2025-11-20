import numpy as np

# Softmax with help from Claude 4.5
class Softmax:
    """Softmax activation function.
    
    For numerical stability, we subtract max before exponentiating.
    Forward: softmax(x)_i = exp(x_i - max(x)) / sum(exp(x_j - max(x)))
    """
    
    def forward(self, x):
        """Apply softmax to each row (sample) independently.
        
        Args:
            x: Input of shape (batch_size, n_classes)
            
        Returns:
            Probabilities of shape (batch_size, n_classes)
        """
        # Subtract max for numerical stability
        x = np.asarray(x, dtype=np.float64)
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def backward(self, grad_output, input_cache, output_cache):
        """Compute gradient of softmax.
        
        For softmax, the Jacobian is complex, but when combined with
        cross-entropy loss, it simplifies. Here we implement the general case.
        
        For a single sample: J_ij = s_i * (δ_ij - s_j)
        where s is the softmax output and δ_ij is Kronecker delta.
        
        Args:
            grad_output: Gradient from next layer (batch_size, n_classes)
            input_cache: Cached input (not needed, can use output)
            output_cache: Cached softmax output (batch_size, n_classes)
            
        Returns:
            Gradient w.r.t. input (batch_size, n_classes)
        """
        # For each sample, multiply Jacobian by gradient
        s = output_cache
        batch_size, n_classes = s.shape
        
        grad_input = np.zeros_like(grad_output)
        
        for i in range(batch_size):
            s_i = s[i:i+1, :].T  # (n_classes, 1)
            grad_i = grad_output[i:i+1, :].T  # (n_classes, 1)
            
            # Jacobian: J_kj = s_k * (δ_kj - s_j)
            # This creates a matrix where J[k,j] = s[k] * δ[k,j] - s[k] * s[j]
            jacobian = np.diagflat(s_i) - s_i @ s_i.T
            
            # grad_input = J^T @ grad_output (in matrix form)
            grad_input[i:i+1, :] = (jacobian @ grad_i).T
        
        return grad_input


class ReLU:
    def forward(self, x):
        x = np.asarray(x, dtype=np.float64)
        return np.maximum(0, x)
    
    def backward(self, grad_output, input_cache, output_cache):
        return grad_output * (input_cache > 0)


class Sigmoid:
    def forward(self, x):
        x = np.asarray(x, dtype=np.float64)
        # Numerical stability
        return np.where(
            x >= 0,
            1 / (1 + np.exp(-x)),
            np.exp(x) / (1 + np.exp(x))
        )
    
    def backward(self, grad_output, input_cache, output_cache):
        s = output_cache
        return grad_output * s * (1 - s)


class Tanh:
    def forward(self, x):
        x = np.asarray(x, dtype=np.float64)
        return np.tanh(x)
    
    def backward(self, grad_output, input_cache, output_cache):
        return grad_output * (1 - output_cache ** 2)
