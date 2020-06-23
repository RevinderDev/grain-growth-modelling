import wx
import threading
from grid_drawing import GridClass, PyGameWindow


class Frame(wx.Frame):
    FONT_SIZE = 9
    MAX_FPS = 100
    MIN_FPS = 0

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Grain Growth", pos=wx.DefaultPosition,
                          size=wx.Size(325, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.is_thread_alive = False
        self.sizer_ver_main = wx.BoxSizer(wx.VERTICAL)
        self.sizer_ver_input = wx.BoxSizer(wx.VERTICAL)
        self.drawing_thread = None
        self.init_ui()

    def init_ui(self):
        # --- Init UI functions ---
        self.init_helpers()
        self.init_grid_size()
        self.init_neigh_combo_box()
        self.init_create_grid_button()
        self.init_bound_combo_box()
        self.init_fps_input()
        self.init_random_cells()
        self.init_radius_random_input()
        self.init_cells_control_buttons()

        self.init_control_buttons()

        # --- Set main sizers ---
        self.sizer_ver_main.Add(self.sizer_ver_input, proportion=0, flag=wx.EXPAND, border=5)
        self.SetSizer(self.sizer_ver_main)
        self.Layout()
        self.Centre(wx.BOTH)
        # and a status bar
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Welcome to student project of grain growth!")

    def init_radius_random_input(self):
        sizer_hor_radius_grains = wx.BoxSizer(wx.HORIZONTAL)
        # --- Label radius grain ---
        self.label_radius_grain = wx.StaticText(self, wx.ID_ANY, u"Radius:", wx.DefaultPosition,
                                                wx.DefaultSize, style=0)
        self.label_radius_grain.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
        self.label_radius_grain.Wrap(-1)
        # --- Input radius grain ---
        self.input_radius_grains = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_radius_grains.SetValue("0")

        self.radius_cells_button = wx.Button(self, wx.ID_ANY, u"Randomize with radius", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.radius_cells_button .Bind(wx.EVT_BUTTON, self.on_radius_cells)

        sizer_hor_radius_grains.Add(self.label_radius_grain, 0, wx.ALL, 5)
        sizer_hor_radius_grains.Add(self.input_radius_grains, 0, wx.ALL, 5)
        sizer_hor_radius_grains.Add(self.radius_cells_button, 5, wx.EXPAND, 5)
        self.sizer_ver_input.Add(sizer_hor_radius_grains)

    def init_bound_combo_box(self):
        sizer_hor_bound = wx.BoxSizer(wx.HORIZONTAL)

        self.label_bound_choice = wx.StaticText(self, wx.ID_ANY, u"Bounds:", wx.DefaultPosition,
                                                wx.DefaultSize, style=0)
        self.label_bound_choice.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
        self.label_bound_choice.Wrap(-1)

        self.bound_choices_array = ['Periodical', 'Non periodical']
        self.bound_combo = wx.ComboBox(self, wx.ID_ANY, value=self.bound_choices_array[0],
                                       choices=self.bound_choices_array)
        self.bound_combo.Bind(wx.EVT_COMBOBOX, self.change_bound)

        sizer_hor_bound.Add(self.label_bound_choice, 0, wx.ALL, 5)
        sizer_hor_bound.Add(self.bound_combo, 0, wx.ALL, 5)

        self.sizer_ver_input.Add(sizer_hor_bound, 0, wx.ALL, 5)


    def init_cells_control_buttons(self):
        sizer_hor_cells_control_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # --- Start button ---
        self.random_cells_button = wx.Button(self, wx.ID_ANY, u"Completely Random", wx.DefaultPosition,
                                             wx.DefaultSize, style=0)
        self.random_cells_button.Bind(wx.EVT_BUTTON, self.on_random_cells)
        sizer_hor_cells_control_buttons.Add(self.random_cells_button, 5, wx.EXPAND, 5)

        # --- Pause button ---
        self.evenly_cells_button = wx.Button(self, wx.ID_ANY, u"Evenly", wx.DefaultPosition,
                                             wx.DefaultSize, style=0)
        self.evenly_cells_button.Bind(wx.EVT_BUTTON, self.on_evenly_cells)
        sizer_hor_cells_control_buttons.Add(self.evenly_cells_button, 5, wx.EXPAND, 5)

        self.sizer_ver_input.Add(sizer_hor_cells_control_buttons, 0, wx.EXPAND, 5)

    def init_random_cells(self):
        sizer_hor_random_grains = wx.BoxSizer(wx.HORIZONTAL)
        self.label_grains_input = wx.StaticText(self, wx.ID_ANY, u"Grains:", wx.DefaultPosition,
                                                wx.DefaultSize, style=0)
        self.label_grains_input.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
        self.label_grains_input.Wrap(-1)
        self.input_grains = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_grains.SetValue("0")

        sizer_hor_random_grains.Add(self.label_grains_input, 0, wx.ALL, 5)
        sizer_hor_random_grains.Add(self.input_grains, 0, wx.ALL, 5)
        self.sizer_ver_input.Add(sizer_hor_random_grains)

    def init_fps_input(self):
        sizer_hor_fps = wx.BoxSizer(wx.HORIZONTAL)
        self.label_fps_input = wx.StaticText(self, wx.ID_ANY, u"Speed [FPS]:", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.label_fps_input.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
        self.label_fps_input.Wrap(-1)
        self.input_fps = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_fps.SetValue("60")

        self.apply_fps_button = wx.Button(self, wx.ID_ANY, u"Apply change", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.apply_fps_button.Bind(wx.EVT_BUTTON, self.on_fps_click)
        sizer_hor_fps.Add(self.apply_fps_button, 5, wx.EXPAND, 5)

        sizer_hor_fps.Add(self.label_fps_input, 0, wx.ALL, 5)
        sizer_hor_fps.Add(self.input_fps, 0, wx.ALL, 5)
        self.sizer_ver_input.Add(sizer_hor_fps)

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
        self.pause_drawing_grid_button.Bind(wx.EVT_BUTTON, self.on_pause)
        sizer_ver_control_buttons.Add(self.pause_drawing_grid_button, 5, wx.EXPAND, 5)

        # --- Clean button ---
        self.clean_grid_button = wx.Button(self, wx.ID_ANY, u"Clean", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.clean_grid_button.Bind(wx.EVT_BUTTON, self.on_clean)
        sizer_ver_control_buttons.Add(self.clean_grid_button, 5, wx.EXPAND, 5)

        self.sizer_ver_input.Add(sizer_ver_control_buttons, 0, wx.EXPAND, 5)

    def init_neigh_combo_box(self):
        sizer_hor_neigh = wx.BoxSizer(wx.HORIZONTAL)

        # --- Label neigh choice ----
        self.label_neigh_choice = wx.StaticText(self, wx.ID_ANY, u"Choose neighbourhood:", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.label_neigh_choice.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
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
        self.label_grid_size.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
        self.label_grid_size.Wrap(-1)

        sizer_ver_grid_size_labels.Add(self.empty_label, 0, wx.ALL, 5)
        sizer_ver_grid_size_labels.Add(self.label_grid_size, 0, wx.ALL, 5)
        sizer_hor_grid_size.Add(sizer_ver_grid_size_labels, 0, wx.ALL, 5)

        # --- Input grid size X ---
        sizer_ver_grid_size_input_x = wx.BoxSizer(wx.VERTICAL)

        self.label_grid_size_x = wx.StaticText(self, wx.ID_ANY, u"Width:")
        self.label_grid_size_x.Wrap(-1)
        self.label_grid_size_x.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
        self.input_grid_size_x = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.input_grid_size_x.SetValue("100")

        sizer_ver_grid_size_input_x.Add(self.label_grid_size_x, 0, wx.ALL, 5)
        sizer_ver_grid_size_input_x.Add(self.input_grid_size_x, 0, wx.ALL, 5)
        sizer_hor_grid_size.Add(sizer_ver_grid_size_input_x, 0, wx.ALL, 5)

        # --- Input grid size Y ---
        sizer_ver_grid_size_input_y = wx.BoxSizer(wx.VERTICAL)

        self.label_grid_size_y = wx.StaticText(self, wx.ID_ANY, u"Height:")
        self.label_grid_size_y.Wrap(-1)
        self.label_grid_size_y.SetFont(wx.Font(wx.FontInfo(Frame.FONT_SIZE)))
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
        self.create_drawing_grid_button.Bind(wx.EVT_BUTTON, self.create_grid)

        self.sizer_ver_input.Add(self.create_drawing_grid_button, 0, wx.EXPAND, 5)

    def on_fps_click(self, event):
        fps = int(self.input_fps.GetValue())
        if fps > Frame.MAX_FPS or fps <= Frame.MIN_FPS:
            self.error_dialog = wx.MessageDialog(self, 'Value has to be between 0 and 100.', 'Error changing FPS!',
                                                 wx.ICON_ERROR)
            val = self.error_dialog.ShowModal()
            self.error_dialog.Show()
            if val == wx.ID_CANCEL:
                self.error_dialog.Destroy()
                return
        self.drawing_thread.set_fps(fps)

    def on_random_cells(self, event):
        grain_number = int(self.input_grains.GetValue())
        self.drawing_thread.grid.randomize_cells(grain_number)

    def on_evenly_cells(self, event):
        self.drawing_thread.grid.evenly_cells(self.input_grains.GetValue())

    def on_pause(self, event):
        self.statusBar.SetStatusText("Paused!")
        self.drawing_thread.grid.grain_growth = False

    def on_start(self, event):
        if self.drawing_thread is None:
            self.create_grid(event)
        self.statusBar.SetStatusText("Running!")
        self.drawing_thread.neigh_choice = self.neigh_combo.GetValue()
        self.drawing_thread.grid.grain_growth = True

    def on_clean(self, event):
        self.drawing_thread.grid.clean_grid()

    def change_neighbourhood(self, event):
        self.drawing_thread.neigh_choice = self.neigh_combo.GetValue()

    def change_bound(self, event):
        self.drawing_thread.bound_choice = self.bound_combo.GetValue()

    def on_radius_cells(self, event):
        radius = int(self.input_radius_grains.GetValue())
        grains = int(self.input_grains.GetValue())
        self.drawing_thread.grid.randomize_radius_cells(radius, grains)

    def create_grid(self, event):
        if self.drawing_thread is not None and self.drawing_thread.grid is not None:
            wx.MessageBox('Cannot open two grids at once', 'Error', wx.OK | wx.ICON_ERROR)
            return

        x_coordinate = int(self.input_grid_size_x.GetValue())
        y_coordinate = int(self.input_grid_size_y.GetValue())
        if x_coordinate <= 0 or y_coordinate <= 0:
            error_dialog = wx.MessageDialog(self, 'Size cannot be negative.', 'Error creating grid!',
                                            wx.ICON_ERROR)
            val = error_dialog.ShowModal()
            error_dialog.Show()
            if val == wx.ID_CANCEL:
                error_dialog.Destroy()
                return
        self.drawing_thread = DrawingThread()
        self.drawing_thread.set_coords(x_coordinate, y_coordinate)
        self.drawing_thread.start()

    def OnClose(self, event):
        self.drawing_thread.grid_window.close()
        self.drawing_thread.join()
        self.Close(True)


class DrawingThread(threading.Thread):

    def __init__(self):
        super(DrawingThread, self).__init__()
        self.x = 100
        self.y = 100
        self.grid = GridClass(self)

    def run(self):
        self.grid.init_grid(self.x, self.y)
        self.grid_window = PyGameWindow(self.grid)
        self.grid_window.main_loop()

    @property
    def neigh_choice(self):
        return self.grid.neighbourhood_type

    @neigh_choice.setter
    def neigh_choice(self, value):
        self.grid.neighbourhood_type = value

    @property
    def bound_choice(self):
        return self.grid.bound_choice

    @bound_choice.setter
    def bound_choice(self, value):
        self.grid.bound_choice = value

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def set_fps(self, value):
        self.grid.GROWTH_SPEED = value


if __name__ == '__main__':
    app = wx.App()
    frm = Frame(None)
    frm.Show()
    app.MainLoop()
