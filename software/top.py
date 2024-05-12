import sys
import os

import wx
from gui import Gui

if __name__ == "__main__":
    app = wx.App()
    gui = Gui("Music Logger")
    gui.Show(True)
    app.MainLoop()