#-*- coding: utf-8 -*-
import sys
import math
import wx
#from pylab import *
import os


class MainWindow(wx.Frame):

    def __init__(self, parent, id, title):
        super(MainWindow,self).__init__( parent, id, title, size=(1060, 600))
        width = 1060
        height = 600

        self.PicShow = None


        # 参数选择框
        panel = wx.Panel(self)
        firstPanel = wx.Panel(panel, pos=(0, 0), size=(width, 40))

        #下半部分布局
        leftPanel = wx.Panel(panel, pos=(0, 100), size=(100, 500))
        midPanel = wx.Panel(panel, pos=(100, 100), size=(750, 500))
        rightPanel = wx.Panel(panel, pos=(850, 100), size=(250, 500))


        # 获取图片存放路径及名称
        self.path = wx.TextCtrl(midPanel, -1, '', style=wx.TE_READONLY, pos=(50, 10), size=(580, 30))
        browse = wx.Button(midPanel, label='浏览', pos=(640, 10), size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.showPicture, browse)

        # 图片显示区域
        self.picSize = (670, 400)    # 图片显示区大小
        self.picPanel = wx.Panel(midPanel, pos=(50, 50), size=self.picSize, style=wx.SIMPLE_BORDER)

        # 触发按钮区域

        self.x_text = wx.StaticText(rightPanel, label = 'X:', style=wx.ALIGN_RIGHT,pos=(30, 110), size=(40, 30))
        self.xpos = wx.TextCtrl(rightPanel, -1, '', style=wx.TE_READONLY, pos=(50, 100), size=(80, 35))
        self.y_text = wx.StaticText(rightPanel, label = 'Y:', style=wx.ALIGN_RIGHT,pos=(30, 210), size=(40, 30))
        self.ypos = wx.TextCtrl(rightPanel, -1, '', style=wx.TE_READONLY, pos=(50, 200), size=(80, 35))
        confirm = wx.Button(rightPanel, label='Save', pos=(10, 300), size=(80, 40))
        cancel = wx.Button(rightPanel, label='Cancel', pos=(100, 300), size=(80, 40))
        reset = wx.Button(rightPanel, label='Reset', pos=(50, 400), size=(80, 40))
        self.Bind(wx.EVT_BUTTON, self.confirm, confirm)
        self.Bind(wx.EVT_BUTTON, self.cancel, cancel)
        self.Bind(wx.EVT_BUTTON, self.reset, reset)

        self.Centre()
        self.Show(True)



    def showPicture(self, e):
        """
        显示图片
        """
        if self.PicShow is not None:
            self.PicShow.Destroy()

        file_wildcard = "png files(*.png)|*.png|(*.jpg)|*.jpg|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, 'Open file...', os.getcwd(), style=wx.OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.picName = dlg.GetFilename()
            self.picPath = dlg.GetPath()
            print(self.picPath)
            self.path.SetValue(self.picPath)
            im = wx.Image(self.picPath)
            stX = (self.picSize[0] - im.GetWidth()) / 2
            stY = (self.picSize[1] - im.GetHeight()) / 2
            self.PicShow = wx.StaticBitmap(self.picPanel, -1, pos=(stX, stY)) # 此处根据图片大小调整pos位置
            self.PicShow.SetBitmap(wx.BitmapFromImage(im))

            self.show_all_point(None)
            self.PicShow.Bind(wx.EVT_LEFT_DCLICK, self.mark)


        #x = ginput(3)
        dlg.Destroy()

    def show_all_point(self, ip):
        im_name = self.picName
        fn = './results/' + im_name.split('.')[0] + '.txt'
        if not os.path.isfile(fn):
            os.system('touch ' + fn)
        f = open(fn, 'r')
        points = []
        if ip is not None:
            points.append(ip)

        for line in f:
            p = line.strip('\r\n').split('\t')
            p[0], p[1] = int(p[0]), int(p[1])
            points.append(p)

        img = wx.Image(self.path.GetValue(), wx.BITMAP_TYPE_ANY)
        #bit = wx.EmptyBitmap(517, 524)
        imgBit = wx.BitmapFromImage(img)
        dc = wx.MemoryDC(imgBit)
        dc.SetPen(wx.Pen(wx.RED, 3))

        for i in range(len(points)):
            p = points[i]
            lt = (p[0]-1, p[1]-1)
            rt = (p[0]+1, p[1]-1)
            lb = (p[0]-1, p[1]+1)
            rb = (p[0]+1, p[1]+1)

            dc.DrawLines((lt, rt, rb, lb, lt))

        dc.SelectObject(wx.NullBitmap)
        self.PicShow.SetBitmap(imgBit)
        imgBit.SaveFile('bit.bmp', wx.BITMAP_TYPE_BMP)

    def mark(self, e):
        p = e.GetPosition()
        self.xpos.SetValue(str(p[0]))
        self.ypos.SetValue(str(p[1]))


        self.show_all_point(p)
        #imgBit.SaveFile('bit.bmp', wx.BITMAP_TYPE_BMP)


    def confirm(self, e):
        if self.PicShow is None:
            return
        im_name = self.picName
        fn = './results/' + im_name.split('.')[0] + '.txt'
        f = open(fn, 'a+')
        x = self.xpos.GetValue()
        y = self.ypos.GetValue()

        print('Saving (' + self.xpos.GetValue() + ', ' + self.ypos.GetValue() + ')')
        f.write(x + '\t' + y + '\n')
        f.close()
        self.show_all_point(None)

    def cancel(self, e):
        if self.PicShow == None:
            return
        im_name = self.picName
        fn = './results/' + im_name.split('.')[0] + '.txt'
        with open(fn) as f:
            lines = f.readlines()
            curr = lines[:-1]
        f = open(fn, 'w')
        f.writelines(curr)
        f.close()
        self.show_all_point(None)


    def reset(self, e):
        if self.PicShow == None:
            return
        fn = './results/' + self.picName.split('.')[0] + '.txt'
        if os.path.isfile(fn):
            os.system('rm ' + fn)
        self.show_all_point(None)





if __name__ == '__main__':

    app = wx.App()
    frame = MainWindow(None, id = -1, title= "Image Marking Tool")
    app.MainLoop()




