from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    create_cell_count_label = None
    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_obj = None
        self.x = x
        self.y = y
        
        #Append the obj to the Cell.all list
        Cell.all.append(self)
        
    def create_btn(self, location):
        btn = Button(
            location,
            width = 12,
            height = 4,
            
        )
        btn.bind('<Button-1>', self.left_click_action )#left click
        btn.bind('<Button-3>', self.right_click_action) #right click
        self.cell_btn_obj = btn
        
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg = 'black',
            fg='white',
            text = f'Cells Left:{Cell.cell_count}',
           # width =12,
           # height =4,
            font = ('', 25)
        )
        Cell.cell_count_label = lbl
     
    def left_click_action(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            #cancel events already open
        self.cell_btn_obj.unbind('<Button-1>')
        if Cell.cell_count == settings.MINES_COUNT:
            ctypes.windll.user32.MessageBoxW(0, 'YOU LOST!', 'GAME OVER', 0)
            
        
    def get_cell_by_axis(self, x,y):
        #Return a cel obj base on the value of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
            
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1 , self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y +1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        cells =[cell for cell in cells if cell is not None]
        return cells
    
    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter
    
    def show_cell(self):
       if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_obj.configure(text = self.surrounded_cells_mines_length)
        #Replace  the text of cell count label with the new count
            if Cell.cell_count_label:
                Cell.cell_count_label.configure(
                    text =f'Cells Left:{Cell.cell_count}'
                )
        
        #Mark the cell as opened
       self.is_opened = True
        
    def show_mine(self):
        #A logic to interrupt the game and say that player lost
        ctypes.windll.user32.MessageBoxW(0, 'YOU LOST!', 'GAME OVER', 0)
        sys.exit(0)
        self.cell_btn_obj.configure( bg = 'red')
        
        
        
    def right_click_action(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_obj.configure(
                bg = 'orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_obj.configure(
                bg = 'SystemButtonFace'
            )
            self.is_mine_candidate = False
            
    @staticmethod
    def randomize():
        picked_cells = random.sample( #selects to random cells
           Cell.all, settings.MINES_COUNT
        )
        for picked in picked_cells:
           picked.is_mine = True
       
    def __repr__(self):
        return f'Cell({self.x}, {self.y})'
    