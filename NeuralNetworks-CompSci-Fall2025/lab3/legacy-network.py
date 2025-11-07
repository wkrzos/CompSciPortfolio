from typing import List, Callable
import math
import random


def softmax(z: List[float]) -> List[float]:
	max_z = max(z) # a trick to achieve numerical stability but i don't understand it yet
	exps = [math.exp(v - max_z) for v in z]
	s = sum(exps)
	return [e / s for e in exps]

def relu(z: List[float]) -> List[float]:
    
    return (1 / (1 - math.exp(z)))


def mse_loss(predictions: List[float], targets: List[float]) -> float:
	n = len(predictions)
	return sum((p - t) ** 2 for p, t in zip(predictions, targets)) / n


def mse_derivative(predictions: List[float], targets: List[float]) -> List[float]:
	n = len(predictions)
	return [2 * (p - t) / n for p, t in zip(predictions, targets)]


def cross_entropy_loss(probs: List[float], targets: List[float]) -> float:
	eps = 1e-12
	return -sum(t * math.log(max(p, eps)) for p, t in zip(probs, targets))


def cross_entropy_derivative(probs: List[float], targets: List[float]) -> List[float]:
	return [p - t for p, t in zip(probs, targets)]


class Neuron:

	def __init__(self, n_inputs: int, activation: Callable = None):
		self.n_inputs = n_inputs
		# initialize small random weights
		self.weights = [random.uniform(-0.5, 0.5) for _ in range(n_inputs)]
		self.bias = random.uniform(-0.5, 0.5)
		# activation: None means identity
		self.activation = activation

	def forward(self, inputs: List[float]) -> float:
		if len(inputs) != self.n_inputs:
			raise ValueError("inputs length must match number of neuron inputs")
		z = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias
		return z if self.activation is None else self.activation(z)

class Network:
	def __init__(self, layers: List[List[Neuron]]):
		self.layers = layers

	def forward(self, inputs: List[float]) -> List[float]:
		for layer in self.layers:
			outputs = [n.forward(inputs) for n in layer]
			inputs = outputs
		return outputs


# gpt for now
def create_network(layer_sizes: List[int], activation: Callable = None) -> Network:
	"""
	layer_sizes is [n_input, n_hidden1, n_hidden2, ..., n_output].
	The returned structure excludes the input layer (contains only neuron layers
	corresponding to hidden and output layers).
	"""
	if len(layer_sizes) < 2:
		raise ValueError("layer_sizes must contain at least input and output sizes")
	network: List[List[Neuron]] = []
	for i in range(1, len(layer_sizes)):
		prev = layer_sizes[i - 1]
		curr = layer_sizes[i]
		layer = [Neuron(prev, activation=activation) for _ in range(curr)]
		network.append(layer)
	return Network(network)


if __name__ == "__main__":
	# quick smoke test
	net = create_network([3, 5, 5, 5, 2], activation=math.tanh)
	sample = [0.1, -0.2, 0.3]
	outputs = net.forward(sample)
	# apply softmax to the final layer outputs to get probabilities
	probs = softmax(outputs)
	print("network outputs (softmax probabilities):", probs)
