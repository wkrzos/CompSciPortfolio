#!/bin/bash
# Quick examples for running the neural network training

echo "================================"
echo "Neural Network Training Examples"
echo "================================"
echo ""

# Get the Python path
PYTHON="/home/wojciu/projects/CompSciPortfolio/NeuralNetworks-CompSci-Fall2025/venv/bin/python"

echo "1. Basic training (1 hidden layer, 64 neurons)"
echo "   Command: $PYTHON train.py --hidden-layers 64 --learning-rate 0.1 --weight-std 0.1"
echo ""

echo "2. Two hidden layers (64, 32 neurons)"
echo "   Command: $PYTHON train.py --hidden-layers 64 32 --learning-rate 0.1 --weight-std 0.1 --epochs 150"
echo ""

echo "3. Different learning rates comparison"
echo "   Low LR:  $PYTHON train.py --learning-rate 0.01"
echo "   Med LR:  $PYTHON train.py --learning-rate 0.1"
echo "   High LR: $PYTHON train.py --learning-rate 0.5"
echo ""

echo "4. Different hidden layer sizes"
echo "   Small:  $PYTHON train.py --hidden-layers 16 --learning-rate 0.1 --weight-std 0.1"
echo "   Medium: $PYTHON train.py --hidden-layers 64 --learning-rate 0.1 --weight-std 0.1"
echo "   Large:  $PYTHON train.py --hidden-layers 128 --learning-rate 0.1 --weight-std 0.1"
echo ""

echo "5. Without normalization (to see the difference)"
echo "   Command: $PYTHON train.py --no-normalize --hidden-layers 64 --learning-rate 0.1 --weight-std 0.1"
echo ""

echo "6. Different weight initialization"
echo "   Small std:  $PYTHON train.py --weight-std 0.01 --learning-rate 0.1"
echo "   Medium std: $PYTHON train.py --weight-std 0.1 --learning-rate 0.1"
echo "   Large std:  $PYTHON train.py --weight-std 0.5 --learning-rate 0.1"
echo ""

echo "7. Run all experiments (saves results to results/ folder)"
echo "   Command: $PYTHON run_experiments.py"
echo ""

echo "================================"
echo "Recommended starting point:"
echo "================================"
$PYTHON train.py --hidden-layers 64 --learning-rate 0.1 --weight-std 0.1 --epochs 100
