# helper functions 

# pip install -r requirements.txt
from neuron import h, rxd
from neuron.units import ms, mV, μm
import pygame
import pygame_gui
import pygame_chart as pyc


class NEURON:

    def __init__(self, name):
        self.name = name
        self.neuron = []
        self.iclamp = []

    def make_a_neuron(self):
        # this function make a default neuron, with the name that was initialized with 

        h.load_file("stdrun.hoc")
        neuron = h.Section(name = self.name)
        self.neuron = neuron

    def update_axon_length(self, new_length):
        self.neuron.L = new_length * μm
    
    def update_axon_diam(self, new_diam):
        self.neuron.diam = new_diam * μm
    
    def update_Ra(self, new_Ra):
        self.neuron.Ra = new_Ra

    def update_cm(self, new_cm):
        self.neuron.cm = new_cm 
    
    def insert_stimulation(self, loc):
        iclamp = h.IClamp(self.neuron(loc))
        self.iclamp = iclamp
    
    def update_stim_delay(self, delay):
        self.iclamp.delay = delay * ms

    def update_stim_dur(self, dur):
        self.iclamp.dur = dur * ms

    def update_stim_amp(self, amp):
        self.iclamp.amp = amp

    def insert_ion_chan(self, chan):
        self.neuron.insert(chan)


def setup_gui_page(MANAGER):
    # This function set up the bacis text and option component on the pygame screen
    # Input: 
    #       Manager: a pygame manager that will monitor the events and elements happen on the screen 
    # Output:
    #       Input_leaky_input & Input_hh_input: we return these two variable because it is a selection list. We need to 
    #       access the screen event, i.e. select "yes" or "no", to determine the property of the neuron 

    TEXT_BOX_WIDTH = 105
    TEXT_POS_HEIGHT = 60

    tips = "User tips: 1. Hit 'Enter' to input values; 2. Ion channel cannot be unselected. Please restart to try new values! "

    user_tips =  pygame_gui.elements.UILabel(text = tips, relative_rect=pygame.Rect((300, 10), (520, 35)),
                                                manager = MANAGER,object_id = "#tips")
    
    error_m = pygame_gui.elements.UILabel(text = "Only numbers accepted!", relative_rect=pygame.Rect((300, 35), (520, 30)),
                                                manager = MANAGER,object_id = "#error_message")
    error_m.disable()

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

    
    return Ion_leaky_input, Ion_HH_input, error_m


def raise_error_message(MANAGER, is_error, error_m):
    if is_error:
        error_m.enable()
    else:
        error_m.disable()
