# chutesladders

simulating chutes and ladders

running a monte carlo sim on a state transition matrix that represents the game

when i first learned first-step analysis i realized you can literally do this, and i thought it was super cool

i also messed around with what the game-length distribution looks like under different dice pmfs, thats why there are two matrix csvs

next step is to try something similar on a game with actual agency (mdp) and see if i can discover an optimal policy

if running sim make sure the transition matrix path in `chutesladders.py` points to the csv you want
