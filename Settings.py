import os
import wx
import json

class Settings(wx.Dialog):
    """provides a settings dialog and saves user input to a json file"""
    def __init__(self, parent, ID, title, size=(400, 400), pos=(100, 100), style=wx.DEFAULT_DIALOG_STYLE, useMetal=False):
        filename = os.path.dirname(__file__) + 'settings.json'
        self.getInfo(filename)

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size)
        self.PostCreate(pre)
        self.Center()
        self.UiInit()

    def UiInit(self):
        panel = wx.Panel(self)
        vertSizer = wx.BoxSizer(wx.VERTICAL)
        #Last.fm settings
        settings = wx.StaticBox(panel, label='Settings')
        settingsSizer = wx.StaticBoxSizer(settings, orient=wx.VERTICAL)

        usernameSizer = wx.BoxSizer(wx.HORIZONTAL)
        userLabel = wx.StaticText(panel, -1, 'Last.fm Username: ')
        usernameSizer.Add(userLabel, flag=wx.ALL | wx.EXPAND, border=5)
        self.userText = wx.TextCtrl(panel, -1, "", size=(150, -1))
        self.userText.SetHelpText("Enter the last.fm username for scrobbling")
        self.userText.SetValue(self.username)
        usernameSizer.Add(self.userText, flag=wx.ALL | wx.EXPAND, border=5)
        settingsSizer.Add(usernameSizer)

        passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordLabel = wx.StaticText(panel, -1, 'Last.fm Password: ')
        passwordSizer.Add(passwordLabel,  flag=wx.ALL | wx.EXPAND, border=5)
        self.passText = wx.TextCtrl(panel, -1, "", style=wx.TE_PASSWORD, size=(150, -1))
        self.passText.SetValue(self.password)
        passwordSizer.Add(self.passText, flag=wx.ALL | wx.EXPAND, border=5)
        settingsSizer.Add(passwordSizer)
        #end last.fm settings

        #ok and cancel
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK)
        cancelButton = wx.Button(self, wx.ID_CANCEL)
        okButton.SetDefault()
        buttonSizer.Add(okButton)
        buttonSizer.Add(cancelButton, flag=wx.LEFT, border=5)

        vertSizer.Add(panel, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vertSizer.Add(buttonSizer,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        panel.SetSizer(settingsSizer)
        self.SetSizer(vertSizer)

    def getInfo(self, filename):
        try:
            with open( os.path.abspath(os.path.dirname(__file__)) + '\\settings.json', 'r') as f:
                settingsDict = json.load(f)
        except IOError as io:
            with open( os.path.abspath(os.path.dirname(__file__)) + '\\settings.json', 'w') as f:
                settingsData = [ {
                    'username' : "username",
                    'password' : "password"} ]
                json.dump(settingsData, f, indent=4)
            with open( os.path.abspath(os.path.dirname(__file__)) + '\\settings.json', 'r') as f:
                settingsDict = json.load(f)

        self.username= settingsDict[0]['username']
        self.password = settingsDict[0]['password']

if __name__ == '__main__':
    print("You must open the main.pyw file")