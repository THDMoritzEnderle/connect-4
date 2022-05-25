from behave import given, when, then
import wexpect
from init import init

'''
Notes: Whenever you start a scenario, start with Given starting main.py in everything.feature to setup the environment
You can send a user input with context.child.sendline(Your command in String)
You can also expect a String from the console with context.child.expect(Expected String)
It is important for testing purposes that you setup the timer correctly. Right now we are using the timeout of 3.
If the timeout is not set correctly, it will stop behave for 2 minutes so please dont forget that.
Example: context.child.expect("Connect 4 Main Menu", timeout=3)

You can also debug behave.
I created a file called behave.ini which allows us to read printed statements.
To turn it on, just put both stderr_capture and stdout_capture to False.
(Tip: if you want to work on your scenario only without reading debugging messages from other scenarios,
comment every other scenario except yours in everything.feature with #. This make your scenario isolated.)
To print console or user input just use
print(context.child.before, end='')
print(context.child.after, end='')

-Johni
'''

'''
Btw, I also created a file called init.py where you can change your project directory more easier.
Just change the project_path variable.

-Johni
'''

@given('starting main.py')
def step_impl(context):
    # Start cmd as child process
    context.child = wexpect.spawn('cmd.exe')
    # Change into right directory
    cmd_commands = ["cd " + init.project_path, init.start_game]

    # Loops through cmd commands
    for command in cmd_commands:
        context.child.expect('>', timeout=3)
        context.child.sendline(command)
        print(context.child.before, end='')
        print(context.child.after, end='')

# Scenario: Starting the game and quitting
@when('the user selects Quit')
def step_impl(context):
    # Expecting from console and sending input
    context.child.expect('Please select an option: ', timeout=3)
    context.child.sendline('3')
    print(context.child.before, end='')
    print(context.child.after, end='')

@then('the game closes itself')
def step_impl(context):
    # Expecting Goodbye! from console
    context.child.expect('Goodbye!', timeout=3)
    print(context.child.before, end='')
    print(context.child.after, end='')

# Scenario: Starting the game and choosing 'Play Game'
@when('the user selects "Play Game"')
def step_impl(context):
    # Expects to be in main menu and gets into game mode menu
    context.child.expect('~Connect 4 Main Menu~', timeout=3)
    context.child.sendline('1')
    print(context.child.before, end='')
    print(context.child.after, end='')

@then('the user gets transferred to the next menu')
def step_impl(context,):
    # Expects to be in game mode menu
    context.child.expect('~Game Mode Selection Menu~', timeout=3)
    print(context.child.before, end='')
    print(context.child.after, end='')

# Scenario: Going back to the start menu
@when('the user is in the gamemode menu')
def step_impl(context):
    # Expecting to be in Main menu and going into gamemode menu
    context.child.expect('Please select an option: ', timeout=3)
    context.child.sendline('1')
    print(context.child.before, end='')
    print(context.child.after, end='')

@when('the user selects the <- back button')
def step_impl(context):
    # Selecting <- back button
    context.child.expect('Game Mode Selection Menu', timeout=3)
    context.child.sendline('4')
    print(context.child.before, end='')
    print(context.child.after, end='')

@then('the user gets transferred to the start menu')
def step_impl(context):
    # Expecting to be in main menu
    context.child.expect('Connect 4 Main Menu', timeout=3)
    print(context.child.before, end='')
    print(context.child.after, end='')

# Scenario: Quitting during game
@when('there is a game running')
def step_impl(context):
    # Sets up the game
    menu_selection = {'~Connect 4 Main Menu~': '1', 'Game Mode Selection Menu': '1'}

    # Goes through the menus to select 'Player vs Player'
    for expect, send in menu_selection.items():
        context.child.expect(expect, timeout=3)
        context.child.sendline(send)
        print(context.child.before, end='')
        print(context.child.after, end='')

    # In game
    context.child.expect('Which column do you want to place your checker?', timeout=3)
    print(context.child.before, end='')
    print(context.child.after, end='')

@when('the Quit button is selected')
def step_impl(context):
    # Selects quit button during game
    context.child.expect('Please select an option:', timeout=3)
    context.child.sendline('8')
    print(context.child.before, end='')
    print(context.child.after, end='')

@then('the game quits')
def step_impl(context):
    # Game should quit
    context.child.expect('You have chosen "quit"', timeout=3)
    print(context.child.before, end='')
    print(context.child.after, end='')

@then('the user will be asked if they want to save the game')
def step_impl(context):
    # User should be asked if they want to save the game
    context.child.expect('Do you want to save the current game?', timeout=3)
    print(context.child.before, end='')
    print(context.child.after, end='')

'''
@given('the user is in the gamemode menu')
@when('the user selects the "<- back" button')
@then('the user gets transferred to the start menu')


@given('the user is in the gamemode menu')
@when('the user selects "Player vs Player"')
@then('the selected gamemode starts')


@given('the Player selects column <columns>')
@when('the move is valid')
@then('a checker has to be in the lowest free row of the selected column')


@given('Player selects column <columns>')
@when('the move is invalid')
@then('the message "this column is already full!" appears as long as the input is invalid')


@given('two players play against each other')
@when('a player wins')
@then('there is a congratulation message')
@then('the user can return back to the main menu')


@given('two players play against each other')
@when('the board is full')
@when('no one has won')
@then('the message "The game is a draw!" appears')
@then('the user can return back to the main menu')


@given('there is a game running')
@when('the "quit" button is selected')
@then('the user will be asked if they want to save the game')
'''
