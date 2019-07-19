import cv2
import socket
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

UDP_IP = "10.1.1.128"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#openCV IP camera capture (seperate window from control panel)
class Capture():
    def __init__(self):
        self.capturing = False
        self.c = cv2.VideoCapture("http://10.1.1.128:8080/stream/video.mjpeg")

    def startCapture(self):
        print ("pressed start")
        self.capturing = True
        cap = self.c
        while(self.capturing):
            ret, frame = cap.read()
            cv2.imshow("Capture", frame)
            cv2.waitKey(5)
        cv2.destroyAllWindows()

    def endCapture(self):
        print ("pressed End")
        self.capturing = False

    def quitCapture(self):
        print ("pressed Quit")
        cap = self.c
        cv2.destroyAllWindows()
        cap.release()
        QtCore.QCoreApplication.quit()
        
    def upCapture(self):
        print ("up")
        sock.sendto(str.encode("up"), (UDP_IP, UDP_PORT))
    
    def downCapture(self):
        print ("down")
        sock.sendto(str.encode("down"), (UDP_IP, UDP_PORT))

#Control panel window
class Window(QtWidgets.QWidget):
    def __init__(self):

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Control Panel')

        self.capture = Capture()
        self.start_button = QtWidgets.QPushButton('Start',self)
        self.start_button.clicked.connect(self.capture.startCapture)

        self.end_button = QtWidgets.QPushButton('End',self)
        self.end_button.clicked.connect(self.capture.endCapture)

        self.quit_button = QtWidgets.QPushButton('Quit',self)
        self.quit_button.clicked.connect(self.capture.quitCapture)
        
        self.up_button = QtWidgets.QPushButton('up',self)
        self.up_button.clicked.connect(self.capture.upCapture)
        
        self.down_button = QtWidgets.QPushButton('down',self)
        self.down_button.clicked.connect(self.capture.downCapture)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.end_button)
        vbox.addWidget(self.quit_button)
        vbox.addWidget(self.up_button)
        vbox.addWidget(self.down_button)

        self.setLayout(vbox)
        self.setGeometry(100,100,200,200)
        self.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
