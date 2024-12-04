# pip install -r requirements.txt
from neuron import h, rxd
from neuron.units import ms, mV, μm
import pygame
import pygame_gui
import pygame_chart as pyc
import neuron_class as Nclass

def run_simulation(cell_type):
    # This is the main function for running neuron simulation
    # Input: cell_type
    #       'soma' : simulate a single cell body (soma) 
    #       'basic_neuron' : simulate a neuron with a soma and a axon
    #       '

    pygame.init()

    WIDTH, HEIGHT = 900, 700

    SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neuron Simulator")

    CLOCK = pygame.time.Clock()
    MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

    # Upper text displace and text input section 



    is_running = True
    is_error = False

    # create a neuron object 
    if cell_type == "soma":
        neuron = Nclass.SOMA()
        neuron.make_a_neuron()
        img_file = "img/soma_img.jpg"
        img_rate = 0.6
        img_center = 200, 500
        [x, y, width, height] = 450, 370, 350, 250
        Ion_leaky_input, Ion_HH_input, error_m = neuron.setup_gui_page(MANAGER)

    elif cell_type == "dend_soma":
        neuron = Nclass.DEND_SOMA()
        neuron.make_a_neuron()
        img_file = "img/dend_soma_img.jpg"
        img_rate = 0.6
        img_center = 250, 500
        [x, y, width, height] = 450, 370, 350, 250
        Ion_leaky_input, Ion_HH_input, error_m, Stim_part = neuron.setup_gui_page(MANAGER)
    '''
        
    elif cell_type == "basic_neuron":
        neuron = Nclass.NEURON()
        neuron.make_a_neuron()
        img_file = "neuron_img.jpg"
        img_rate = 0.7
    '''

    NEURON_IMG = pygame.image.load(img_file).convert()
    NEURON_IMG = pygame.transform.rotozoom(NEURON_IMG, 0,img_rate)
    NEURON_RECT = NEURON_IMG.get_rect()
    NEURON_RECT.center = img_center


    

    draw = False


    # create a canvas for drawing
    Figure = pyc.Figure(SCREEN, x, y,width, height)

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
                    neuron.raise_error_message(MANAGER, is_error, error_m)
                    # change neuron morphalogy
                    if event.ui_object_id == "#axon_leng_input":
                        neuron.update_axon_length(text_input)

                    elif event.ui_object_id == "#axon_diam_input":
                        neuron.update_axon_diam(text_input)

                    elif event.ui_object_id == "#dend_leng_input":
                        neuron.update_dend_length(text_input)

                    elif event.ui_object_id == "#dend_diam_input":
                        neuron.update_dend_diam(text_input)  

                    elif event.ui_object_id == "#soma_diam_input":
                        neuron.update_soma_diam(text_input)

                    elif event.ui_object_id == "#mem_r_input":
                        neuron.update_Ra(text_input)
                
                    elif event.ui_object_id == "#membrane_c_input":
                        neuron.update_cm(text_input)

                    elif event.ui_object_id == "#stim_loc_input":
                        neuron.insert_stimulation(text_input)

                    elif event.ui_object_id == "#stim_delay_input":
                        neuron.update_stim_delay(text_input)
            
                    elif event.ui_object_id == "#stim_dur_input":
                        neuron.update_stim_dur(text_input)

                    elif event.ui_object_id == "#stim_amp_input":
                        neuron.update_stim_amp(text_input)
                except:
                    is_error = True
                    neuron.raise_error_message(MANAGER, is_error, error_m)


            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "#Recordbutton":
                    draw = True
                    
                    t, v = neuron.cal_simulation(h)
                    # print(neuron.stim_part)

                    h.finitialize(-65 * mV)

                    h.continuerun(50 * ms)
                if event.ui_object_id == "#Restartbutton":
                    is_running = False
                    run_simulation(cell_type)
                    
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if cell_type == "dend_soma" :
                    if event.ui_object_id == "#stim_part":
                        neuron.update_stim_part(Stim_part.get_single_selection())
               

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
            Figure.add_xaxis_label("Time (ms)")
            Figure.add_yaxis_label("V (mv)")

        pygame.display.update()


# run_simulation("soma")
run_simulation("dend_soma")
# run_simulation("basic_neuron")

