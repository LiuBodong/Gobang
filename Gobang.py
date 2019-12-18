from tkinter import *
from tkinter.messagebox import *
from enum import Enum
import sys

class Piece(Enum):
    White = 1
    Black = 2
    NotDefiend = 3

class Gobang:
    def __init__(self):
        """
        初始化
        """
        self.__root = Tk()
        self.__root.title("Gobang")
        self.__width = 15
        self.__height = 15
        self.__radius = 30
        self.__w = (self.__width) * self.__radius * 2
        self.__h = (self.__height) * self.__radius * 2
        self.__root.geometry("{}x{}".format(self.__w, self.__h))
        self.__canvas = Canvas(self.__root, width=self.__w, height=self.__h)
        self.__last_x = -1
        self.__last_y = -1
        self.__last_point = None
        self.__color = Piece.White
        self.__pieces = [[Piece.NotDefiend for y in range(0, self.__height)] for x in range(0, self.__width)]
        
        
    def __draw_lines(self):
        """
        画棋盘
        """
        for x in range(0, self.__width):
            self.__canvas.create_line(self.__radius + x * self.__radius * 2, 
                                      self.__radius, 
                                      self.__radius + x * self.__radius * 2,
                                      self.__radius + (self.__height - 1) * self.__radius * 2)
        for y in range(0, self.__height):
            self.__canvas.create_line(self.__radius, 
                                      self.__radius + y * self.__radius * 2, 
                                      self.__radius + (self.__width - 1) * self.__radius * 2,
                                      self.__radius + y * self.__radius * 2)

    def __get_current_position(self, x, y):
        """
        根据当前鼠标位置计算棋子位置
        """    
        selected_x = max(0, min(int(x / (self.__radius * 2)), self.__width - 1))
        selected_y = max(0, min(int(y / (self.__radius * 2)), self.__height - 1))
        return (selected_x, selected_y)

    def __color_continius(self, arr, color):
        """
        判断某一颜色的棋子最大连续个数
        """
        max_count = 1
        _count = 1
        for i in range(0, len(arr) - 1):
            x1, y1 = arr[i]
            x2, y2 = arr[i + 1]
            if self.__pieces[x1][y1] == color and self.__pieces[x2][y2] == color:
                _count += 1
            else:
                _count = 1
            if _count >= max_count:
                    max_count = _count
        return max_count
            
    def __check_win(self, selected_x, selected_y, color):
        """
        判断某一颜色棋子的输赢，以当前棋子为中心，4子为半径判断四个方向即可
        """
        _row = []
        for x in range(selected_x - 4, selected_x + 5):
            if x >= 0 and x < self.__width:
                _row.append((x, selected_y))
        if self.__color_continius(_row, color) >= 5:
            return True
        _col = []
        for x in range(selected_y - 4, selected_y + 5):
            if x >= 0 and x < self.__height:
                _col.append((selected_x, x))
        if self.__color_continius(_col, color) >= 5:
            return True
        lb_rt = []
        for x in range(-4, 5):
            s_x = selected_x + x
            s_y = selected_y - x
            if s_x >= 0 and s_x < self.__width and s_y > 0 and s_y < self.__height:
                lb_rt.append((s_x, s_y))
        if self.__color_continius(lb_rt, color) >= 5:
            return True
        lt_rb = []
        for x in range(-4, 5):
            s_x = selected_x + x
            s_y = selected_y + x
            if s_x >= 0 and s_x < self.__width and s_y > 0 and s_y < self.__height:
                lt_rb.append((s_x, s_y))
        if self.__color_continius(lt_rb, color) >= 5:
            return True
        return False

    def __is_draw(self):
        """
        判断是否是和棋
        """
        is_draw = True
        for x in self.__pieces:
            for y in x:
                if y == Piece.NotDefiend:
                    is_draw = False
        return is_draw

    def __bind_mouse_functions(self):
        """
        绑定鼠标事件
        """
        def move_handler(event):
            """
            鼠标移过棋盘，显示棋子
            """
            selected_x, selected_y = self.__get_current_position(event.x, event.y)
            color = "black" if self.__color == Piece.Black else "white"
            if selected_x != self.__last_x or selected_y != self.__last_y:
                self.__canvas.delete(self.__last_point)
                self.__last_point = self.__canvas.create_oval(self.__radius + selected_x * self.__radius * 2 - self.__radius,
                                                              self.__radius + selected_y * self.__radius * 2 - self.__radius,
                                                              self.__radius + selected_x * self.__radius * 2 + self.__radius,
                                                              self.__radius + selected_y * self.__radius * 2 + self.__radius,
                                                              fill=color)
                self.__last_x = selected_x
                self.__last_y = selected_y
         
        def click_handler(event):
            """
            鼠标点击棋盘，落子并判断输赢
            """
            selected_x, selected_y = self.__get_current_position(event.x, event.y)
            if self.__pieces[selected_x][selected_y] != Piece.NotDefiend:
                # 棋子已经存在，不可落子
                pass
            else:
                self.__pieces[selected_x][selected_y] = self.__color
                color = "black" if self.__color == Piece.Black else "white"
                self.__canvas.create_oval(self.__radius + selected_x * self.__radius * 2 - self.__radius,
                                              self.__radius + selected_y * self.__radius * 2 - self.__radius,
                                              self.__radius + selected_x * self.__radius * 2 + self.__radius,
                                              self.__radius + selected_y * self.__radius * 2 + self.__radius,
                                              fill=color)
                if self.__is_draw():
                    message = "draw chess!"
                    showinfo("Info", message)
                    self.__reset()
                elif self.__check_win(selected_x, selected_y, self.__color):
                    message = "{} win!".format(color)
                    showinfo("Info", message)
                    self.__reset()
                if self.__color == Piece.White:
                    self.__color = Piece.Black
                else:
                    self.__color = Piece.White

        self.__canvas.bind('<Motion>', move_handler)
        self.__canvas.bind('<Button-1>', click_handler)

    def __reset(self):
        """
        重置游戏
        """
        self.__canvas.quit()
        self.__root.quit()
        self.__root.destroy()
        self.__init__()
        self.start()

    def start(self):
        self.__canvas.pack()
        self.__draw_lines()
        self.__bind_mouse_functions()
        self.__root.mainloop()

if __name__ == "__main__":
    gobang = Gobang()
    gobang.start()
