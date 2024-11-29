# pip install -r requirements.txt
from neuron import h, rxd
import pygame
import pygame_gui



pygame.init()


WIDTH, HEIGHT = 850, 600

SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neuron Simulator")

CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

display_stim = False

# Upper text displace and text input section 


TEXT_BOX_WIDTH = 105
TEXT_POS_HEIGHT = 60


NEURON_IMG = pygame.image.load("neuron_img.jpg").convert()
NEURON_IMG = pygame.transform.rotozoom(NEURON_IMG, 0, 0.7)
NEURON_RECT = NEURON_IMG.get_rect()
NEURON_RECT.center = 200, 480


STIM_IMG = pygame.image.load("stim_img.jpg").convert()
STIM_IMG = pygame.transform.rotozoom(STIM_IMG, 0, 0.15)
STIM_RECT = STIM_IMG.get_rect()
STIM_RECT.center = 280, 450



Section_title  = pygame_gui.elements.UILabel(text = "Neuron Properties", relative_rect=pygame.Rect((30, 25), (255, 35)),
                                               manager = MANAGER, anchors={'left': 'left', 'top':'top'})

# Axon length
Axon_length_title = pygame_gui.elements.UITextBox(html_text = "Axon Length(&#181;m): ", relative_rect=pygame.Rect((30, 65), (TEXT_BOX_WIDTH + 40, 30)),
                                               manager = MANAGER,  object_id = "#axon_length")
Axon_length_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#axon_length_input")

# Axon diameter
Axon_diameter_title = pygame_gui.elements.UITextBox(html_text = "Axon Diameter(&#181;m): ", relative_rect=pygame.Rect((205, 65), (TEXT_BOX_WIDTH + 40, 30)),
                                               manager = MANAGER,  object_id = "#axon_diameter")
Axon_diameter_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((205, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#axon_diameter_input")


# Axon Resistent 

Axon_R_title = pygame_gui.elements.UITextBox(html_text = "Axon Resistance(&ohm;*cm): ", relative_rect=pygame.Rect((395, 65), (TEXT_BOX_WIDTH + 80, 30)),
                                               manager = MANAGER,  object_id = "#axon_r")
Axon_R_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((395, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#axon_r_input")


# Membrane Capacity
M_capacity_title = pygame_gui.elements.UITextBox(html_text = "Membrane Capacity(&#181;F/cm&sup2;): ", relative_rect=pygame.Rect((595, 65), (TEXT_BOX_WIDTH + 100, 30)),
                                               manager = MANAGER,  object_id = "#membrane_c")
M_capacity_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((595, 90), (TEXT_BOX_WIDTH, 30)),
                                                manager=MANAGER, object_id = "#membrane_c_input")




# Ion Channels 
Ion_chan_title = pygame_gui.elements.UITextBox(html_text = "Ion Channels: ", relative_rect=pygame.Rect((30, 125), (TEXT_BOX_WIDTH, 30)),
                                               manager = MANAGER,  object_id = "#ion_chan")
Ion_leaky_chan = pygame_gui.elements.UITextBox(html_text = "Passive Leaky Channel: ", relative_rect=pygame.Rect((30, 160), (TEXT_BOX_WIDTH + 100, 30)),
                                               manager = MANAGER,  object_id = "#ion_chan")
Ion_HH_chan = pygame_gui.elements.UITextBox(html_text = "Hodgkin-Huxley Na&#8314;, K&#8314; Channel: ", relative_rect=pygame.Rect((350, 160), (TEXT_BOX_WIDTH+ 300, 30)),
                                               manager = MANAGER,  object_id = "#ion_chan")

Ion_leaky_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((100 + TEXT_BOX_WIDTH, 150), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                manager=MANAGER, object_id = "#leaky_input")
Ion_HH_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((480 + TEXT_BOX_WIDTH, 150), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                manager=MANAGER, object_id = "#HH_input")



## neuron image 

Section_title_2  = pygame_gui.elements.UILabel(text = "Neuron and Stimulation ", relative_rect=pygame.Rect((30, 260), (320, 35)),
                                               manager = MANAGER, anchors={'left': 'left', 'top':'top'})

stim = pygame_gui.elements.UITextBox(html_text = "Electrical Stimulation:", relative_rect=pygame.Rect((30, 320), (200, 30)),
                                               manager = MANAGER,  object_id = "#stim")
stim_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 310), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                manager=MANAGER, object_id = "#stim_input")
## plot action potential 


Section_title_3  = pygame_gui.elements.UILabel(text = "Recorded Potential", relative_rect=pygame.Rect((450, 260), (270, 35)),
                                               manager = MANAGER, anchors={'left': 'left', 'top':'top'})


is_running = True

# create a neuron object 
soma = soma = h.Section(name = 'soma')

while is_running:
    UI_REFRESH_RATE = CLOCK.tick(60)/100.0



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#axon_length_input":
            input_time = pygame.time.get_ticks()
            # print(input_time)
          
            soma.L = float(event.text)
            '''except:
                print(pygame.time.get_ticks())
                v = 1
                error = pygame_gui.elements.UILabel(text = "Numerical Input Only! ", relative_rect=pygame.Rect((300, 25), (255, 35)),
                                               manager = MANAGER, anchors={'left': 'left', 'top':'top'}, visible = v, object_id= "#error_message")
                

                if pygame.time.get_ticks() >=input_time + 20: 
                    v = 0
                    '''


        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#axon_diameter_input":
            soma.diam = float(event.text)

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#axon_r_input":
            soma.Ra = float(event.text)
        
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#membrane_c_input":
            soma.cm = float(event.text)
            # insert a input type check here 


        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_object_id == "#stim_input":
                if stim_input.get_single_selection() == "Yes":
                    # insert stimulation image 
                    display_stim = True
                    # pop up text input box 
                    # start sitmulation in soma
                if stim_input.get_single_selection() == "No":
                    display_stim = False 
            
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
    if display_stim:  
        STIM_RECT.x = 230
        STIM_RECT.y = 400
        # print(STIM_RECT)
    else:
        
        STIM_RECT.x = -40
        STIM_RECT.y = -40
        
        #print(STIM_RECT)
        # STIM_RECT.move_ip(20, 20)
    
    SCREEN.blit(STIM_IMG, STIM_RECT)
        # pygame.display.update()
    MANAGER.update(UI_REFRESH_RATE)
    
    MANAGER.draw_ui(SCREEN)

    pygame.display.update()


