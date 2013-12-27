# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import time

class CoverLabel(QtGui.QLabel):
  ''' 封面按钮 '''
  def __init__(self, parent):
    super(CoverLabel, self).__init__(parent)
    self.setFixedSize(QtCore.QSize(300, 300))
    self.__parent = parent

  def set_img(self, img_path='temp/cover'):
    self.setPixmap(QtGui.QPixmap(img_path))

class LoveBtn(QtGui.QLabel):
  ''' 是否喜爱的按钮 '''
  def __init__(self, parent, love_img, normal_img,
               love_hover_img, normal_hover_img, love):
    super(LoveBtn, self).__init__(parent)
    self.__love_img = QtGui.QPixmap(love_img)
    self.__normal_img = QtGui.QPixmap(normal_img)
    self.__love_hover_img = QtGui.QPixmap(love_hover_img)
    self.__normal_hover_img = QtGui.QPixmap(normal_hover_img)
    self.setFixedSize(QtCore.QSize(40, 40))
    self.set_img(love)

  def mouseReleaseEvent(self, event):
    if self.__love:
      self.setPixmap(self.__normal_hover_img)
    else:
      self.setPixmap(self.__love_hover_img)
    self.__love = False if self.__love else True
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    if self.__love:
      self.setPixmap(self.__love_hover_img)
    else:
      self.setPixmap(self.__normal_hover_img)

  def leaveEvent(self, event):
    if self.__love:
      self.setPixmap(self.__love_img)
    else:
      self.setPixmap(self.__normal_img)

  def set_img(self, love):
    self.__love = True if love == 'l' else False
    if self.__love:
      self.setPixmap(self.__love_img)
    else:
      self.setPixmap(self.__normal_img)

class ImageBtn(QtGui.QLabel):
  def __init__(self, parent, normal_img, hover_img):
    super(ImageBtn, self).__init__(parent)
    self.__normal_img = QtGui.QPixmap(normal_img)
    self.__hover_img = QtGui.QPixmap(hover_img)
    self.setPixmap(self.__normal_img)
    self.setFixedSize(QtCore.QSize(40, 40))

  def mouseReleaseEvent(self, event):
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    self.setPixmap(self.__hover_img)
    
  def leaveEvent(self, event):
    self.setPixmap(self.__normal_img)

class ToggleBtn(QtGui.QLabel):
  def __init__(self, parent, enable_img, disable_img, enable=True):
    super(ToggleBtn, self).__init__(parent)
    self.__enable_img = QtGui.QPixmap(enable_img)
    self.__disable_img = QtGui.QPixmap(disable_img)
    self.setFixedSize(QtCore.QSize(120, 120))
    self.__enable = enable
    
  def __set_img(self):
    if self.__enable:
      self.setPixmap(self.__enable_img)
    else:
      self.setPixmap(self.__disable_img)

  def mouseReleaseEvent(self, event):
    self.__enable = False if self.__enable else True
    self.__set_img() 
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    self.__set_img()

  def leaveEvent(self, event):
    self.setPixmap(QtGui.QPixmap(None))


class ProcessBar(QtGui.QWidget):
  def __init__(self, parent):
    super(ProcessBar, self).__init__(parent)
    self.__width = 300
    self.__rate = 0.0
    self.setMinimumSize(300, 2)
    self.connect(self, QtCore.SIGNAL("update_rate(float)"), self.set_rate)
    self.__normal_color = QtGui.QColor(0x33,0x33,0x33)
    self.__played_color = QtGui.QColor(0x99,0x99,0x99)

  def paintEvent(self, e):
    qp = QtGui.QPainter()
    qp.begin(self)
    self.__draw_bg(qp)
    qp.end()

  def __draw_bg(self, qp):
    mid = int(self.__width * self.__rate)
    qp.setPen(self.__played_color)
    qp.drawRect(0, 0, mid, 1)
    qp.setPen(self.__normal_color)
    qp.drawRect(mid, 0, self.__width, 1)

  def set_rate(self, rate):
    self.__rate = rate
    self.repaint()

   
class QTimer(QtCore.QTimer):
  # ms
  def __init__(self, interval):
    super(QTimer, self).__init__()
    self.__interval = interval
    self.__timer = QtCore.QTimer()
    QtCore.QObject.connect(
      self.__timer,
      QtCore.SIGNAL("timeout()"),
      self.__on_timer
    )
    self.init()
  
  def init(self):
    self.__start_time = time.time() # ms
    self.__remnant_time = 0 # ms

  def __on_timer(self):
    self.__timer.stop()
    self.emit(QtCore.SIGNAL("timeout()"))
    self.start(self.__interval)

  def pause(self):
    if self.isActive():
      self.stop()
      self.__remnant_time = 1000 - (( time.time() - self.__start_time ) % 1000)
    else:
      if self.__remnant_time:
        self.__timer.start(self.__remnant_time)
      else:
        self.start(self.__interval)
  
