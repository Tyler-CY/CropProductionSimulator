"""
The main file of the interactive application. Run this file to start the app.
"""
import pygame
from typing import Any

import crop_data
import weather_data
import prompt
import plot_graph


crop_rating_per_crop_per_cd_per_year = crop_data.six_crop_rating()
crop_rating_per_crop_per_cd = crop_data.average_crop_rating_per_cd()
crop_rating_per_crop = crop_data.average_crop_rating()
#####################################################################################################################
# pygame initialization
#####################################################################################################################
pygame.init()

# create a screen with width SWIDTH and length SLENGTH, and FPS
SWIDTH, SLENGTH = 1600, 900
screen = pygame.display.set_mode((SWIDTH, SLENGTH))
FPS = 300

# Title
pygame.display.set_caption('Climate Change and Crop Production')


#####################################################################################################################
# menus
#####################################################################################################################
def main_menu() -> None:
    """
    main menu of the interactive application
    """
    clock = pygame.time.Clock()

    running = True
    while running:
        # background creation
        screen.fill((255, 155, 155))
        image('images/cropped/Alberta.jpg', (SWIDTH * 0.15, SLENGTH * 0.15))

        # button creation
        button_test = Button((0, 255, 255), [0, 0, 86, 64], pygame.quit, None, ['QUIT'], 0)
        button_test.draw()
        portion = SWIDTH / 3
        future_button = Button((255, 0, 0), [0 * portion, SLENGTH - 64, portion, 64], future_predictions, None,
                               ['Future Weather'], 0)
        future_button.draw()
        interactive_button = Button((0, 0, 255), [1 * portion, SLENGTH - 64, portion, 64], interactive, None,
                                    ['Interactive'], 0)
        interactive_button.draw()
        past_button = Button((0, 255, 0), [2 * portion, SLENGTH - 64, portion, 64], past_crop, None,
                             ['Past Crop Production'], 0)
        past_button.draw()
        # list of buttons
        buttons_main = [button_test, future_button, past_button, interactive_button]

        # message creation
        welcome = Message('Welcome!', (0, 0, 255), SWIDTH - SWIDTH / 3.5, 100)
        instructions = Message('Instructions', (0, 0, 255), SWIDTH - SWIDTH / 3.5, 200)
        in1 = Message('QUIT to quit application', (0, 0, 255), SWIDTH - SWIDTH / 3.5, 250)
        in2 = Message('CLICK on buttons below', (0, 0, 255), SWIDTH - SWIDTH / 3.5, 300)
        in3 = Message('For more information', (0, 0, 255), SWIDTH - SWIDTH / 3.5, 350)

        messages = [welcome, instructions, in1, in2, in3]
        for message in messages:
            message.create()

        # run through every single event
        for event in pygame.event.get():

            # keep track of the mouse position
            pos = pygame.mouse.get_pos()

            # events
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_main:
                    if button.hover(pos):
                        button.execute()

        # update Surface
        pygame.display.update()
        clock.tick(FPS)


def future_predictions() -> None:
    """
    Future prediction of crops production based on climate parameters
    """
    clock = pygame.time.Clock()

    running = True
    while running:

        # clear the screen with selected color, and paste a background
        screen.fill((20, 155, 155))

        # image creation
        # in the order of temperature, precipitation and frost
        image('images/cropped/Temperature.jpg', (-1100, 0))
        image('images/cropped/Precipitation.jpg', (SWIDTH * 1 / 3, 0))
        image('images/cropped/Frost.jpg', (SWIDTH * 2 / 3, 0))

        # button creation
        portion = SWIDTH / 3
        temp_data = 'data/weather/temperature.csv'
        temperature_button = Button((255, 0, 0), [0 * portion, 0, portion, 64], weather,
                                    temp_data, ['Temperature'], 0)
        temperature_button.draw()
        prec_data = 'data/weather/precipitation.csv'
        precipitation_button = Button((0, 255, 0), [1 * portion, 0, portion, 64], weather, prec_data, ['Precipitation'],
                                      0)
        precipitation_button.draw()
        frost_data = 'data/weather/frost.csv'
        frost_button = Button((0, 0, 255), [2 * portion, 0, portion, 64], weather, frost_data, ['Frost'], 0)
        frost_button.draw()
        button_future = [temperature_button, precipitation_button, frost_button]

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_future:
                    if button.hover(pos):
                        button.execute()

        pygame.display.update()
        clock.tick(FPS)


def past_crop() -> None:
    """
    Past trends of crops production based on climate parameters
    """
    clock = pygame.time.Clock()

    running = True
    while running:

        screen.fill((20, 155, 155))

        # image creation
        # in the order of wheat, canola and barley
        image('images/cropped/Wheat.jpg', (0, 0))
        image('images/cropped/Canola.jpg', (SWIDTH / 3, 0))
        image('images/cropped/Barley.jpg', (2 * SWIDTH / 3, 0))

        portion = SWIDTH / 3
        wheat_button = Button((255, 0, 0), [0 * portion, 0, portion, 64], crop, 'All_wheat', ['Wheat'], 0)
        wheat_button.draw()
        canola_button = Button((0, 255, 0), [1 * portion, 0, portion, 64], crop, 'Canola', ['Canola'], 0)
        canola_button.draw()
        barley_button = Button((0, 0, 255), [2 * portion, 0, portion, 64], crop, 'Barley', ['Barley'], 0)
        barley_button.draw()
        button_past = [wheat_button, canola_button, barley_button]

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_past:
                    if button.hover(pos):
                        button.execute()

        pygame.display.update()
        clock.tick(FPS)


def interactive() -> None:
    """
    Interactive page of the application
    """
    global GG
    clock = pygame.time.Clock()

    # constants
    var = 10
    weather_cycle = 0
    crop_cycle = 0
    period_cycle = 0
    mode_cycle = 0
    rcp_cycle = 0
    graph_cycle = 0
    cycles = [period_cycle, mode_cycle, rcp_cycle, graph_cycle, crop_cycle, weather_cycle]

    running = True
    while running:

        mx, my = pygame.mouse.get_pos()

        # clear the screen with selected color, and paste a background
        screen.fill((234, 234, 40))

        welcome = Message('You can simulate weather and crop events here.', (0, 0, 255), 0.01 * SWIDTH, 100 - 50)
        instructions = Message('Instructions:', (0, 0, 255), 0.01 * SWIDTH, 200 - 50)
        in1 = Message('CLICK buttons to change crop, scenarios, and model.', (0, 0, 255), 0.01 * SWIDTH, 250 - 50)
        in1a = Message('CLICK and DRAG purple slide to change C.D..', (0, 0, 255), 0.01 * SWIDTH, 300 - 50)
        in2 = Message('CLICK on GRAPH to view graph.', (0, 0, 255), 0.01 * SWIDTH, 350 - 50)
        in2a = Message('ESC to go back to previous page.', (0, 0, 255), 0.01 * SWIDTH, 400 - 50)
        in2b = Message('Additional information:', (0, 0, 255), 0.01 * SWIDTH, 400)
        in3 = Message('Unit of Temperature: Degree Celsius', (0, 0, 255), 0.01 * SWIDTH, 450)
        in4 = Message('Unit of Precipitation: Wet Days with more than 1mm rainfall', (0, 0, 255), 0.01 * SWIDTH, 500)
        in5 = Message('Unit of Frost: Numbers of days with min temperature < 0 degree Celsius', (0, 0, 255), 0.01 * SWIDTH, 550)
        messages = [welcome, instructions, in1, in1a, in2, in2a, in3, in4, in5]
        for message in messages:
            message.create()

        # slider creation
        # slider + text showing relative position
        color = (180, 0, 180)
        position = [0.2 * SWIDTH, 0.9 * SLENGTH, var, 32]
        pygame.draw.rect(screen, color, position)
        clicked = pygame.mouse.get_pressed()
        if position[0] < mx < position[0] + SWIDTH * 0.6 and position[1] < my < position[1] + position[3]:
            if clicked[0] == 1:
                var = mx - position[0]
                pygame.draw.rect(screen, color, position)

        # scaling the bar to the real census division due to CSV file format
        cd = 18
        if 0 <= int(var // 51) <= 4:
            cd = int(var // 51) + 1
        elif int(var // 51) == 5:
            cd = '6 & 15'
        elif 6 <= int(var // 51) <= 13:
            cd = int(var // 51) + 1
        elif 14 <= int(var // 51) <= 17:
            cd = int(var // 51) + 2
        elif int(var // 51) == 18:
            cd = 'All'

        # slider assist
        bar1 = Message('Census Division: ' + str(cd), (0, 0, 0), 0.005 * SWIDTH, 0.9 * SLENGTH)
        bar1.create()
        bar2 = Message('Reading row: ' + str(int(var // 51)), (0, 0, 0), 0.005 * SWIDTH, 0.95 * SLENGTH)
        bar2.create()

        # button creation
        thank_button = Button((0, 155, 205), [0, 0, SWIDTH, 32], None, None, ['Interactive Stimulation'], 0)
        thank_button.draw()

        period = ['1950 to 2004', '2005 to 2014', '2015 to 2100']
        mode = ['Median', 'Min', 'Max']
        rcp = ['RCP 2.6', 'RCP 4.5', 'RCP 8.5']
        crop = ['All_wheat', 'Barley', 'Canola']
        weather = ['Temperature', 'Precipitation', 'Frost']

        weather_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.300 * SLENGTH, 256, 64], None,
                                None, weather, cycles[5])
        weather_button.draw()
        crop_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.420 * SLENGTH, 256, 64], None,
                             None, crop, cycles[4])
        crop_button.draw()
        period_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.540 * SLENGTH, 256, 64], None,
                               None, period, cycles[0])
        period_button.draw()
        mode_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.660 * SLENGTH, 256, 64], None,
                             None, mode, cycles[1])
        mode_button.draw()
        rcp_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.780 * SLENGTH, 256, 64], None,
                            None, rcp, cycles[2])
        rcp_button.draw()

        weather_file = {'Temperature': 'data/weather/temperature.csv',
                        'Precipitation': 'data/weather/precipitation.csv',
                        'Frost': 'data/weather/frost.csv'}

        GG = (weather_file[weather[cycles[5] % 3]], (cycles[0]) % len(period),
              cycles[1] % len(mode) + 1, (cycles[2] % len(rcp) + 1) * 3)
        crop_index = crop[crop_cycle % 3]

        cd_index = int(var // 51)
        data = (weather_file[weather[cycles[5] % 3]], (cycles[0]) % len(period), cycles[1] % len(mode) + 1,
                (cycles[2] % len(rcp) + 1) * 3)
        graph_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.180 * SLENGTH, 256, 64], plot_graph.plot_column,
                              data, ['GRAPH'], 0)
        graph_button.draw()

        if cycles[0] % 3 == 1:
            crop_chosen = crop_data.six_crop_rating()[1][crop_data.six_crop_rating()[0].index(crop_index)][cd_index]
            graph_button = Button2((200, 200, 200), [SWIDTH * 0.75, 0.180 * SLENGTH, 256, 64], plot_graph.mix_subplots,
                                   [weather_data.wanted_column(GG), crop_chosen], GG[1], ['GRAPH'], 0)
            graph_button.draw()
        if cycles[0] % 3 == 2:
            crop_sim = crop[crop_cycle]
            weather_sim = weather_file[weather[cycles[5] % 3]]
            cd_sim = int(var // 51)
            m1_sim = cycles[1] % len(mode) + 1
            m2_sim = (cycles[2] % len(rcp) + 1) * 3
            graph_button = Button2((200, 200, 200), [SWIDTH * 0.75, 0.180 * SLENGTH, 256, 64], plot_graph.simulate,
                                   [weather_sim, crop_sim], [cd_sim, m1_sim, m2_sim], ['GRAPH'], 0)
            graph_button.draw()
        button_interactive = [period_button, mode_button, rcp_button, graph_button, crop_button, weather_button]

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, len(button_interactive)):
                    if button_interactive[i].hover(pos):
                        cycles[i] = button_interactive[i].execute()

        # update Surface
        pygame.display.update()
        clock.tick(FPS)


def crop(choice: str) -> None:
    """
    crop page to see past crop information
    """
    clock = pygame.time.Clock()

    # constants
    var = 10
    crop_index = crop_rating_per_crop_per_cd_per_year[0].index(choice)

    running = True
    while running:

        # keep track of the mouse position
        mx, my = pygame.mouse.get_pos()

        # clear the screen with selected color, and paste a background
        screen.fill((204, 255, 229))

        # message creation
        welcome = Message('You can view past crop production yield here.', (0, 0, 255), 0.01 * SWIDTH, 100 - 50)
        instructions = Message('Instructions:', (0, 0, 255), 0.01 * SWIDTH, 200 - 50)
        in1 = Message('CLICK and DRAG purple slide to change C.D..', (0, 0, 255), 0.01 * SWIDTH, 250 - 50)
        in2 = Message('CLICK on GRAPH to view graph.', (0, 0, 255), 0.01 * SWIDTH, 300 - 50)
        in2a = Message('ESC to go back to previous page.', (0, 0, 255), 0.01 * SWIDTH, 350 - 50)
        in3 = Message('Additional Information:', (0, 0, 255), 0.01 * SWIDTH, 400 - 50)
        messages = [welcome, instructions, in1, in2, in2a, in3]
        for message in messages:
            message.create()

        # additional information
        if choice == 'All_wheat':
            messages = prompt.prompt_all_wheat
            y_loc = 400
            for i in range(0, len(messages)):
                new = Message(messages[i], (255, 55, 55), 0.01 * SWIDTH, y_loc + i * 50)
                new.create()
        if choice == 'Barley':
            messages = prompt.prompt_barley
            y_loc = 400
            for i in range(0, len(messages)):
                new = Message(messages[i], (255, 55, 55), 0.01 * SWIDTH, y_loc + i * 50)
                new.create()
        if choice == 'Canola':
            messages = prompt.prompt_canola
            y_loc = 400
            for i in range(0, len(messages)):
                new = Message(messages[i], (255, 55, 55), 0.01 * SWIDTH, y_loc + i * 50)
                new.create()

        # slider + text showing relative position
        color = (180, 0, 180)
        position = [0.2 * SWIDTH, 0.8 * SLENGTH, var, 32]
        pygame.draw.rect(screen, color, position)
        clicked = pygame.mouse.get_pressed()
        if position[0] < mx < position[0] + SWIDTH * 0.6 and position[1] < my < position[1] + position[3]:
            if clicked[0] == 1:
                var = mx - position[0]
                pygame.draw.rect(screen, color, position)

        # scaling the bar to the real census division due to CSV file format
        cd = 18
        if 0 <= int(var // 51) <= 4:
            cd = int(var // 51) + 1
        elif int(var // 51) == 5:
            cd = '6 & 15'
        elif 6 <= int(var // 51) <= 13:
            cd = int(var // 51) + 1
        elif 14 <= int(var // 51) <= 17:
            cd = int(var // 51) + 2
        elif int(var // 51) == 18:
            cd = 'All'

        # message creation 2: additional information about the graph
        bar1 = Message('Census Division: ' + str(cd), (0, 0, 0), 0.005 * SWIDTH, 0.80 * SLENGTH)
        bar1.create()
        bar2 = Message('Average Crop Rating for this Census Division: ' + str(crop_rating_per_crop_per_cd[crop_index][
                                                                                  int(var // 51)]), (0, 0, 0),
                       0.005 * SWIDTH, 0.85 * SLENGTH)
        bar2.create()
        bar3 = Message('Average Crop Rating across all Census Division: ' + str(crop_rating_per_crop[1][crop_index]),
                       (0, 0, 0), 0.005 * SWIDTH, 0.90 * SLENGTH)
        bar3.create()
        bar4 = Message('Reading row: ' + str(int(var // 51)), (0, 0, 0), 0.005 * SWIDTH, 0.95 * SLENGTH)
        bar4.create()

        # button creation
        thank_button = Button((0, 255, 255), [0, 0, SWIDTH, 32], None, None, [choice], 0)
        thank_button.draw()
        button_text = ['GRAPH', 'STOP']
        plot_crop = Button((135, 135, 135), [SWIDTH * 0.85, 0.875 * SLENGTH, 128, 64], plot_graph.plot_graph,
                           (choice, int(var // 51)), button_text, 0)
        plot_crop.draw()
        button_crop = [thank_button, plot_crop]

        # run through every single event
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    past_crop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_crop:
                    if button.hover(pos):
                        button.execute()

        # update Surface
        pygame.display.update()
        clock.tick(FPS)


def weather(filename: str) -> None:
    """
    weather page to see past and future weather information
    """
    clock = pygame.time.Clock()

    # constants
    period_cycle = 0
    mode_cycle = 0
    rcp_cycle = 0
    graph_cycle = 0
    cycles = [period_cycle, mode_cycle, rcp_cycle, graph_cycle]

    running = True
    while running:

        # clear the screen with selected color, and paste a background
        screen.fill((210, 122, 130))

        welcome = Message('You can view past and future weather events here.', (0, 0, 255), 0.01 * SWIDTH, 100 - 50)
        instructions = Message('Instructions:', (0, 0, 255), 0.01 * SWIDTH, 200 - 50)
        in1 = Message('CLICK buttons to change scenarios and model.', (0, 0, 255), 0.01 * SWIDTH, 250 - 50)
        in2 = Message('CLICK on GRAPH to view graph.', (0, 0, 255), 0.01 * SWIDTH, 300 - 50)
        in2a = Message('ESC to go back to previous page.', (0, 0, 255), 0.01 * SWIDTH, 350 - 50)
        in3 = Message('Additional Information:', (0, 0, 255), 0.01 * SWIDTH, 400 - 50)
        messages = [welcome, instructions, in1, in2, in2a, in3]
        for message in messages:
            message.create()

        common_prompt = prompt.prompt_weather
        y_loc = 400
        for i in range(0, len(common_prompt)):
            new = Message(common_prompt[i], (0, 255, 0), 0.01 * SWIDTH, y_loc + i * 50)
            new.create()

        if filename == 'data/weather/temperature.csv':
            messages = prompt.prompt_temp
            y_loc = 550
            for i in range(0, len(messages)):
                new = Message(messages[i], (255, 55, 55), 0.01 * SWIDTH, y_loc + i * 50)
                new.create()
        if filename == 'data/weather/precipitation.csv':
            messages = prompt.prompt_prec
            y_loc = 400
            for i in range(0, len(messages)):
                new = Message(messages[i], (255, 55, 55), 0.01 * SWIDTH, y_loc + i * 50)
                new.create()
        if filename == 'data/weather/frost.csv':
            messages = prompt.prompt_frost
            y_loc = 400
            for i in range(0, len(messages)):
                new = Message(messages[i], (255, 55, 55), 0.01 * SWIDTH, y_loc + i * 50)
                new.create()

        # button creation
        period = ['1950 to 2004', '2005 to 2014', '2015 to 2100']
        mode = ['Median', 'Min', 'Max']
        rcp = ['RCP 2.6', 'RCP 4.5', 'RCP 8.5']
        period_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.475 * SLENGTH, 256, 64], None,
                               None, period, cycles[0])
        period_button.draw()
        mode_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.675 * SLENGTH, 256, 64], None,
                             None, mode, cycles[1])
        mode_button.draw()
        rcp_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.875 * SLENGTH, 256, 64], None,
                            None, rcp, cycles[2])
        rcp_button.draw()

        data = (filename, (cycles[0]) % len(period), cycles[1] % len(mode) + 1, (cycles[2] % len(rcp) + 1) * 3)
        graph_button = Button((200, 200, 200), [SWIDTH * 0.75, 0.275 * SLENGTH, 256, 64], plot_graph.plot_column,
                              data, ['GRAPH'], 0)
        graph_button.draw()
        button_weather = [period_button, mode_button, rcp_button, graph_button]

        # run through every single eventweather
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    future_predictions()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, len(button_weather)):
                    if button_weather[i].hover(pos):
                        cycles[i] = button_weather[i].execute()

        # update Surface
        pygame.display.update()
        clock.tick(FPS)


#####################################################################################################################
# helper functions/classes (pygame)
#####################################################################################################################
class Button:
    """
    Create a button. Note that button take only 1 function name and only 1 corresponding input

    Instance attributes:
    color: The color of the button
    position: the position and size of the button, represented in a list [pos_x, pos_y, width, length]
    func: name of function; this function will execute when the button is pressed
    args: the arguments of the function; the arguments will be passed to the function when the button is pressed
    text: a list of possible text showing on the button
    text_cycle: responsible for choosing which string from text is shown, decided by text[text_cycle]

    >>> test_button = Button(color=(0,0,0), position=[0,0,100,100], func=func, args=args, text=['text'], text_cycle=3)
    >>> test_button.draw()
    """
    color: tuple
    position: list
    func: Any
    args: Any
    text: list
    text_cycle: int

    def __init__(self, color: tuple, position: list, func, args, text: list, text_cycle: int):
        self.color = color
        self.position = position
        self.func = func
        self.args = args
        self.text = text
        self.text_cycle = text_cycle

    def draw(self) -> None:
        """
        Draw the button the screen
        """
        pygame.draw.rect(screen, self.color, self.position)

        current_text = self.text[self.text_cycle % len(self.text)]
        if self.text != '':
            font = pygame.font.SysFont('', int(self.position[3] * 0.75))
            text = font.render(current_text, True, (0, 0, 0))
            text_loc = (self.position[0] + (self.position[2] / 2 - text.get_width() / 2),
                        self.position[1] + (self.position[3] / 2 - text.get_height() / 2))
            screen.blit(text, text_loc)

    def hover(self, pos) -> bool:
        """
        Determine whether the mouse is on top of the button
        """
        if self.position[0] < pos[0] < self.position[0] + self.position[2] \
                and self.position[1] < pos[1] < self.position[1] + self.position[3]:
            return True
        return False

    def execute(self) -> Any:
        """
        args will be passed to func, and the function will execute if the button is pressed
        """
        if self.func is None:
            pass
            return self.text_cycle + 1
        elif self.args is None:
            self.func()
            return self.text_cycle + 1
        else:
            self.func(self.args)
            return self.text_cycle + 1


class Button2:
    """
    Create a button. Note that button take only 1 function name and 2 corresponding inputs

    Instance attributes:
    color: The color of the button
    position: the position and size of the button, represented in a list [pos_x, pos_y, width, length]
    func: name of function; this function will execute when the button is pressed
    args1: the first argument of the function; the argument will be passed to the function when the button is pressed
    args2: the second argument of the function; the argument will be passed to the function when the button is pressed
    text: a list of possible text showing on the button
    text_cycle: responsible for choosing which string from text is shown, decided by text[text_cycle]

    >>> test = Button(color=(0,0,0), position=[0,0,100,100], func=max, args1=4, args2= 5, text=['text'], text_cycle=3)
    >>> test.draw()
    """
    color: tuple
    position: list
    func: Any
    args1: Any
    args2: Any
    text: list
    text_cycle: int

    def __init__(self, color: tuple, position: list, func, args1, args2, text: list, text_cycle: int):
        self.color = color
        self.position = position
        self.func = func
        self.args1 = args1
        self.args2 = args2
        self.text = text
        self.text_cycle = text_cycle

    def draw(self) -> None:
        """
        Draw the button the screen
        """
        pygame.draw.rect(screen, self.color, self.position)

        current_text = self.text[self.text_cycle % len(self.text)]
        if self.text != '':
            font = pygame.font.SysFont('', int(self.position[3] * 0.75))
            text = font.render(current_text, True, (0, 0, 0))
            text_loc = (self.position[0] + (self.position[2] / 2 - text.get_width() / 2),
                        self.position[1] + (self.position[3] / 2 - text.get_height() / 2))
            screen.blit(text, text_loc)

    def hover(self, pos) -> bool:
        """
        Determine whether the mouse is on top of the button
        """
        if self.position[0] < pos[0] < self.position[0] + self.position[2] \
                and self.position[1] < pos[1] < self.position[1] + self.position[3]:
            return True
        return False

    def execute(self) -> int:
        """
        args1 and args2 will be passed to func, and the function will execute if the button is pressed
        """
        self.func(self.args1, self.args2)
        return self.text_cycle + 1


class Message:
    """
    Display a message on the screen.

    instance attributes:
    msg: the message
    color: a tuple
    x: the top_left_corner_x_position of the message
    y: the top_left_corner_y_position of the message
    """

    def __init__(self, msg: str, color: tuple, x: float, y: float):
        self.msg = msg
        self.color = color
        self.x = x
        self.y = y

    def create(self) -> None:
        """
        Create a message on the screen
        """
        font = pygame.font.SysFont('', 45)
        message = font.render(self.msg, True, self.color)
        screen.blit(message, [self.x, self.y])


def image(filename: str, position: tuple) -> None:
    """
    Blit an image to the screen.
    filename is a string corresponding to the location of the file and position is a tuple corresponding to
    (top_left_corner_x_position, top_left_corner_y_position)
    """
    image = pygame.image.load(filename)
    screen.blit(image, position)


#####################################################################################################################
# RUN THE PROGRAM ON MAIN.PY
#####################################################################################################################
