import json
from pathlib import Path
from visualization import plot_comparison


def load_all_results(results_dir='results'):
    results_dir = Path(results_dir)
    all_results = {}
    
    for json_file in sorted(results_dir.glob('*_results.json')):
        config_name = json_file.stem.replace('_results', '')
        with open(json_file, 'r') as f:
            data = json.load(f)
            all_results[config_name] = data['history']
    
    return all_results


def main():
    print("Loading results...")
    all_results = load_all_results()
    
    if not all_results:
        print("No results found!")
        return
    
    print(f"Found {len(all_results)} experiments")
    
    output_dir = Path('results')
    
    print("Generating comparison plots...")
    plot_comparison(all_results, output_dir, 'val_acc')
    plot_comparison(all_results, output_dir, 'val_loss')
    
    print("\n=== Final Results Summary ===")
    for config_name, history in sorted(all_results.items()):
        final_val_acc = history['val_acc'][-1]
        print(f"{config_name:30s} - Val Acc: {final_val_acc:.4f}")
    
    print("\nComparison plots saved!")


if __name__ == '__main__':
    main()
