import torch
import torch.nn as nn


class CNNModel(nn.Module):
    """
    Convolutional Neural Network model for image classification.

    Args:
        out_channels (int): Number of output channels in conv layer
        kernel_size (int): Size of the convolutional kernel
        pool_size (int): Size of max pooling window
        num_classes (int): Number of output classes (default: 10 for Fashion-MNIST)
    """

    def __init__(self, out_channels=32, kernel_size=3, pool_size=2, num_classes=10):
        super(CNNModel, self).__init__()

        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.pool_size = pool_size

        # Calculate padding to maintain spatial dimensions
        padding = (kernel_size - 1) // 2

        # First convolutional block: 1 input channel (grayscale), out_channels output channels
        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=out_channels,
            kernel_size=kernel_size,
            padding=padding
        )
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=pool_size, stride=pool_size)

        # Second convolutional block: out_channels input, 2*out_channels output
        self.conv2 = nn.Conv2d(
            in_channels=out_channels,
            out_channels=out_channels * 2,
            kernel_size=kernel_size,
            padding=padding
        )
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=pool_size, stride=pool_size)

        # Flatten layer
        self.flatten = nn.Flatten()

        # Fully connected layer with lazy initialization
        self.fc = nn.LazyLinear(num_classes)

    def forward(self, x):
        """
        Forward pass through the network.

        Args:
            x: Input tensor of shape (batch_size, 1, height, width)

        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        # First conv block
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)

        # Second conv block
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)

        # Flatten and FC layer
        x = self.flatten(x)
        x = self.fc(x)

        return x


class CNNModelDeeper(nn.Module):
    """
    Deeper Convolutional Neural Network with 3 convolutional blocks.
    """

    def __init__(self, out_channels=32, kernel_size=3, pool_size=2, num_classes=10):
        super(CNNModelDeeper, self).__init__()

        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.pool_size = pool_size

        padding = (kernel_size - 1) // 2

        # First conv block
        self.conv1 = nn.Conv2d(1, out_channels, kernel_size, padding=padding)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(pool_size, stride=pool_size)

        # Second conv block
        self.conv2 = nn.Conv2d(out_channels, out_channels * 2, kernel_size, padding=padding)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(pool_size, stride=pool_size)

        # Third conv block
        self.conv3 = nn.Conv2d(out_channels * 2, out_channels * 4, kernel_size, padding=padding)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(pool_size, stride=pool_size)

        self.flatten = nn.Flatten()
        self.fc = nn.LazyLinear(num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)

        x = self.conv3(x)
        x = self.relu3(x)
        x = self.pool3(x)

        x = self.flatten(x)
        x = self.fc(x)

        return x
