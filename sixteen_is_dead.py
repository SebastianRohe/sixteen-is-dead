"""A simple dice game called sixteen is dead."""

from math import sqrt, log, e

__author__ = "Sebastian Rohe"
__copyright__ = "Copyright 2018/2019"
__credits__ = "EPR 2018/2019"
__email__ = "sebastian.rohe@googlemail.com"

import random
import time
import sys


def get_players():
    """Function to create players. User determines number and names of players via console input. Returns players."""
    number_of_players = 0
    # Number of players has to be bigger than 1.
    while (number_of_players < 2):
        # Try catch to intercept invalid inputs.
        while True:
            try:
                # Number of players are determined by input.
                number_of_players = int(input("Please enter the number of players: "))
                break
            except ValueError:
                print("Only integer values allowed. Please try again.")
    # Empty list of players.
    players = []

    # Every player gets unique id, name and sum with default value 0 at the start.
    for i in range(1, number_of_players + 1):
        player = input("Please enter name of player " + str(i) + ": ")
        players.append({"id": i, "name": player, "sum": 0})
    return players


def roll_dice(number=1, faces=6, seed=None):
    """Function to simulate a dice roll. Generated random numbers will be added in a list. Returns list."""
    dices = []

    # Intercept invalid parameters for dice roll.
    if (number < 1 or number > 10 or faces < 2 or faces > 100):
        print("Invalid dice parameters")
        number = 1
        faces = 6
    # Random numbers will get added to list.
    for i in range(0, number):
        dices.append(random.randint(1, faces + 1))

    return dices


def roll_cheating_dice():
    """Function to simulate cheating dice. Number 3 is twice as likely to appear."""
    dice = [1, 2, 3, 3, 4, 5, 6]
    return dice[random.randint(0, 6)]


def sixteen_is_dead(num_of_players, players):
    """Function to handle main game and all required functionalities."""
    print("\n########## - NEW GAME - ##########")
    current_player = 0
    selection = ''

    while (True):
        # Inform which players turn it is.
        print("\nTurn of Player " + str(current_player + 1) + " ("
		+ players[current_player]["name"] + ")")
        players[current_player]["sum"] = 0
        # First dice roll happens automatically. It is required that every player rolls the dice at least once.
        players[current_player]["sum"] += roll_dice()[0]
        # Wait till current player enters 'y' or 'n'.
        while (selection != 'y' or selection != 'n'):
            # If player does not get 9 or 10 as sum.
            if (players[current_player]["sum"] != 9 and players[current_player]["sum"] != 10):
                # Ask player if he wants to continue rolling the dice.
                selection = ''
                while (not (selection == 'y' or selection == 'n')):
                    selection = input("Current sum: " + str(players[current_player]["sum"]) \
                                      + ". Roll again? (y/n): ")
            # If the sum reaches 9, it is next players turn.
            elif (players[current_player]["sum"] == 9):
                print("Current sum: " + str(players[current_player]["sum"]) + \
                      ". Not allowed to continue rolling! ")
                selection = 'n'
            # If sum is 10, roll one more time.
            elif (players[current_player]["sum"] == 10):
                print("Current sum: " + str(players[current_player]["sum"]) + \
                      ". Roll dice again!: ")
                # Wait short a period of time.
                time.sleep(3)
                selection = 'y'
            # If player wants to roll again (see below). (*)
            if (selection == 'y'):
                players[current_player]["sum"] += roll_dice()[0]
                # If sum of player is bigger than 15 current player lost. Otherwise roll the dice until player enters 'n' to stop.
                if (players[current_player]["sum"] >= 16):
                    print("Player " + str(current_player + 1) + " " + players[current_player] \
                        ["name"] + " reached sum " + str(players[current_player]["sum"]) + \
                          " and lost the game!")
                    selection = ''
                    # Game over. Ask user if he wants to start new round.
                    while (not (selection == 'y' or selection == 'n')):
                        selection = input("Start new round? (y/n): ")
                    # Refresh and start new round.
                    if (selection == 'y'):
                        for i in range(0, num_of_players):
                            players[i]["sum"] = 0
                        current_player = 0
                        print("\n########## - NEW GAME - ##########")
                        break
                    elif (selection == 'n'):
                        return
            # If player does not want to roll again. (*)
            elif (selection == 'n'):
                # Pass dice to next player.
                current_player += 1
                # If all players rolled and nobody did lost yet.
                if (current_player > num_of_players - 1):
                    # Check for player with least points.
                    min_sum = 9999999
                    for i in range(0, num_of_players):
                        if (players[i]["sum"] < min_sum):
                            min_sum = players[i]["sum"]
                    for i in range(0, num_of_players):
                        if (players[i]["sum"] == min_sum):
                            print("Player " + str(i + 1) + " " + players[i]["name"] + \
                                  " reached lowest sum " + str(players[i]["sum"]) + " and lost the game!")
                    # Ask for another round.
                    selection = ''
                    while (not (selection == 'y' or selection == 'n')):
                        selection = input("Start new round? (y/n):")
                    if (selection == 'y'):
                        print("\n########## - NEW GAME - ##########")
                        current_player = 0
                    else:
                        return
                break


if (__name__ == "__main__"):
    # Call of all methods and functions to run the game.
    selection = ''
    while (not (selection == 'y' or selection == 'n')):
        selection = input("Start new game? (y/n): ")
        if (selection == 'y'):
            players = get_players()
            sixteen_is_dead(len(players), players)
        elif (selection == 'n'):
            sys.exit()
