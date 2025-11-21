"""
Quick test script to verify the setup and run a simple experiment.
"""

import torch
from model import create_model, count_parameters
from train import get_data_loaders, train_model

def quick_test():
    """Run a quick test with small configuration."""
    print("="*80)
    print("Quick Test - FashionMNIST Classification")
    print("="*80)

    # Check device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nDevice: {device}")

    # Create a simple model
    print("\nCreating single-layer network...")
    model = create_model('single', hidden_size=128)
    print(f"Model parameters: {count_parameters(model):,}")

    # Get small data loaders
    print("\nLoading FashionMNIST data (10% of training data)...")
    train_loader, test_loader = get_data_loaders(
        batch_size=32,
        data_fraction=0.1,
        noise_std=0.0,
        noise_train=False
    )

    print(f"Training samples: {len(train_loader.dataset)}")
    print(f"Test samples: {len(test_loader.dataset)}")

    # Train for a few epochs
    print("\nTraining for 5 epochs...")
    history = train_model(
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        num_epochs=5,
        learning_rate=0.001,
        device=device,
        noise_std=0.0,
        noise_train=False,
        verbose=True
    )

    # Print results
    print("\n" + "="*80)
    print("Quick Test Results:")
    print("="*80)
    print(f"Final Train Accuracy: {history['train_acc'][-1]:.2f}%")
    print(f"Final Test Accuracy: {history['test_acc'][-1]:.2f}%")
    print(f"Best Test Accuracy: {max(history['test_acc']):.2f}%")
    print("="*80)
    print("\nSetup verified successfully! You can now run full experiments.")
    print("Use: ./run_experiments.sh all")
    print("="*80)

if __name__ == '__main__':
    quick_test()
