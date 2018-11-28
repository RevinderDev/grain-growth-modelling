import wx
import threading
from src.grid_drawing import GridClass, PyGameWindow


class Frame(wx.Frame):

    def init_ui(self):
        # --- Main sizers ---
        self.sizer_ver_main = wx.BoxSizer(wx.VERTICAL)
        self.sizer_ver_input = wx.BoxSizer(wx.VERTICAL)
        self.font_size = 9

        # --- Init UI functions ---
        self.init_helpers()
        self.init_grid_size()
        self.init_neigh_combo_box()
        self.init_create_grid_button()



        self.init_control_buttons()

        # --- Set main sizers ---
        self.sizer_ver_main.Add(self.sizer_ver_input, 0, wx.EXPAND, 5)
        self.SetSizer(self.sizer_ver_main)
        self.Layout()
        self.Centre(wx.BOTH)
        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to student project of grain growth!")

    def init_control_buttons(self):
        sizer_ver_control_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # --- Start button ---
        self.start_drawing_grid_button = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.start_drawing_grid_button.Bind(wx.EVT_BUTTON, self.on_start)
        sizer_ver_control_buttons.Add(self.start_drawing_grid_button, 5, wx.EXPAND, 5)

        # --- Pause button ---
        self.pause_drawing_grid_button = wx.Button(self, wx.ID_ANY, u"Pause", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.pause_drawing_grid_button .Bind(wx.EVT_BUTTON, self.on_pause)
        sizer_ver_control_buttons.Add(self.pause_drawing_grid_button , 5, wx.EXPAND, 5)

        # --- Clean button ---
        self.clean_grid_button = wx.Button(self, wx.ID_ANY, u"Clean", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.clean_grid_button .Bind(wx.EVT_BUTTON, self.on_clean)
        sizer_ver_control_buttons.Add(self.clean_grid_button , 5, wx.EXPAND, 5)

        self.sizer_ver_input.Add(sizer_ver_control_buttons, 0, wx.EXPAND, 5)


    def init_neigh_combo_box(self):
        sizer_hor_neigh = wx.BoxSizer(wx.HORIZONTAL)

        # --- Label neigh choice ----
        self.label_neigh_choice = wx.StaticText(self, wx.ID_ANY, u"Choose neighbourhood:", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.label_neigh_choice.SetFont(wx.Font(wx.FontInfo(self.font_size)))
        self.label_neigh_choice.Wrap(-1)
        # --- Neighboor combo box ---
        self.neigh_choices_array = ['Moore', 'Von Neumann', 'Hexagonal Left', 'Hexagonal Right', 'Random Hexagonal',
                                    'Random Pentagonal']
        self.neigh_combo = wx.ComboBox(self, wx.ID_ANY, "Moore", choices=self.neigh_choices_array)
        self.neigh_combo.Bind(wx.EVT_COMBOBOX, self.change_neighbourhood)

        sizer_hor_neigh.Add(self.label_neigh_choice, 0, wx.ALL, 5)
        sizer_hor_neigh.Add(self.neigh_combo, 0, wx.ALL, 5)

        self.sizer_ver_input.Add(sizer_hor_neigh, 0, wx.ALL, 5)

    def init_helpers(self):
        self.empty_label = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.empty_label.Wrap(-1)

    def init_grid_size(self):
        sizer_hor_grid_size = wx.BoxSizer(wx.HORIZONTAL)

        # --- Label grid size ---
        sizer_ver_grid_size_labels = wx.BoxSizer(wx.VERTICAL)

        self.label_grid_size = wx.StaticText(self, wx.ID_ANY, u"Grid size:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_grid_size.SetFont(wx.Font(wx.FontInfo(self.font_size)))
        self.label_grid_size.Wrap(-1)

        sizer_ver_grid_size_labels.Add(self.empty_label, 0, wx.ALL, 5)
        sizer_ver_grid_size_labels.Add(self.label_grid_size, 0, wx.ALL, 5)
        sizer_hor_grid_size.Add(sizer_ver_grid_size_labels, 0, wx.ALL, 5)

        # --- Input grid size X ---
        sizer_ver_grid_size_input_x = wx.BoxSizer(wx.VERTICAL)

        self.label_grid_size_x = wx.StaticText(self, wx.ID_ANY, u"Width:")
        self.label_grid_size_x.Wrap(-1)
        self.label_grid_size_x.SetFont(wx.Font(wx.FontInfo(self.font_size)))
        self.input_grid_size_x = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_grid_size_x.SetValue("100")

        sizer_ver_grid_size_input_x.Add(self.label_grid_size_x, 0, wx.ALL, 5)
        sizer_ver_grid_size_input_x.Add(self.input_grid_size_x, 0, wx.ALL, 5)
        sizer_hor_grid_size.Add(sizer_ver_grid_size_input_x, 0, wx.ALL, 5)

        # --- Input grid size Y ---
        sizer_ver_grid_size_input_y = wx.BoxSizer(wx.VERTICAL)

        self.label_grid_size_y = wx.StaticText(self, wx.ID_ANY, u"Height:")
        self.label_grid_size_y.Wrap(-1)
        self.label_grid_size_y.SetFont(wx.Font(wx.FontInfo(self.font_size)))
        self.input_grid_size_y = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_grid_size_y.SetValue("100")

        sizer_ver_grid_size_input_y.Add(self.label_grid_size_y, 0, wx.ALL, 5)
        sizer_ver_grid_size_input_y.Add(self.input_grid_size_y, 0, wx.ALL, 5)
        sizer_hor_grid_size.Add(sizer_ver_grid_size_input_y, 0, wx.ALL, 5)

        self.sizer_ver_input.Add(sizer_hor_grid_size, 0, wx.ALL, 5)

    def init_create_grid_button(self):
        # --- Start drawing button ---
        self.create_drawing_grid_button = wx.Button(self, wx.ID_ANY, u"Create drawing grid", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.create_drawing_grid_button .Bind(wx.EVT_BUTTON, self.create_grid)

        self.sizer_ver_input.Add(self.create_drawing_grid_button , 0, wx.EXPAND, 5)

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Grain Growth", pos=wx.DefaultPosition,
                          size=wx.Size(370, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.is_thread_alive = False
        self.init_ui()


    def on_pause(self,event):
        self.drawing_thread.grid.grain_growth = False

    def on_start(self, event):
        self.drawing_thread.neigh_choice = self.neigh_combo.GetValue()
        self.drawing_thread.grid.grain_growth = True

    def on_clean(self,event):
        self.drawing_thread.grid.clean_grid()

    def change_neighbourhood(self, event):
        print("Chosen neighbourhood: " + self.neigh_combo.GetValue())
        self.drawing_thread.neigh_choice = self.neigh_combo.GetValue()

    def create_grid(self, event):
        x_coordinate = int(self.input_grid_size_x.GetValue())
        y_coordinate = int(self.input_grid_size_y.GetValue())
        self.drawing_thread = DrawingThread()
        self.drawing_thread.set_coords(x_coordinate, y_coordinate)
        self.drawing_thread.start()

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.drawing_thread.join()
        self.Close(True)


class DrawingThread(threading.Thread):

    def __init__(self):
        super(DrawingThread, self).__init__()
        self.x = 100
        self.y = 100
        self.grid = GridClass()

    def run(self):
        self.grid.init_grid(self.x, self.y)
        self.grid_window = PyGameWindow(self.grid)
        self.grid_window.main_loop(self.grid)

    @property
    def neigh_choice(self):
        return self.grid.neighbourhood_type

    @neigh_choice.setter
    def neigh_choice(self, value):
        self.grid.neighbourhood_type = value


    def set_coords(self, x, y):
        if x <= 0 or y <= 0:
            raise ValueError("Coords cannot be negative!")
        self.x = x
        self.y = y


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = Frame(None)
    frm.Show()
    app.MainLoop()
