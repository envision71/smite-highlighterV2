# smite-highlighterV2

## How it works
When changes in regions of interest of the HUD such as the health bar and the K/D/A a clip is created. If something covers these elements a clip will also be created. 
To tell when a game has ened or started it compares the frame to the images provided. If the program does not detect that a game has started it will not clip anything.
Like wise if it has not detected that a game has ended it will countune to make a clip.

## Usage
Fill out to use either K/D/A, HP bar, or both to create clips. Then enter the time before and after an event to clip.
Enter a mp4 file of SMITE you want to highlight and an output directory for the clips to output to.
Prodvide the script with an image of the loading frames, victory or defeat screen, and middle of the game. This is for the program to obtain regions of interest to look at.
