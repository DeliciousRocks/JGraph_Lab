# JGraph_Lab

My JGraph lab takes JSON representations of Magic the Gathering cards and renders them as images.

Python is the primary tool doing the heavy lifitng behind the scenes and the following modules are required:
json, os, re, sys, and from PIL import Image; Aside from that, there is no compliation required and the inclused scripts should demonstrate the abilites of the project.

There are three seperate scripts used to set everything up; these three scripts can be run individually, or do_it_all.sh can be called to handle everything; before they will work properly you will need to list them as executable using `cmod +x filename.sh`.

1)Decompress.sh inflates the Art_Assests folder as GitHub was not a fan of me trying to upload a bunch of images; it also didn't like my encapsulated post script for the frames, so the script also recreates the neccessary .eps files from the included .jgr files in "Frames_EPS".

2)printCards.sh creates the 5 different cards' .jgr files, it does this by calling printCard.py and passing it the information about the card as a JSON file and the image that will be used for the card's artwork.

3)createImages.sh then takes the previously created .jgr files and convertes them into images of the cards.

Additionally, I've included pixelExtractor.py, which while no longer used in the current process was used to help extract the original .jgr files.

While I prepared many features to allow for many different cards to be prepresented, many of which are not displayed in the 5 demo cards, the game is constantly evolving and as a result I was unable to include every graphical element currently used in the game; that said, this program supports most of the standard frames and symbols required to create a Magic the Gathering card; below is a comparison between the an actual version of "Shivan Dragon" and one created with my program.


![s-l500](https://user-images.githubusercontent.com/7126642/193717328-f9c9d413-5364-4dc2-b8a1-0943d921617c.jpg)

As a final note, the last two scripts take a bit to run; a alot of the post script is composed of individual points that take a while to get drawn.
