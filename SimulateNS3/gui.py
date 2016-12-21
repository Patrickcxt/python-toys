from PIL import Image
import sys
import math
import wx
import os
import numpy as np
import matplotlib.pyplot as pil

#import hist
#import filter3


class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        super(MainWindow,self).__init__( parent, id, title, size=(600, 300))

        self.savetype = 0

        menuBar = wx.MenuBar()

        # File Menu
        filemenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file")
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", "Save a file")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        # Show Histogram Menu
        shmenu = wx.Menu()
        sh = shmenu.Append(-1, "Show Histogram")


        # Sharpen Menu
        funmenu = wx.Menu()
        hist = funmenu.Append(-1, "Histogram euqalization")
        sp1 = funmenu.Append(-1, "Average Filter")
        sp2 = funmenu.Append(-1, "Laplace Filter")
        sp3 = funmenu.Append(-1, "Sobel1 Filter")
        sp4 = funmenu.Append(-1, "Sobel2 Filter")

        # create the menubar
        menuBar.Append(filemenu, "&File")
        menuBar.Append(shmenu, "&Histogram")
        menuBar.Append(funmenu, "&Adjust")
        self.SetMenuBar(menuBar)

        # set events
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_MENU, self.OnShow_Histogram, sh)
        self.Bind(wx.EVT_MENU, self.OnEuqalize_hist, hist)

        self.Bind(wx.EVT_MENU, self.OnOptionalAverage, sp1)
        self.Bind(wx.EVT_MENU, lambda evt, mark=1 : self.OnFilter(evt, mark), sp2)
        self.Bind(wx.EVT_MENU, lambda evt, mark=2 : self.OnFilter(evt, mark), sp3)
        self.Bind(wx.EVT_MENU, lambda evt, mark=3 : self.OnFilter(evt, mark), sp4)


        self.Centre()
        self.Show(True)

    def OnOpen(self, e):
        file_wildcard = "png files(*.png)|*.png|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "Open png file...", os.getcwd(),style = wx.OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.sname = dlg.GetFilename()
            print self.sname
            self.source = Image.open(self.sname)
            self.PicShow = wx.StaticBitmap(self, -1, pos = (400, 200))
            self.im = wx.Image(self.sname)
            self.PicShow.SetBitmap(wx.BitmapFromImage(self.im))
            #self.SetTitle(self.title + '--' + self.filename)
        dlg.Destroy()

    def OnSave(self, e):
        file_wildcard = "png files(*.png)|*.png|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "Save image as ..", os.getcwd(), style = wx.SAVE|wx.OVERWRITE_PROMPT, wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.tname = dlg.GetFilename()
            if self.savetype == 0:
                self.source.save(self.tname)
            else:
                self.target.save(self.tname)
        dlg.Destroy()


    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A small image processor", "Image Processor", wx.Ok)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnShow_Histogram(self, e):
        if self.savetype == 0:
            self.target = hist.plot_hist(self.source)
        else:
            self.target = hist.plot_hist(self.target)

    def OnEuqalize_hist(self, e):
        self.target = hist.euqalize_hist(self.source)
        self.do()
        self.savetype = 1

    def OnFilter(self, e, mark):
        self.target = filter3.filter2d(self.source, mark, (3, 3))
        self.do()
        self.savetype = 1


    def OnQuantize(self, e, mark):
        self.level = mark
        self.do(1)
        self.savetype = 1

    def OnOptionalAverage(self, e):
        dlg = wx.TextEntryDialog(None, "Please input the size (width x height):", "Optional Filter Size")
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
            (width, height) = response.split('x')
        dlg.Destroy()
        self.target = filter3.filter2d(self.source, 0, (int(width), int(height)))
        self.do()
        self.savetype = 1


    def do(self):
        self.target.save("tmp.png")
        self.im = wx.Image("tmp.png")
        self.PicShow.SetBitmap(wx.BitmapFromImage(self.im))



if __name__ == '__main__':

    app = wx.App()
    frame = MainWindow(None, id = -1, title= "Simple Image Processor!")
    app.MainLoop()




