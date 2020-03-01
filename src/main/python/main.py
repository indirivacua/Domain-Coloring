from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from cmath import *
from dc import dcmod
import pygame
from os import getcwd
pygame.init()


class Error(QMessageBox):
    def __init__(self,text):
        super().__init__()
        self.setIcon(self.Critical)
        self.setWindowTitle('Error')
        self.setText(text)
        self.setStandardButtons(self.Ok)
        self.exec_()
        
class Warn(QMessageBox):
    def __init__(self,text):
        super().__init__()
        self.setIcon(self.Warning)
        self.setWindowTitle('Warning')
        self.setText(text)
        self.setStandardButtons(self.Ok | self.Abort)
        self.ans=self.exec_()
        if self.ans==self.Ok:
            self.ans=True
        else:
            self.ans=False
            
class Info(QMessageBox):
    def __init__(self,title,text):
        super().__init__()
        self.setIcon(self.Information)
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(self.Ok)
        self.exec_()
        

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.name="Domain Coloring"
        self.graphed=False
        self.initUI()
        
    def closeEvent(self,event):
        #app.exit()
        exit(0)
        
    def work(self,b):
        if b==self.rb1 and b.isChecked():
            self.aafactor=1
        elif b==self.rb2 and b.isChecked():
            self.aafactor=2
        elif b==self.rb3 and b.isChecked():
            self.aafactor=4

    def graphit(self):

        #Warn user on their first time.
        if "True" in open(appctxt.get_resource("first")).read():
            Info("Time","The graphs take some time to generate. Be patient.\nYou can make it faster by lowering the smoothing factor or decreasing the resolution.")
            with open(appctxt.get_resource("first"),'w') as f:
                f.write("False")

        funstr=self.fun.text()
        funstr=funstr.replace("^","**")
        fun=eval("lambda z:"+funstr)
        w=int(self.xscreen.text())
        h=int(self.yscreen.text())
        self.img=dcmod.color_it(int(self.xrange.text()),int(self.yrange.text()),float(self.scale.text()),(w,h),self.aafactor,fun)

        graph=pygame.image.fromstring(self.img.tobytes(),self.img.size,self.img.mode)
        pygame.display.set_caption("Domain Coloring")
        screen=pygame.display.set_mode((w,h))
        screen.blit(graph,(0,0))
        pygame.display.flip()

        self.graphed=True

    def saveit(self):

        if self.graphed:
            out_dia=QFileDialog()
            out_dia.setFileMode(QFileDialog.AnyFile)
            out_dia.setAcceptMode(QFileDialog.AcceptSave)
            file_ops="Image Files (*.png *.jpg *.gif *.bmp) ;; All Files (*.*)"
            outpath=out_dia.getSaveFileName(self,'Open file',getcwd(),file_ops)[0]

            if outpath:
                self.img.save(outpath)
                Info("Saved","Graph saved as "+str(outpath))
        else:
            Error("You need to graph something first!")
        
    def initUI(self):
        self.layout=QVBoxLayout()
        self.def_box=QGroupBox("Advanced Settings")
        self.def_lay=QVBoxLayout()
        appctxt.app.setStyle('Fusion')
        self.setWindowTitle(self.name)

        #Scale selector
        self.scalelay=QHBoxLayout()
        scale_label=QLabel('Brightness scale (0-1):')
        scale_label.setAlignment(Qt.AlignCenter)
        self.scale=QLineEdit("0.6")
        self.scalelay.addWidget(scale_label)
        self.scalelay.addWidget(self.scale)

        #Range selectors
        self.rangelay=QHBoxLayout()
        xrange_label=QLabel('x axis range:')
        xrange_label.setAlignment(Qt.AlignCenter)
        self.xrange=QLineEdit("6")
        yrange_label=QLabel(' y axis range:')
        yrange_label.setAlignment(Qt.AlignCenter)
        self.yrange=QLineEdit("6")

        self.rangelay.addWidget(xrange_label)
        self.rangelay.addWidget(self.xrange)
        self.rangelay.addWidget(yrange_label)
        self.rangelay.addWidget(self.yrange)

        #Screen dimension selectors
        self.screenlay=QHBoxLayout()
        xscreen_label=QLabel('Image resolution:')
        xscreen_label.setAlignment(Qt.AlignCenter)
        self.xscreen=QLineEdit("700")
        yscreen_label=QLabel('by')
        yscreen_label.setAlignment(Qt.AlignCenter)
        self.yscreen=QLineEdit("700")

        self.screenlay.addWidget(xscreen_label)
        self.screenlay.addWidget(self.xscreen)
        self.screenlay.addWidget(yscreen_label)
        self.screenlay.addWidget(self.yscreen)

        #Radio buttons
        self.radlay=QHBoxLayout()
        self.aafactor=1
        self.radlay.addWidget(QLabel('Smoothing factor: '))
        self.rb1=QRadioButton("1")
        self.rb1.setChecked(True)
        self.rb1.toggled.connect(lambda:self.work(self.rb1))
        self.radlay.setAlignment(Qt.AlignLeft)
        self.radlay.addWidget(self.rb1)
        
        self.radlay.addItem(QSpacerItem(20,0))
        
        self.rb2=QRadioButton("2")
        self.rb2.setChecked(False)
        self.rb2.toggled.connect(lambda:self.work(self.rb2))
        self.radlay.addWidget(self.rb2)

        self.radlay.addItem(QSpacerItem(20,0))
        
        self.rb3=QRadioButton("4")
        self.rb3.setChecked(False)
        self.rb3.toggled.connect(lambda:self.work(self.rb3))
        self.radlay.addWidget(self.rb3)

        #Function entry
        self.funlay=QHBoxLayout()
        fun_label=QLabel('Function:')
        fun_label.setAlignment(Qt.AlignCenter)
        self.fun=QLineEdit("sin(z)")
        self.funlay.addWidget(fun_label)
        self.funlay.addWidget(self.fun)

        #Graph and save buttons
        self.graph_but=QPushButton("Graph")
        self.graph_but.clicked.connect(self.graphit)
        self.save_but=QPushButton("Save as image")
        self.save_but.clicked.connect(self.saveit)
        
        #Final init
        self.layout.setSpacing(15)
        self.setLayout(self.layout)
        self.layout.addLayout(self.funlay)
        self.layout.addLayout(self.rangelay)
        self.layout.addLayout(self.screenlay)

        self.layout.addItem(QSpacerItem(0,10))
        self.def_lay.setSpacing(15)
        self.def_lay.addLayout(self.scalelay)
        self.def_lay.addLayout(self.radlay)
        self.def_box.setLayout(self.def_lay)
        self.layout.addWidget(self.def_box)
        
        self.layout.addWidget(self.graph_but)
        self.layout.addWidget(self.save_but)

if __name__=="__main__":
    appctxt=ApplicationContext()
    window=Window()
    window.show()
    appctxt.app.exec_()
