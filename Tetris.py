import pygame
import os
import json
import random
from pygame.locals import *

configFileName = 'config.json'
errorsLogFileName = 'error.log'

if os.path.exists(configFileName):
    with open(configFileName, 'r') as configFile:
        try:
            configData = json.load(configFile)
            screenWidth = configData['screenWidth']
            screenHeight = configData['screenHeight']
            tableWidth = configData['tableWidth']
            tableHeight = configData['tableHeight']
            tableColumns = configData['tableColumns']
            tableRows = configData['tableRows']
            showNext = configData['showNext']
            showGrid = configData['showGrid']
            fullScreen = configData['fullScreen']
            startingSpeed = configData['startingSpeed']
        except:
            quit('Error in Read Config File ...')
else:
    configDict = {'screenWidth': 800, 'screenHeight': 600, 'showNext': 1, "tableColumns": 10, "tableRows": 21,
                  "tableWidth": 300, "tableHeight": 500, "startingSpeed": 0.8, 'showGrid': 1, 'fullScreen': 0}
    screenWidth = configDict['screenWidth']
    screenHeight = configDict['screenHeight']
    tableWidth = configDict['tableWidth']
    tableHeight = configDict['tableHeight']
    tableColumns = configDict['tableColumns']
    tableRows = configDict['tableRows']
    showNext = configDict['showNext']
    showGrid = configDict['showGrid']
    fullScreen = configDict['fullScreen']
    startingSpeed = configDict['startingSpeed']
    with open(configFileName, 'w') as configFile:
        json.dump(configDict, configFile)

if os.path.exists(errorsLogFileName):
    try:
        os.remove(errorsLogFileName)
    except:
        print('Error file could not be deleted!\n')

middleScreenWidth = int(screenWidth / 2)
middleScreenHeight = int(screenHeight / 2)
tableLeft = middleScreenWidth - int(tableWidth / 2)
tableRight = middleScreenWidth + int(tableWidth / 2)
tableTop = middleScreenHeight - int(tableHeight / 2)
tableBottom = middleScreenHeight + int(tableHeight / 2)
tableMiddle = tableLeft + int(tableWidth / 2)
gridWidth = int(tableWidth / tableColumns)
gridHeight = int(tableHeight / tableRows)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

colorList = [
    BLACK,
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
    (180, 134, 122)
]


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GridPosition(Position):
    def __init__(self, x, y, grid_color):
        super().__init__(x, y)
        self.color = grid_color


class Object:
    def __init__(self, position, state):
        self.position = position
        self.lastPosition = None
        self.state = state


class Shape(Object):
    shapeList = [
        # O, J, L, I, T, Z, S
        # I Piece
        [
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        ],
        # J Piece
        [
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 0]
            ]
        ],
        # L Piece
        [
            [
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1]
            ],
            [
                [0, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 1, 0, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 1, 1, 1],
                [0, 0, 0, 0]
            ]
        ],
        # O Piece
        [
            [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]
            ]
        ],
        # S Piece
        [
            [
                [0, 0, 0, 0],
                [0, 0, 1, 1],
                [0, 1, 1, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0]
            ]
        ],
        # T Piece
        [
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 0]
            ]
        ],
        # Z Piece
        [
            [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0]
            ]
        ],
    ]

    def __init__(self, position=Position(int(tableColumns / 2), -1), state=0, shape_no=None):
        super().__init__(position, state)
        if shape_no is None:
            shape_no = int(random.random() * 7)
        self.shape = self.shapeList[shape_no]
        self.shapeNo = shape_no
        self.color = colorList[shape_no + 1]
        self.fillNo = shape_no + 1
        self.hardDrop = False

    def get_shape(self):
        return self.shape[self.state]

    def change_state(self):
        self.state += 1
        if self.state >= len(self.shape):
            self.state -= len(self.shape)

    def reverse_state(self):
        self.state -= 1
        if self.state < 0:
            self.state += len(self.shape)

    def move_right(self):
        self.lastPosition = self.position
        self.position.x += 1

    def move_left(self):
        self.lastPosition = self.position
        self.position.x -= 1

    def move_down(self):
        self.lastPosition = self.position
        self.position.y += 1

    def move_back_down(self):
        self.position.y -= 1

    def hard_drop(self):
        self.hardDrop = True


class PyGameHelper:
    __instance = None
    surface = None
    size = 480, 270
    width = 480
    height = 270
    font = None

    @staticmethod
    def get_instance():
        if PyGameHelper.__instance is None:
            PyGameHelper()
        return PyGameHelper.__instance

    def __init__(self):
        if PyGameHelper.__instance is not None:
            raise Exception("Error 101")
        else:
            PyGameHelper.__instance = self
            pygame.init()

    def create_surface(self):
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        return self.surface

    @staticmethod
    def set_window_name(window_name):
        pygame.display.set_caption(window_name)

    def set_size(self, width, height):
        self.size = self.width, self.height = width, height
        self.create_surface()

    def set_font(self, font_name='freesansbold.ttf', size=14):
        self.font = pygame.font.Font(font_name, size)

    def add_text(self, text, position=(0, 0), text_color=WHITE):
        if not self.font:
            self.set_font()
        render_text = self.font.render(str(text), True, text_color)
        self.surface.blit(render_text, position)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_rectangle(self, rect_color, rect_left, rect_top, rect_width, rect_height, width=0):
        rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)
        pygame.draw.rect(self.surface, rect_color, rect, width)

    def draw_line(self, line_color, start_pos, end_pos, width=1):
        pygame.draw.line(self.surface, line_color, start_pos, end_pos, width)

    def draw_horizontal_line(self, line_color, y_coord, x_start, x_end, width=1):
        self.draw_line(line_color, (x_start, y_coord), (x_end, y_coord), width)

    def draw_vertical_line(self, line_color, x_coord, y_start, y_end, width=1):
        self.draw_line(line_color, (x_coord, y_start), (x_coord, y_end), width)

    def fill_with_color(self, fill_color, rect=None, special_flags=0):
        self.surface.fill(fill_color, rect, special_flags)

    @staticmethod
    def get_rect(rect_left, rect_top, rect_width, rect_height):
        return pygame.Rect(rect_left, rect_top, rect_width, rect_height)

    @staticmethod
    def get_events():
        return pygame.event.get()


class Tetris:

    def __init__(self, name):
        self.gameOver = False
        self.occupied = []
        self.occupied_color = {}
        self.gameName = name
        self._running = True
        self._display_surf = None
        self.helperInstance = PyGameHelper()
        self.helperInstance.set_size(screenWidth, screenHeight)
        self.tableMatrix = []
        self.clock = pygame.time.Clock()
        self.time = 0
        self.speed = startingSpeed
        self.level = 1
        self.score = 0
        self.current_piece = self.get_piece()
        self.next_piece = self.get_piece()

    def on_init(self):
        self._display_surf = self.helperInstance.create_surface()
        self.helperInstance.set_window_name(self.gameName)
        self._running = True
        self.helperInstance.fill_with_color(GRAY)
        self.helperInstance.update()
        self.free_table()
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_piece.change_state()
                if not self.check_piece():
                    self.current_piece.reverse_state()
            if event.key == pygame.K_DOWN:
                self.move_down()
            if event.key == pygame.K_LEFT:
                self.current_piece.move_left()
                if not self.check_piece():
                    self.current_piece.move_right()
            if event.key == pygame.K_RIGHT:
                self.current_piece.move_right()
                if not self.check_piece():
                    self.current_piece.move_left()
            if event.key == pygame.K_SPACE:
                self.current_piece.hard_drop()

    def free_table(self):
        for y in range(tableRows):
            self.tableMatrix.append(list())
            for x in range(tableColumns):
                self.tableMatrix[y].append(0)
                self.tableMatrix[y][x] = 0

    def on_loop(self):
        self.draw_table()

    def on_render(self):
        self.helperInstance.update()

    def draw_table(self):
        for y in range(tableRows):
            for x in range(tableColumns):
                self.helperInstance.draw_rectangle(colorList[self.tableMatrix[y][x]], tableLeft + x * gridWidth,
                                                   tableTop + y * gridHeight, gridWidth, gridHeight)
                # if self.tableMatrix[y][x] == 0:
                #     self.helperInstance.draw_rectangle(BLACK, tableLeft + x * gridWidth, tableTop + y * gridHeight,
                #                                        gridWidth, gridHeight)
                # else:
                #     self.helperInstance.draw_rectangle(colorList[self.tableMatrix[y][x]], tableLeft + x * gridWidth,
                #                                        tableTop + y * gridHeight,
                #                                        gridWidth, gridHeight)
        self.draw_table_borders()
        self.draw_free_table()
        self.draw_piece()

    def draw_table_borders(self):
        self.helperInstance.draw_vertical_line(WHITE, tableLeft, tableTop, tableBottom, 2)
        self.helperInstance.draw_vertical_line(WHITE, tableRight, tableTop, tableBottom, 2)
        self.helperInstance.draw_horizontal_line(WHITE, tableTop, tableLeft, tableRight, 2)
        self.helperInstance.draw_horizontal_line(WHITE, tableBottom, tableLeft, tableRight, 2)

    def draw_piece(self):
        empty_rows_count = 0
        empty_cols_count = 0
        empty_row = True
        empty_col = True
        shape = self.current_piece.get_shape()
        for firstCounter in range(4):
            for secondCounter in range(4):
                if shape[firstCounter][secondCounter] == 0:
                    if (self.current_piece.position.y + firstCounter - empty_rows_count) < tableRows and (
                            self.current_piece.position.x + secondCounter - empty_cols_count) < tableColumns and self.check_position(
                        Position(self.current_piece.position.x + secondCounter - empty_cols_count,
                                 self.current_piece.position.y + firstCounter - empty_rows_count)):
                        self.tableMatrix[(self.current_piece.position.y + firstCounter - empty_rows_count)][
                            (self.current_piece.position.x + secondCounter - empty_cols_count)] = 0
                if shape[firstCounter][secondCounter] != 0:
                    # empty_col = False
                    # self.helperInstance.draw_rectangle(self.current_piece.color, tableLeft + (self.current_piece.position.x +
                    #                                    secondCounter - empty_cols_count + 1 ) * gridWidth, tableTop + (self.current_piece.position.y +
                    #                                    firstCounter - empty_rows_count + 1) * gridHeight, gridWidth, gridHeight)
                    # if self.current_piece.lastPosition:
                    #     self.tableMatrix[(self.current_piece.lastPosition.y + firstCounter - empty_rows_count)][(self.current_piece.lastPosition.x + secondCounter - empty_cols_count )] = 0

                    # if (self.current_piece.position.y + firstCounter - empty_rows_count) < tableRows and (self.current_piece.position.x + secondCounter - empty_cols_count ) < tableColumns:
                    #     self.tableMatrix[(self.current_piece.position.y + firstCounter - empty_rows_count)][(self.current_piece.position.x + secondCounter - empty_cols_count )] = self.current_piece.fillNo
                    if (self.current_piece.position.y + firstCounter - empty_rows_count) < tableRows and (
                            self.current_piece.position.x + secondCounter - empty_cols_count) < tableColumns and self.check_position(
                        Position(self.current_piece.position.x + secondCounter - empty_cols_count,
                                 self.current_piece.position.y + firstCounter - empty_rows_count)):
                        self.tableMatrix[(self.current_piece.position.y + firstCounter - empty_rows_count)][(
                                self.current_piece.position.x + secondCounter - empty_cols_count)] = self.current_piece.fillNo
                if shape[secondCounter][firstCounter] != 0:
                    empty_row = False
                    # self.helperInstance.draw_rectangle(self.current_piece.color, tableLeft + (self.current_piece.position.x +
                    #                                    firstCounter - empty_cols_count + 1) * gridWidth, tableTop + (self.current_piece.position.y +
                    #                                    secondCounter - empty_rows_count + 1) * gridHeight, gridWidth, gridHeight)
                    # if (self.current_piece.position.y + firstCounter - empty_rows_count + 1) < tableRows and (self.current_piece.position.x + secondCounter - empty_cols_count + 1 ) < tableColumns:
                    #     self.tableMatrix[(self.current_piece.position.y + firstCounter - empty_rows_count + 1)][(self.current_piece.position.x + secondCounter - empty_cols_count + 1 )] = self.current_piece.fillNo

            # if empty_row:
            #     empty_rows_count += 1
            # if empty_col:
            #     empty_cols_count += 1

    def draw_next_piece(self):
        for y in range(6):
            for x in range(6):
                self.helperInstance.draw_rectangle(BLACK, tableRight + 50 + x * gridWidth,
                                                   tableTop + y * gridHeight, gridWidth, gridHeight)
        next_shape = self.next_piece.get_shape()
        for y in range(4):
            for x in range(4):
                if next_shape[y][x] != 0:
                    self.helperInstance.draw_rectangle(self.next_piece.color, tableRight + 50 + (x + 1) * gridWidth,
                                                       tableTop + (y + 1) * gridHeight, gridWidth, gridHeight)

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False

        self.draw_next_piece()
        self.score_level()

        while self._running:
            if not self.gameOver:
                self.time += self.clock.get_rawtime()
                self.clock.tick()
                if self.current_piece.hardDrop:
                    self.time -= 0
                    self.move_down()
                elif self.time > self.speed * 1000:
                    self.time -= self.speed * 1000
                    self.move_down()

                for event in self.helperInstance.get_events():
                    self.on_event(event)
                self.on_loop()
                self.on_render()
            elif self.gameOver:
                self.helperInstance.add_text('Game Over!', (middleScreenWidth, middleScreenHeight), (255, 0, 0))
                for event in self.helperInstance.get_events():
                    self.on_event(event)
                self.on_render()
        self.on_cleanup()

    @staticmethod
    def get_piece():
        return Shape()

    def check_position(self, position):
        # if position.x < 0 and position.x >= tableColumns and 0 > position.y and position.y >= tableRows and position.y >= len(
        #         self.tableMatrix) and position.x >= len(self.tableMatrix[position.y]) and (
        #         position in self.occupied):
        #     return False
        # return True
        if 0 <= position.x < tableColumns and 0 <= position.y < tableRows and not (
                (position.x, position.y) in self.occupied):
            return True
        return False

    def draw_free_table(self):
        for y in range(tableRows):
            for x in range(tableColumns):
                if (x, y) not in self.occupied:
                    self.tableMatrix[y][x] = 0

    def check_piece(self):
        shape = self.current_piece.get_shape()
        for firstCounter in range(4):
            for secondCounter in range(4):
                if shape[firstCounter][secondCounter] != 0:
                    if not self.check_position(Position(self.current_piece.position.x + secondCounter,
                                                        self.current_piece.position.y + firstCounter)):
                        return False
        return True

    def hit(self):
        self.occupy()
        self.go_next_piece()
        self.remove_line()
        self.is_game_over()

    def occupy(self):
        shape = self.current_piece.get_shape()
        for y in range(4):
            for x in range(4):
                if shape[y][x] != 0:
                    self.occupied.append((self.current_piece.position.x + x, self.current_piece.position.y + y))
                    self.occupied_color[(
                        self.current_piece.position.x + x,
                        self.current_piece.position.y + y)] = self.current_piece.color

    def go_next_piece(self):
        self.current_piece = self.next_piece
        self.current_piece.position = Position(int(tableColumns / 2), -1)
        self.current_piece.hardDrop = False
        self.next_piece = self.get_piece()
        self.draw_next_piece()

    def is_hit(self):
        shape = self.current_piece.get_shape()
        for firstCounter in range(4):
            for secondCounter in range(4):
                if shape[firstCounter][secondCounter] != 0:
                    if self.current_piece.position.y + firstCounter == tableRows - 1 or (
                            self.current_piece.position.x + secondCounter,
                            self.current_piece.position.y + firstCounter + 1) in self.occupied:
                        return True
        return False

    def remove_line(self):
        current_line = tableRows - 1
        is_line_removed = False
        while current_line >= 0:
            full_line = True
            for col in range(tableColumns):
                if not ((col, current_line) in self.occupied):
                    full_line = False
                    break
            if full_line:
                rearranged_occupied = []
                reformed_occupied_color = {}
                is_line_removed = True
                for x, y in self.occupied:
                    if y > current_line:
                        rearranged_occupied.append((x, y))
                        # reformed_occupied_color[(x, y)] = self.occupied_color[(x, y)]
                        reformed_occupied_color[(x, y)] = self.tableMatrix[y][x]
                    elif y < current_line:
                        rearranged_occupied.append((x, y + 1))
                        # reformed_occupied_color[(x, y + 1)] = self.occupied_color[(x, y)]
                        reformed_occupied_color[(x, y + 1)] = self.tableMatrix[y][x]
                        # self.tableMatrix[y+1][x] = self.tableMatrix[y][x]
                        # self.tableMatrix[y][x] = 0
                current_line += 1
                self.occupied = rearranged_occupied
                self.occupied_color = reformed_occupied_color
                self.score += 1
                if self.score > 4:
                    self.level = self.score // 4
                    self.level += 1
                    self.speed = self.speed * 0.95 / self.level
            current_line -= 1
        if is_line_removed:
            for y in range(tableRows):
                for x in range(tableColumns):
                    if (x, y) in self.occupied_color.keys():
                        self.tableMatrix[y][x] = self.occupied_color[(x, y)]
                    else:
                        self.tableMatrix[y][x] = 0
            self.draw_table()
            self.score_level()

    def is_game_over(self):
        for x, y in self.occupied:
            if y < 0:
                self.gameOver = True
        return self.gameOver

    def move_down(self):
        self.current_piece.move_down()
        if not self.check_piece():
            self.current_piece.move_back_down()
            if self.is_hit():
                self.hit()

    def score_level(self):
        self.helperInstance.draw_rectangle(GRAY, tableRight + 25, tableBottom - 75, 100, 80)
        self.helperInstance.add_text('Score: ' + str(self.score), (tableRight + 50, tableBottom - 60))
        self.helperInstance.add_text('Level: ' + str(self.level), (tableRight + 50, tableBottom - 30))
        self.helperInstance.add_text('Speed: {:.2f}'.format(self.speed), (tableRight + 50, tableBottom - 5))


if __name__ == "__main__":
    Game = Tetris('Tetris')
    Game.on_execute()
