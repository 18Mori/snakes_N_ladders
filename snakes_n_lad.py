from tkinter import *
import random
import tkinter as tk

game = Tk()
game.geometry("800x800")
game.config(bg="lightblue")
game.title("Snakes and Ladders")


snakes = {
    16:6, 47:26, 49:11, 56:53, 62:19, 64:60, 87:24, 93:73, 95:75, 98:78
}

ladders = {
    1:38, 4:14, 9:31, 21:42, 28:84, 36:44, 51:67, 71:91, 80:100
}

#GAME LOGIC
class Player:
  def __init__(self,name, color):
    self.name = name
    self.color = color
    self.token_id = None
    self.position = 0

  def __str__(self):
    return self.name


class gameBoard:
  def __init__(self,snakes, ladders):
    self.snakes = snakes
    self.ladders = ladders

# Encounter a snake
  def check_cell(self,player):
    current_pos = player.position
    if current_pos in self.snakes:
      New_pos = self.snakes[current_pos]
      return(New_pos,f"{player.name} got bitten by a snake! slide down to {New_pos}")
    elif current_pos in self.ladders:
      New_pos = self.ladders[current_pos]
      return(New_pos,f"{player.name} climbed a ladder! Moved to {New_pos}")
    else:
      print(f"{player.name} is at position {current_pos}")
    return player.position

#Encounter a ladder
    if curent_pos in self.ladders:
      New_pos = self.ladders[current_pos]
      player.position = New_pos
      return (New_pos, f"{player.name} climbed a ladder! climbed up to {New_pos}")
    else:
      print(f"{player.name} is at position {current_pos}")
    
    return current_pos
  

def roll_dice():
  return random.randint(1, 6)


#GAME INTERFACE
class SLgame(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Snakes and Ladders")
    self.geometry("800x800")
    self.config(bg="lightblue")
    self.players = []
    self.current_player_index = 0
    self.game_board = gameBoard(snakes, ladders)
    self.game_over = False
    self.welcome_screen()

  def welcome_screen(self):
    self.setup_screen = tk.Frame(self, bg="lightblue")
    self.setup_screen.pack(fill="both", expand=True)


game.mainloop()