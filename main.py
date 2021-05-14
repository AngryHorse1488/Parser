import os, sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
    QSizePolicy, QLabel, QFontDialog, QApplication, QFileDialog,)
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
import functions as fc
from tensorflow.keras.models import load_model
import GUI2
import dialog
from learning import learning
#from dialog import Ui_Dialog as dialog

class Label:
    def f(self1, self):
        print(self.name.text())
        
    def open(nisemono, self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(caption = "Выберите папку")
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            #for file_name in os.listdir(directory):  # для каждого файла в директории
            self.path.setText(directory)   # добавить файл в listWidget


    def __init__(self, path, name, check, btn):
        self.check = check
        self.path = path
        self.name = name
        self.btn = btn

        self.btn.clicked.connect(lambda: self.open(self))
        
            

class ExampleAppDialog(QtWidgets.QDialog, dialog.Ui_Dialog):
    
    def __init__(self):
            
        super().__init__()
        self.setupUi(self)
        self.Undo.clicked.connect(self.close)
        self.Start.clicked.connect(self.learning_)

        self.labeles_list = []

        self.labeles_list.append(Label(self.lineEdit_4, self.lineEdit_6,  self.checkBox,   self.pushButton)) 
        self.labeles_list.append(Label(self.lineEdit_3,   self.lineEdit_7,  self.checkBox_2, self.pushButton_2))
        self.labeles_list.append(Label(self.lineEdit, self.lineEdit_8,  self.checkBox_3, self.pushButton_3))
        self.labeles_list.append(Label(self.lineEdit_2, self.lineEdit_9, self.checkBox_4, self.pushButton_4))
        self.labeles_list.append(Label(self.lineEdit_5, self.lineEdit_10, self.checkBox_5, self.pushButton_5))
        self.NameProgramm()



    def NameProgramm(self): #смена имени и иконки
            self.setWindowTitle('Docthrush Learning')
            self.setWindowIcon(QIcon('icon.ico'))
    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.lineEdit.setText(directory)   # добавить файл в listWidget

    def learning_(self):
        paths = []
        classnames = []
        
        modelname = self.ClassName_line.text()

        if not modelname:
        	print('Please input the name of the model')
        	return

        for i in range(5):
            if self.labeles_list[i].check.isChecked():
                path = self.labeles_list[i].path.text()
                if not os.path.isdir(path):
                    print(f'Please select correct paths (incorrect path {i + 1})')
                    return
                paths.append(self.labeles_list[i].path.text())
                classnames.append(self.labeles_list[i].name.text())

        if not (len(paths) == 0):
            print(paths, '\n\n', classnames, '\n\n', modelname)
            try:
                learning(paths, classnames, modelname)
            except Exception as e:
                print('Please select correct paths')
                print(e)
        else:
            print('Please select paths')
        
    

    

class ExampleApp(QtWidgets.QMainWindow, GUI2.Ui_MainWindow): #main
    
    

    def browse_folder(self):
        self.lineEdit.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            
            self.lineEdit.setText(directory)   # добавить файл в listWidget

    def browse_model(self):
        self.lineEdit_2.clear()
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")
        # print(directory[0])
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
           
            self.lineEdit_2.setText(directory[0])   # добавить файл в listWidget
   
   
    def use(self, modelname):
    
        if not (os.path.isdir(self.lineEdit.text()) and os.path.isfile(self.lineEdit_2.text())):
            print('Please select correct paths') 
            return

        try:
            model=load_model(self.lineEdit_2.text())
            pred = fc.usenet(self.lineEdit.text(), model)

            fc.rename(self.lineEdit.text(), self.lineEdit_2.text(), pred)
        except OSError:
            print('Please select correct paths')  
                

    def NameProgramm(self): #смена имени и иконки
            self.setWindowTitle('Docthrush')
            self.setWindowIcon(QIcon('icon.ico'))
    

    
    def __init__(self):       
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_2.clicked.connect(self.use)
        self.dial = ExampleAppDialog()
        self.Learning.clicked.connect(self.dial.exec)###############################################################################
        self.ClassButton.clicked.connect(self.browse_model)
        self.NameProgramm()
    


def main():
    os.system("cls")
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    main_window = ExampleApp()  # Создаём объект класса ExampleApp
    main_window.show()  # Показываем окно
    dial = ExampleAppDialog()
    app.exec_()  # и запускаем приложение
   
      
    

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()