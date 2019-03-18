from javax.swing import JFrame, JPanel, JButton, JLabel, JTextField, ImageIcon
from java.awt.BorderLayout import NORTH
from java.awt.event import ActionListener, WindowAdapter
from os import listdir
from os.path import isfile, join
import random
import platform

#relative paths to pictures  (RESOURCE FOLDER)
rpenguin = '/penguin.jpg'
rchrome = '/chrome.jpg'
rfox = '/fox.jpg'
rfish = '/fish.jpg'
rbird = '/bird.jpg'
rcharizard = '/charizard.jpg'
rsonic = '/sonic.png'


class TicTacToeGame(WindowAdapter):

   # Tic Tac Toe game with Mario and Dizzy animated icons/music.
   # Computer plays with Mario and player plays with Dizzy.

   # game title
   game_title = "Tic Tac Toe: You vs Mario"
   # welcome status message.
   welcome_status = "Welcome! Please make your first move."
   # in-game status message.
   in_game_status = "Mario chases You! Hurry up!"
   # board 3x3 with the default color - white
   board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
   # total number of cells
   size = len(board) * len(board)   
   # size of cell
   tile_size = 128
   # status bar height
   status_bar_height = 50
   # status bar top margin
   status_bar_margin_top = -15
   # status bar left margin
   status_bar_margin_left = 10
   # number of cells in a row/column
   cells = 3
   # winner
   winner = None
   # Mario image
   mario = '/MARIO_128x128.gif'
   # Dizzy image
   dizzy = None
   
    
   
   # Blank
   blank = '/BLANK.gif'
   # supported musice sounds
   sounds = ['/DIZZY.wav', '/MARIO.wav']
   # currently played sound
   sound = None
   # last chosen sound
   last_sound = 0
   # won sound
   won_sound = '/WON.wav'
   # lose sound
   lose_sound = '/LOSE.wav'
   # tie sound
   tie_sound = '/TIE.wav'
   # action sound
   action_sound = '/ACTION.wav'

   def __init__(self, resources_directory):

     # Game constructor.
     #
     # Parameters:
     #   resources_directory Directory to look for images and audio files.
     
     is_windows = platform.platform().lower().find('win') > 0
     self.main_window_padding_right = 20 if is_windows else 0
     self.main_window_padding_bottom = 40 if is_windows else 0
     
     self.resources_directory = resources_directory

     self.button1 = JButton("", actionPerformed=self.clicked1)
     self.button2 = JButton("", actionPerformed=self.clicked2)
     self.button3 = JButton("", actionPerformed=self.clicked3)
     self.button4 = JButton("", actionPerformed=self.clicked4)
     self.button5 = JButton("", actionPerformed=self.clicked5)
     self.button6 = JButton("", actionPerformed=self.clicked6)
     self.button7 = JButton("", actionPerformed=self.clicked7)
     self.button8 = JButton("", actionPerformed=self.clicked8)
     self.button9 = JButton("", actionPerformed=self.clicked9)
     image_size = self.tile_size
     self.button1.setBounds(0 * image_size, 0 * image_size, image_size, image_size)
     self.button2.setBounds(1 * image_size, 0 * image_size, image_size, image_size)
     self.button3.setBounds(2 * image_size, 0 * image_size, image_size, image_size)
     self.button4.setBounds(0 * image_size, 1 * image_size, image_size, image_size)
     self.button5.setBounds(1 * image_size, 1 * image_size, image_size, image_size)
     self.button6.setBounds(2 * image_size, 1 * image_size, image_size, image_size)
     self.button7.setBounds(0 * image_size, 2 * image_size, image_size, image_size)
     self.button8.setBounds(1 * image_size, 2 * image_size, image_size, image_size)
     self.button9.setBounds(2 * image_size, 2 * image_size, image_size, image_size)
     self.buttons = [self.button1, self.button2, self.button3, 
        self.button4, self.button5, self.button6, 
        self.button7, self.button8, self.button9]
     self.buttons_mapped = [[self.button1, self.button2, self.button3], 
        [self.button4, self.button5, self.button6], 
        [self.button7, self.button8, self.button9]]
     
     width = self.tile_size * self.cells
     height = width
     self.frame = JFrame(self.game_title, size = (width, height + self.status_bar_height))
     self.frame.setLocation(200, 100)
     self.frame.setLayout(None)
     
     for button in self.buttons:
        self.frame.add(button)
     
     self.status_label = JLabel("")
     self.status_label.setBounds(self.status_bar_margin_left, height + self.status_bar_margin_top, width, self.status_bar_height)
     self.frame.add(self.status_label)
        
     self.frame.setVisible(True)
     self.frame.addWindowListener(self)
     random.shuffle(self.sounds)

     self.restart()


   # Restarts the game.  
   def restart(self):
     
     self.dizzy = None
     self.dizzy = self.choosePlayer()
     self.winner = None
     self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
     for button in self.buttons:
       button.setIcon(ImageIcon(self.resources_directory + self.blank))
     self.stop_playing_background()
     self.sound = self.play_sound_safe(self.sounds[self.last_sound])
     self.last_sound = self.last_sound + 1
     if self.last_sound >= len(self.sounds):
       self.last_sound = 0
     self.status_label.setText(self.welcome_status)

    
   # Stops playing any background music, if any playing now.
   def stop_playing_background(self):
    
     if self.sound != None:
       self.sound.stopPlaying()
       self.sound = None

   def set_dizzy(self, button):

     # Draws Dizzy in a given button, sets game status to "Playing" and
     # plays action sound.
     # 
     # Parameters:
     #   button to set Dizzy icon to.

     button.setIcon(ImageIcon(self.resources_directory + self.dizzy))
     self.status_label.setText(self.in_game_status)
     self.play_sound_safe(self.action_sound)

   
   def set_mario(self, button):

     # Draws Mario in a given button.
     #
     # Parameters:
     #   button to set Mario icon to.

     button.setIcon(ImageIcon(self.resources_directory + self.mario))
          
   def clicked1(self, event):

     # Event listener method for the button of the game at 0x0.
     #
     # Parameters:
     #  event Click event.

     if self.board[0][0] != ' ':
       return
     self.board[0][0] = 'X'
     self.set_dizzy(self.button1)
     self.computer_move()

   def clicked2(self, event):

     # Event listener method for the button of the game at 0x1.
     #
     # Parameters:
     #  event Click event.

     if self.board[0][1] != ' ':
       return
     self.board[0][1] = 'X'
     self.set_dizzy(self.button2)
     self.computer_move()
     
   def clicked3(self, event):

     # Event listener method for the button of the game at 0x2.
     #
     # Parameters:
     #  event Click event.

     if self.board[0][2] != ' ':
       return
     self.board[0][2] = 'X'
     self.set_dizzy(self.button3)
     self.computer_move()
     
   def clicked4(self, event):

     # Event listener method for the button of the game at 1x0.
     #
     # Parameters:
     #  event Click event.

     if self.board[1][0] != ' ':
       return
     self.board[1][0] = 'X'
     self.set_dizzy(self.button4)
     self.computer_move()

   def clicked5(self, event):

     # Event listener method for the button of the game at 1x1.
     #
     # Parameters:
     #  event Click event.

     if self.board[1][1] != ' ':
       return
     self.board[1][1] = 'X'
     self.set_dizzy(self.button5)
     self.computer_move()

   def clicked6(self, event):

     # Event listener method for the button of the game at 1x2.
     #
     # Parameters:
     #  event Click event.

     if self.board[1][2] != ' ':
       return
     self.board[1][2] = 'X'
     self.set_dizzy(self.button6)
     self.computer_move()

   def clicked7(self, event):

     # Event listener method for the button of the game at 2x0.
     #
     # Parameters:
     #  event Click event.

     if self.board[2][0] != ' ':
       return
     self.board[2][0] = 'X'
     self.set_dizzy(self.button7)
     self.computer_move()
     
   def clicked8(self, event):

     # Event listener method for the button of the game at 2x1.
     
     # Parameters:
     #  event Click event.

     if self.board[2][1] != ' ':
       return
     self.board[2][1] = 'X'
     self.set_dizzy(self.button8)
     self.computer_move()
     
   def clicked9(self, event):

     # Event listener method for the button of the game at 2x2.
     #
     # Parameters:
     #  event Click event.

     if self.board[2][2] != ' ':
       return
     self.board[2][2] = 'X'
     self.set_dizzy(self.button9)
     self.computer_move()
   
   # Makes the next move on the board on behalf of the computer.
   def computer_move(self):

     # first move optimization - always start in the middle if possible
     if self.board[1][1] == ' ':
       self.board[1][1] = '0'
       self.set_mario(self.buttons_mapped[1][1])
       self.test_state()
       return
     while self.has_empty_cell():
       y = random.randint(0, self.cells - 1)
       x = random.randint(0, self.cells - 1)
       if self.board[y][x] == ' ':
         self.board[y][x] = '0'
         self.set_mario(self.buttons_mapped[y][x])
         break
     self.test_state()

   def test_state(self):

     # Tests the board for a winning state.
     # If there is a winner then stops currently playing 
     # background sound, creates winning label, plays result 
     # sound and notifies/asks the user about continuation.

     if self.is_any_line_filled('X'):
        self.winner = self.dizzy # dizzy
     elif self.is_any_line_filled('0'):
        self.winner = self.mario # mario
     elif not self.has_empty_cell():
        self.winner = self.blank # tie
     if self.winner:
        label = 'Tie.'
        self.stop_playing_background()
        if self.winner == self.mario:
          label = 'You lose!'
          self.play_sound_safe(self.lose_sound)
        elif self.winner == self.dizzy:
          label = 'You won!'
          self.play_sound_safe(self.won_sound)
        else:
          self.play_sound_safe(self.tie_sound)
        self.notify_and_ask_about_continuation(label)
  
   def notify_and_ask_about_continuation(self, label):   

     # Shows modal window with the result of the game and asks the use whether they want to
     # continue the game. 
     # If user answers "Y" or "y" restarts the game.
     # If user answers "N" or "n" closes the game window and frees the resources.
     
     # Parameters:
     #   label Game result label.

     answer = None
     self.status_label.setText(label)
     while True:
       answer = str(requestString(label + "\r\n" + "Do you want to play again? (Y/N)"))
       if answer.lower() == "y":
         self.restart()
         break
       elif answer.lower() == "n":
         self.windowClosing(None)
         break
     
   def is_any_line_filled(self, character):

     # Checks the winning condition for the given character 'X' or '0'.
     #
     # Returns:
     #  Whether the given character 'X' or '0' has a winning line filled.

     is_row = self.is_row_filled(character)
     is_col = self.is_col_filled(character)
     is_d1 = self.is_diag_filled1(character)
     is_d2 = self.is_diag_filled2(character)
    
     return is_row or is_col or is_d1 or is_d2

   def has_empty_cell(self):

     #Checks if the game board contains an empty cell for the next move.
     #
     #Returns:
     #  Whether there is an empty cell on the board.

     for row in range(len(self.board)):
       for col in range(len(self.board)):
         if self.board[row][col] == ' ':
             return True
     return False

   def is_row_filled(self, color):

     # Check row win condition.
     #
     # Parameters:
     #   color (string) - color to check if the whole row of the same color
     # Returns:
     #   True (boolean) - if the whole row of the same color
     #   False (boolean) - if the row is not of the same color

     for row in range(len(self.board)):
       count = 0       
       for col in range(len(self.board)):
         if self.board[row][col] == color:
           count = count + 1
       if count == self.cells:
         return True
     return False

   def is_col_filled(self, color):

     #Check column win condition.
     #
     # Parameters:
     #   color (string) - color to check if the whole column of the same color
     # Returns:
     #   True (boolean) - if the whole column of the same color
     #   False (boolean) - if the column is not of the same color

     for col in range(len(self.board)):
       count = 0
       for row in range(len(self.board)):
         if self.board[row][col] == color:
           count = count + 1
       if count == self.cells:
         return True
     return False

   def is_diag_filled1(self, color):

     # Checks first diagonal win condition.
     #
     # Parameters:
     #   color (string) - color to check if the whole diagonal of the same color
     # Returns:
     #    True (boolean) - if the whole diagonal of the same color
     #    False (boolean) - if the diagonal is not of the same color

     count = 0       
     for idx in range(len(self.board)):
       if self.board[idx][idx] == color:
         count = count + 1
     return count == self.cells

   def is_diag_filled2(self, color):

     # Checks second diagonal win condition.
     # 
     # Parameters:
     #   color (string) - color to check if the whole diagonal of the same color
     # Returns:
     #    True (boolean) - if the whole diagonal of the same color
     #   False (boolean) - if the diagonal is not of the same color

     count = 0       
     for idx in range(len(self.board)):
       if self.board[idx][self.cells - 1 - idx] == color:
         count = count + 1
     return count == self.cells

   def play_sound_safe(self, sound):

     # Method tries to play given sound catching possible exceptions.
     # For example, if the sound wasn't found in resource directory
     #
     # Parameters:
     #    sound string with a file of a sound with leading slash '/'.
     # Returns:
     #    Created Sound object fromo makeSound.

     snd = None
     try:
       snd = makeSound(self.resources_directory + sound)
       play(snd)
     except:
       showError("Error while playing sound " + str(sound) + ".")
     return snd

   def windowClosing(self, event):

     # Method is invoked when a user closes game window or finishes playing.
     # It is the implementation of WindowAdapter interface.
     #
     # Parameters: final event from Swing/AWT

     self.stop_playing_background()
     self.buttons = []
     self.buttons_mapped = []
     self.button1 = None
     self.button2 = None
     self.button3 = None
     self.button4 = None
     self.button5 = None
     self.button6 = None
     self.button7 = None
     self.button8 = None
     self.button9 = None
     self.status_label = None
     self.frame.getContentPane().removeAll()
     self.frame.dispose()
     self.frame = None


   def choosePlayer(self):
     
     while true:
       
       select = requestString("You are against Mario. Choose Your Character: penguin chrome fox fish bird charizard sonic ")
       selection = select.lower()
     
       if selection == "penguin":
         return rpenguin
         break
       if selection == "chrome":
         return rchrome
         break
       if selection == "fox":
         return rfox
         break
       if selection == "fish":
         return rfish 
         break
       if selection == "bird":
         return rbird 
         break
       if selection == "charizard":
         return rcharizard 
         break
       if selection == "sonic":
         return rsonic 
         break
       
                           
def main():
  path = os.path.dirname(__file__)
  abs_path = os.path.abspath(path)   
  resources_dir = abs_path + "/RESOURCES"
  resources_files = [file for file in listdir(resources_dir) if isfile(join(resources_dir, file))]
  TicTacToeGame(resources_dir)
  
main()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     