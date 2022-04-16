#!/bin/python3
# nom           : Blacks
# prenom        : Simon
# Description   : Jeu quoridor en python

import os        # to clear the screen
import pickle    # for the save
import glob      # list saved files
import random    # for the bot

class Game:
    """a Game is a quoridor game allowing Players to play to the game"""
    def __init__(self, board_size = 10):
        """
        Create a Game and set default setup
        """
        self.board_size = board_size
        self.board = [ ["."] * board_size for i in range(board_size) ]
        self.players = []
        self.round = 0
        self.n_wall = 15
        self.fname = ""
        self.controls = ['z', 's', 'q', 'd', 'w']

    def save(self):
        """save the current game into a file"""
        with open(self.fname,"wb") as f:
            pickle.dump([self.board, self.board_size, self.players, self.round, self.controls], f)
        f.close()

    def load_save(self):
        """load a save asked to the user and run it"""
        files = glob.glob('*.qrd')
        if len(files) == 0:
            print("seems to be empty here...")
        else:
            for i in range(len(files)):
                print(i,"->",files[i])
            choice = input("which save to load(ENTER to skip) : ")
            if choice == "-1":
                return 0
            try:
                choice = int(choice)
            except ValueError:
                print("Bad choice...")
                return 0
            if choice < 0 or choice > len(files)-1:
                print("bad choice...")
                return 0
            self.fname = files[int(choice)]
            with open(self.fname, "rb") as f:
                self.board, self.board_size, self.players, self.round, self.controls = pickle.load(f)
            f.close()
            self.play()

    def remove_save(self):
        """remove a save given by a user"""
        files = glob.glob('*.qrd')
        if len(files) == 0:
            print("no save here...")
        else:
            for i in range(len(files)):
                print(i,"->",files[i])
            choice = input("which save to remove(ENTER to skip) : ")
            if choice == "-1":
                return 0
            try:
                choice = int(choice)
            except ValueError:
                print("Bad choice...")
                return 0
            os.remove(files[int(choice)])

    def set_difficulty(self):
        """set the difficulty (change number of walls allowed)"""
        diff = ""
        while diff not in ('1','2','3'):
            print("Difficulty :\n\t1. Easy\n\t2. Medium\n\t3. Hardest")
            diff = input("> ")
            if diff == '1':
                print("Easy")
                self.n_wall = 8
            elif diff == '2':
                print("Medium")
                self.n_wall = 6
            elif diff == '3':
                print("Hard")
                self.n_wall = 5
            os.system('cls' if os.name == 'nt' else 'clear')

    def change_controls(self):
        """ask user to change the game controls"""
        self.controls[0] = input("go up : ")
        self.controls[1]= input("go down : ")
        self.controls[2] = input("go left : ")
        self.controls[3] = input("go right : ")
        self.controls[4] = input("place wall : ")
        if len(self.controls) != len(set(self.controls)): # check if there is double same controls
            print("cannot use the same control for many actions...controls set to default....")
            self.controls = ['z', 's', 'q', 'd', 'w']
            print("up:{}\ndown:{}\nleft:{}\nright:{}\nwall:{}\n".format(self.controls[0],self.controls[1],self.controls[2],self.controls[3],self.controls[4]))
        else:
            print("controls changed")
            print("up:{}\ndown:{}\nleft:{}\nright:{}\nwall:{}\n".format(self.controls[0],self.controls[1],self.controls[2],self.controls[3],self.controls[4]))

    def save_menu(self):
        """menu to load/remove save"""
        choice = input("save(h for help)> ")
        while choice not in ("-1","quit","exit"):
            if choice in ("load","l"):
                self.load_save()
            elif choice in ("remove","r"):
                self.remove_save()
            elif choice == "h":
                print("Usage :\n\tload/l -> load a save\n\tremove/r -> remove a save\n\t-1/quit/exit -> quit save menu\n")
            else:
                print(f"{choice}: Command not found...")
            choice = input("save(h for help)> ")

    def menu(self):
        """show the menu, allow to start a new game or load/remove a save"""
        choice = input("(h for help)> ")
        while choice not in ("-1", "quit", "exit"):
            # show help
            if choice == "h":
                print("Usage\n\tplay/p -> to start a game\n\tsave/s -> load or remove save\n\tcontrols/c -> change controls\n\t-1/quit/exit -> quit (works during the game too)\n")
            # start the game
            elif choice in ("controls","c"):
                self.change_controls()
            elif choice in ("play","p"):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.set_difficulty()
                self.add_player()
                self.play()
            elif choice in ("save","s"):
                self.save_menu()
            else:
                print(f"{choice}: Command not found...")
            choice = input("(h for help)> ")

    def add_wall(self, position):
        """get a position and add a wall on the board, walls are X"""
        self.board[position[1]][position[0]] = 'X'

    def add_player(self):
        """ask for the number of player and their names"""
        if len(self.players) != None:
            n_player = input("How many players (2/4) : ")
            while n_player not in ('2','4'):
                print("bad choice...")
                n_player = input("How many players (2/4) : ")
            for i in range(int(n_player)):
                print(f"player{i+1} name : ", end='\0')
                name = input()
                is_bot = input("is that player a bot (yes/no) : ")
                while is_bot not in ("yes", "no"):
                    is_bot = input("is that player bot (yes/no) : ")
                if is_bot == "yes":
                    is_bot = True
                elif is_bot == "no":
                    is_bot = False
                self.players.append(Player(name, self, self.place_player(), len(self.players)+1, self.n_wall, is_bot))

    def place_player(self):
        """add player on the board with the player's number"""
        if len(self.players)+1 == 1:
            self.board[9][int(self.board_size/2)] = "1"
            return (int(self.board_size/2),9)
        elif len(self.players)+1 == 2:
            self.board[0][int(self.board_size/2)] = "2"
            return (int(self.board_size/2),0)
        elif len(self.players)+1 == 3:
            self.board[int(self.board_size/2)][0] = "3"
            return (0,int(self.board_size/2))
        elif len(self.players)+1 == 4:
            self.board[int(self.board_size/2)][9] = "4"
            return (9,int(self.board_size/2))

    def is_wall(self, position):
        """return 1 if the position already equal to a wall (X)"""
        if self.board[position[1]][position[0]] == 'X':
            return 1
        return 0

    def is_player(self, position):
        """return 1 if the position already equal to a player (1,2,3,4)"""
        if self.board[position[1]][position[0]] != ".":
            return 1
        return 0

    def draw(self):
        """print the board with 3 range of numbers (top, left, bottom)"""
        print("   ", *range(0, self.board_size))
        print()
        for i in range(len(self.board)): # for every line
            print(i, end="   ")
            for j in range(len(self.board[i])): # for every point
                print(self.board[i][j], end=" ")
            print()
        print()
        print("   ", *range(0, self.board_size))

    def play(self):
        """run a game"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.draw()
            self.players[self.round%len(self.players)].play()
            if self.players[self.round%len(self.players)].saved:
                print("game saved!")
                 # put all the game variables to null
                del self.players[:]
                self.round = 0
                self.board = [ ["."] * self.board_size for i in range(self.board_size)  ]
                self.controls = ['z', 's', 'q', 'd', 'w']
                return 0
            if self.players[self.round%len(self.players)].is_winner() == 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.draw()
                print(self.players[self.round%len(self.players)].name, "({}) won!".format(self.players[self.round%len(self.players)].numero))
                # put all the game variables to null
                del self.players[:]
                self.round = 0
                self.board = [ ["."] * self.board_size for i in range(self.board_size)  ]
                self.controls = ['z', 's', 'q', 'd', 'w']
                return 0
            self.round +=1

class Player:
    """Player is a user playing to a game"""
    def __init__(self, name , partie, start, numero, n_wall, bot):
        """
        Create a Player linked to a Game
        """
        self.name = name
        self.partie = partie
        self.start = start
        self.where = self.start
        self.numero = numero
        self.n_wall = n_wall
        self.saved = False
        self.bot = bot

    def move(self, mvmt):
        """Get the position of where the player wanna go and move it if free"""
        try:
            if self.is_free(mvmt) == 0:
                self.partie.board[self.where[1]][self.where[0]] = "."
                self.where = mvmt
                self.move((self.where[0],self.where[1]))
                self.partie.board[mvmt[1]][mvmt[0]] = self.numero
                return 0
        except:
            print("you cannot leave the board...")

    def place_wall(self):
        """
        ask where to place the wall, then verify if have walls and if 
        it's on the board, if there is already a player or a wall
        """
        if self.n_wall > 0:
            x = int(input("x : "))
            y = int(input("y : "))
            try:
                if self.partie.is_wall((x,y)) == 1:
                    print("there is already a wall there...")
                elif self.partie.is_player((x,y)) == 1:
                    print("there is a player there...")
                else:
                    try:
                        self.partie.add_wall((x,y))
                        self.n_wall -= 1
                        return 0
                    except:
                        print("x/y not in the board...")
            except:
                print("x/y not in the board...")
        else:
                    print("no more wall...")

    def is_winner(self):
        """
        if a player succeeded to go to the opposit of the board return 1
        """
        if self.numero == 1:
            if self.where[1] == 0:
                return 1
        if self.numero == 2:
            if self.where[1] == 9:
                return 1
        if self.numero == 3:
            if self.where[0] == 9:
                return 1
        if self.numero == 4:
            if self.where[0] == 0:
                return 1
        return 0

    def is_free(self, place):
        """verify if there is already a player or a wall at the given place"""
        if self.partie.is_wall(place) == 1:
            print("there is a wall...")
            return -1
        elif self.partie.is_player(place) == 1:
            print("there is a player there...")
            return -1
        if place[1] == -1:
            print("you cannot leave the board...")
            return -1    
        if place[0] == -1:
            print("you cannot leave the board...")
            return -1
        return 0

    def save(self):
        """ ask for the file name, save the game and then go back to the menu"""
        self.partie.fname = input("filename : ")
        self.partie.fname +=".qrd"
        self.partie.save()
        self.saved = True
        return 0

    def play(self):
        """ask for the player between place a wall, move or save or quit"""
        if not self.bot:
            choice = ""
            while choice not in (self.partie.controls[0],self.partie.controls[1],self.partie.controls[2],self.partie.controls[3],self.partie.controls[4],'save'):
                print("{}({}) -> wall = {} :".format(self.name,self.numero, self.n_wall))
                print("-> place wall ({}) or move ({},{},{},{}) or save : ".format(self.partie.controls[4],self.partie.controls[0],self.partie.controls[1],self.partie.controls[2],self.partie.controls[3]), end='\0')
                choice = input()
                if choice == self.partie.controls[4]:
                    if self.place_wall()  == 0:
                        break
                elif choice == self.partie.controls[0]: # go up
                    if self.move((self.where[0], self.where[1]-1)) == 0:
                        break
                elif choice == self.partie.controls[2]: # go left
                    if self.move((self.where[0]-1, self.where[1])) == 0:
                        break
                elif choice == self.partie.controls[1]: # go down
                    if self.move((self.where[0], self.where[1]+1)) == 0:
                        break
                elif choice == self.partie.controls[3]: # go right
                    if  self.move((self.where[0]+1, self.where[1])) == 0:
                        break
                elif choice == "save":
                    if self.save() == 0:
                        break
                elif choice in ("-1","quit","exit"):
                    exit(0)
                else :
                    print("Not a good choice...")
                choice = ""
        else:
            move = [(self.where[0], self.where[1]-1), (self.where[0]-1, self.where[1]), (self.where[0], self.where[1]+1),(self.where[0]+1, self.where[1])]
            mvmt = random.choice(move)
            while self.move(mvmt) != 0:
                mvmt = random.choice(move)

os.system('cls' if os.name == 'nt' else 'clear')
game = Game()
game.menu()
