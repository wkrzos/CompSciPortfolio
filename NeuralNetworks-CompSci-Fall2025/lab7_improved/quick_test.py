"""
Quick test script to verify model and training pipeline.
"""

import torch
from model import RecurrentNet, BidirectionalRecurrentNet, count_parameters
from train import train_model
from utils import load_imdb_data, prepare_dataloaders, get_sequence_stats


def test_basic_training():
    """Test basic training with minimal configuration."""
    print("="*80)
    print("QUICK TEST - Basic Training")
    print("="*80)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nDevice: {device}")

    # Load small subset
    print("\nLoading IMDB data (5000 words, max_len=50)...")
    train_data, train_labels, test_data, test_labels, word_index = load_imdb_data(
        max_words=5000,
        max_len=50
    )

    # Statistics
    train_stats = get_sequence_stats(train_data)
    test_stats = get_sequence_stats(test_data)

    print(f"Train: {len(train_data)} sequences, mean_len={train_stats['mean']:.1f}")
    print(f"Test: {len(test_data)} sequences, mean_len={test_stats['mean']:.1f}")

    # Prepare dataloaders (use 5% of data)
    train_loader, val_loader, test_loader = prepare_dataloaders(
        train_data, train_labels, test_data, test_labels,
        batch_size=32,
        subsample_fraction=0.05
    )

    print(f"Train batches: {len(train_loader)}")
    print(f"Val batches: {len(val_loader)}")
    print(f"Test batches: {len(test_loader)}")

    # Create model
    model = RecurrentNet(
        vocab_size=5000,
        embedding_dim=64,
        hidden_dim=64,
        num_classes=2,
        rnn_type='LSTM',
        num_layers=1,
        dropout=0.3
    )

    print(f"\nModel: {model.__class__.__name__}")
    print(f"Parameters: {count_parameters(model):,}")

    # Train for 2 epochs
    print("\nTraining for 2 epochs...")
    results, trained_model = train_model(
        model, train_loader, val_loader, test_loader, device,
        epochs=2,
        learning_rate=0.001,
        patience=10
    )

    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    print(f"Test Accuracy: {results['test_accuracy']:.4f}")
    # Validation loss history is stored in results['history']
    val_loss = results['history']['val_loss'][-1]
    print(f"Final Val Loss: {val_loss:.4f}")
    print(f"Best Val Accuracy: {results['best_val_accuracy']:.4f}")
    print(f"Epochs Trained: {results['epochs_trained']}")

    return results


def test_model_architectures():
    """Test different model architectures."""
    print("\n" + "="*80)
    print("QUICK TEST - Model Architectures")
    print("="*80)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Test configurations
    configs = [
        {'name': 'LSTM', 'rnn_type': 'LSTM', 'hidden_dim': 64, 'bidirectional': False},
        {'name': 'RNN', 'rnn_type': 'RNN', 'hidden_dim': 64, 'bidirectional': False},
        {'name': 'BiLSTM', 'rnn_type': 'LSTM', 'hidden_dim': 64, 'bidirectional': True},
    ]

    vocab_size = 5000
    embedding_dim = 64

    for config in configs:
        print(f"\n{config['name']}:")

        if config['bidirectional']:
            model = BidirectionalRecurrentNet(
                vocab_size=vocab_size,
                embedding_dim=embedding_dim,
                hidden_dim=config['hidden_dim'],
                num_classes=2,
                rnn_type=config['rnn_type'],
                num_layers=1
            )
        else:
            model = RecurrentNet(
                vocab_size=vocab_size,
                embedding_dim=embedding_dim,
                hidden_dim=config['hidden_dim'],
                num_classes=2,
                rnn_type=config['rnn_type'],
                num_layers=1
            )

        n_params = count_parameters(model)
        print(f"  Parameters: {n_params:,}")

        # Test forward pass
        dummy_input = torch.randint(0, vocab_size, (4, 20)).to(device)

        model = model.to(device)
        model.eval()

        with torch.no_grad():
            output = model(dummy_input)

        print(f"  Output shape: {output.shape}")
        print(f"  Output range: [{output.min():.3f}, {output.max():.3f}]")


def test_truncation_lengths():
    """Test different sequence truncation lengths."""
    print("\n" + "="*80)
    print("QUICK TEST - Truncation Lengths")
    print("="*80)

    truncation_lengths = [None, 20, 50, 100, 200]

    for max_len in truncation_lengths:
        max_len_str = 'full' if max_len is None else str(max_len)
        print(f"\nMax length: {max_len_str}")

        train_data, train_labels, test_data, test_labels, word_index = load_imdb_data(
            max_words=5000,
            max_len=max_len
        )

        train_stats = get_sequence_stats(train_data)
        test_stats = get_sequence_stats(test_data)

        print(f"  Train: mean={train_stats['mean']:.1f}, "
              f"median={train_stats['median']:.1f}, "
              f"max={train_stats['max']}, "
              f"std={train_stats['std']:.1f}")
        print(f"  Test: mean={test_stats['mean']:.1f}, "
              f"median={test_stats['median']:.1f}, "
              f"max={test_stats['max']}, "
              f"std={test_stats['std']:.1f}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Quick tests for RNN/LSTM models')
    parser.add_argument('--test', type=str, default='all',
                        choices=['all', 'training', 'architectures', 'truncation'],
                        help='Which test to run')

    args = parser.parse_args()

    if args.test in ['all', 'architectures']:
        test_model_architectures()

    if args.test in ['all', 'truncation']:
        test_truncation_lengths()

    if args.test in ['all', 'training']:
        test_basic_training()

    print("\n" + "="*80)
    print("All tests completed!")
    print("="*80)
