"""
Quick test to verify early stopping functionality.
"""

import torch
from model import create_model
from train import get_data_loaders, train_model

def test_early_stopping():
    """Test early stopping with a simple configuration."""
    print("Testing Early Stopping Implementation")
    print("=" * 80)

    # Simple configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Create small model
    model = create_model('single', hidden_size=64)
    print(f"Model created with {sum(p.numel() for p in model.parameters()):,} parameters")

    # Get small batch of data
    train_loader, test_loader = get_data_loaders(
        batch_size=128,
        data_fraction=0.1,  # Use only 10% of data for faster testing
        noise_std=0.0,
        noise_train=False
    )

    print("\nTraining WITH early stopping (patience=3, min_delta=0.001):")
    print("-" * 80)
    history_with_es = train_model(
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        num_epochs=20,
        learning_rate=0.001,
        device=device,
        noise_std=0.0,
        noise_train=False,
        verbose=True,
        early_stopping=True,
        patience=3,
        min_delta=0.001
    )

    print("\n" + "=" * 80)
    print("RESULTS:")
    print(f"Total epochs trained: {len(history_with_es['train_acc'])}")
    if history_with_es['stopped_epoch'] is not None:
        print(f"✓ Early stopping triggered at epoch {history_with_es['stopped_epoch']}")
        print(f"✓ Saved {20 - history_with_es['stopped_epoch']} epochs of training!")
    else:
        print("✗ Early stopping was NOT triggered (model trained full 20 epochs)")

    print(f"\nFinal metrics:")
    print(f"  Train accuracy: {history_with_es['train_acc'][-1]:.2f}%")
    print(f"  Test accuracy:  {history_with_es['test_acc'][-1]:.2f}%")
    print(f"  Best test acc:  {max(history_with_es['test_acc']):.2f}%")
    print(f"  Overfit gap:    {history_with_es['train_acc'][-1] - history_with_es['test_acc'][-1]:.2f}%")

    # Create fresh model for comparison
    print("\n" + "=" * 80)
    print("\nTraining WITHOUT early stopping (for comparison):")
    print("-" * 80)
    model_no_es = create_model('single', hidden_size=64)
    history_no_es = train_model(
        model=model_no_es,
        train_loader=train_loader,
        test_loader=test_loader,
        num_epochs=20,
        learning_rate=0.001,
        device=device,
        noise_std=0.0,
        noise_train=False,
        verbose=True,
        early_stopping=False
    )

    print("\n" + "=" * 80)
    print("COMPARISON:")
    print(f"WITH early stopping:    {len(history_with_es['train_acc'])} epochs, test acc: {history_with_es['test_acc'][-1]:.2f}%")
    print(f"WITHOUT early stopping: {len(history_no_es['train_acc'])} epochs, test acc: {history_no_es['test_acc'][-1]:.2f}%")

    if history_with_es['stopped_epoch'] is not None:
        time_saved = sum(history_no_es['epoch_times'][history_with_es['stopped_epoch']:])
        print(f"\nTime saved with early stopping: {time_saved:.1f} seconds")
        print(f"Performance difference: {history_with_es['test_acc'][-1] - history_no_es['test_acc'][-1]:.2f}%")

if __name__ == "__main__":
    test_early_stopping()
