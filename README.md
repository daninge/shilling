# Shilling

A decentralised file storage system for computationally limited devices. This was in part made for Harvard's CS244 in Spring 2018, taught by [Professor Kung](https://en.wikipedia.org/wiki/H._T._Kung). 

## Usage


## Installation
We will use a Python virtual environment for convenience. Also, packages require Python 3 in order to be run. If you haven't installed virtualenv yet, 
```
pip3 install virtualenv 
virtualenv venv
source venv/bin/activate
```
You can confirm using ```which python``` whether or not you are using a system Python installation or the one from the virtual environment. 

The dependencies include ```web3``` and ```solc```. To install these, run
```
brew tap ethereum/ethereum
brew install solidity
pip3 install web3
pip3 install py-solc
```

## Overview

Our system will consider the following four adversarial nodes:

* __Client Nodes:__ These nodes have files that they wish to store. They will offer a reward for storing a file for a given time period. These nodes are not restricted by computational power.
* __Storage Miners:__ These nodes have limited computational power. These nodes are purely responsible for storing data, and only require the computational ability to store the data and transfer it into and out of storage.
* __Retrieval Miners:__ These nodes act as file servers for the network for a fee.
* __Proof Miners:__ These nodes will perform proof-of-works for more computationally limited devices for a fee.


![POWDiagram1](docs/shillingdiagram1.png)


## Acknowledgements
We would like to thank all of the feedback we recieved from CS244, especially from [Professor Kung](https://en.wikipedia.org/wiki/H._T._Kung) and the TFs! Also, shoutout to [Professor Barak](http://www.boazbarak.org/) for all of the crypto help. 
