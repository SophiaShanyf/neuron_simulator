from neuron import h, rxd
from neuron.units import ms, mV, μm
import pygame
import pygame_gui
import pygame_chart as pyc
import test_functions as tf
from main import *



## Test classes 

#SOMA 
soma = SOMA()
soma.make_a_neuron()
tf.test_soma_property(soma)

# Dendtrite and soma 
neuron = DEND_SOMA()
neuron.make_a_neuron()
tf.test_dend_soma_property(neuron)

# test pygame 
tf.run_pygame()


# test entire module 

run_simulation('soma', 'neuron_simulator/theme.json')

run_simulation('dend_soma',  'neuron_simulator/theme.json')

