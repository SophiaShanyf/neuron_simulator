# pip install -r requirements.txt
from neuron import h, rxd
import pygame
import pygame_gui



pygame.init()

WIDTH, HEIGHT = 800, 500

SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neuron Simulator")

CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))


Axon_length_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 50), (100, 25)),
                                                manager=MANAGER, object_id = "#axon_length_input")




is_running = True

# create a neuron object 
soma = soma = h.Section(name = 'soma')

while is_running:
    UI_REFRESH_RATE = CLOCK.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#axon_length_input":
            soma.L = int(event.text)
            # insert a input type check here 

        MANAGER.process_events(event)
    SCREEN.fill("White")
    MANAGER.update(UI_REFRESH_RATE)


    
    MANAGER.draw_ui(SCREEN)

    pygame.display.update()


