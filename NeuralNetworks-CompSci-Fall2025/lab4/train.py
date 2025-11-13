import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import argparse
from pathlib import Path

from model import HeartDiseaseNet
from utils import load_data, save_results
from visualization import plot_training_results


def parse_args():
    parser = argparse.ArgumentParser(description='Train neural network with PyTorch')
    
    parser.add_argument('--data', type=str, default='processed_heart_cleveland.csv')
    parser.add_argument('--hidden-layers', type=int, nargs='+', default=[32])
    parser.add_argument('--optimizer', type=str, default='sgd', 
                       choices=['sgd', 'adam', 'rmsprop'])
    parser.add_argument('--learning-rate', type=float, default=0.01)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output-dir', type=str, default='results')
    parser.add_argument('--quiet', action='store_true')
    
    return parser.parse_args()


def get_optimizer(name, parameters, lr):
    name = name.lower()
    if name == 'sgd':
        return optim.SGD(parameters, lr=lr, momentum=0.9)
    elif name == 'adam':
        return optim.Adam(parameters, lr=lr)
    elif name == 'rmsprop':
        return optim.RMSprop(parameters, lr=lr)
    else:
        raise ValueError(f"Unknown optimizer: {name}")


def train_one_epoch(model, train_loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * inputs.size(0)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


def validate(model, val_loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc, np.array(all_preds), np.array(all_labels)


def train_model(model, train_loader, val_loader, criterion, optimizer, 
                epochs, device, verbose=True):
    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss': [], 'val_acc': []
    }
    
    for epoch in range(epochs):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, 
                                                optimizer, device)
        val_loss, val_acc, _, _ = validate(model, val_loader, criterion, device)
        
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        if verbose and (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1:3d}/{epochs} - "
                  f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f} - "
                  f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
    
    return history


def main():
    args = parse_args()
    
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    print("\n[1] Loading data...")
    x_train, y_train, x_test, y_test = load_data(args.data, test_size=0.2, 
                                                  random_state=args.seed)
    
    train_dataset = TensorDataset(
        torch.FloatTensor(x_train),
        torch.LongTensor(y_train)
    )
    test_dataset = TensorDataset(
        torch.FloatTensor(x_test),
        torch.LongTensor(y_test)
    )
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    print(f"Train samples: {len(x_train)}, Test samples: {len(x_test)}")
    
    print("\n[2] Building model...")
    model = HeartDiseaseNet(
        input_dim=x_train.shape[1],
        hidden_layers=args.hidden_layers,
        n_classes=2
    ).to(device)
    
    print(f"Architecture: {x_train.shape[1]} -> {' -> '.join(map(str, args.hidden_layers))} -> 2")
    print(f"Parameters: {sum(p.numel() for p in model.parameters())}")
    
    criterion = nn.CrossEntropyLoss()
    optimizer = get_optimizer(args.optimizer, model.parameters(), args.learning_rate)
    
    print(f"\n[3] Training...")
    print(f"Optimizer: {args.optimizer.upper()}")
    print(f"Learning rate: {args.learning_rate}")
    print(f"Batch size: {args.batch_size}")
    print(f"Epochs: {args.epochs}")
    print("-" * 70)
    
    history = train_model(model, train_loader, test_loader, criterion, 
                         optimizer, args.epochs, device, verbose=not args.quiet)
    
    print("\n[4] Final Evaluation")
    train_loss, train_acc, train_preds, train_labels = validate(
        model, train_loader, criterion, device
    )
    test_loss, test_acc, test_preds, test_labels = validate(
        model, test_loader, criterion, device
    )
    
    print(f"Train - Loss: {train_loss:.4f}, Acc: {train_acc:.4f} ({train_acc*100:.2f}%)")
    print(f"Test  - Loss: {test_loss:.4f}, Acc: {test_acc:.4f} ({test_acc*100:.2f}%)")
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    config_name = f"{args.optimizer}_lr{args.learning_rate}_bs{args.batch_size}"
    
    save_results(history, train_acc, test_acc, output_dir, config_name)
    
    plot_training_results(history, train_labels, train_preds,
                         test_labels, test_preds, output_dir, config_name)
    
    print(f"\n✓ Results saved to {output_dir}/")


if __name__ == '__main__':
    main()
