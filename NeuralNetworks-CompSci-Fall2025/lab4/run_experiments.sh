#!/bin/bash

source ../venv/bin/activate

mkdir -p results

echo "Running experiments with different optimizers, learning rates, and batch sizes..."
echo "================================================================"

# Experiment 1: Different optimizers with default settings
echo -e "\n[Experiment 1] Testing optimizers: SGD, Adam, RMSprop"
python train.py --optimizer sgd --learning-rate 0.01 --batch-size 32 --epochs 100
python train.py --optimizer adam --learning-rate 0.01 --batch-size 32 --epochs 100
python train.py --optimizer rmsprop --learning-rate 0.01 --batch-size 32 --epochs 100

# Experiment 2: Different batch sizes with Adam
echo -e "\n[Experiment 2] Testing batch sizes: 8, 32, 64"
python train.py --optimizer adam --learning-rate 0.01 --batch-size 8 --epochs 100
python train.py --optimizer adam --learning-rate 0.01 --batch-size 64 --epochs 100

# Experiment 3: Different learning rates for SGD
echo -e "\n[Experiment 3] Testing SGD learning rates: 0.001, 0.01, 0.1"
python train.py --optimizer sgd --learning-rate 0.001 --batch-size 32 --epochs 100
python train.py --optimizer sgd --learning-rate 0.1 --batch-size 32 --epochs 100

# Experiment 4: Different learning rates for Adam
echo -e "\n[Experiment 4] Testing Adam learning rates: 0.0001, 0.001, 0.01"
python train.py --optimizer adam --learning-rate 0.0001 --batch-size 32 --epochs 100
python train.py --optimizer adam --learning-rate 0.001 --batch-size 32 --epochs 100

echo -e "\n================================================================"
echo "All experiments completed!"
echo "Generating comparison plots..."

python compare_results.py

echo "Done!"
