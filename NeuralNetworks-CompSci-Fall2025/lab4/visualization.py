import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
from pathlib import Path


def plot_training_results(history, train_labels, train_preds, 
                          test_labels, test_preds, output_dir, config_name):
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    epochs = range(1, len(history['train_loss']) + 1)
    
    axes[0, 0].plot(epochs, history['train_loss'], 'b-', label='Train', linewidth=2)
    axes[0, 0].plot(epochs, history['val_loss'], 'r-', label='Validation', linewidth=2)
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].set_title('Loss')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(epochs, history['train_acc'], 'b-', label='Train', linewidth=2)
    axes[0, 1].plot(epochs, history['val_acc'], 'r-', label='Validation', linewidth=2)
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Accuracy')
    axes[0, 1].set_title('Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_ylim([0, 1.05])
    
    cm_train = confusion_matrix(train_labels, train_preds)
    im = axes[1, 0].imshow(cm_train, cmap='Blues')
    axes[1, 0].set_title('Confusion Matrix - Train')
    axes[1, 0].set_xlabel('Predicted')
    axes[1, 0].set_ylabel('True')
    axes[1, 0].set_xticks([0, 1])
    axes[1, 0].set_yticks([0, 1])
    axes[1, 0].set_xticklabels(['Healthy', 'Disease'])
    axes[1, 0].set_yticklabels(['Healthy', 'Disease'])
    for i in range(2):
        for j in range(2):
            axes[1, 0].text(j, i, str(cm_train[i, j]), ha='center', va='center',
                          color='white' if cm_train[i, j] > cm_train.max()/2 else 'black',
                          fontsize=16, fontweight='bold')
    
    cm_test = confusion_matrix(test_labels, test_preds)
    im = axes[1, 1].imshow(cm_test, cmap='Blues')
    axes[1, 1].set_title('Confusion Matrix - Test')
    axes[1, 1].set_xlabel('Predicted')
    axes[1, 1].set_ylabel('True')
    axes[1, 1].set_xticks([0, 1])
    axes[1, 1].set_yticks([0, 1])
    axes[1, 1].set_xticklabels(['Healthy', 'Disease'])
    axes[1, 1].set_yticklabels(['Healthy', 'Disease'])
    for i in range(2):
        for j in range(2):
            axes[1, 1].text(j, i, str(cm_test[i, j]), ha='center', va='center',
                          color='white' if cm_test[i, j] > cm_test.max()/2 else 'black',
                          fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    save_path = output_dir / f'{config_name}.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Plot saved: {save_path}")


def plot_comparison(all_results, output_dir, metric='val_acc'):
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(all_results)))
    
    for (config_name, history), color in zip(all_results.items(), colors):
        epochs = range(1, len(history[metric]) + 1)
        ax.plot(epochs, history[metric], linewidth=2, label=config_name, color=color)
    
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Accuracy' if 'acc' in metric else 'Loss', fontsize=12)
    ax.set_title(f'{"Validation Accuracy" if metric=="val_acc" else "Validation Loss"} Comparison', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    if 'acc' in metric:
        ax.set_ylim([0, 1.05])
    
    plt.tight_layout()
    save_path = output_dir / f'comparison_{metric}.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Comparison plot saved: {save_path}")
