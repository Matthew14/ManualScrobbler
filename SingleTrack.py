import wx
import lastfm
from lastfm import LastFM
import time
class SingleTrackPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.UiInit()
    def UiInit(self):
        vertSizer = wx.BoxSizer(wx.VERTICAL)

        inputSizer = wx.BoxSizer(wx.VERTICAL)

        #title input
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleLabel = wx.StaticText(self, -1, 'Track Title: ')
        titleSizer.Add(titleLabel, flag=wx.ALL | wx.EXPAND, border=5)
        self.titleText = wx.TextCtrl(self, -1, "", size=(150, -1))
        self.titleText.SetHelpText("Track Title")
        titleSizer.Add(self.titleText, flag=wx.ALL | wx.EXPAND, border=5)
        inputSizer.Add(titleSizer)

        #artist input
        artistSizer = wx.BoxSizer(wx.HORIZONTAL)
        artistLabel = wx.StaticText(self, -1, 'Artist: ')
        artistSizer.Add(artistLabel, flag=wx.ALL | wx.EXPAND, border=5)
        self.artistText = wx.TextCtrl(self, -1, "", size=(150, -1))
        self.artistText.SetHelpText("Artist")
        artistSizer.Add(self.artistText, flag=wx.ALL | wx.EXPAND, border=5)
        inputSizer.Add(artistSizer)

        #the buttons
        vertSizer.Add(inputSizer)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrobbleButton = wx.Button(self, wx.NewId(), label="Scrobble")
        scrobbleButton.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnScrobble, scrobbleButton)
        buttonSizer.Add(scrobbleButton)
        vertSizer.Add(buttonSizer)
        self.SetSizer(vertSizer)

    def OnScrobble(self, event):
        """Scrobbles using LastFM and sets a confirmation dialog"""

        try:
            lfm = LastFM()
            starttime = int(time.time())
            lfm.scrobble(self.artistText.GetValue(), self.titleText.GetValue(), starttime)
            wx.MessageBox("Scrobbled: {} - {}".format(self.artistText.GetValue(), self.titleText.GetValue()), "Done", wx.OK)
            self.artistText.SetValue("")
            self.titleText.SetValue("")
        except lastfm.pylast.WSError as e:
            wx.MessageBox(str(e), 'Uh Oh', wx.OK | wx.ICON_ERROR)