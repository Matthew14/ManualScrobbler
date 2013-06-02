import wx
import json
import os
from Settings import Settings
from SingleTrack import SingleTrackPanel
from Album import AlbumPanel
from lastfm import LastFM

class ScrobbleFrame(wx.Frame):
    def __init__(self, parent, id):
        self.name = "Matt's Manual Scrobbler"
        self.size = (900, 600)
        wx.Frame.__init__(self, parent, id, self.name, size = self.size,
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Setup()

    def Setup(self):
        self.panel = wx.Panel(self)
        notebook = wx.Notebook(self.panel)
        singleTrackPage = SingleTrackPanel(notebook)
        albumPage = AlbumPanel(notebook)
        notebook.AddPage(singleTrackPage, "Single Track")
        notebook.AddPage(albumPage, "Album")

        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

        self.CreateStatusBar()
        self.menuInit()

    def menuInit(self):
        self.menuBar = wx.MenuBar()
        editMenu =  wx.Menu()
        settings = editMenu.Append(wx.NewId(), '&Preferences\tCtrl+P', 'Opens a settings dialog.')
        self.menuBar.Append(editMenu, '&Edit')

        self.Bind(wx.EVT_MENU, self.onSettings, settings)

        self.SetMenuBar(self.menuBar)

    def onSettings(self, event):
      """
        Gets the username and password fields from the dialog and saves it as
        json
      """
      settings = Settings(self, -1, 'Preferences')

      ans = settings.ShowModal()
      if ans == wx.ID_OK:
         username = settings.userText.GetValue()
         password = settings.passText.GetValue()
         settingsData = [ {
            'username' : username,
            'password' : password} ]

         with open( os.path.abspath(os.path.dirname(__file__)) + '\\settings.json', 'w') as f:
            json.dump(settingsData, f, indent=4)
      settings.Destroy()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = ScrobbleFrame(None, -1)
    frame.Show()
    app.MainLoop()