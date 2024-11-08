import itertools
import random


class Minesweeper():


    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):

        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):


        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):

        return self.mines_found == self.mines


class Sentence():


    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):

        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):

        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):

        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):

        self.moves_made.add(cell)
        self.safes.add(cell)
        Undetermined_cells = []
        count_mines = 0
        for i in range(cell[0] -1 ,cell[0]+2):
            for j in range(cell[1]-1,cell[1]+2):
                if (i,j) in self.mines:
                    count_mines+=1
                if 0<= i <self.height and 0<= j < self.width and (i,j) not in self.safes and (i,j) not in self.mines:
                    Undetermined_cells.append((i,j))
        newSentence = Sentence(Undetermined_cells,count-count_mines)
        self.knowledge.append(newSentence)
        for sentence in self.knowledge:
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)
        for sentence in self.knowledge:
            if newSentence.cells.issubset(sentence.cells) and sentence.count> 0 and newSentence.count > 0 and newSentence!= sentence:
                new_subset = sentence.cells.difference(newSentence.cells)
                new_subset_sentence = Sentence(list(new_subset),sentence.count-newSentence.count)
                self.knowledge.append(new_subset_sentence)














    def make_safe_move(self):

        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):

        possibleMoves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    possibleMoves.append((i,j))
        if len(possibleMoves)!=0:
            return random.choice(possibleMoves)
        else:
            return None
