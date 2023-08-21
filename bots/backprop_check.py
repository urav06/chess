import numpy as np
from bots.models import *
new_neural_network = Network([2,3,2], relu, relu_derivative)
for val in new_neural_network.weights:
  val.fil(1)
for val in new_neural_network.biases:
    val.fill(1)
new_neural_network.feed_forward(np.array([1,1]).reshape(-1,1))
new_neural_network.backprop(np.array([1,1]).reshape(-1,1), np.array([-2,1]).reshape(-1,1), 0.01)