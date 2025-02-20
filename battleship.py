"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["bsize"] = 500
    data["csize"] = data["bsize"] / data["rows"]
    data["noofships"] = 5
    data["userboard"] = emptyGrid(data["rows"], data["cols"])
    #data["userboard"] = test.testGrid()
    data["pcboard"] = addShips(emptyGrid(data["rows"], data["cols"]), data["noofships"])
    data["tempship"] = []
    data["usertrack"] = 0
    data["winnertrack"] = None
    data["maxturn"] = 50
    data["currentturn"] = 0
    return 


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userboard"], True)
    drawShip(data, userCanvas, data["tempship"])
    drawGrid(data, compCanvas, data["pcboard"], False)
    drawGameOver(data, userCanvas)
    return 


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.kesym == "Return":
        makeModel(data)


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winnertrack"] != None:
        return 
    p = getClickedCell(data,event)
    if board == "user":
        clickUserBoard(data, p[0], p[1])
    else:
        runGameTurn(data, p[0], p[1])
    return 

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = [[EMPTY_UNCLICKED] * cols for i in range(rows)]
    return grid

'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row,col = random.randint(1,8), random.randint(1,8)
    edge = random.randint(0, 1) 
    ship1 = []
    if edge == 1:
        for row in range(row-1, row+2):
            ship1.append([row, col])#vertical
    elif edge == 0:#Horizontal
        for col in range(col-1, col+2):
            ship1.append([row, col])
    return ship1
'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in ship:           
        if grid[i[0]][i[1]] != EMPTY_UNCLICKED:
            return False
    return True

'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):   
    count = 0
    while count < numShips:
        ship2 = createShip()
        if checkShip(grid, ship2):
            for i in range(len(ship2)):
                grid[ship2[i][0]][ship2[i][1]] = SHIP_UNCLICKED
            count += 1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(data["rows"]):
        for col in range(data["cols"]):
            if grid[row][col] == SHIP_UNCLICKED:
                canvas.create_rectangle(data["csize"] * col, data["csize"] * row, data["csize"] * (col+1), data["csize"] * (row+1), fill = "yellow")
            elif grid[row][col] == EMPTY_UNCLICKED:
                canvas.create_rectangle(data["csize"] * col, data["csize"] * row, data["csize"] * (col+1), data["csize"] * (row+1), fill = "blue")
            elif grid[row][col] == SHIP_CLICKED:
                canvas.create_rectangle(data["csize"] * col, data["csize"] * row, data["csize"] * (col+1), data["csize"] * (row+1), fill = "red")
            elif grid[row][col] == EMPTY_CLICKED:
                canvas.create_rectangle(data["csize"] * col, data["csize"] * row, data["csize"] * (col+1), data["csize"] * (row+1), fill = "white")
            if (grid[row][col] == SHIP_UNCLICKED) and (showShips == False):
                canvas.create_rectangle(data["csize"] * col, data["csize"] * row, data["csize"] * (col+1), data["csize"] * (row+1), fill = "blue")
    return data


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if (ship[0][1] == ship[1][1] == ship[2][1]) and (ship[0][0] + 1 == ship[1][0] == ship[2][0] - 1):
        return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if (ship[0][0] == ship[1][0] == ship[2][0]) and (ship[0][1] + 1 == ship[1][1] == ship[2][1] - 1):
        return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x, y = int(event.x / data["csize"]) , int(event.y / data["csize"])
    return [y,x]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in ship:
        canvas.create_rectangle(data["csize"] * (i[1]) , data["csize"] * (i[0]), data["csize"] * (i[1]+1), data["csize"] * (i[0]+1), fill = "white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship) == 3:
        if checkShip(grid, ship) and (isVertical(ship) or isHorizontal(ship)):
            return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["userboard"],data["tempship"]):
        for i in range(len(data["tempship"])):
                data["userboard"][data["tempship"][i][0]][data["tempship"][i][1]] = SHIP_UNCLICKED
        data["usertrack"] +=1
    else:
        print("Ship is not valid")
    data["tempship"] = []

    return 


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["usertrack"] == 5:
        print("You can start the game")
        return 
    for i in data["tempship"]:
        if [row,col] == i:
            return 
    data["tempship"].append([row,col])
    if len(data["tempship"]) == 3:
        placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED:
        board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["winnertrack"] = player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if (data["pcboard"][row][col] == SHIP_CLICKED) or (data["pcboard"][row][col] == EMPTY_CLICKED) :
        return
    else:
        updateBoard(data, data["pcboard"], row, col, "user")
    #getting the computer guesses
    x = getComputerGuess(data["userboard"])
    #calling updateboard function with values of getcomputerguesses
    updateBoard(data, data["userboard"], x[0], x[1], "comp")
    data["currentturn"] +=1
    if data["currentturn"] == data["maxturn"] :
        data["winnertrack"] = "draw"

'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    #generating random row,col values
    row,col = random.randint(0,9),random.randint(0,9)
    #checking the condition the cells are clicked, if clicked it generates random row,col values.Executes until row,col are unclicked indexes
    while (board[row][col] == EMPTY_CLICKED or board[row][col] == SHIP_CLICKED):
        row,col = random.randint(0,9), random.randint(0,9)
    #if row,col are unclicked indexes return row,col in a list
    if (board[row][col] == EMPTY_UNCLICKED) or (board[row][col] == SHIP_UNCLICKED) :
        return [row, col]
    return


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == SHIP_UNCLICKED:
                return False
    return True
'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winnertrack"] == "user" :
        canvas.create_text(300,50, text ="Congratulations", fill = "dark red", font = ("Georgia 20 bold"))
        canvas.create_text(300,200, text ="Press Enter to play again", fill = "dark red", font = ("Georgia 20 bold"))

    elif data["winnertrack"] == "comp" :
        canvas.create_text(300,50, text = "You lost the game", fill = "dark red", font = ("Georgia 20 bold"))
        canvas.create_text(300,200, text ="Press Enter to play again", fill = "dark red", font = ("Georgia 20 bold"))
    elif data["winnertrack"] == "draw" :
        canvas.create_text(300,50, text = "Out of moves,it's a draw", fill = "dark red", font = ("Georgia 20 bold"))
        canvas.create_text(300,200, text ="Press Enter to play again", fill = "dark red", font = ("Georgia 20 bold"))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)