# pip install -r requirements.txt
from neuron import h, rxd
from neuron.units import ms, mV, μm
import pygame
import pygame_gui
import pygame_chart as pyc
import helper_functions as hf

def play_game():
    pygame.init()

    WIDTH, HEIGHT = 900, 650

    SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neuron Simulator")

    CLOCK = pygame.time.Clock()
    MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

    # Upper text displace and text input section 


    NEURON_IMG = pygame.image.load("neuron_img.jpg").convert()
    NEURON_IMG = pygame.transform.rotozoom(NEURON_IMG, 0, 0.7)
    NEURON_RECT = NEURON_IMG.get_rect()
    NEURON_RECT.center = 200, 500

    Ion_leaky_input, Ion_HH_input, error_m = hf.setup_gui_page(MANAGER)

    is_running = True
    is_error = False

    # create a neuron object 
    neuron = hf.NEURON("soma")
    neuron.make_a_neuron()
    draw = False


    # create a canvas for drawing
    Figure = pyc.Figure(SCREEN, 520, 370, 300, 300)

    while is_running:
        UI_REFRESH_RATE = CLOCK.tick(60)/100.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            # numeric input
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED: 
                # check if it is numeric input 
                try:
                    text_input = float(event.text)
                    is_error = False
                    hf.raise_error_message(MANAGER, is_error, error_m)
                    if event.ui_object_id == "#axon_length_input":
                        neuron.update_axon_length(text_input)

                    elif event.ui_object_id == "#axon_diameter_input":
                        neuron.update_axon_diam(text_input)

                    elif event.ui_object_id == "#axon_r_input":
                        neuron.update_Ra(text_input)
                
                    elif event.ui_object_id == "#membrane_c_input":
                        neuron.update_cm(text_input)

                    elif event.ui_object_id == "#stim_loc_input":
                        neuron.insert_stimulation(text_input)

                    elif event.ui_object_id == "#stim_delay_input":
                        neuron.update_stim_delay(text_input)
            
                    elif event.ui_object_id == "#stim_dur_input":
                        neuron.update_stim_dur(text_input)

                    if event.ui_object_id == "#stim_amp_input":
                        neuron.update_stim_amp(text_input)
                except:
                    is_error = True
                    hf.raise_error_message(MANAGER, is_error, error_m)


            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "#Recordbutton":
                    draw = True
                    
                    t = h.Vector().record(h._ref_t)
                    v = h.Vector().record(neuron.neuron(0.5)._ref_v)

                    h.finitialize(-65 * mV)

                    h.continuerun(50 * ms)
                if event.ui_object_id == "#Restartbutton":
                    is_running = False
                    play_game()
                    
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            
                if event.ui_object_id == "#leaky_input":
                    if Ion_leaky_input.get_single_selection() == "Yes":

                        neuron.insert_ion_chan("pas")

                if event.ui_object_id == "#HH_input":
                    if Ion_HH_input.get_single_selection() == "Yes":
                        neuron.insert_ion_chan("hh")

            MANAGER.process_events(event)
        SCREEN.fill("White")
        SCREEN.blit(NEURON_IMG, NEURON_RECT)
        # print(pygame.time.get_ticks())
        # print(display_stim)
            # pygame.display.update()
        MANAGER.update(UI_REFRESH_RATE)
        
        MANAGER.draw_ui(SCREEN)
        if draw:

            Figure.line('Chart1', list(t),list(v))
                    # draw figure with specified properties
            Figure.draw()   

        pygame.display.update()

play_game()