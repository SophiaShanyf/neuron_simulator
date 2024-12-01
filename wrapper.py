# pip install -r requirements.txt
from neuron import h, rxd
from neuron.units import ms, mV, μm
import pygame
import pygame_gui
import pygame_chart as pyc




pygame.init()


WIDTH, HEIGHT = 900, 650

SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neuron Simulator")

CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

# Upper text displace and text input section 


TEXT_BOX_WIDTH = 105
TEXT_POS_HEIGHT = 60


NEURON_IMG = pygame.image.load("neuron_img.jpg").convert()
NEURON_IMG = pygame.transform.rotozoom(NEURON_IMG, 0, 0.7)
NEURON_RECT = NEURON_IMG.get_rect()
NEURON_RECT.center = 200, 500


tips = "User tips: 1. Hit 'Enter' to input values; 2. Ion channel cannot be unselected. Please restart to try new values! "

user_tips =  pygame_gui.elements.UILabel(text = tips, relative_rect=pygame.Rect((300, 25), (550, 35)),
                                               manager = MANAGER,object_id = "#tips")

Section_title  = pygame_gui.elements.UILabel(text = "Neuron Properties", relative_rect=pygame.Rect((30, 25), (255, 35)),
                                               manager = MANAGER, anchors={'left': 'left', 'top':'top'})

# Axon length
Axon_length_title = pygame_gui.elements.UITextBox(html_text = "Axon Length(&#181;m): ", relative_rect=pygame.Rect((30, 65), (TEXT_BOX_WIDTH + 40, 30)),
                                               manager = MANAGER,  object_id = "#axon_length")
Axon_length_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#axon_length_input")

# Axon diameter
Axon_diameter_title = pygame_gui.elements.UITextBox(html_text = "Axon Diameter(&#181;m): ", relative_rect=pygame.Rect((215, 65), (TEXT_BOX_WIDTH + 40, 30)),
                                               manager = MANAGER,  object_id = "#axon_diameter")
Axon_diameter_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((215, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#axon_diameter_input")


# Axon Resistent 

Axon_R_title = pygame_gui.elements.UITextBox(html_text = "Axon Resistance(&ohm;*cm): ", relative_rect=pygame.Rect((415, 65), (TEXT_BOX_WIDTH + 80, 30)),
                                               manager = MANAGER,  object_id = "#axon_r")
Axon_R_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((415, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#axon_r_input")


# Membrane Capacity
M_capacity_title = pygame_gui.elements.UITextBox(html_text = "Membrane Capacity(&#181;F/cm&sup2;): ", relative_rect=pygame.Rect((625, 65), (TEXT_BOX_WIDTH + 100, 30)),
                                               manager = MANAGER,  object_id = "#membrane_c")
M_capacity_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((625, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#membrane_c_input")


# Ion Channels 
Ion_chan_title = pygame_gui.elements.UITextBox(html_text = "Ion Channels: ", relative_rect=pygame.Rect((30, 135), (TEXT_BOX_WIDTH, 30)),
                                               manager = MANAGER,  object_id = "#ion_chan")
Ion_leaky_chan = pygame_gui.elements.UITextBox(html_text = "Passive Leaky Channel: ", relative_rect=pygame.Rect((30, 170), (TEXT_BOX_WIDTH + 100, 30)),
                                               manager = MANAGER,  object_id = "#ion_chan")
Ion_HH_chan = pygame_gui.elements.UITextBox(html_text = "Hodgkin-Huxley Na&#8314;, K&#8314; Channel: ", relative_rect=pygame.Rect((350, 170), (TEXT_BOX_WIDTH+ 300, 30)),
                                               manager = MANAGER,  object_id = "#ion_chan")

Ion_leaky_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                manager=MANAGER, object_id = "#leaky_input")
Ion_HH_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((580, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                manager=MANAGER, object_id = "#HH_input")



## neuron image 

Section_title_2  = pygame_gui.elements.UILabel(text = "Electrical Stimulation ", relative_rect=pygame.Rect((30, 260), (380, 35)),
                                               manager = MANAGER, anchors={'left': 'left', 'top':'top'})


# location
Stim_location_title = pygame_gui.elements.UITextBox(html_text = "Location (0-1): ", relative_rect=pygame.Rect((30, 320), (130, 30)),
                                               manager = MANAGER)
Stim_location_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 320), (50, 30)),
                                                manager=MANAGER, object_id = "#stim_loc_input")
#  delay

Stim_delay_title = pygame_gui.elements.UITextBox(html_text = "Delay (ms): ", relative_rect=pygame.Rect((210, 320), (130, 30)),
                                               manager = MANAGER)
Stim_delay_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((310, 320), (50, 30)),
                                                manager=MANAGER, object_id = "#stim_delay_input")
# duration

Stim_dur_title = pygame_gui.elements.UITextBox(html_text = "Duration (ms): ", relative_rect=pygame.Rect((30, 350), (130, 30)),
                                               manager = MANAGER)
Stim_dur_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 350), (50, 30)),
                                                manager=MANAGER, object_id = "#stim_dur_input")
# amplitude
Stim_amp_title = pygame_gui.elements.UITextBox(html_text = "Amplitude (nA): ", relative_rect=pygame.Rect((210, 350), (130, 30)),
                                               manager = MANAGER)
Stim_amp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((340, 350), (50, 30)),
                                                manager=MANAGER, object_id = "#stim_amp_input")


#stim_input =  pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 310), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
#                                               manager=MANAGER, object_id = "#stim_input")
## plot action potential 


Section_title_3  = pygame_gui.elements.UILabel(text = "Simulation", relative_rect=pygame.Rect((450, 260), (380, 35)),
                                                manager = MANAGER, anchors={'left': 'left', 'top':'top'})

Record_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 320), (80, 35)), text='Run', manager= MANAGER, object_id = "#Recordbutton")
Restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((640, 320), (150, 35)), text='Restart', manager= MANAGER, object_id = "#Restartbutton")

is_running = True

# create a neuron object 
h.load_file("stdrun.hoc")
soma = h.Section(name = 'soma')
draw = False



# create a canvas for drawing
Figure = pyc.Figure(SCREEN, 520, 370, 300, 300)

while is_running:
    UI_REFRESH_RATE = CLOCK.tick(60)/100.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#axon_length_input":
            # input_time = pygame.time.get_ticks()
            # print(input_time)
          
            soma.L = float(event.text) * μm
            print(soma.psection)
            '''except:
                print(pygame.time.get_ticks())
                v = 1
                error = pygame_gui.elements.UILabel(text = "Numerical Input Only! ", relative_rect=pygame.Rect((300, 25), (255, 35)),
                                               manager = MANAGER, anchors={'left': 'left', 'top':'top'}, visible = v, object_id= "#error_message")
                

                if pygame.time.get_ticks() >=input_time + 20: 
                    v = 0
                    '''

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#axon_diameter_input":
            soma.diam = float(event.text) * μm

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#axon_r_input":
            soma.Ra = float(event.text)
        
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#membrane_c_input":
            soma.cm = float(event.text)

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#stim_loc_input":
            iclamp = h.IClamp(soma(float(event.text)))

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#stim_delay_input":
            iclamp.delay = float(event.text) * ms
        
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#stim_dur_input":
            iclamp.dur = float(event.text) * ms

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#stim_amp_input":
            iclamp.amp = float(event.text)

        

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "#Recordbutton":
                draw = True
                
                t = h.Vector().record(h._ref_t)
                v = h.Vector().record(soma(0.5)._ref_v)

                h.finitialize(-65 * mV)

                h.continuerun(50 * ms)
            if event.ui_object_id == "#Restartbutton":
                is_running = False
                
            

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
           
        
            '''
            if event.ui_object_id == "#stim_input":
                if stim_input.get_single_selection() == "Yes":
                    # insert stimulation image 
                    display_stim = True
                    # pop up text input box 
                    # start sitmulation in soma
                if stim_input.get_single_selection() == "No":
                    display_stim = False 
            '''
            if event.ui_object_id == "#leaky_input":
                if Ion_leaky_input.get_single_selection() == "Yes":
                    soma = soma.insert("pas")
                pass


            if event.ui_object_id == "#HH_input":
                if Ion_HH_input.get_single_selection() == "Yes":
                    soma = soma.insert("hh")
                pass

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


