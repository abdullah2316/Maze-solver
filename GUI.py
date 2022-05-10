import pygame, sys
import os, sys
import gamedata


def change_color(pos, surface, color):
    myrect = pygame.Rect(pos[1] * gamedata.BLOCK_WIDTH, pos[0] * gamedata.BLOCK_HEIGHT, gamedata.BLOCK_WIDTH,
                         gamedata.BLOCK_HEIGHT)
    pygame.draw.rect(surface, color, myrect)


def get_box_color(tile_contents):
    tile_color = gamedata.GOLD
    if tile_contents == 0:
        tile_color = gamedata.GREY
    if tile_contents == 1:
        tile_color = gamedata.BLUE
    if tile_contents == 2 or tile_contents == 4:
        tile_color = gamedata.GREEN

    return tile_color


def draw_map(surface, grid_boxes):
    gamedata.BLOCK_HEIGHT = round(gamedata.SCREEN_HEIGHT / gamedata.NUMBER_OF_BLOCKS_HIGH)
    gamedata.BLOCK_WIDTH = round(gamedata.SCREEN_WIDTH / gamedata.NUMBER_OF_BLOCKS_WIDE)
    for j, row in enumerate(grid_boxes):
        for i, box in enumerate(row):
            myrect = pygame.Rect(i * gamedata.BLOCK_WIDTH, j * gamedata.BLOCK_HEIGHT, gamedata.BLOCK_WIDTH,
                                 gamedata.BLOCK_HEIGHT)
            pygame.draw.rect(surface, get_box_color(box), myrect)


def draw_grid(surface):
    for i in range(gamedata.NUMBER_OF_BLOCKS_WIDE):
        new_height = round(i * gamedata.BLOCK_HEIGHT)
        new_width = round(i * gamedata.BLOCK_WIDTH)

        pygame.draw.line(surface, gamedata.BLACK, (0, new_height), (gamedata.SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(surface, gamedata.BLACK, (new_width, 0), (new_width, gamedata.SCREEN_HEIGHT), 2)


def game_loop(surface, state_data, visited, goal):
    count = 0
    flag = True
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        if count == 0:
            draw_map(surface, state_data)
            draw_grid(surface)

        elif count < len(visited):
            change_color(visited[count], surface, gamedata.DARKORANGE)
            draw_grid(surface)
            pygame.time.wait(100)
        elif flag:
            change_color(goal.get_agentposition(), surface, gamedata.DARKGREEN)
            if goal.parent is None:
                flag = False
            goal = goal.parent
            draw_grid(surface)
            pygame.time.wait(100)

        pygame.display.update()

        count += 1


def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((gamedata.SCREEN_WIDTH, gamedata.SCREEN_HEIGHT))
    pygame.display.set_caption(gamedata.TITLE)
    surface.fill(gamedata.UGLY_PINK)
    return surface


# def read_map():
#     filepath = gamedata.MAPFILE
#     with open(filepath, 'r') as f:
#         state_data = f.readlines()
#     state_data = [line.strip() for line in state_data]
#     return (state_data)


def UI_init(start_state, size, visited, goal):

    gamedata.NUMBER_OF_BLOCKS_WIDE = size[1]  # columns
    gamedata.NUMBER_OF_BLOCKS_HIGH = size[0]  # rows
    gamedata.TITLE = "SEARCHING MAZE"
    surface = initialize_game()

    game_loop(surface, start_state, visited, goal)
