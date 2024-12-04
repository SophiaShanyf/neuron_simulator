# helper functions 

# pip install -r requirements.txt
from neuron import h, rxd
from neuron.units import ms, mV, μm
import pygame
import pygame_gui
import pygame_chart as pyc

# Code adapted from The neuron simulator documentation: https://nrn.readthedocs.io/en/latest/index.html
class SOMA:

    def __init__(self):
        self.neuron = []
        self.iclamp = []

    def make_a_neuron(self):
        # this function make a default neuron, with the name that was initialized with 

        h.load_file("stdrun.hoc")
        neuron = h.Section(name = 'soma')
        self.neuron = neuron


    def update_soma_diam(self, new_diam):
        self.neuron.L = self.neuron.diam = new_diam * μm
    
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

    def cal_simulation(self, h):
        t = h.Vector().record(h._ref_t)
        v = h.Vector().record(self.neuron(0.5)._ref_v)
      
        return t, v



    def setup_gui_page(self, MANAGER):
    # This function set up the bacis text and option component on the pygame screen
    # Input: 
    #       Manager: a pygame manager that will monitor the events and elements happen on the screen 
    # Output:
    #       Input_leaky_input & Input_hh_input: we return these two variable because it is a selection list. We need to 
    #       access the screen event, i.e. select "yes" or "no", to determine the property of the neuron 

        TEXT_BOX_WIDTH = 105
        TEXT_POS_HEIGHT = 60

        tips = "User tips: 1. Hit 'Enter' to input values; 2. Ion channel cannot be unselected. Please restart to try new values! "

        user_tips =  pygame_gui.elements.UILabel(text = tips, relative_rect=pygame.Rect( (30, 650), (800, 40)),
                                                    manager = MANAGER,anchors={'left': 'left', 'top':'top'}, object_id = "#tips")
        
        error_m = pygame_gui.elements.UILabel(text = "Only numbers accepted!", relative_rect=pygame.Rect((30, 620), (800, 30)),
                                                    manager = MANAGER,object_id = "#error_message")
        error_m.disable()

        Section_title  = pygame_gui.elements.UILabel(text = "Soma Properties", relative_rect=pygame.Rect((30, 25), (255, 35)),
                                                    manager = MANAGER, anchors={'left': 'left', 'top':'top'})

        # Axon length
        Soma_diam_title = pygame_gui.elements.UITextBox(html_text = "Soma Diameter(&#181;m): ", relative_rect=pygame.Rect((30, 65), (200, 30)),
                                                    manager = MANAGER,  object_id = "#soma_diam")
        Soma_diam_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#soma_diam_input")


        # Axon Resistent 

        Soma_R_title = pygame_gui.elements.UITextBox(html_text = "Soma Resistance(&ohm;*cm): ", relative_rect=pygame.Rect((280, 65), (TEXT_BOX_WIDTH + 80, 30)),
                                                    manager = MANAGER,  object_id = "#mem_r")
        Soma_R_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((280, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#mem_r_input")


        # Membrane Capacity
        M_capacity_title = pygame_gui.elements.UITextBox(html_text = "Membrane Capacity(&#181;F/cm&sup2;): ", relative_rect=pygame.Rect((520, 65), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager = MANAGER,  object_id = "#membrane_c")
        M_capacity_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((520, 90), (TEXT_BOX_WIDTH, 30)),
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

        Record_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 320), (130, 35)), text='Record', manager= MANAGER, object_id = "#Recordbutton")
        Restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((660, 320), (130, 35)), text='Restart', manager= MANAGER, object_id = "#Restartbutton")

        
        return Ion_leaky_input, Ion_HH_input, error_m
    
    def raise_error_message(self, MANAGER, is_error, error_m):
        if is_error:
            error_m.enable()
        else:
            error_m.disable()


class DEND_SOMA:

    def __init__(self):
        self.neuron = []
        self.iclamp = []
        self.soma = []
        self.dend = []
        self.all = []
        self.stim_part = []
       
        self.stim_loc = 0.5
    
        
    def make_a_neuron(self):
        # this function make a default neuron, with the name that was initialized with 

        h.load_file("stdrun.hoc")
        self.h = h
        self.soma = h.Section(name = 'soma')
        self.update_common_soma_property()
        self.dend = h.Section(name = 'dend')
        self.stim_part = self.dend
        self.record_part = self.soma
        self.all = [self.soma, self.dend]
        self.neuron = self.dend.connect(self.soma)

    def update_common_soma_property(self):
        self.soma.insert('hh')
        for seg in self.soma:
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003  # Leak conductance in S/cm2
            seg.hh.el = -54.3 * mV 

    def update_stim_part(self, part):
        if part == "Soma":
            self.stim_part = self.soma
        elif part == "Dendrite":
            self.stim_part = self.dend
        print(self.stim_part)
        self.insert_stimulation(self.stim_loc)

 # neuron
    def update_soma_diam(self, new_diam):
        self.soma.L = self.soma.diam = new_diam * μm

    def update_dend_length(self, new_length):
        self.dend.L = new_length * μm
    
    def update_dend_diam(self, new_diam):
        self.dend.diam = new_diam * μm
    
    def update_Ra(self, new_Ra):
        for part in self.all:
            part.Ra = new_Ra
            

    def update_cm(self, new_cm):
        for part in self.all:
            part.cm = new_cm
       
    def insert_stimulation(self, loc):
        self.stim_loc = loc
        self.iclamp  = h.IClamp(self.stim_part(loc))
        
    
    def update_stim_delay(self, delay):
        self.iclamp.delay = delay * ms

    def update_stim_dur(self, dur):
        self.iclamp.dur = dur * ms

    def update_stim_amp(self, amp):
        self.iclamp.amp = amp

    def insert_ion_chan(self, chan):
        self.dend.insert(chan)
    
    def cal_simulation(self, h):
        v = h.Vector().record(self.soma(0.5)._ref_v)
        t = h.Vector().record(h._ref_t)
        return t, v

    def setup_gui_page(self, MANAGER):
    # This function set up the bacis text and option component on the pygame screen
    # Input: 
    #       Manager: a pygame manager that will monitor the events and elements happen on the screen 
    # Output:
    #       Input_leaky_input & Input_hh_input: we return these two variable because it is a selection list. We need to 
    #       access the screen event, i.e. select "yes" or "no", to determine the property of the neuron 

        TEXT_BOX_WIDTH = 105
        TEXT_POS_HEIGHT = 60

        tips = "User tips: 1. Hit 'Enter' to input values; 2. Ion channel cannot be unselected. Please restart to try new values! "

        user_tips =  pygame_gui.elements.UILabel(text = tips, relative_rect=pygame.Rect( (30, 650), (800, 40)),
                                                    manager = MANAGER,anchors={'left': 'left', 'top':'top'}, object_id = "#tips")
        
        error_m = pygame_gui.elements.UILabel(text = "Only numbers accepted!", relative_rect=pygame.Rect((30, 620), (800, 30)),
                                                    manager = MANAGER,object_id = "#error_message")
        error_m.disable()

        Section_title  = pygame_gui.elements.UILabel(text = "Neuron Properties", relative_rect=pygame.Rect((30, 25), (255, 35)),
                                                    manager = MANAGER, anchors={'left': 'left', 'top':'top'})

        # Soma diameter
        Soma_diam_title = pygame_gui.elements.UITextBox(html_text = "Soma Diameter(&#181;m): ", relative_rect=pygame.Rect((30, 65), (200, 30)),
                                                    manager = MANAGER,  object_id = "#soma_diam")
        Soma_diam_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#soma_diam_input")


        # dendtrite length
        Dend_length_title =  pygame_gui.elements.UITextBox(html_text = "Dendrite Length(&#181;m): ", relative_rect=pygame.Rect((220, 65), (200, 30)),
                                                    manager = MANAGER,  object_id = "#dend_leng")
        Dend_length_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((220, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#dend_leng_input")
        # Axon diameter
        Dend_diam_title =  pygame_gui.elements.UITextBox(html_text = "Dendrite Diam(&#181;m): ", relative_rect=pygame.Rect((410, 65), (200, 30)),
                                                    manager = MANAGER,  object_id = "#soma_diam")
        Dend_diam_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((410, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#dend_diam_input")
        
        # Memebrane Resistent 
        Mem_R_title = pygame_gui.elements.UITextBox(html_text = "Membrane Resistance(&ohm;*cm): ", relative_rect=pygame.Rect((600, 65), (TEXT_BOX_WIDTH + 120, 30)),
                                                    manager = MANAGER,  object_id = "#mem_r")
        Mem_R_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#mem_r_input")


        # Membrane Capacity
        M_capacity_title = pygame_gui.elements.UITextBox(html_text = "Membrane Capacity(&#181;F/cm&sup2;): ", relative_rect=pygame.Rect((30, 135), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager = MANAGER,  object_id = "#membrane_c")
        M_capacity_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 160), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#membrane_c_input")


        # Ion Channels 
        Ion_chan_title = pygame_gui.elements.UITextBox(html_text = "Ion Channels on Dendrite: ", relative_rect=pygame.Rect((250, 135), (TEXT_BOX_WIDTH + 200, 30)),
                                                    manager = MANAGER,  object_id = "#ion_chan")
        Ion_leaky_chan = pygame_gui.elements.UITextBox(html_text = "Passive Leaky Channel: ", relative_rect=pygame.Rect((250, 170), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager = MANAGER,  object_id = "#ion_chan")
        Ion_leaky_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((420, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                        manager=MANAGER, object_id = "#leaky_input")
        

        Ion_HH_chan = pygame_gui.elements.UITextBox(html_text = "Hodgkin-Huxley Na&#8314;, K&#8314; Channel: ", relative_rect=pygame.Rect((550, 170), (TEXT_BOX_WIDTH+ 300, 30)),
                                                    manager = MANAGER,  object_id = "#ion_chan")
        Ion_HH_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((780, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                        manager=MANAGER, object_id = "#HH_input")




        Section_title_2  = pygame_gui.elements.UILabel(text = "Electrical Stimulation ", relative_rect=pygame.Rect((30, 260), (380, 35)),
                                                    manager = MANAGER, anchors={'left': 'left', 'top':'top'})

        Stim_part = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((30, 310), (380, 50)), item_list = ("Soma", "Dendrite"), default_selection="Dendrite",
                                                        manager=MANAGER, object_id = "#stim_part")

        # location
        Stim_location_title = pygame_gui.elements.UITextBox(html_text = "Location (0-1): ", relative_rect=pygame.Rect((30, 370), (130, 30)),
                                                    manager = MANAGER)
        Stim_location_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 370), (50, 30)),
                                                        manager=MANAGER, object_id = "#stim_loc_input")
        #  delay

        Stim_delay_title = pygame_gui.elements.UITextBox(html_text = "Delay (ms): ", relative_rect=pygame.Rect((210, 370), (130, 30)),
                                                    manager = MANAGER)
        Stim_delay_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((320, 370), (50, 30)),
                                                        manager=MANAGER, object_id = "#stim_delay_input")
        # duration

        Stim_dur_title = pygame_gui.elements.UITextBox(html_text = "Duration (ms): ", relative_rect=pygame.Rect((30, 400), (130, 30)),
                                                    manager = MANAGER)
        Stim_dur_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 400), (50, 30)),
                                                        manager=MANAGER, object_id = "#stim_dur_input")
        # amplitude
        Stim_amp_title = pygame_gui.elements.UITextBox(html_text = "Amplitude (nA): ", relative_rect=pygame.Rect((210, 400), (130, 30)),
                                                    manager = MANAGER)
        Stim_amp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((340, 400), (50, 30)),
                                                        manager=MANAGER, object_id = "#stim_amp_input")


        #stim_input =  pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 310), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
        #                                               manager=MANAGER, object_id = "#stim_input")
        ## plot action potential 


        Section_title_3  = pygame_gui.elements.UILabel(text = "Simulation", relative_rect=pygame.Rect((450, 260), (380, 35)),
                                                        manager = MANAGER, anchors={'left': 'left', 'top':'top'})
        
        

        Record_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 310), (150, 35)), text='Record', manager= MANAGER, object_id = "#Recordbutton")

        Restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 310), (150, 35)), text='Restart', manager= MANAGER, object_id = "#Restartbutton")

        return Ion_leaky_input, Ion_HH_input, error_m, Stim_part
    
    def raise_error_message(self, MANAGER, is_error, error_m):
        if is_error:
            error_m.enable()
        else:
            error_m.disable()







class NEURON:

    def __init__(self):
        self.neuron = []
        self.iclamp = []
        self.soma = []
        self.dend = []
        self.axon = []


    def make_a_neuron(self):
        # this function make a default neuron, with the name that was initialized with 

        h.load_file("stdrun.hoc")
        self.soma = h.Section(name = 'soma')
        self.dend = h.Section(name = 'dend')
        self.axon = h.Section(name = 'axon')
        
        self.neuron = self.axon.connect(self.soma)

 # neuron
    def update_soma_diam(self, new_diam):
        self.soma.L = self.soma.diam = new_diam * μm

    def update_axon_length(self, new_length):
        self.axon.L = new_length * μm
    
    def update_axon_diam(self, new_diam):
        self.axon.diam = new_diam * μm
    
    def update_Ra(self, new_Ra):
        self.axon.Ra = new_Ra
        self.soma.Ra = new_Ra

    def update_cm(self, new_cm):
        self.axon.cm = new_cm 
        self.soma.cm = new_cm
    
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
    def setup_gui_page(self, MANAGER):
    # This function set up the bacis text and option component on the pygame screen
    # Input: 
    #       Manager: a pygame manager that will monitor the events and elements happen on the screen 
    # Output:
    #       Input_leaky_input & Input_hh_input: we return these two variable because it is a selection list. We need to 
    #       access the screen event, i.e. select "yes" or "no", to determine the property of the neuron 

        TEXT_BOX_WIDTH = 105
        TEXT_POS_HEIGHT = 60

        tips = "User tips: 1. Hit 'Enter' to input values; 2. Ion channel cannot be unselected. Please restart to try new values! "

        user_tips =  pygame_gui.elements.UILabel(text = tips, relative_rect=pygame.Rect( (30, 650), (800, 40)),
                                                    manager = MANAGER,anchors={'left': 'left', 'top':'top'}, object_id = "#tips")
        
        error_m = pygame_gui.elements.UILabel(text = "Only numbers accepted!", relative_rect=pygame.Rect((30, 620), (800, 30)),
                                                    manager = MANAGER,object_id = "#error_message")
        error_m.disable()

        Section_title  = pygame_gui.elements.UILabel(text = "Neuron Properties", relative_rect=pygame.Rect((30, 25), (255, 35)),
                                                    manager = MANAGER, anchors={'left': 'left', 'top':'top'})

        # Axon length
        Soma_diam_title = pygame_gui.elements.UITextBox(html_text = "Soma Diameter(&#181;m): ", relative_rect=pygame.Rect((30, 65), (200, 30)),
                                                    manager = MANAGER,  object_id = "#soma_diam")
        Soma_diam_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#soma_diam_input")


        # Axon Resistent 

        Soma_R_title = pygame_gui.elements.UITextBox(html_text = "Soma Resistance(&ohm;*cm): ", relative_rect=pygame.Rect((280, 65), (TEXT_BOX_WIDTH + 80, 30)),
                                                    manager = MANAGER,  object_id = "#soma_r")
        Soma_R_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((280, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=MANAGER, object_id = "#soma_r_input")


        # Membrane Capacity
        M_capacity_title = pygame_gui.elements.UITextBox(html_text = "Membrane Capacity(&#181;F/cm&sup2;): ", relative_rect=pygame.Rect((520, 65), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager = MANAGER,  object_id = "#membrane_c")
        M_capacity_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((520, 90), (TEXT_BOX_WIDTH, 30)),
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

        Record_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 320), (80, 35)), text='Record', manager= MANAGER, object_id = "#Recordbutton")
        Restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((640, 320), (150, 35)), text='Restart', manager= MANAGER, object_id = "#Restartbutton")

        
        return Ion_leaky_input, Ion_HH_input, error_m
    
    def raise_error_message(self, MANAGER, is_error, error_m):
        if is_error:
            error_m.enable()
        else:
            error_m.disable()





