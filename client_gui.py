import pygame
import pygame_gui
from dataStructures import Grid, AgentsHandler, LoopingAgent
from MakeMaze import make_maze_recursion
from main import ShowSim

# Initialize Pygame and Pygame GUI
pygame.init()
pygame.display.set_caption("Main Screen with Controls")
window_width, window_height = 800, 500
window_surface = pygame.display.set_mode((window_width, window_height))

# Define the height of the controls section
controls_height = 100
screen_height = window_height - controls_height

# Create the main screen and controls background surfaces

grid_width, grid_height = 10, 10
# 340, 130
grid = make_maze_recursion(grid_width, grid_height)
# grid = Grid(width=grid_width, height=grid_height,
#             border_walls=True, fill=True)
# grid = Grid(file_path="./test.txt")

agents = [
    LoopingAgent(1, 1, grid_height - 2, grid_width - 2),
    # Agent(1, grid_width-2, grid_height-2, 1),
    # Agent(grid_height-2, 1, 1, grid_width-2),
    # Agent(grid_height-2, grid_width-2, 1, 1)
]

agents_handler = AgentsHandler(agents=agents, grid=grid)
sim = ShowSim(grid, agents_handler)
main_screen = sim.screen

controls_surface = pygame.Surface((window_width, controls_height))

# Set background colors for clarity
main_screen.fill(pygame.Color("#333333"))
controls_surface.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((window_width, window_height))

# Create buttons on the controls surface
reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, screen_height + 20), (150, 50)),
    text="Reset",
    manager=manager,
)

create_agent_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((220, screen_height + 20), (150, 50)),
    text="Create New Agent",
    manager=manager,
)

show_paths_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((390, screen_height + 20), (150, 50)),
    text="Show Paths",
    manager=manager,
)

pause_play_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((560, screen_height + 20), (150, 50)),
    text="Pause/Play",
    manager=manager,
)

clock = pygame.time.Clock()
is_running = True


# Define functions for each button
def reset():
    print("Resetting...")


def create_new_agent():
    print("Creating new agent...")


def show_paths():
    print("Showing paths...")


def pause_play():
    print("Toggling Pause/Play...")


while is_running:
    time_delta = clock.tick(60) / 1000.0
    sim.handle_events()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Handle button events
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == reset_button:
                reset()
            if event.ui_element == create_agent_button:
                create_new_agent()
            if event.ui_element == show_paths_button:
                show_paths()
            if event.ui_element == pause_play_button:
                pause_play()

        manager.process_events(event)

    manager.update(time_delta)

    # Render the main screen (above controls)
    main_screen.fill(pygame.Color("#333333"))  # Clear the screen
    # Draw your game content or graphics here
    pygame.draw.circle(
        main_screen, pygame.Color("#FF0000"), (300, 150), 50
    )  # Example: Red circle

    # Blit the main screen and controls surface to the window
    window_surface.blit(main_screen, (0, 0))
    window_surface.blit(controls_surface, (0, screen_height))

    # Draw the GUI controls
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
