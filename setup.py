from setuptools import setup

setup(
   name='neuron_simulator',
   version='1.0',
   description='a visualization tool for neuron spiking graph',
   author='Sophia Shan',
   author_email='shanyufei2001@gmail.com',
   packages=['neuron', 'pysimplegui'],  #same as name
   # install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)