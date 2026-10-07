import pygame
import sys
import random
import src.utils as utils
import os


move_rate=utils.block_size

list_color= [utils.cyan, utils.yellow, utils.purple, utils.orange, utils.blue, utils.lime_green, utils.red, utils.pink ]

block_fall_event= pygame.USEREVENT + 1

def spawn_new_block():
    shape_type= random.choice(list(utils.shape.keys()))
    shape_layout= utils.shape[shape_type]
    shape_color= utils.shape_color[shape_type]
    return (utils.grid_width//2), 0, shape_layout, shape_color

def is_valid_position(pivot_x, pivot_y, shape_layout, grid):
   for row_off, col_off in shape_layout:
    block_x= pivot_x + (col_off * utils.block_size)
    block_y= pivot_y + (row_off * utils.block_size)

    if block_x<0 or block_x>= utils.grid_width or block_y>= utils.Y:
       return False

    if block_y>=0:
       grid_x= block_x // utils.block_size
       grid_y= block_y // utils.block_size
       if grid[grid_y][grid_x] is not None:
          return False
   return True

def check_clear_lines(grid, grid_cols):
    lines_cleared=0

  # Iterate bakcwards from the bottom row (19) to top (0)
    for r in range(len(grid) - 1, -1, -1):
        # If there are no None Values in this row it is full
        if None not in grid[r]:
            # remove the row
            del grid[r]
            # insert a brand new empty row at the very top
            grid.insert(0, [None] * grid_cols)
            lines_cleared += 1

    # Tetris scoring system
    score_table = {
        1: 100,
        2: 300,
        3: 500,
        4: 800
    }
    return score_table.get(lines_cleared, 0)

# high score functions
def load_high_score():
    with open("./src/high_score_track.txt", "r") as file:
        return int(file.read().strip())

# Save the high score to the TXT
def save_high_score(new_score):
    high_score = load_high_score()
    if new_score > high_score:
        with open("./src/high_score_track.txt", "w") as file:
            file.write(str(new_score))

# Main Function
def main():
    pygame.init()

    normal_fall_speed = 500
    soft_drop_speed = 80
    current_fall_speed = normal_fall_speed

    pygame.time.set_timer(block_fall_event, current_fall_speed)
    SCREEN = pygame.display.set_mode((utils.X, utils.Y))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Tetris")

    # intialize the score font
    pygame.font.init()

    # use font from flappy bird
    score_font = pygame.font.SysFont('./assets/ARCADECLASSIC.TTF', 24)

    # Load the score and highschore
    score = 0
    high_score = load_high_score()
    
    # Creating a 20x20 grid martix to store the landed blocks
    # Rows = 400 // 20 = 20 | cols = 400 // 20 = 20
    grid_rows = utils.Y // utils.block_size
    grid_cols = utils.grid_width // utils.block_size

    # Create an empty list for the grid rows
    grid = []

    # Loop for all the rows on the screen
    for row in range(grid_rows):
        new_row = []

        # fill this with empty columns
        for col in range(grid_cols):
            new_row.append(None)

        # add the completed row to our main grid
        grid.append(new_row)

    # this makes every block spawn in the center 0
    # the spawn new block funct returns a tuple of coords
    x_pos, y_pos, current_shape, current_color = spawn_new_block()

    # Check if the new block clips existing blocks
    if not is_valid_position(x_pos, y_pos, current_shape, grid):
        print("Game_Over!")
        running = False
    soft_drop=False
    # Main while loop
    running = True
    while running == True:
        # wipe the screen to prevent block trail
        SCREEN.fill(utils.tetris_blue)

        # Draw Grid
        utils.draw_grid(SCREEN)
    
        # Draw all the static blocks that have already been stacked
        for r in range(grid_rows):
            for c in range(grid_cols):
                if grid[r][c] is not None:
                    # render the locked block using the color stored in the grid
                    locked_rect = pygame.Rect(c * utils.block_size, r * utils.block_size, utils.block_size, utils.block_size)
                    pygame.draw.rect(SCREEN, grid[r][c], locked_rect)

        # Handle the inputs
        keys = pygame.key.get_pressed()
        new_soft_drop = keys[pygame.K_DOWN]
        if new_soft_drop != soft_drop:
            soft_drop = new_soft_drop
            pygame.event.clear(block_fall_event)
            current_fall_speed = soft_drop_speed if soft_drop else normal_fall_speed
            pygame.time.set_timer(block_fall_event, current_fall_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(score)
                pygame.quit()
                running = False

            # continuous falling event falling from timer    
            if event.type == block_fall_event:
                fall_distance = utils.block_size

                # Test if moving down by one block is safe
                if is_valid_position(x_pos, y_pos + fall_distance, current_shape, grid):
                    y_pos += fall_distance
                else:
                    # It cant move down down so lock all 4 blocks into the grid matrix
                    for row_off, col_off in current_shape:
                        block_x = x_pos + (col_off * utils.block_size)
                    
                        block_y = y_pos + (row_off * utils.block_size)
                        if block_y >= 0:
                            grid_y= block_y // utils.block_size
                            grid_x= block_x // utils.block_size
                            grid[grid_y][grid_x] = current_color

                    score+=5
                    score+=check_clear_lines(grid, grid_cols)
                        

                    # Spawn the next piece
                    x_pos, y_pos, current_shape, current_color = spawn_new_block()
                    pygame.event.clear(block_fall_event)

                    # Check if the new block clips existing blocks
                    if not is_valid_position(x_pos, y_pos, current_shape, grid):
                        print("Game_Over!")
                        running = False
                    break
                    
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    # Check if the new block clips existing blocks
                    if not is_valid_position(x_pos, y_pos, current_shape, grid):
                        print("Game_Over!")
                        running = False
        
                # Move to the right
                if event.key == pygame.K_RIGHT:
                    if is_valid_position(x_pos + move_rate, y_pos, current_shape, grid):
                        x_pos += move_rate

                    
                # Move to the left                    
                if event.key == pygame.K_LEFT:
                    if is_valid_position(x_pos - move_rate, y_pos, current_shape, grid):
                        x_pos -= move_rate

                # Rotate the piece
                if event.key == pygame.K_UP:
                    # Calculate the rotated shape coordinates
                    rotated_shape = []
                    
                    # Loop through the blocks in postion in current shape matrix
                    for row, col in current_shape:
                        # Apply the 90 degree turn
                        new_block = (col, -row)
                        rotated_shape.append(new_block)

                    # Check if the rotated version is safe to use
                    if is_valid_position(x_pos, y_pos, rotated_shape, grid):
                        current_shape = rotated_shape
                        
        # Make it so it is not just a single block
        for row_off, col_off in current_shape:
            block_x = x_pos + (col_off * utils.block_size)
            block_y = y_pos + (row_off * utils.block_size)

            # Only draw if it is visible on board
            if block_y >= 0:
                # Define and draw active falling piece
                current_block = pygame.Rect(block_x, block_y, utils.block_size, utils.block_size)
                pygame.draw.rect(SCREEN, current_color, current_block)

        # Draw Vertical line
        pygame.draw.line(SCREEN, utils.white, (utils.grid_width, 0), (utils.grid_width, utils.Y), 2)

        # Render the text surfaces
        score_label = score_font.render("SCORE", True, utils.white)
        score_number = score_font.render(str(score), True, utils.cyan)

        high_score_label = score_font.render("HIGH SCORE", True, utils.white)
        high_score_number = score_font.render(str(high_score), True, utils.yellow)

        # BLit is draw the text surfaces with a specific offset
        SCREEN.blit(score_label, (utils.grid_width + 20, 30))
        SCREEN.blit(score_number, (utils.grid_width + 20, 60))

        SCREEN.blit(high_score_label, (utils.grid_width + 20, 130))
        SCREEN.blit(high_score_number, (utils.grid_width + 20, 160))
                
        # Update The display
        pygame.display.update()
        CLOCK.tick(60)

    # Save high score
    save_high_score(score)
    # Quit the game
    pygame.quit()
    sys.exit()
        
# End of main loop
#
if __name__=="__main__":
    main()
#
# End of File

   


