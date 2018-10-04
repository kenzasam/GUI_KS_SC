''' LLGUI

If you haven't used this before, read LLGUI-ReadMe

1.0: LL: GUI. Buttons for sequences. To skip typing using pyperclip
1.1: LL: collapsible panes and categories for sequences
1.1.1: LL: #Actuations Can be set via the textbox
2.0.0: LL and Guy: .exe implemented
2.0.1: Guy: external protocol import fix
2.0.2: LL: GUI Space allocation fix
2.0.3: LL: Intelligent Column allocation, stop all, and stop sequence button added.
2.0.4: Guy: Add udpSend support for remote operation.
2.0.5: LL: Bugfix for Stop All button.
2.0.6: LL: File opening dialog to load protocols.
3.0.0: KS: Adding Magnet functionality
3.0.1: KS: Adding Function Buttons with number fields

Big thanks to Guy Soffer for his tips and help!
Laura Leclerc
'''

import wx, os, sys
import pyperclip
import Tkinter, tkFileDialog
from optparse import OptionParser
from GSOF_ArduBridge import UDP_Send
import os.path

class seqSelector(wx.Frame):
    def __init__(self, setup, port=-1, ip='127.0.0.1', columns=2):
        ###sendinging stuff to ArduBridge Shell
        self.udpSend = False
        if port > 1:
            self.udpSend = UDP_Send.udpSend(nameID='', DesIP=ip, DesPort=port)
        ###
        ###
        #setting up wx Main Frame window
        self.setup=setup
        wx.Frame.__init__( self, None, wx.ID_ANY, "Protocol GUI", size=(400,400))
        self.panel = wx.Panel(self, wx.ID_ANY)
        ico=wx.Icon('shih.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        topSizer =  wx.BoxSizer(wx.HORIZONTAL)
        titlebox0  = wx.BoxSizer(wx.HORIZONTAL)
        DropletSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5)
        titlebox1  = wx.BoxSizer(wx.HORIZONTAL)
        fnSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5)
        titlebox2  = wx.BoxSizer(wx.HORIZONTAL)
        seqSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5) #sizer for the window
        MAINbox = wx.BoxSizer(wx.VERTICAL)
        #################
        #################top bar, topSizer
        topSizer = wx.FlexGridSizer(1,5,2,2) #sizer for the top left contents
        self.openPortBtn = wx.Button( self.panel, label='Open Port', name='openPort()', size=(66,24))
        self.openPortBtn.Bind(wx.EVT_BUTTON, self.onRemoteOpenPort)
        self.openPortBtn.SetToolTip(wx.ToolTip('Open the ArduBridge COM-port'))
        topSizer.Add(self.openPortBtn, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.closePortBtn = wx.Button( self.panel, label='Close Port', name='closePort()', size=(70,24))
        self.closePortBtn.Bind(wx.EVT_BUTTON, self.onRemoteClosePort)
        self.closePortBtn.SetToolTip(wx.ToolTip('Close the ArduBridge COM-port'))
        topSizer.Add(self.closePortBtn, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.closeBtn = wx.Button( self.panel, label='Close Ardu', name='close()', size=(70,24))
        self.closeBtn.Bind(wx.EVT_BUTTON, self.onFuncButton)
        self.closeBtn.SetToolTip(wx.ToolTip('Close all ArduBridge thread and COM-port'))
        topSizer.Add(self.closeBtn, flag=wx.ALIGN_CENTER_HORIZONTAL)
        MAINbox.Add(topSizer, 0, wx.RIGHT )
        #############droplet generation########
        line = wx.StaticLine(self.panel, wx.ID_ANY,style=wx.LI_HORIZONTAL )
        MAINbox.Add( line, 0, wx.ALL|wx.EXPAND, 2 )
        title = wx.StaticText(self.panel, label='Droplet Generation')
        titlebox0.Add(title, flag=wx.RIGHT, border=8)
        MAINbox.Add(titlebox0, 0, wx.ALIGN_CENTER_VERTICAL)
        #generate droplets left, right, double
        boxa=wx.BoxSizer(wx.HORIZONTAL)
        self.LeftBtn=wx.Button( self.panel, label='Left', name='', size=(70,24)) #ADDED KS
        self.LeftBtn.Bind(wx.EVT_BUTTON, self.onLeft)
        boxa.Add(self.LeftBtn, flag=wx.RIGHT, border=8)
        boxa1=wx.BoxSizer(wx.VERTICAL)
        boxa11=wx.BoxSizer(wx.HORIZONTAL)
        self.texta1=wx.StaticText(self.panel,  wx.ID_ANY, label='#')
        boxa11.Add(self.texta1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entrya1=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        boxa11.Add(self.entrya1, proportion=0.5, border=8)
        boxa12=wx.BoxSizer(wx.HORIZONTAL)
        self.texta2=wx.StaticText(self.panel, wx.ID_ANY, label='period')
        boxa12.Add(self.texta2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entrya2=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        boxa12.Add(self.entrya2, proportion=0.5, border=8)
        boxa1.Add(boxa11)
        boxa1.Add(boxa12)
        boxa.Add(boxa1, flag=wx.LEFT)
        DropletSizer.Add(boxa, flag=wx.ALIGN_CENTER_VERTICAL)
        ##
        boxb=wx.BoxSizer(wx.HORIZONTAL)
        self.RightBtn=wx.Button( self.panel, label='Right', name='', size=(70,24)) #ADDED KS
        self.RightBtn.Bind(wx.EVT_BUTTON, self.onRight)
        boxb.Add(self.RightBtn, flag=wx.RIGHT, border=8)
        boxb1=wx.BoxSizer(wx.VERTICAL)
        boxb11=wx.BoxSizer(wx.HORIZONTAL)
        self.textb1=wx.StaticText(self.panel,  wx.ID_ANY, label='#')
        boxb11.Add(self.textb1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryb1=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        boxb11.Add(self.entryb1, proportion=0.5, border=8)
        boxb12=wx.BoxSizer(wx.HORIZONTAL)
        self.textb2=wx.StaticText(self.panel, wx.ID_ANY, label='period')
        boxb12.Add(self.textb2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryb2=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        boxb12.Add(self.entryb2, proportion=0.5, border=8)
        boxb1.Add(boxb11)
        boxb1.Add(boxb12)
        boxb.Add(boxb1, flag=wx.LEFT)
        DropletSizer.Add(boxb, flag=wx.ALIGN_CENTER_VERTICAL)
        ##
        boxc=wx.BoxSizer(wx.HORIZONTAL)
        self.DoubleBtn=wx.Button( self.panel, label='Double', name='', size=(70,24)) #ADDED KS
        self.DoubleBtn.Bind(wx.EVT_BUTTON, self.onDouble)
        boxc.Add(self.DoubleBtn, flag=wx.RIGHT, border=8)
        boxc1=wx.BoxSizer(wx.VERTICAL)
        boxc11=wx.BoxSizer(wx.HORIZONTAL)
        self.textc1=wx.StaticText(self.panel,  wx.ID_ANY, label='#')
        boxc11.Add(self.textc1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryc1=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        boxc11.Add(self.entryc1, proportion=0.5, border=8)
        boxc12=wx.BoxSizer(wx.HORIZONTAL)
        self.textc2=wx.StaticText(self.panel, wx.ID_ANY, label='period')
        boxc12.Add(self.textc2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryc2=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        boxc12.Add(self.entryc2, proportion=0.5, border=8)
        boxc1.Add(boxc11)
        boxc1.Add(boxc12)
        boxc.Add(boxc1, flag=wx.LEFT)
        DropletSizer.Add(boxc, flag=wx.ALIGN_CENTER_VERTICAL)
        MAINbox.Add(DropletSizer, 0, wx.ALIGN_CENTER_VERTICAL)        
        #############function#####sizer########
        line = wx.StaticLine(self.panel, wx.ID_ANY,style=wx.LI_HORIZONTAL )
        MAINbox.Add( line, 0, wx.ALL|wx.EXPAND, 2 )
        title1 = wx.StaticText(self.panel, label='Functions')
        titlebox1.Add(title1, flag=wx.RIGHT, border=8)
        MAINbox.Add(titlebox1, 0, wx.ALIGN_CENTER_VERTICAL)
        #Encapsulate
        box1=wx.BoxSizer(wx.HORIZONTAL)
        self.EncapsulateBtn=wx.Button( self.panel, label='Ecapsulate', name='Encapsulate()', size=(70,24)) #ADDED KS
        self.EncapsulateBtn.Bind(wx.EVT_BUTTON, self.onEncapsulate)
        box1.Add(self.EncapsulateBtn, flag=wx.RIGHT, border=8)
        self.entry1=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        box1.Add(self.entry1, proportion=1)
        fnSizer.Add(box1, flag=wx.ALIGN_CENTER_VERTICAL)
        #Release
        box2=wx.BoxSizer(wx.HORIZONTAL)
        self.ReleaseBtn=wx.Button( self.panel, label='Release', name='Release()', size=(70,24)) #ADDED KS
        self.ReleaseBtn.Bind(wx.EVT_BUTTON, self.onRelease)
        box2.Add(self.ReleaseBtn, flag=wx.RIGHT, border=8)
        self.entry2=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        box2.Add(self.entry2, proportion=1)
        fnSizer.Add(box2, flag=wx.ALIGN_CENTER_VERTICAL)
        #Keep
        box3=wx.BoxSizer(wx.HORIZONTAL)
        self.KeepBtn=wx.Button( self.panel, label='Keep', name='Keep()', size=(70,24)) #ADDED KS
        self.KeepBtn.Bind(wx.EVT_BUTTON, self.onKeep)
        box3.Add(self.KeepBtn, flag=wx.ALIGN_CENTER_HORIZONTAL, border=8)
        box31=wx.BoxSizer(wx.VERTICAL)
        box311=wx.BoxSizer(wx.HORIZONTAL)
        self.text3=wx.StaticText(self.panel,  wx.ID_ANY, label='nr')
        box311.Add(self.text3, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry3=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        box311.Add(self.entry3, proportion=0.5, border=8)
        box312=wx.BoxSizer(wx.HORIZONTAL)
        self.text4=wx.StaticText(self.panel, wx.ID_ANY, label='time')
        box312.Add(self.text4, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry4=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        box312.Add(self.entry4, proportion=0.5, border=8)
        box31.Add(box311)
        box31.Add(box312)
        box3.Add(box31, flag=wx.LEFT)
        fnSizer.Add(box3, flag=wx.ALIGN_CENTER_VERTICAL)
        #KeepAllButOne
        box4=wx.BoxSizer(wx.HORIZONTAL)
        self.KeepAllBtn=wx.Button( self.panel, label='Keep All', name='KeepAll()', size=(70,24)) #ADDED KS
        self.KeepAllBtn.Bind(wx.EVT_BUTTON, self.onKeepAllBut)
        box4.Add(self.KeepAllBtn, flag=wx.ALIGN_CENTER_HORIZONTAL, border=8)
        box41=wx.BoxSizer(wx.VERTICAL)
        box411=wx.BoxSizer(wx.HORIZONTAL)
        self.text5=wx.StaticText(self.panel,  wx.ID_ANY, label='except nr')
        box411.Add(self.text5, border=8)
        self.entry5=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        box411.Add(self.entry5, proportion=0.5)
        box412=wx.BoxSizer(wx.HORIZONTAL)
        self.text6=wx.StaticText(self.panel,  wx.ID_ANY, label='time')
        box412.Add(self.text6, border=8)
        self.entry6=wx.TextCtrl(self.panel, wx.ID_ANY,'', size=(30, -1))
        box412.Add(self.entry6, proportion=0.5)
        box41.Add(box411)
        box41.Add(box412)
        box4.Add(box41)
        fnSizer.Add(box4, flag=wx.ALIGN_CENTER_VERTICAL)
        MAINbox.Add(fnSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        ##################SEQUENCES
        line = wx.StaticLine(self.panel, wx.ID_ANY,style=wx.LI_HORIZONTAL )
        MAINbox.Add( line, 0, wx.ALL|wx.EXPAND, 2 )
        title2 = wx.StaticText(self.panel, label='Sequences')
        titlebox2.Add(title2, flag=wx.LEFT, border=8)
        MAINbox.Add(titlebox2, 0, wx.ALIGN_CENTER_VERTICAL)
        #getting some values to work with for sizing panel contents later...
        categLengths = {}
        for categories in self.setup.categoryDict.keys():
            categLengths[categories]=(len(self.setup.categoryDict[categories]))
        print categLengths
        categVals = list(categLengths.values())
        categKeys = list(categLengths.keys())
        categDenominator = (int(max(categVals)/5))
        for i in range(0,(len(categLengths))):
            if categDenominator == 0:
                categLengths[categKeys[i]]= 2
            elif categDenominator == 1:
                categLengths[categKeys[i]]= 2
            elif (categVals[i]/categDenominator) <= 2:
                categLengths[categKeys[i]]= 3
            elif (categVals[i]/categDenominator) <= 4:
                categLengths[categKeys[i]]= 4
            else:
                categLengths[categKeys[i]]=5
        #...now there is a dictionary with the panelsizer's columns for each category key.
        for categories in self.setup.categoryDict.keys():
            self.categPanes=[]
            self.categPanes.append(wx.CollapsiblePane(self.panel, -1, label=categories))
            self.buildPanes(self.categPanes[-1], seqSizer)
            thisPanel = self.categPanes[-1].GetPane()
            #sizer for the panel contents
            if categDenominator >= 2: #more than 10 sequences in a category
                panelSizer = wx.GridSizer( cols = categLengths[categories] )
            else:
                panelSizer = wx.GridSizer( cols = 2 )
            sortedCategory = self.setup.categoryDict[categories]
            sortedCategory.sort()
            for i in range(0,len(self.setup.categoryDict[categories])):
                thisSeq = wx.Button( thisPanel, label=sortedCategory[i], name=sortedCategory[i], size=(((len(sortedCategory[i])*7)+10),24))
                self.buildButtons(thisSeq, seqSizer, self.setup.seq[sortedCategory[i]].desc )
                panelSizer.Add( thisSeq, 0, wx.GROW | wx.ALL ,0 )
                thisPanel.SetSizer(panelSizer)
        panelSizer.SetSizeHints(thisPanel)
        #seqSizer.Add(panelSizer, wx.ALL)
        MAINbox.Add(seqSizer, 0, wx.ALL )
        ####################
        self.panel.SetSizerAndFit(MAINbox)
        self.Fit()

    def buildButtons(self, btn, sizer, desc):
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        btn.SetToolTip(wx.ToolTip(desc))

    def onButton(self, event):
        label = event.GetEventObject().GetLabel()
        s = str( 'setup.seq[\'%s\'].start(%s)'%(label, str(self.numActsTxtBox.GetValue())) )
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onFuncButton(self, event):
        s = str(event.GetEventObject().GetName())
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onRemoteOpenPort(self, event):
        s = 'ardu.OpenClosePort(1)'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onRemoteClosePort(self, event):
        s = 'ardu.OpenClosePort(0)'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    ####### EXTRA BUTTON FUNCTIONS #####
    def onLeft(self, event):
        try:
            nr=int(float(self.entrya1.GetValue()))
            t=int(float(self.entrya2.GetValue()))
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        s = 'setup.DropGenL(%d,%d)'%(nr,t)
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onRight(self, event):
        try:
            nr=int(float(self.entryb1.GetValue()))
            t=int(float(self.entryb2.GetValue()))
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        s = 'setup.DropGenR(%d,%d)'%(nr,t)
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onDouble(self, event):
        try:
            nr=int(float(self.entryb1.GetValue()))
            t=int(float(self.entryb2.GetValue()))
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        s = 'setup.DropGenD(%d,%d)'%(nr,t)
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onEncapsulate(self, event):
        try:
            nr=int(float(self.entry1.GetValue()))
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        s = str('setup.Encapsulate(%d)'%(nr))
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onRelease(self, event):
        try:
            nr=int(float(self.entry2.GetValue()))
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        s = 'setup.Release(%d)'%(nr)
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onKeep(self, event):
        try:
            nr=int(float(self.entry3.GetValue()))
            t=int(float(self.entry4.GetValue()))
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        s = 'setup.Keep(%d,%d)'%(nr,t)
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    def onKeepAllBut(self, event):
        try:
            nr=int(float(self.entry5.GetValue()))
            t=int(float(self.entry6.GetValue()))
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        s = 'setup.KeepAllBut(%d,%d)'%(nr,t)
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    ##############################

    def buildPanes(self, categPane, seqSizer):
        categPane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)
        seqSizer.Add(categPane, 0, wx.GROW | wx.ALL, 0)

    def OnPaneChanged(self, evt):
        self.panel.GetSizer().Layout()
        self.panel.Fit()
        self.Fit()
#########
if __name__ == "__main__":

    def fileChooser():
        root = Tkinter.Tk()
        root.withdraw()
        filename = tkFileDialog.askopenfilename()
        return filename

    ver = '3.0.2'
    date = '06/08/2018'
    print 'GUI: Protocol GUI Ver:%s'%(ver)
    print 'based on LLGUI (Laura Leclerc & Guy Soffer, 2018)'
    #Command line option parser
    parser = OptionParser()
    parser.add_option('-p', '--protocol', dest='prot', help='TBD', type='string', default='Demoprotocol')
    parser.add_option('-u', '--port', dest='port', help='Remote port to send the commands', type='int', default=7010)
    parser.add_option('-i', '--ip', dest='ip', help='Remote ip to send the commands', type='string', default='127.0.0.1')
    (options, args) = parser.parse_args()
    path = os.path.split(options.prot)

    #file chooser opens if no other file was specified in the additional text file
    if path[1] == 'Demoprotocol':
        newPath = fileChooser()
        path = os.path.split(newPath)
    else:
        print 'Loading protocol specified in accompanying address file, which is in your folder.'

    #parser resumes
    lib = str(path[1])[:-3]
    path = path[0]
    sys.path.append(path)
    #lib = options.prot
    print 'Importing %s'%(lib)
    print 'Using remote-ip:port -> %s:%d'%(options.ip, options.port)
    protocol = __import__(lib)
    setup = protocol.Setup(ExtGpio=False, gpio=False, chipViewer=False)
#    setup = protocol.Setup(ExtGpio=False, gpio=False, chipViewer=False, magPin=0)
#    setup.enOut(True)
    app = wx.App(False)
    frame = seqSelector(setup, ip=options.ip, port=options.port)
    frame.Show()
    app.MainLoop()
