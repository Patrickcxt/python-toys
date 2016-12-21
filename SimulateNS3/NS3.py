#-*- coding: utf-8 -*-
import sys
import math
import wx
import os


class MainWindow(wx.Frame):

    def __init__(self, parent, id, title):
        super(MainWindow,self).__init__( parent, id, title, size=(1060, 600))
        width = 1060
        height = 600

        # 以下为下拉框参数,需自行修改
        topoList = ['三层树', 'fattree', 'Bcube', 'Dcell']           # 拓扑
        nodeNumList = [str(i) for i in range(1, 129)]                # 节点数
        otherList = ['1', '2', '3', '4', '5']                        #其他参数
        flowModelList = ['one-to-one', 'all-to-all', 'one-to-many']  # 流量模型
        nodeWayList = ['uniform', 'stride', 'staggered']             # 节点选取方式
        onList = ['CBR', 'Uniform', 'exponential', 'lognormal']      # on-off流量(on)
        offList = ['CBR', 'Uniform', 'exponential', 'lognormal']     # on-off流量(off)

        # 参数选择框
        panel = wx.Panel(self)
        firstPanel = wx.Panel(panel, pos=(0, 0), size=(width, 40))
        #firstPanel = wx.Panel(panel, pos=(0, 0), size=(900, 40), style=wx.SIMPLE_BORDER)
        self.but1_1 = wx.StaticText(firstPanel, label = '拓扑选择', style=wx.ALIGN_CENTER, pos=(30, 10), size=(100, 30))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.but1_1.SetFont(font)
        self.but1_2 = wx.StaticText(firstPanel, label = '拓扑:', style=wx.ALIGN_RIGHT,pos=(130, 13), size=(60, 30))
        self.but1_3 = wx.ComboBox(firstPanel, choices=topoList, style=wx.CB_DROPDOWN, pos=(200, 10), size=(120, 30))
        self.but1_4 = wx.StaticText(firstPanel, label = '节点数:', style=wx.ALIGN_RIGHT, pos=(330, 13), size=(100, 30))
        self.but1_5 = wx.ComboBox(firstPanel, choices=nodeNumList, style=wx.CB_DROPDOWN, pos=(430, 10), size=(120, 30))
        self.but1_6 = wx.StaticText(firstPanel, label = '其他参数:', style=wx.ALIGN_RIGHT, pos=(560, 13), size=(120, 30))
        self.but1_7 = wx.ComboBox(firstPanel, choices=otherList, style=wx.CB_DROPDOWN, pos=(680, 10), size=(120, 30))

        secondPanel = wx.Panel(panel, pos=(0, 40), size=(width, 40))
        #secondPanel = wx.Panel(panel, pos=(0, 40), size=(900, 40), style=wx.SIMPLE_BORDER)
        self.but2_1 = wx.StaticText(secondPanel, label = '流量选择', pos=(30, 10), size=(100, 30))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.but2_1.SetFont(font)
        self.but2_2 = wx.StaticText(secondPanel, label = '流量模型:', pos=(130, 13), size=(80, 30))
        self.but2_3 = wx.ComboBox(secondPanel, choices=flowModelList, style=wx.CB_DROPDOWN, pos=(200, 10), size=(120, 30))
        self.but2_4 = wx.StaticText(secondPanel, label = '节点选取方式:', pos=(330, 13), size=(100, 30))
        self.but2_5 = wx.ComboBox(secondPanel, choices=nodeWayList, style=wx.CB_DROPDOWN, pos=(430, 10), size=(120, 30))
        self.but2_6 = wx.StaticText(secondPanel, label = 'on-off流量(on):', pos=(560, 13), size=(110, 30))
        self.but2_7 = wx.ComboBox(secondPanel, choices=onList, style=wx.CB_DROPDOWN, pos=(680, 10), size=(120, 30))
        self.but2_8 = wx.StaticText(secondPanel, label = 'on-off流量(off):', pos=(810, 13), size=(110, 30))
        self.but2_9 = wx.ComboBox(secondPanel, choices=offList, style=wx.CB_DROPDOWN, pos=(920, 10), size=(120, 30))

        self.init()   # 将所有下拉框(除节点数外)设置为不可编辑

        # 下拉框响应
        self.Bind(wx.EVT_COMBOBOX, self.limit_1, self.but2_3)
        self.Bind(wx.EVT_COMBOBOX, self.limit_2, self.but2_7)
        self.Bind(wx.EVT_COMBOBOX, self.limit_3, self.but2_9)

        #下半部分布局
        leftPanel = wx.Panel(panel, pos=(0, 100), size=(100, 500))
        self.midPanel = wx.Panel(panel, pos=(100, 100), size=(750, 500))
        rightPanel = wx.Panel(panel, pos=(850, 100), size=(150, 500))


        # 获取图片存放路径及名称
        self.path = wx.TextCtrl(self.midPanel, -1, '', style=wx.TE_READONLY, pos=(50, 10), size=(580, 30))
        browse = wx.Button(self.midPanel, label='浏览', pos=(640, 10), size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.showPicture, browse)

        # 图片显示区域
        self.picSize = (670, 400)    # 图片显示区大小
        self.picPanel = wx.Panel(self.midPanel, pos=(50, 50), size=self.picSize, style=wx.SIMPLE_BORDER)

        # 触发按钮区域
        simulate = wx.Button(rightPanel, label='开始仿真', pos=(0, 100), size=(80, 40))
        animate = wx.Button(rightPanel, label='仿真过程动画显示', pos=(0, 200), size=(140, 40))
        self.Bind(wx.EVT_BUTTON, self.Simulate, simulate)
        self.Bind(wx.EVT_BUTTON, self.Animate, animate)


        self.Centre()
        self.Show(True)

    def init(self):
        """
        将所有下拉框(除节点数外)设置为不可编辑
        """

        self.but1_3.SetEditable(False)
        self.but1_7.SetEditable(False)
        self.but2_3.SetEditable(False)
        self.but2_5.SetEditable(False)
        self.but2_7.SetEditable(False)
        self.but2_9.SetEditable(False)

    def limit_1(self, e):
        """
        若流量模型为all-to-all, 则节点选取方式不可选
        """
        if (self.but2_3.GetValue() == 'all-to-all'):
            self.but2_5.SetValue('')
            self.but2_5.Enable(False)
        else:
            self.but2_5.Enable(True)

    def limit_2(self, e):
        """
        若on-off(on) 选择CBR，则on-off(off) 也必须为CBR
        """
        if self.but2_7.GetValue() == 'CBR':
            self.but2_9.SetValue('CBR')
            self.but2_9.Enable(False)
        elif self.but2_9.GetValue() == 'CBR':
            self.but2_9.SetValue('')
            self.but2_9.Enable(True)
        else:
            self.but2_9.Enable(True)


    def limit_3(self, e):
        """
        若on-off(off) 选择CBR，则on-off(on) 也必须为CBR
        """
        if self.but2_9.GetValue() == 'CBR':
            self.but2_7.SetValue('CBR')
            self.but2_7.Enable(False)
        elif self.but2_7.GetValue() == 'CBR':
            self.but2_7.SetValue('')
            self.but2_7.Enable(True)
        else:
            self.but2_7.Enable(True)


    def showPicture(self, e):
        """
        显示图片
        """

        self.picPanel = wx.Panel(self.midPanel, pos=(50, 50), size=self.picSize, style=wx.SIMPLE_BORDER)
        file_wildcard = "png files(*.png)|*.png|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, 'Open file...', os.getcwd(), style=wx.OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.picPath = dlg.GetPath()
            self.path.SetValue(self.picPath)
            im = wx.Image(self.picPath)
            stX = (self.picSize[0] - im.GetWidth()) / 2
            stY = (self.picSize[1] - im.GetHeight()) / 2
            PicShow = wx.StaticBitmap(self.picPanel, -1, pos=(stX, stY)) # 此处根据图片大小调整pos位置
            PicShow.SetBitmap(wx.BitmapFromImage(im))
        dlg.Destroy()


    def Simulate(self, e):
        """
        执行仿真函数
        """
        # 获取所有选择参数
        topo = self.but1_3.GetValue()        # 拓扑
        numOfNode = self.but1_5.GetValue()   # 节点数
        otherArg = self.but1_7.GetValue()    # 其他参数
        flowModel = self.but2_3.GetValue()   # 流量模型
        nodeChoice = self.but2_5.GetValue()  # 节点选取方式
        on = self.but2_7.GetValue()          # on-off流量(on)
        off = self.but2_9.GetValue()         # on-off流量(off)

        command = './waf --run "my/scratch/test'
        command += ' --topo=' + str(topo)
        command += ' --numOfNode=' + str(numOfNode)
        command += ' --otherArg=' + str(otherArg)
        command += ' --flowMode=' + str(flowModel)
        command += ' --nodeChoice=' + str(nodeChoice)
        command += ' --on=' + str(on)
        command += ' --off=' + str(off)
        command += '"'
        #print command

        # 调用命令行
        os.system(command)

    def Animate(self, e):
        """
        此处填入仿真过程动画显示所需要的命令行
        """

        # 调用命令行
        #os.system('~/mySoftware/ns3/netanim-3.104/./NetAnim')
        os.system('cd ~/code & ./main')
        os.system('./main')


if __name__ == '__main__':

    app = wx.App()
    frame = MainWindow(None, id = -1, title= "NS3仿真平台")
    app.MainLoop()




