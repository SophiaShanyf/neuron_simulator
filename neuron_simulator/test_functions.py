
import pygame
import pygame_gui

def test_soma_property(soma):

    print("1. Test neuron morphalogy")
    print(soma.neuron.psection())

    print("2. Test neuron property update functions")
    print("- Soma diameter")
    soma.update_soma_diam(10)
    if soma.neuron.L == 10: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")


    print("- Memebrane resistent ")
    soma.update_Ra(10)
    if soma.neuron.Ra == 10: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")

    
    print("- Insert Stimulation ")
    soma.insert_stimulation(0.5)
    if soma.iclamp != None: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")


    print("- Stimulation parameter ")
    soma.update_stim_amp(10)
    if soma.iclamp.amp == 10: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")


    print("- Insert ion channel ")
    soma.insert_ion_chan('pas')
    print(soma.neuron.psection())



def test_dend_soma_property(neuron):
    print("- Test neuron morphalogy")
    print(neuron.neuron.psection())

    print("- Test neuron property update functions")
    print("- Soma diameter")
    neuron.update_soma_diam(10)
    if neuron.soma.L == 10: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")

    print("- dendrite diameter")
    neuron.update_dend_diam(10)
    if neuron.dend.L == 10: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")


    print("- Memebrane resistent ")
    neuron.update_Ra(10)
    if neuron.soma.Ra == neuron.dend.Ra == 10: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")

    
    print("- Insert Stimulation ")
    neuron.insert_stimulation(0.5)
    if neuron.iclamp != None: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")


    print("- Stimulation parameter ")
    neuron.update_stim_amp(10)
    if neuron.iclamp.amp == 10: 
        print("Success!")
    else:
        print("Something wrong with update function :( ")


    print("- Insert ion channel ")
    neuron.insert_ion_chan('hh')
    print(neuron.neuron.psection())

    
def run_pygame():
    pygame.init()

    WIDTH, HEIGHT = 900, 700

    SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')
    is_running = True

    while is_running:
        UI_REFRESH_RATE = CLOCK.tick(60)/100.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        MANAGER.process_events(event)
        SCREEN.fill("White")
        MANAGER.update(UI_REFRESH_RATE)
        
        MANAGER.draw_ui(SCREEN)
        pygame.display.update()