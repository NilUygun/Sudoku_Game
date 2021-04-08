from tkinter import *
from tkinter import ttk, messagebox
import random

def startGame():
    tabs.select(gameScreen)

def howToPlayScreen():
    tabs.select(howToPlay)

def returnToMainMenu():
    tabs.select(startScreen)

# Create the buttons for a single 3 by 3 grid. 
def createMiniGrid(frame,column,row):
    miniGrid = []
    for i in range(3):
        columnList = []
        for j in range(3):
            button = Button(frame, text="0", font=("Helvetica", 12), height=2, width=4, bg="SystemButtonFace", command= lambda mainColumn=column, mainRow=row, miniColumn=i, miniRow=j: clickonAbutton(mainColumn, mainRow, miniColumn, miniRow))
            button.grid(row=j, column=i)
            columnList.append(button)
        miniGrid.append(columnList) 
    return miniGrid

def checkColumn():
    columns = [[],[],[],[],[],[],[],[],[]]
    wrongNumPositions = []
    
    # Makes a list that consists of numbers in each of the 9 main grid columns. 
    for column in range(3):
        for row in range(3):
            for miniColumn in range(3):
                for miniRow in range(3):
                    buttonNum = int(buttons[column][row][miniColumn][miniRow]["text"])
                    columnNum = column * 3 + miniColumn
                    columns[columnNum].append(buttonNum)
    
    # Loops through each value and position to find the duplicates. Adds the duplicates to the wrongNumPositions list. 
    for num in range(1,10):
        for i in range(9):
            pos = []
            for j in range(9):
                currentValue = columns[i][j]
                if currentValue == num:
                    wrongPosition = (i,j)
                    pos.append(wrongPosition)
            if len(pos)>1:
                for i in range(len(pos)):
                    wrongNumPositions.append(pos[i])
    
    # Uses row and column info to change the corresponding buttons' colours. 
    for wrongNum in wrongNumPositions:
        column = wrongNum[0]
        row = wrongNum[1]
        mainColumn = column//3
        miniColumn = column-(mainColumn*3)
        
        mainRow = row//3
        miniRow = row-(mainRow*3)
        buttons[mainColumn][mainRow][miniColumn][miniRow]["bg"] = "red"

def checkRow():
    wrongNumPositions = []
    rows = [[],[],[],[],[],[],[],[],[]]
    
    # Makes a list that consists of numbers in each of the 9 main grid rows. 
    for column in range(3):
        for row in range(3):
            for miniColumn in range(3):
                for miniRow in range(3):
                    buttonNum = int(buttons[column][row][miniColumn][miniRow]["text"])
                    rowNum = row * 3 + miniRow
                    rows[rowNum].append(buttonNum)

    # Loops through each value and position to find the duplicates. Adds the duplicates to the wrongNumPositions list. 
    for num in range(1,10):
        for i in range(9):
            pos = []
            for j in range(9):
                currentValue = rows[i][j]
                if currentValue == num:
                    wrongPosition = (j,i)
                    pos.append(wrongPosition)
            if len(pos)>1:
                for i in range(len(pos)):
                    wrongNumPositions.append(pos[i])
    
    # Uses row and column info to change the corresponding buttons' colours. 
    for wrongNum in wrongNumPositions:
        column = wrongNum[0]
        row = wrongNum[1]
        mainColumn = column//3
        miniColumn = column-(mainColumn*3)
        
        mainRow = row//3
        miniRow = row-(mainRow*3)
        buttons[mainColumn][mainRow][miniColumn][miniRow]["bg"] = "red"

def checkMiniGrid():
    # Loops through each miniGrid. 
    for column in range(3):
        for row in range(3):

            # Changes miniGrid list with the values that the user fills them with. 
            miniGridButtons = buttons[column][row]
            miniGrid = []
            wrongNumPositions = []

            for i in range(3):
                for j in range(3):
                    num = int(miniGridButtons[i][j]["text"])
                    miniGrid.append(num)
            
            # Loops through each value and position to find the duplicates. Adds the duplicates to the wrongNumPositions list. 
            for num in range(1,10):
                pos = []
                for j in range(9):
                    currentValue = miniGrid[j]
                    if currentValue == num:
                        wrongPosition = j
                        pos.append(wrongPosition)
                if len(pos)>1:
                    for i in range(len(pos)):
                        wrongNumPositions.append(pos[i])
            
            # Uses row and column info to change the corresponding buttons' colours. 
            for wrongNum in wrongNumPositions:
                miniColumn = wrongNum//3
                miniRow = wrongNum % 3
                buttons[column][row][miniColumn][miniRow]["bg"] = "red"

# Goes through each button: 
# from a main column to a main row in that main column (= one of the 9 frames)
# and finally to a button located at a given column and row at that frame
# Checks if the text of the button is blank. 
def isGridFull():
    for column in range(3):
        for row in range(3):
            for miniColumn in range(3):
                for miniRow in range(3):
                    buttonNum = buttons[column][row][miniColumn][miniRow]["text"]
                    if buttonNum == "":
                        return False
    return True

# If the grid is full, checks the grid for errors and highlights them with red.
# If not, displays an error message. 
def showAllErrors():
    isFull = isGridFull()
    if isFull == True:
        checkColumn()
        checkRow()
        checkMiniGrid()
    else:
        messagebox.showwarning("Warning"," The Sudoku grid is not full. \n Please fill in all the squares and try again!")

def areThereErrors():
    for column in range(3):
        for row in range(3):
            for miniGridColumn in range(3):
                for miniGridRow in range(3):
                    button = buttons[column][row][miniGridColumn][miniGridRow]
                    if button["bg"] == "red" or button["text"]=="":
                        return True
    return False

# Changes the colour of each red button to default grey.
# Shows the error (if any) when clicked on "Check".
# If there are no error, displays congrats message and asks the user if they want to play again.
def checkAll():
    for column in range(3):
        for row in range(3):
            for miniGridColumn in range(3):
                for miniGridRow in range(3):
                    button = buttons[column][row][miniGridColumn][miniGridRow]
                    if button["bg"] == "red":
                        button["bg"] = "SystemButtonFace"
    showAllErrors()
    error = areThereErrors()
    if error == False:
        yesorNo = messagebox.askquestion("Congratulations!"," You completed the Sudoku successfully. \n Do you want to try another one?")
        clearGrid()
        fillInGameGrid(emptySudokuNumbers[random.randint(0,len(emptySudokuNumbers))])
        if yesorNo == "no":
            returnToMainMenu()
    else:
        pass

# If the user clicks on a button and presses backspace, it clears the text of that button. 
# if pressed key is a number, it fills that square with that number. 
def pressAKey(event):
    try:
        button = buttons[selectedMainGridColumn][selectedMainGridRow][selectedMiniGridColumn][selectedMiniGridRow]
        pressedKey = event.char
        if event.keycode == 8 and button["bg"] != "lightgrey":
            button["text"] = ""
        int(pressedKey)
        if pressedKey != "0" and button["bg"] != "lightgrey":
            button["text"]=pressedKey
    except ValueError:
        pass

# Changes the colour of the button from light purple to default grey. 
def cleanGridColour():
    for column in range(3):
        for row in range(3):
            for miniGridColumn in range(3):
                for miniGridRow in range(3):
                    button = buttons[column][row][miniGridColumn][miniGridRow]
                    if button["bg"] == "#ccacf2":
                        button["bg"] = "SystemButtonFace"

# Changes the colour of the selected button into light purple if the button's background is not grey. 
def clickonAbutton(mainGridColumn, mainGridRow, miniGridColumn, miniGridRow):
    cleanGridColour()
    global selectedMainGridColumn, selectedMainGridRow, selectedMiniGridColumn, selectedMiniGridRow
    selectedMainGridColumn = mainGridColumn
    selectedMainGridRow = mainGridRow
    selectedMiniGridColumn = miniGridColumn
    selectedMiniGridRow =  miniGridRow
    button = buttons[selectedMainGridColumn][selectedMainGridRow][selectedMiniGridColumn][selectedMiniGridRow]
    if button["bg"] != "lightgrey":
        button["bg"]= "#ccacf2"

# Go to each button in the buttons list and change its text according to the emptySudokuGrids list. 
def fillInGameGrid(emptySudokuNumbers):
    for column in range(3):
        for row in range(3):
            for miniGridColumn in range(3):
                for miniGridRow in range(3):
                    buttons[column][row][miniGridColumn][miniGridRow]["text"] = emptySudokuNumbers[column][row][miniGridColumn][miniGridRow]
                    if emptySudokuNumbers[column][row][miniGridColumn][miniGridRow] != '':
                        buttons[column][row][miniGridColumn][miniGridRow]["bg"] = "lightgrey"

# Clears all the text and background colours of the buttons in the grid. 
def clearGrid():
    for column in range(3):
        for row in range(3):
            for miniColumn in range(3):
                for miniRow in range(3):
                    button = buttons[column][row][miniColumn][miniRow]
                    button["text"] = ""
                    button["bg"] = "SystemButtonFace"

selectedMainGridColumn = None
selectedMainGridRow = None
selectedMiniGridColumn = None
selectedMiniGridRow = None

# Create the main window. 
window = Tk()
window.title("Sudoku")
window.geometry("600x600")
window.bind('<Key>', pressAKey)

# Create the main menu and the Sudoku grid tab. 
tabs = ttk.Notebook(window)
gameScreen = Frame(tabs)
startScreen = Frame(tabs)
howToPlay = Frame(tabs)
tabs.add(startScreen, text= "Start")
tabs.add(gameScreen, text= "Sudoku Grid")
tabs.add(howToPlay, text= "How to Play")
tabs.pack(expand = True, fill = BOTH)
gameScreen.config(bg="#acf2eb")
startScreen.config(bg="#ccacf2")
howToPlay.config(bg="#ccacf2")

# Hide the tabs bar at the top. 
style = ttk.Style()
style.layout('TNotebook.Tab', [])

gameTitle = Label(startScreen, text="Sudoku")
gameTitle.config(font=("Helvetica", 30), bg="#ccacf2")
gameTitle.pack(expand = True)

welcome = Label(startScreen, font=("Helvetica", 18), text="Welcome to Sudoku!", bg="#ccacf2")
welcome.place(x=180, y=200)

myName = Label(startScreen, font=("Helvetica", 12), text="By Nil Uygun", bg="#ccacf2")
myName.place(x=255, y=340)

# Create buttons on the main menu. 
mainbuttonFrame = Frame(startScreen)
mainbuttonFrame.pack(expand = True)
mainbuttonFrame.config(bg="#ccacf2")

startButton = Button(mainbuttonFrame, text="Start!", height=1, width=7, command=startGame)
startButton.pack(side = LEFT, padx = 10)

howtoplayButton = Button(mainbuttonFrame, text="How to Play", height=1, width=15, command=howToPlayScreen)
howtoplayButton.pack(side = RIGHT)

# Create a return to Main Menu button for the How to Play tab. 
mainMenuButton = Button(howToPlay, text=("Main Menu"), height=1, width=10, command=returnToMainMenu)
mainMenuButton.place(x=400, y=400)

# Create a Check button for the Sudoku grid tab. 
checkButton = Button(gameScreen, text = "Check", height=1, width=8, command=checkAll)
checkButton.place(x=440, y=500)

# Create main menu button for the game tab. 
returnToMainMenuButton = Button(gameScreen, text = "Main Menu", height=1, width=10, command=returnToMainMenu)
returnToMainMenuButton.place(x=350, y=500)

# Create a label with instructions for How to Play tab. 
tabTitle = Label(howToPlay, bg="#ccacf2", font=("Helvetica", 16), text="How to Play")
instructions1 = Label(howToPlay, bg="#ccacf2", font=("Helvetica", 14), text="Click “Start!” to play. \n To fill in the Sudoku grid, \n click on a square and use the keyboard \n to type in the number you want.")
instructions2 = Label(howToPlay, bg="#ccacf2", font=("Helvetica", 14), text="When you are done, \n click on the “Check” button to view your score.")
tabTitle.place(x=230, y=100)
instructions1.place(x=120, y=150)
instructions2.place(x=90, y=300)

sudokuGridFrame = Frame(gameScreen)
sudokuGridFrame.pack()

# Create mini frames.
miniFrames = []
for i in range(3):
    columnOfFrames = []
    for column in range(3):
        gridFrame = Frame(sudokuGridFrame, highlightthickness=1, highlightbackground="black")
        columnOfFrames.append(gridFrame)
    miniFrames.append(columnOfFrames)

# Place the frames according to column and row info given. 
# miniFrames[0] = first column
for column in range(3):
    for row in range(3):
        miniFrames[column][row].grid(row=row, column=column)

# Goes through each frame and creates their buttons using the function createMiniGrid. 
buttons = [[0,0,0],[0,0,0],[0,0,0]]
for i in range(3): 
    for j in range(3):
        frame = miniFrames[i][j]
        miniGridButtons = createMiniGrid(frame,i,j)
        buttons[i][j]= miniGridButtons

# Make a list of numbers that will be written on sudoku grid buttons at the start of the game. 
emptySudokuNumbers = [[[[['', '', 4], ['', '', 6], [8, '', 9]], [[2, 3, ''], ['', '', 9], [4, 6, '']], [['', '', ''], [3, 4, ''], [2, '', 1]]], [[['', '', ''], [9, 5, ''], ['', '', 8]], [['', '', ''], ['', 8, ''], [7, '', 4]], [[8, '', ''], ['', 6, 4], [5, '', '']]], [[['', 7, 1], [6, 8, ''], ['', 9, 5]], [[6, '', ''], [9, '', 5], ['', '', 1]], [['', '', ''], ['', '', 2], [4, 3, '']]]],
[[[['', '', ''], [3, '', ''], ['', 4, '']], [[2, '', ''], [1, 5, 9], [3, 6, '']], [[3, '', ''], [4, '', ''], [1, 2, '']]], [[['', 3, ''], [2, '', ''], [5, '', 8]], [[4, 8, 2], [5, '', 1], ['', '', 3]], [['', '', 7], ['', 8, ''], [2, '', 4]]], [[['', '', ''], [9, 6, ''], ['', '', '']], [['', 3, ''], ['', '', ''], ['', 2, 6]], [['', '', ''], [7, 4, 2], [5, '', '']]]],
[[[['', 1, ''], [8, 3, 6], [7, '', '']], [['', '', ''], [1, '', ''], ['', 6, '']], [['', '', 9], ['', 7, 4], [1, 5, 3]]], [[[9, '', 3], [1, 6, ''], ['', 7, '']], [['', '', 1], ['', '', 2], ['', '', '']], [['', '', 5], ['', '', 7], [4, '', 1]]], [[['', '', 1], [4, '', ''], [3, '', '']], [['', '', ''], [9, '', ''], ['', '', 6]], [['', 3, 8], ['', '', 6], [5, '', 2]]]],
[[[[2, '', ''], ['', '', ''], ['', 4, '']], [[3, 4, 8], ['', '', ''], ['', '', 7]], [['', '', 9], ['', 4, 8], ['', 1, 5]]], [[['', '', 3], ['', 5, ''], ['', '', '']], [['', '', ''], ['', '', 2], [5, 9, '']], [[5, '', 7], [9, '', 4], ['', 6, 2]]], [[[5, '', 1], ['', '', 2], ['', 9, '']], [[8, '', ''], ['', '', 1], ['', '', 5]], [['', 9, 3], [4, 5, 6], ['', 2, 1]]]],
[[[['', 1, 5], ['', '', 7], ['', 4, 9]], [['', 4, 8], [1, '', 9], ['', '', '']], [[3, '', ''], ['', '', ''], ['', '', 5]]], [[['', 3, ''], [2, '', 4], ['', '', '']], [[4, '', ''], [6, '', 1], [5, 9, '']], [['', 8, ''], ['', '', 7], ['', '', 1]]], [[[4, '', 2], [1, 8, ''], ['', '', '']], [['', '', ''], ['', 2, 6], ['', '', '']], [['', '', 3], ['', '', 4], [8, 1, 2]]]]]

#randomGrid = random.randint(0, len(emptySudokuNumbers))
randomGrid = 0
fillInGameGrid(emptySudokuNumbers[randomGrid])

window.mainloop()