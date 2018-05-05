#!/bin/sh

# install options for MAC
brew install python3
brew upgrade python3
brew install sl
brew tap ethereum/ethereum
brew install solidity
pip3 install -r requirements.txt

git submodule update --init --recursive
git submodule foreach git pull origin master

