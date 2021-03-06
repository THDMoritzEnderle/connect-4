Feature: A game of connect-4
Scenario: Starting the game and quitting
  Given starting main.py
   When the user selects "Quit"
   Then the game closes itself

Scenario: Starting the game and choosing 'Play Game'
   Given starting main.py
   When the user selects "Play Game"
   Then the user gets transferred to the next menu

Scenario: Going back to the start menu
   Given starting main.py
   When the user is in the gamemode menu
   When the user selects the back button
   Then the user gets transferred to the start menu

Scenario: Selecting 'Player vs Player'
   Given starting main.py
   When the user selects "Play Game"
   And the user selects "Player vs Player"
   Then the selected gamemode starts

Scenario: Player's turn is valid
   Given starting main.py
   When the user selects "Play Game"
   And the user selects "Player vs Player"
   And the player selects column 1
   Then the move is valid

Scenario: Player's turn is invalid
   Given starting main.py
   When there is a game running
   And player makes invalid move
   Then a message will appear which says that the move is invalid
   And the game asks for a new input

Scenario: Player wins
   Given starting main.py
   When there is a game running
   And a player wins
   Then there is a congratulation message
   And the user can return back to the main menu

Scenario: Draw
   Given starting main.py
   When there is a game running
   And the board is full
   Then the message "The game is a draw!" appears
   And the user can return back to the main menu

Scenario: Quitting during game
   Given starting main.py
   When there is a game running
   And the quit button is selected
   Then the game quits
   And the user will be asked if they want to save the game

Scenario: Looking at the Rules
   Given starting main.py
   When the user presses rules
   Then the rules appears
   And when the user presses enter, he is back to the main menu

Scenario: A game vs AI
   Given starting main.py
   When the user selects "Player vs AI"
   Then plays a game vs AI and looses

Scenario: Testing 5 moves
   Given starting main.py
   When the user selects "Play Game"
   And the user selects "Player vs Player"
   And the player selects column 2
   And the player selects column 2
   And the player selects column 3
   And the player selects column 4
   And the player selects column 5
   Then its player 2 turn.
