
import sympy as sp
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel,QApplication,QDialog,QTextEdit, QMainWindow,QSplitter,QCheckBox, QVBoxLayout,QComboBox, QWidget, QLabel, QPushButton, QHBoxLayout,QLineEdit,QFormLayout
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from ploting_and_animation import plot,animate_rectangle,animate_trapeze, animate_simpson,Plot3D
from logica import solve_simpson,solve_rectangle,solve_trapeze,solve_Gauss_Chebyshev,solve_Trapeze_R2_v1,solve_Trapeze_R2_v2,solve_simpson_R2,solve_Gauss_Legendre,solve_composite_rectangle,solve_composite_simpson,solve_composite_trapeze
import re
from csv_txt_etc import ReadCSV,Rez_CSV,SaveCSV,ReadTXT,SolveTXT
class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        
        self.df=None
        self.rezz=None
        self.initUI()
        
        self.setupConnections()
    def initUI(self):
        
        ##fereastra aplicatie principala
        self.setWindowTitle('Quadrature_author_Ciofu_Dragos')
        self.setFixedSize(1520, 855)  
        
        #fereastra canvas pentru animatie
        self.figure=plt.figure(figsize=(10,10), facecolor='#1a1a1a')
        self.figure.suptitle('Zona de plotare si animare', fontsize=25, color='white')
        self.canvas = FigureCanvas(self.figure)
        
        self.canvas.setParent(self)
        self.canvas.resize(1000, 800)
        self.canvas.move(20, 20)
        
        #layouts , pentru organizare
        self.layout_principal = QVBoxLayout()
        self.layout_input_f = QFormLayout()
        self.layout_butoane_csv = QHBoxLayout()
        self.layout_csv = QVBoxLayout()
        self.layout_rez = QHBoxLayout()
        self.layout_optiuni = QHBoxLayout()
        self.layout_optiuni2 = QHBoxLayout()
        self.layout_butoane_solve = QHBoxLayout()
        
        #container pentru widgeturile de input manual al functiei
        self.container = QWidget(self)
        self.container.setGeometry(1030, 20, 450, 800)
        self.container.setLayout(self.layout_principal)
        
        ##font si size pentru text
        self.label_font = QFont("Arial Black", 11, QFont.Bold)
        self.label_font2 = QFont("Arial Black", 11, QFont.Bold)
        self.font_title = QFont('Arial Black', 17, QFont.Bold)
        self.font_title2 = QFont('Arial Black', 17, QFont.Bold)
        #qlabels pentru introducerea datelor corespunzator
        #labels layout_sec1
        self.label_functie = QLabel("Functie: ")
        self.label_interval = QLabel("Interval [a,b]: ")
        self.label_iteratii = QLabel("Iteratii: ")
        self.label_eroare = QLabel("Eroare: ")
        self.label_rezolvare = QLabel("Solve si optiuni ")
        self.label_method = QLabel("Metoda quadratura ")
        self.label_input = QLabel("Optiuni input si 'ghid'")
        self.label_result = QLabel('Rezultat :')
        
        #butoane
        self.button_incarcare = QPushButton("Incarca .csv")
        self.button_incarcare.setFixedSize(120, 40)
        self.button_incarcare2 = QPushButton("Incarca .txt")
        self.button_incarcare2.setFixedSize(120, 40)
        self.button_info = QPushButton("Ghid")
        self.button_info.setFixedSize(120, 40)
        self.button_rezolvare = QPushButton("Rezolva")
        self.button_rezolvare.setFixedSize(120, 40)
        self.button_rez_txt = QPushButton("Rezolva (csv/txt)")
        self.button_rez_txt.setFixedSize(120, 40)
        self.button_rez_down = QPushButton("Rezolva mp4/img")
        self.button_rez_down.setFixedSize(120, 40)
        self.button_info.setStyleSheet("""
    border: 2px solid red;
    color: red;
""")
        #combobox
        self.combo = QComboBox()
        self.combo.setFixedSize(160, 30)
        self.combo.addItem("simpson")
        self.combo.addItem('dreptunghi')
        self.combo.addItem('trapez')
        self.combo.addItem("compozita simpson")
        self.combo.addItem('compozita dreptunghi')
        self.combo.addItem('compozita trapez')
        self.combo.addItem("Gauss Legendre")
        self.combo.addItem('Gauss Chebyshev')
        self.combo.addItem('trapez R**2')
        self.combo.addItem('trapez v2 R**2')
        self.combo.addItem('simpson R**2')
        
        #checkboxuri
        self.checkbox1 = QCheckBox("animatie metoda ")
        self.checkbox2 = QCheckBox("erori")
        self.checkbox3 = QCheckBox("timp executie")
        self.checkbox4 = QCheckBox("rez scipy (precis)")
        self.checkbox5 = QCheckBox("plotare integrala")
        
        #widgeturi pentru input text 
        self.solveBox = QTextEdit()
        self.solveBox.setFixedSize(430, 200)
        self.interval_integrare = QLineEdit()
        self.text_functie = QLineEdit()
        self.nr_iteratii = QLineEdit()
        self.eroare = QLineEdit()
        self.solveBox.setStyleSheet("""
    border: 2px solid darkgreen;
    color: darkblue;
    font:14px arial black;
""")
        #setare font pentru elementele text
        self.label_functie.setFont(self.label_font)
        self.label_interval.setFont(self.label_font)
        self.label_iteratii.setFont(self.label_font)
        self.label_eroare.setFont(self.label_font)
        self.label_input.setFont(self.font_title)
        self.label_rezolvare.setFont(self.font_title2)
        self.label_method.setFont(self.label_font2)
        self.label_result.setFont(self.label_font2)
        
        #adaugare la layout widgeturi.layout de tip form ,2 coloane
        self.layout_input_f.addRow(self.label_functie, self.text_functie)
        self.layout_input_f.addRow(self.label_interval, self.interval_integrare)
        self.layout_input_f.addRow(self.label_iteratii, self.nr_iteratii)
        self.layout_input_f.addRow(self.label_eroare, self.eroare)
        
        #adaugare butoane_csv la layout_csv
        self.layout_butoane_csv.addStretch()
        self.layout_butoane_csv.addWidget(self.button_incarcare)
        self.layout_butoane_csv.addWidget(self.button_incarcare2)
        self.layout_butoane_csv.addWidget(self.button_info)
        self.layout_butoane_csv.addStretch()
        
        #adaugare la layout_rez
        self.layout_rez.addStretch()
        self.layout_rez.addWidget(self.label_method)
        self.layout_rez.addSpacing(0)
        self.layout_rez.addWidget(self.combo)
        self.layout_rez.addStretch()
        
        #adaugarea la layout_optiuni
        self.layout_optiuni.addStretch()
        self.layout_optiuni.addWidget(self.checkbox1)
        self.layout_optiuni.addSpacing(0)
        self.layout_optiuni.addWidget(self.checkbox2)
        self.layout_optiuni.addStretch()
        
        #adaugare la layout optiuni2
        self.layout_optiuni2.addStretch()
        self.layout_optiuni2.addWidget(self.checkbox3)
        self.layout_optiuni.addSpacing(0)
        self.layout_optiuni2.addWidget(self.checkbox4)
        self.layout_optiuni2.addWidget(self.checkbox5)
        self.layout_optiuni2.addStretch()
        
        #adaugare la layoutul pentru butoanele solve
        self.layout_butoane_solve.addStretch()
        self.layout_butoane_solve.addWidget(self.button_rezolvare)
        self.layout_butoane_solve.addWidget(self.button_rez_down)
        self.layout_butoane_solve.addWidget(self.button_rez_txt)
        self.layout_butoane_solve.addStretch()
        
        #adaugare la layout_principal
        self.layout_principal.addWidget(self.label_input, alignment=Qt.AlignHCenter)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addLayout(self.layout_input_f)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addLayout(self.layout_butoane_csv)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addWidget(self.label_rezolvare, alignment=Qt.AlignHCenter)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addLayout(self.layout_rez)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addLayout(self.layout_optiuni)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addLayout(self.layout_optiuni2)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addLayout(self.layout_butoane_solve)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addWidget(self.label_result)
        self.layout_principal.addSpacing(12)
        self.layout_principal.addWidget(self.solveBox)
        self.layout_principal.addStretch()
        
    def setupConnections(self):
        self.button_rezolvare.clicked.connect(self.rezolva)
        self.button_rez_down.clicked.connect(self.rezolva2)
        self.combo.currentIndexChanged.connect(self.check_method)
        self.checkbox1.stateChanged.connect(self.check_ceckbox1)
        self.checkbox5.stateChanged.connect(self.check_ceckbox5)
        self.button_incarcare.clicked.connect(self.read_csv)
        self.button_incarcare2.clicked.connect(self.read_txt)
        self.button_info.clicked.connect(self.ghid)
    
    def rez_csv(self):
        
        try:
            self.rezz=Rez_CSV(self.read_combo(),self.read_checkboxes(), self.df)
            
            df=self.rezz.df
            SaveCSV(df).save_csv()
            if len(self.rezz.erori_exec)!=0:
                self.show_dialog2(self.rezz.erori_exec)
            self.button_incarcare.clicked.connect(self.read_csv)
            self.button_incarcare2.clicked.connect(self.read_txt)
            self.button_rez_txt.clicked.disconnect(self.rez_csv)
        except Exception as e:
            self.show_dialog(e)
        
        self.rezz=None
        
                                
    def read_csv(self):
        try:
            self.button_rez_txt.clicked.disconnect(self.solve_txt)
           
        except TypeError:
            pass
        try:
            
                
            
            self.df=ReadCSV().load_csv()
            stringg= [
        "Fisier Csv incarcat cu succes!",
        "Apasa rezolva csv pentru a descarca fisierul csv cu rezultatele selectate prin checkboxuri(default primesti doar rezultatul aproximarilor)",
        "Plotare integrala si Animatie nu vor functiona,",
        "apasa checkboxurile ramase pentru adaugarea",
        " de coloane corespunzatoare la csv-ul final."
        
    ]
            
            self.button_rez_txt.clicked.connect(self.rez_csv)
            self.show_dialog3(stringg)
            self.button_incarcare2.clicked.disconnect(self.read_txt)
            self.button_incarcare.clicked.disconnect(self.read_csv)
            
        except Exception as e:
            self.show_dialog(e)
        
   
    def solve_txt(self):
        
          try:  
            
            self.rezz=SolveTXT(self.read_checkboxes(),self.path)
            self.button_incarcare.clicked.connect(self.read_csv)
            self.button_incarcare2.clicked.connect(self.read_txt)
            self.button_rez_txt.clicked.disconnect(self.solve_txt)
          except Exception as e:
              self.show_dialog(e)
          
          self.rezz=None
          
    def read_txt(self):
        try:
            self.button_rez_txt.clicked.disconnect(self.rez_csv)
            
        except TypeError:
            pass 
        try:
            
                
            self.path=ReadTXT().load_txt()
            
            stringg= [
        "Fisier Txt incarcat cu succes!",
        "Pregateste un fisier text in care se vor scrie rezultatele",
        "Apasa rezolva txt si selecteaza din file manager fisierul in care sa se scrie",
        "Plotare integrala si Animatie nu vor functiona,",
        "apasa checkboxurile ramase pentru adaugarea",
        " de optiunilor corespunzatoare la fisierul rezultat."
        
    ]
            
            self.button_rez_txt.clicked.connect(self.solve_txt)
            
            self.show_dialog3(stringg)
            self.button_incarcare2.clicked.disconnect(self.read_txt)
            self.button_incarcare.clicked.disconnect(self.read_csv)
        except Exception as e:
            self.show_dialog(e)
        
    
    
    def rezolva(self):
        self.solveBox.clear()
        
        
        
        try:
            
            
            index=self.read_combo()
            vector=self.read_checkboxes()
            
            
            self.read_data()
            if index==0:
                
                simp=solve_simpson( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                print (simp.timp)
                if 0 in vector:
                    self.anim=animate_simpson(self.f_txt,self.a,self.b,self.iter)
                    
                    new_canvas = self.anim.animate()
                    
                    self.canvas.setParent(None)
                    self.canvas=new_canvas
                    self.canvas.resize(1000, 800)
                    self.canvas.move(20, 20)
                    self.canvas.setParent(self)
                    self.canvas.show()    
                    
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare()
            
            if index==1:
                
                simp=solve_rectangle(self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                if 0 in vector:
                    self.anim=animate_rectangle(self.f_txt,self.a,self.b,simp.vector,simp.vector2,self.iter)
                    new_canvas = self.anim.animate()
                    self.canvas.setParent(None)
                    self.canvas=new_canvas
                    self.canvas.resize(1000, 800)
                    self.canvas.move(20, 20)
                    self.canvas.setParent(self)
                    self.canvas.show()    
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare()
            
            if index==2:
            
            
                
                simp=solve_trapeze( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                if 0 in vector:
                    self.anim=animate_trapeze(self.f_txt,self.a,self.b,self.iter)
                    new_canvas = self.anim.animate()
                    self.canvas.setParent(None)
                    self.canvas=new_canvas
                    self.canvas.resize(1000, 800)
                    self.canvas.move(20, 20)
                    self.canvas.setParent(self)
                    self.canvas.show()    
                    
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    
                    self.plotare()
            
            if index==3:
            
            
                
                simp=solve_composite_simpson( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare()
                    
            if index==4:
            
            
                
                simp=solve_composite_rectangle( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare()
            
            if index==5:
            
            
                
                simp=solve_composite_trapeze( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare()
            
            if index==6:
            
            
                
                simp=solve_Gauss_Legendre( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare()
                    
            if index==7:
            
            
                
                simp=solve_Gauss_Chebyshev( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare()
                    
            if index==8:
            
            
                
                simp=solve_Trapeze_R2_v1( self.f_txt,self.a,self.b,self.c,self.d,self.iter1,self.iter2)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter1} iteratii pe x si {self.iter2} pe y utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    if self.a>0 and self.b>0 and self.c>0 and self.d>0:
                        self.plotare3d()
            
            if index==9:
            
            
                
                simp=solve_Trapeze_R2_v2( self.f_txt,self.a,self.b,self.c,self.d,self.iter1,self.iter2)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter1} iteratii pe x si {self.iter2} pe y utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    if self.a>0 and self.b>0 and self.c>0 and self.d>0:
                        self.plotare3d()
             
            if index==10:
            
            
                
                simp=solve_simpson_R2( self.f_txt,self.a,self.b,self.c,self.d,self.iter1,self.iter2)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter1} iteratii pe x si {self.iter2} pe y utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    
                        self.plotare3d()
        except Exception as e:
            self.show_dialog(e)
             
    def rezolva2(self):
        self.solveBox.clear()
        
        
        try:
            index=self.read_combo()
            vector=self.read_checkboxes()
            self.read_data()
            if index==0:
                
                simp=solve_simpson( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                print (simp.timp)
                if 0 in vector:
                    self.anim=animate_simpson(self.f_txt,self.a,self.b,self.iter)
                    
                    new_canvas = self.anim.animate()
                    self.anim.save_animation()
                    self.canvas.setParent(None)
                    self.canvas=new_canvas
                    self.canvas.resize(1000, 800)
                    self.canvas.move(20, 20)
                    self.canvas.setParent(self)
                    self.canvas.show()    
                    
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
                    
            if index==1:
                
                simp=solve_rectangle(self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                if 0 in vector:
                    self.anim=animate_rectangle(self.f_txt,self.a,self.b,simp.vector,simp.vector2,self.iter)
                    new_canvas = self.anim.animate()
                    self.anim.save_animation()
                    self.canvas.setParent(None)
                    self.canvas=new_canvas
                    self.canvas.resize(1000, 800)
                    self.canvas.move(20, 20)
                    self.canvas.setParent(self)
                    self.canvas.show()    
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
            
            if index==2:
            
            
                
                simp=solve_trapeze( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                if 0 in vector:
                    self.anim=animate_trapeze(self.f_txt,self.a,self.b,self.iter)
                    new_canvas = self.anim.animate()
                    self.anim.save_animation()
                    self.canvas.setParent(None)
                    self.canvas=new_canvas
                    self.canvas.resize(1000, 800)
                    self.canvas.move(20, 20)
                    self.canvas.setParent(self)
                    self.canvas.show()    
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
            
            if index==3:
            
            
                
                simp=solve_composite_simpson( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
                    
            if index==4:
            
            
                
                simp=solve_composite_rectangle( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
            
            if index==5:
            
            
                
                simp=solve_composite_trapeze( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g} si eroarea majorata este {simp.eroare_maj:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
            
            if index==6:
            
            
                
                simp=solve_Gauss_Legendre( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
                    
            if index==7:
            
            
                
                simp=solve_Gauss_Chebyshev( self.f_txt,self.a,self.b,self.iter)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter} iteratii utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    self.plotare2()
                    
            if index==8:
            
            
                
                simp=solve_Trapeze_R2_v1( self.f_txt,self.a,self.b,self.c,self.d,self.iter1,self.iter2)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter1} iteratii pe x si {self.iter2} pe y utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    
                        self.plotare3d2()
            
            if index==9:
            
            
                
                simp=solve_Trapeze_R2_v2( self.f_txt,self.a,self.b,self.c,self.d,self.iter1,self.iter2)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter1} iteratii pe x si {self.iter2} pe y utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    
                        self.plotare3d2()
             
            if index==10:
            
            
                
                simp=solve_simpson_R2( self.f_txt,self.a,self.b,self.c,self.d,self.iter1,self.iter2)
                
                if self.eroaree< simp.eroare:
                    
                    raise ValueError('Aproximarea nu poate fi realizata cu precizia pe care o doresti. Mareste iteratiile. ')
                
                self.solveBox.append(f'Rezultatul aproximarii cu {self.iter1} iteratii pe x si {self.iter2} pe y utilizand metoda {self.combo.currentText()} este: {simp.aprox:.8g}')
                
                
                
                if 1 in vector:
               
                    self.solveBox.append(f'Eroarea absoluta este {simp.eroare:.8g}')
                
                if 2 in vector:
                    timp=str(simp.timp)
                    self.solveBox.append(f'Timpul de executie al metodei este {timp}')
                if 3 in vector:
               
                    self.solveBox.append(f'Rezultatul dat de scipy este: {simp.rez_scipy:.8g}')
                if 4 in vector:
                    
                    self.plotare3d2()  
        except Exception as e :
            self.show_dialog(e)
                
    def read_combo(self):
        index = self.combo.currentIndex()
        return index
   
    
    
    def read_checkboxes(self):
        vector=[]
        if self.checkbox1.isChecked():
            vector.append(0)
        if self.checkbox2.isChecked():
            vector.append(1)
        if self.checkbox3.isChecked():
            vector.append(2)
        if self.checkbox4.isChecked():
            vector.append(3)
        if self.checkbox5.isChecked():
            vector.append(4)
        return vector
   
    def read_data(self):
        
            self.f_txt=self.text_functie.text()
            f_simbol=sp.sympify(self.f_txt)
            
            if len(f_simbol.free_symbols)==1 :
               
                interval_text = self.interval_integrare.text()
                interval=re.split(r'[;,\s]\s*', interval_text)
            
                self.a=float(interval[0])
                self.b=float(interval[1])
                self.iter=int(self.nr_iteratii.text())
                self.eroaree=float(self.eroare.text())
                self.x = sp.symbols('x')
            
            
                self.f_lambda=sp.lambdify(self.x,self.f_txt)
            if len(f_simbol.free_symbols)==1 and self.combo.currentIndex() in [8,9,10]:
                 raise ValueError("Pentru aceasta metoda ai nevoie de o functie cu 2 variabile x,y")
            elif len(f_simbol.free_symbols)==2:
               
                interval_text = self.interval_integrare.text()
                interval=re.split(r'[;,\s]\s*', interval_text)
            
                self.a=float(interval[0])
                self.b=float(interval[1])
                self.c=float(interval[2])
                self.d=float(interval[3])
                text_iter=self.nr_iteratii.text()
                iter_interval=re.split(r'[;,\s]\s*', text_iter)
                if len(iter_interval)==1:
                    self.iter1=int(iter_interval[0])
                    self.iter2=int(iter_interval[0])
                elif len(iter_interval)==2:
                    self.iter1=int(iter_interval[0])
                    self.iter2=int(iter_interval[1])
                else:
                    raise ValueError("Doar 2 valori de iteratie n si m")
                self.x, self.y = sp.symbols('x y')
            
                self.eroaree=float(self.eroare.text())
                self.f_lambda=sp.lambdify([self.x,self.y],self.f_txt)
            
            elif len(f_simbol.free_symbols)>2:
                raise ValueError("Functia ta are prea multe variabile ,maxim 2")
            
            
    def plotare3d(self):
            
            self.plotte=Plot3D(self.f_txt,self.a,self.b,self.c,self.d)
            
            
            new_canvas = self.plotte.canvas
            self.canvas.setParent(None)
            self.canvas=new_canvas
            self.canvas.resize(1000, 800)
            self.canvas.move(20, 20)
            self.canvas.setParent(self)
            self.canvas.show()
            
    def plotare(self):
            
            self.plotte=plot(self.f_txt,self.a,self.b)
            
            
            new_canvas = self.plotte.canvas
            self.canvas.setParent(None)
            self.canvas=new_canvas
            self.canvas.resize(1000, 800)
            self.canvas.move(20, 20)
            self.canvas.setParent(self)
            self.canvas.show()
    
    def plotare3d2(self):
            
            self.plotte=Plot3D(self.f_txt,self.a,self.b,self.c,self.d)
            
            self.plotte.save_plot()
            new_canvas = self.plotte.canvas
            self.canvas.setParent(None)
            self.canvas=new_canvas
            self.canvas.resize(1000, 800)
            self.canvas.move(20, 20)
            self.canvas.setParent(self)
            self.canvas.show()
            
    def plotare2(self):
        
            try:
            
                self.plotte=plot(self.f_txt,self.a,self.b)
                
                self.plotte.save_plot()
                new_canvas = self.plotte.canvas
                self.canvas.setParent(None)
                self.canvas=new_canvas
                self.canvas.resize(1000, 800)
                self.canvas.move(20, 20)
                self.canvas.setParent(self)
                self.canvas.show()
            except Exception as e:
                self.show_dialog(e)
            
            
            
    def check_ceckbox1(self):
        if self.checkbox1.isChecked() and self.checkbox5.isChecked():
            self.checkbox5.blockSignals(True)
            self.checkbox5.setChecked(False)
            self.checkbox5.blockSignals(False)

    def check_ceckbox5(self):
        if self.checkbox5.isChecked() and self.checkbox1.isChecked():
            self.checkbox1.blockSignals(True)
            self.checkbox1.setChecked(False)
            self.checkbox1.blockSignals(False)
    
        
    def check_method(self):
        
       index = self.combo.currentIndex()
             
            
       if index in [3, 4, 5, 6, 7,8,9,10]:
             self.checkbox1.setChecked(False)
             self.checkbox1.setEnabled(False)
             
       else:
            self.checkbox1.setEnabled(True)
            
            
                                
    def ghid(self):
        
        stringg= [
    "Mic ghid pentru evitarea erorilor",
    "\n\n",
    "Pentru input si scirerea functiilor ( fie in cadrul documentelor txt csv) fie in inputul de o singura functie din program se foloseste sintagma sympy:",
    "Trigonometric: sin, cos, tan, cot, sec, csc",
    "Inverse Trigonometric: asin, acos, atan, acot, asec, acsc",
    "Exponential and Logarithmic: exp, log, ln",
    "Hyperbolic: sinh, cosh, tanh, coth, sech, csch////Square Root: sqrt/////",
    "Variabile: x, sau x si y."
    "Cautati pe internet pentru mai multe detalii!",
    "\n\n",
    "In cazul in care se doreste input o functie f(x,y) se va scrie functia , apoi la interval , despartit cu virgule sau spatii , [a,b,c,d] , se va seta eroarea si iteratiile , pot fi o valoarea sau 2 ,n si m , daca se da doar o valoare , n=m.",
    "Butoanele programului sunt intuitive.Rezolva mp4/img permite downloadarea plotarii sau a animatiei dupa caz daca casuta este bifata.",
    
    "Utilizarea programului : se alege o metoda de input,fie in campurile destinate din program fie prin incarcarea unui fisier csv , txt",
    "Pasul 2 : se alege metoda de rezolvare si se bifeaza casutele corespunzatoare , in cazul in care se doresc functionalitati extra precum animatii si celalalte optiuni",
    "Pasul 3 : se apasa butonul corespunzator rezolvarii metodei de input",
    "Informatii pentru csv si text: ",
    "\n\n",
    "Documentul din care se citeste,fie csv sau txt urmeaza modelul metodei de input pentru o singura functie din program ,adica :",
    "Pentru csv , 4 SAU 5 coloane cu orice titluri dar: functie , interval,iteratii,eroare si OPTIONAL a 5 ea coloana cu metodele de rezolvare , valoare numerica , conform ierarhiei metodelor din dropboxul din program,ex simpson=0.",
    "In cazul in care nu exista a 5 ea coloana in csv, se va aplica pentru rezolvarea tuturor functiilor din csv metoda selectata in interfata programului.",
    "\n\n",
    "Pentru txt , aceasi idee doar ca trebuie sa fie neeaparat 5 linii , pe fiecare linie , functie interval iteratii eroare metoda_rezolvare_index.Deci se grupeza functiile si datele sale in 'paragrafe' de cate 5 linii, pot exista spatii intre paragrafe.",
    "\n\n",
    "Informatii despre erori:",
    "\n\n",
    "Programul ajuta la identificarea erorilor prin pop-up windows in care se afiseaza detalii despre erori.Erorile pot fi de scriere , de definire, de incompatibilitati ex 1/x pe intervalul 0 si 1, functii care nu sunt continue ,etc. Asigurati va ca functiile respecta conditiile impuse pentru a putea fi aproximate cu metodele de quadratura ",
    "In cazul de erori la procesarea unei functii din documentul txt/csv, rezultatul va fi nan si programul afiseaza eroarea care a cauzat acest lucru , fie in window pentru csv fie direct in documentul txt .",
    " de coloane corespunzatoare la csv-ul final."
    
]
        self.show_dialog3(stringg)
        
    def show_dialog(self, error_message):
        dialog = DialogWindow(error_message, self)
        dialog.exec_()
    def show_dialog2(self, error_message):
        dialog =DialogWindow_csv(error_message, self)
        dialog.exec_()
    def show_dialog3(self, info):
        dialog =DialogWindow3(info, self)
        dialog.exec_()
        
        
class DialogWindow(QDialog):
    def __init__(self, e, parent=None):
        super().__init__(parent=parent)  
        self.setWindowTitle('Box de erori')
        self.setFixedSize(400, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)
        message = QTextEdit(f" Ceva nu a mers bine! Informatii : <br><br> {e}", self)
        message.setFixedSize(375,375)
        message.setStyleSheet("""
    border: 2px solid red;
    color: red;
""")

class DialogWindow3(QDialog):
    def __init__(self, e, parent=None):
        super().__init__(parent=parent)  
        self.setWindowTitle('Box info')
        self.setFixedSize(400, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        errors_html = "<br>".join(e)
        
        message = QTextEdit(f" :<br><br>{errors_html}", self)
        message.setFixedSize(375, 375)
        message.setReadOnly(True)  
        message.setStyleSheet("""
    border: 2px solid green;
    color:  green;
""")
        
        layout.addWidget(message)
class DialogWindow_csv(QDialog):
    def __init__(self, e, parent=None):
        super().__init__(parent=parent)  
        self.setWindowTitle('Box de erori')
        self.setFixedSize(400, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        errors_html = "<br>".join(e)
        
        message = QTextEdit(f"Csv CREAT cu succes, insa ai avut erori la anumite functii: :<br><br>{errors_html}", self)
        message.setFixedSize(375, 375)
        message.setReadOnly(True)  
        message.setStyleSheet("""
            border: 2px solid red;
            color: red;
        """)
        
        layout.addWidget(message)
        
class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet("""
       QLineEdit {
           font: 16px Verdana;
           color: blue;
           background-color: lightgrey;
           border: 2px solid darkblue;
           border-radius: 10px;
           padding: 2px;
           margin: 3px;
       }
       QCheckBox{
           font: 12px arial black;
           color: darkblue;
           
          
           
           
       }
       QComboBox {
           font: 12px arial black;
           color: darkblue;
           background-color: lightgrey;
           border: 2px solid darkblue;
           border-radius: 10px;
           margin: 3px;
       }
       QPushButton {
           font: 12px arial black;
           color: darkblue;
           background-color: lightgrey;
           border: 2px solid darkblue;
           border-radius: 10px;
           
       }
       QPushButton:hover {
        background-color: lightblue; /* Culoarea de fundal când mouse-ul este deasupra */
        border: 2px solid blue; /* Schimbă culoarea bordurii la hover */
    }
    QPushButton:pressed {
        background-color: grey; 
        
    }
       QTextEdit {
           font: 13px Arial Black;
           color: darkblue;
           background-color: lightgrey;
           border: 2px solid blue;
           border-radius: 10px;
           padding: 2px;
           margin: 3px;
       }
   """)
       
        self.gui = GUI()

    def run(self):
        self.gui.show()
        sys.exit(self.app.exec_())
        
if __name__ == "__main__":
    main = Main()
    main.run()
