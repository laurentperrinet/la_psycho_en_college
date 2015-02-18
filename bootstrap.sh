#!/usr/bin/env bash

# 1. install Xcode:
# From this url : (uncomment the following line)
# open http://itunes.apple.com/us/app/xcode/id497799835?mt=12
# install Xcode on the Mac App Store by clicking on “View in Mac App Store”.

# 2. install HomeBrew
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# to reinstall, do:
# rm -rf /usr/local/Cellar /usr/local/.git && brew cleanup

# adding correct variables
# (see http://stackoverflow.com/questions/26775145/adding-directory-to-a-path-variable-like-path-just-once-in-bash )
var=$(echo $PATH | grep -o  '/usr/local/bin')
if [ -n "$var" ] ; then
	echo "export PATH=/usr/local/bin:$PATH" >> ~/.bash_profile
fi
var=$(echo $PATH | grep -o  '/usr/local/sbin')
if [ -n "$var" ] ; then
	echo "export PATH=/usr/local/sbin:$PATH" >> ~/.bash_profile
fi
var=$(echo $PYTHONPATH | grep -o  '/usr/local/lib/python2.7/site-packages')
if [ -n "$var" ] ; then
	echo "export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH" >> ~/.bash_profile
fi
var=$(echo $PYTHONPATH | grep -o  '/usr/local/opt/vtk5/lib/python2.7/site-packages')
if [ -n "$var" ] ; then
	echo "export PYTHONPATH=/usr/local/opt/vtk5/lib/python2.7/site-packages:$PYTHONPATH" >> ~/.bash_profile
fi

# Make sure we’re using the latest Homebrew.
brew update

# Upgrade any already-installed formulae.
brew upgrade


brew tap caskroom/cask
brew install brew-cask
brew cask install psychopy

#mkdir -p ~/Applications
brew linkapps
# Remove outdated versions from the cellar
brew cleanup

