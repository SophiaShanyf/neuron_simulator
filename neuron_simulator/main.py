# pip install -r requirements.txt
from neuron import h, rxd
from neuron.units import ms, mV, μm
import pygame
import pygame_gui
import pygame_chart as pyc
# Download theme.json to local directory before using the package

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


    def setup_gui_page(self, manager):
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
                                                    manager = manager,anchors={'left': 'left', 'top':'top'}, object_id = "#tips")
        
        error_m = pygame_gui.elements.UILabel(text = "Only numbers accepted!", relative_rect=pygame.Rect((30, 620), (800, 30)),
                                                    manager = manager,object_id = "#error_message")
        error_m.disable()

        Section_title  = pygame_gui.elements.UILabel(text = "Soma Properties", relative_rect=pygame.Rect((30, 25), (255, 35)),
                                                    manager = manager, anchors={'left': 'left', 'top':'top'})

        # Axon length
        Soma_diam_title = pygame_gui.elements.UITextBox(html_text = "Soma Diameter(&#181;m): ", relative_rect=pygame.Rect((30, 65), (200, 30)),
                                                    manager = manager,  object_id = "#soma_diam")
        Soma_diam_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#soma_diam_input")


        # Axon Resistent 

        Soma_R_title = pygame_gui.elements.UITextBox(html_text = "Soma Resistance(&ohm;*cm): ", relative_rect=pygame.Rect((280, 65), (TEXT_BOX_WIDTH + 80, 30)),
                                                    manager = manager,  object_id = "#mem_r")
        Soma_R_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((280, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#mem_r_input")


        # Membrane Capacity
        M_capacity_title = pygame_gui.elements.UITextBox(html_text = "Membrane Capacity(&#181;F/cm&sup2;): ", relative_rect=pygame.Rect((520, 65), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager = manager,  object_id = "#membrane_c")
        M_capacity_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((520, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#membrane_c_input")


        # Ion Channels 
        Ion_chan_title = pygame_gui.elements.UITextBox(html_text = "Ion Channels: ", relative_rect=pygame.Rect((30, 135), (TEXT_BOX_WIDTH, 30)),
                                                    manager = manager,  object_id = "#ion_chan")
        Ion_leaky_chan = pygame_gui.elements.UITextBox(html_text = "Passive Leaky Channel: ", relative_rect=pygame.Rect((30, 170), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager =manager,  object_id = "#ion_chan")
        Ion_HH_chan = pygame_gui.elements.UITextBox(html_text = "Hodgkin-Huxley Na&#8314;, K&#8314; Channel: ", relative_rect=pygame.Rect((350, 170), (TEXT_BOX_WIDTH+ 300, 30)),
                                                    manager = manager,  object_id = "#ion_chan")

        Ion_leaky_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                        manager=manager, object_id = "#leaky_input")
        Ion_HH_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((580, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                        manager=manager, object_id = "#HH_input")



        ## neuron image 

        Section_title_2  = pygame_gui.elements.UILabel(text = "Electrical Stimulation ", relative_rect=pygame.Rect((30, 260), (380, 35)),
                                                    manager =manager, anchors={'left': 'left', 'top':'top'})


        # location
        Stim_location_title = pygame_gui.elements.UITextBox(html_text = "Location (0-1): ", relative_rect=pygame.Rect((30, 320), (130, 30)),
                                                    manager = manager)
        Stim_location_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 320), (50, 30)),
                                                        manager=manager, object_id = "#stim_loc_input")
        #  delay

        Stim_delay_title = pygame_gui.elements.UITextBox(html_text = "Delay (ms): ", relative_rect=pygame.Rect((210, 320), (130, 30)),
                                                    manager =manager)
        Stim_delay_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((310, 320), (50, 30)),
                                                        manager=manager, object_id = "#stim_delay_input")
        # duration

        Stim_dur_title = pygame_gui.elements.UITextBox(html_text = "Duration (ms): ", relative_rect=pygame.Rect((30, 350), (130, 30)),
                                                    manager = manager)
        Stim_dur_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 350), (50, 30)),
                                                        manager=manager, object_id = "#stim_dur_input")
        # amplitude
        Stim_amp_title = pygame_gui.elements.UITextBox(html_text = "Amplitude (nA): ", relative_rect=pygame.Rect((210, 350), (130, 30)),
                                                    manager = manager)
        Stim_amp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((340, 350), (50, 30)),
                                                        manager=manager, object_id = "#stim_amp_input")


        #stim_input =  pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 310), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
        #                                               manager=MANAGER, object_id = "#stim_input")
        ## plot action potential 


        Section_title_3  = pygame_gui.elements.UILabel(text = "Simulation", relative_rect=pygame.Rect((450, 260), (380, 35)),
                                                        manager = manager, anchors={'left': 'left', 'top':'top'})

        Record_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 320), (130, 35)), text='Record', manager= manager, object_id = "#Recordbutton")
        Restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((660, 320), (130, 35)), text='Restart', manager= manager, object_id = "#Restartbutton")

        
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

    def setup_gui_page(self, manager):
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
                                                    manager = manager,anchors={'left': 'left', 'top':'top'}, object_id = "#tips")
        
        error_m = pygame_gui.elements.UILabel(text = "Only numbers accepted!", relative_rect=pygame.Rect((30, 620), (800, 30)),
                                                    manager = manager,object_id = "#error_message")
        error_m.disable()

        Section_title  = pygame_gui.elements.UILabel(text = "Neuron Properties", relative_rect=pygame.Rect((30, 25), (255, 35)),
                                                    manager = manager, anchors={'left': 'left', 'top':'top'})

        # Soma diameter
        Soma_diam_title = pygame_gui.elements.UITextBox(html_text = "Soma Diameter(&#181;m): ", relative_rect=pygame.Rect((30, 65), (200, 30)),
                                                    manager =manager,  object_id = "#soma_diam")
        Soma_diam_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#soma_diam_input")


        # dendtrite length
        Dend_length_title =  pygame_gui.elements.UITextBox(html_text = "Dendrite Length(&#181;m): ", relative_rect=pygame.Rect((220, 65), (200, 30)),
                                                    manager = manager,  object_id = "#dend_leng")
        Dend_length_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((220, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#dend_leng_input")
        # Axon diameter
        Dend_diam_title =  pygame_gui.elements.UITextBox(html_text = "Dendrite Diam(&#181;m): ", relative_rect=pygame.Rect((410, 65), (200, 30)),
                                                    manager =manager,  object_id = "#soma_diam")
        Dend_diam_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((410, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#dend_diam_input")
        
        # Memebrane Resistent 
        Mem_R_title = pygame_gui.elements.UITextBox(html_text = "Membrane Resistance(&ohm;*cm): ", relative_rect=pygame.Rect((600, 65), (TEXT_BOX_WIDTH + 120, 30)),
                                                    manager = manager,  object_id = "#mem_r")
        Mem_R_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, 90), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#mem_r_input")


        # Membrane Capacity
        M_capacity_title = pygame_gui.elements.UITextBox(html_text = "Membrane Capacity(&#181;F/cm&sup2;): ", relative_rect=pygame.Rect((30, 135), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager =manager,  object_id = "#membrane_c")
        M_capacity_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 160), (TEXT_BOX_WIDTH, 30)),
                                                        manager=manager, object_id = "#membrane_c_input")


        # Ion Channels 
        Ion_chan_title = pygame_gui.elements.UITextBox(html_text = "Ion Channels on Dendrite: ", relative_rect=pygame.Rect((250, 135), (TEXT_BOX_WIDTH + 200, 30)),
                                                    manager = manager,  object_id = "#ion_chan")
        Ion_leaky_chan = pygame_gui.elements.UITextBox(html_text = "Passive Leaky Channel: ", relative_rect=pygame.Rect((250, 170), (TEXT_BOX_WIDTH + 100, 30)),
                                                    manager =manager,  object_id = "#ion_chan")
        Ion_leaky_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((420, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                        manager=manager, object_id = "#leaky_input")
        

        Ion_HH_chan = pygame_gui.elements.UITextBox(html_text = "Hodgkin-Huxley Na&#8314;, K&#8314; Channel: ", relative_rect=pygame.Rect((550, 170), (TEXT_BOX_WIDTH+ 300, 30)),
                                                    manager = manager,  object_id = "#ion_chan")
        Ion_HH_input = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((780, 160), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
                                                        manager=manager, object_id = "#HH_input")




        Section_title_2  = pygame_gui.elements.UILabel(text = "Electrical Stimulation ", relative_rect=pygame.Rect((30, 260), (380, 35)),
                                                    manager =manager, anchors={'left': 'left', 'top':'top'})

        Stim_part = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((30, 310), (380, 50)), item_list = ("Soma", "Dendrite"), default_selection="Dendrite",
                                                        manager=manager, object_id = "#stim_part")

        # location
        Stim_location_title = pygame_gui.elements.UITextBox(html_text = "Location (0-1): ", relative_rect=pygame.Rect((30, 370), (130, 30)),
                                                    manager = manager)
        Stim_location_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 370), (50, 30)),
                                                        manager=manager, object_id = "#stim_loc_input")
        #  delay

        Stim_delay_title = pygame_gui.elements.UITextBox(html_text = "Delay (ms): ", relative_rect=pygame.Rect((210, 370), (130, 30)),
                                                    manager = manager)
        Stim_delay_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((320, 370), (50, 30)),
                                                        manager=manager, object_id = "#stim_delay_input")
        # duration

        Stim_dur_title = pygame_gui.elements.UITextBox(html_text = "Duration (ms): ", relative_rect=pygame.Rect((30, 400), (130, 30)),
                                                    manager = manager)
        Stim_dur_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((140, 400), (50, 30)),
                                                        manager=manager, object_id = "#stim_dur_input")
        # amplitude
        Stim_amp_title = pygame_gui.elements.UITextBox(html_text = "Amplitude (nA): ", relative_rect=pygame.Rect((210, 400), (130, 30)),
                                                    manager = manager)
        Stim_amp_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((340, 400), (50, 30)),
                                                        manager=manager, object_id = "#stim_amp_input")


        #stim_input =  pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((200, 310), (TEXT_BOX_WIDTH, 50)), item_list = ("Yes", "No"), default_selection="No",
        #                                               manager=MANAGER, object_id = "#stim_input")
        ## plot action potential 


        Section_title_3  = pygame_gui.elements.UILabel(text = "Simulation", relative_rect=pygame.Rect((450, 260), (380, 35)),
                                                        manager = manager, anchors={'left': 'left', 'top':'top'})
        
        

        Record_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 310), (150, 35)), text='Record', manager= manager, object_id = "#Recordbutton")

        Restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((680, 310), (150, 35)), text='Restart', manager=manager, object_id = "#Restartbutton")

        return Ion_leaky_input, Ion_HH_input, error_m, Stim_part
    
    def raise_error_message(self, MANAGER, is_error, error_m):
        if is_error:
            error_m.enable()
        else:
            error_m.disable()





def run_simulation(cell_type, theme_file = 'theme.json'):
    # This is the main function for running neuron simulation
    # Input: cell_type
    #       'soma' : simulate a single cell body (soma) 
    #       'basic_neuron' : simulate a neuron with a soma and a axon
    #       theme file
    #       a theme file that let pygame decide work and figure style. default is 'theme.json'
    #       this file is accessible from 'https://github.com/SophiaShanyf/neuron_simulator/tree/main'

    pygame.init()

    WIDTH, HEIGHT = 900, 700

    SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neuron Simulator")

    CLOCK = pygame.time.Clock()
    '''with importlib.resources.open_text("neuron_simulator", "theme.json") as file:
        theme = json.load()'''
    
    # data_text = files('neuron_simulator').joinpath('theme.json').read_text()
    MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), theme_file)

    # Upper text displace and text input section 



    is_running = True
    is_error = False

    # create a neuron object 
    if cell_type == "soma":
        neuron = SOMA()
        neuron.make_a_neuron()
        cell_x, cell_y = 200, 500
        # pygame.display.update()
        [x, y, width, height] = 450, 370, 350, 250
        Ion_leaky_input, Ion_HH_input, error_m = neuron.setup_gui_page(MANAGER)

    elif cell_type == "dend_soma":
        neuron = DEND_SOMA()
        neuron.make_a_neuron()
        cell_x, cell_y = 250, 500
        [x, y, width, height] = 450, 370, 350, 250
        Ion_leaky_input, Ion_HH_input, error_m, Stim_part = neuron.setup_gui_page(MANAGER)

    

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
        if cell_type == "soma":
            pygame.draw.circle(SCREEN, "#73c2fb", (cell_x, cell_y), radius = 50, width = 0)
            pygame.draw.circle(SCREEN, "#1034a6",(cell_x - 10, cell_y), radius = 15, width = 0)
        elif cell_type == "dend_soma":
            pygame.draw.circle(SCREEN, "#73c2fb", (cell_x, cell_y), radius = 50, width = 0)
            pygame.draw.rect(SCREEN, "#73c2fb",(cell_x - 100, cell_y - 10, 100, 10),  width = 0)
            pygame.draw.circle(SCREEN, "#1034a6",(cell_x - 10, cell_y), radius = 15, width = 0)
        # SCREEN.blit(NEURON_IMG, NEURON_RECT)
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
# run_simulation("dend_soma")
# run_simulation("basic_neuron")

