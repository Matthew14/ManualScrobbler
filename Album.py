import wx
import lastfm
from lastfm import LastFM
import time
import urllib
import os
class AlbumPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.UiInit()
        self.image = None #for album artwork

    def UiInit(self):
        vertSizer = wx.BoxSizer(wx.VERTICAL)

        inputSizer = wx.BoxSizer(wx.VERTICAL)

        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleLabel = wx.StaticText(self, -1, 'Search Term: ')
        titleSizer.Add(titleLabel, flag=wx.ALL | wx.EXPAND, border=5)
        self.albumText = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.albumText.SetHelpText("Track Title")
        titleSizer.Add(self.albumText, flag=wx.ALL | wx.EXPAND, border=5)
        inputSizer.Add(titleSizer)


        # buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        searchButton = wx.Button(self, wx.NewId(), label="Search")
        searchButton.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.onSearch, searchButton)
        inputSizer.Add(searchButton, flag=wx.ALL | wx.EXPAND, border=5)
        # vertSizer.Add(buttonSizer)
        vertSizer.Add(inputSizer)
        resultSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.albumBox = wx.ListBox(self, 60, (100, 50), (350, 300), [], wx.LB_SINGLE)
        resultSizer.Add(self.albumBox, flag=wx.ALL | wx.EXPAND, border=5)
        self.trackBox = wx.ListBox(self, 60, (100, 50), (190, 300), [], wx.LB_SINGLE)
        resultSizer.Add(self.trackBox, flag=wx.ALL | wx.EXPAND, border=5)

        vertSizer.Add(resultSizer)

        scrobbleButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrobbleAlbumButton = wx.Button(self, wx.NewId(), label="Scrobble Album")
        scrobbleButtonSizer.Add(scrobbleAlbumButton, flag=wx.ALL | wx.EXPAND, border=5)
        scrobbleSelectedButton = wx.Button(self, wx.NewId(), label="Scrobble Selected Tracks")
        scrobbleButtonSizer.Add(scrobbleSelectedButton, flag=wx.ALL | wx.EXPAND, border=5)
        vertSizer.Add(scrobbleButtonSizer)

        self.SetSizer(vertSizer)

        self.Bind(wx.EVT_LISTBOX, self.onListBox, self.albumBox)
        self.Bind(wx.EVT_BUTTON, self.onScrobbleAlbum, scrobbleAlbumButton)
        self.Bind(wx.EVT_BUTTON, self.onScrobbleSelected, scrobbleSelectedButton)

    def onSearch(self, event):
        self.albumBox.Clear()
        try:
            lfm = LastFM()
            results = lfm.albumSearch(self.albumText.GetValue()).get_next_page()
            for result in results:
                self.albumBox.Append(result.get_artist().name + " - " +
                    result.get_title() + " - " + result.get_release_date().split(',')[0], result)
            # self.albumBox.SetSelection(0)
        except lastfm.pylast.WSError as e:
            wx.MessageBox(str(e), 'Uh Oh', wx.OK | wx.ICON_ERROR)

    def onListBox(self, event):
        self.trackBox.Clear()
        selectedAlbum = self.albumBox.GetClientData(event.GetSelection())
        self.DisplayImage(selectedAlbum.get_cover_image())
        trackNo = 1
        for track in selectedAlbum.get_tracks():
            self.trackBox.Append(str(trackNo) + ': ' + track.title, track)
            trackNo += 1

    def onScrobbleAlbum(self, event):
        try:
            lfm = LastFM()
            selectedAlbum = self.albumBox.GetClientData(event.GetSelection())
            starttime = int(time.time()) - 90
            album = selectedAlbum.get_title()
            noTracks = 0
            for track in selectedAlbum.get_tracks():
                noTracks += 1
                starttime += 10
                artist = track.artist.name
                title = track.title
                lfm.scrobble(artist, title, starttime)
            wx.MessageBox(
                "Scrobbled: {} - {} ({} tracks).".format(artist.encode('utf-8'),
                 album.encode('utf-8'), noTracks), "Done", wx.OK)
        except lastfm.pylast.WSError as e:
            wx.MessageBox(str(e), 'Uh Oh', wx.OK | wx.ICON_ERROR)

    def onScrobbleSelected(self, event):
        wx.MessageBox("Not yet implemented", 'Uh Oh', wx.OK | wx.ICON_ERROR)

    def DisplayImage(self , imageURI):
        imgHandle = urllib.urlopen(imageURI)
        if self.image != None:
            self.image.Destroy()
        with open("tmpImage.png", "wb") as img:
            img.write(imgHandle.read())
        tmpFile = 'tmpImage.png'
        tmpFile  = wx.Image(str(tmpFile), wx.BITMAP_TYPE_ANY)
        tmpFile = tmpFile.Scale(250, 250, wx.IMAGE_QUALITY_HIGH)
        tmpFile = tmpFile.ConvertToBitmap()
        tmpFilePos = (600, 100)

        self.image = wx.StaticBitmap(self, -1, tmpFile, tmpFilePos, (tmpFile.GetWidth(), tmpFile.GetHeight()))
        os.remove('tmpImage.png')