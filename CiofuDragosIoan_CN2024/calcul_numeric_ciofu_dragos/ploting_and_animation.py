import matplotlib.pyplot as plt
import numpy as np
import math as m
from PyQt5 import QtWidgets
import sys
import sympy as sp
from logica import Logica_R,Logica_R2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from scipy.integrate import quad, dblquad, tplquad, fixed_quad, quadrature
from matplotlib.animation import FuncAnimation
from scipy.interpolate import interp1d
import tkinter as tk
from tkinter import filedialog

class plot():
    def __init__(self,f,a,b):
        
        self.a=a
        self.b=b
        
        self.x=sp.symbols('x')
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        
        
   
        plt.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)
        self.figure=plt.figure(figsize=(10,10), facecolor='#1a1a1a')
        self.figure.suptitle('Zona de plotare si animare', fontsize=25, color='white')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Axa x', fontsize=15,color='grey')
        self.ax.set_ylabel('Axa y', fontsize=15,color='grey')
        self.ax.grid(True,linestyle='--', linewidth=1, color='lightgrey')
        self.ax.set_facecolor('#1a1a1a')
        self.ax.spines['bottom'].set_color('lightgrey')  
        self.ax.spines['left'].set_color('lightgrey') 
        self.ax.spines['bottom'].set_linewidth(2)
        self.ax.spines['left'].set_linewidth(2)
        self.ax.xaxis.label.set_color('lightgrey')  
        self.ax.yaxis.label.set_color('lightgrey')
        self.ax.tick_params(axis='x', colors='red',direction='inout',length=14,labelsize=15)
        self.ax.tick_params(axis='y', colors='red',direction='inout',length=14,labelsize=15) 
        
        
        self.puncte_x=np.linspace(self.a,self.b,100)
        self.puncte_y=self.f_lambda(self.puncte_x)
        self.ax.plot(self.puncte_x,self.puncte_y,'.-',color='red',label='f(x)',linewidth=3)
        self.ax.plot([self.a, self.a], [0, self.f_lambda(self.a)], color='blue', linewidth=2,linestyle='--')
        self.ax.plot([self.b, self.b], [0, self.f_lambda(self.b)], color='blue', linewidth=2,linestyle='--')
        self.ax.plot([self.a, self.b], [0, 0], color='blue', linewidth=2,linestyle='--')
        self.ax.fill_between(self.puncte_x, self.puncte_y, alpha=0.3, color='lightblue')
        self.ax.set_xticks(list(self.ax.get_xticks()) + [self.a]+[self.b])
        self.ax.set_yticks(list(self.ax.get_yticks()) + [self.f_lambda(self.a)]+[self.f_lambda(self.b)])
        self.ax.legend()
        self.canvas=FigureCanvas(self.figure)
    
    def save_plot(self):
        
        root = tk.Tk()
        root.withdraw() 

        
        file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                 filetypes=[('PNG files', '*.png'),
                                                            ('All files', '*.*')],
                                                 title="Save the plot as...")
        if file_path:  
            self.figure.savefig(file_path, dpi=300)
        root.destroy() 
        
class animate_simpson():
    def __init__(self,f,a,b,n):
        
        self.a=a
        self.b=b
        
        
        self.x=sp.symbols('x')
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        self.n=n
        
   
        plt.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)
        self.figure=plt.figure(figsize=(10,10), facecolor='#1a1a1a')
        self.figure.suptitle('Zona de plotare si animare', fontsize=25, color='white')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Axa x', fontsize=15,color='grey')
        self.ax.set_ylabel('Axa y', fontsize=15,color='grey')
        self.ax.grid(True,linestyle='--', linewidth=1, color='lightgrey')
        self.ax.set_facecolor('#1a1a1a')
        self.ax.spines['bottom'].set_color('lightgrey')  
        self.ax.spines['left'].set_color('lightgrey') 
        self.ax.spines['bottom'].set_linewidth(2)
        self.ax.spines['left'].set_linewidth(2)
        self.ax.xaxis.label.set_color('lightgrey')  
        self.ax.yaxis.label.set_color('lightgrey')
        self.ax.tick_params(axis='x', colors='red',direction='inout',length=14,labelsize=15)
        self.ax.tick_params(axis='y', colors='red',direction='inout',length=14,labelsize=15) 
        
        
        self.puncte_x=np.linspace(self.a,self.b,100)
        self.puncte_y=self.f_lambda(self.puncte_x)
        self.ax.plot(self.puncte_x,self.puncte_y,'.-',color='red',label='f(x)',linewidth=3)
        self.ax.plot([self.a, self.a], [0, self.f_lambda(self.a)], color='blue', linewidth=2)
        self.ax.plot([self.b, self.b], [0, self.f_lambda(self.b)], color='blue', linewidth=2)
        self.ax.plot([self.a, self.b], [0, 0], color='blue', linewidth=2)
        
        self.ax.set_xticks(list(self.ax.get_xticks()) + [self.a]+[self.b])
        self.ax.set_yticks(list(self.ax.get_yticks()) + [self.f_lambda(self.a)]+[self.f_lambda(self.b)])
        self.ax.legend()
        self.canvas=FigureCanvas(self.figure)
        self.lista = []
        self.x=0
        self.switch=True
        
     
    
    def update_frame(self, frame):
        if frame < self.n:
            h = (self.b - self.a) / self.n
            z = self.a + frame * h

            p1 = (z, 0)
            p2 = (z + h, 0)
            p3 = (z, self.f_lambda(z))
            p4 = (z+h/2, self.f_lambda(z+h/2))
            p5=(z+h,self.f_lambda(z+h))
            
            x_points = np.array([p3[0], p4[0], p5[0]])
            y_points = np.array([p3[1], p4[1], p5[1]])
            coefficients = np.polyfit(x_points, y_points, 2)
            parabola = lambda x: coefficients[0] * x**2 + coefficients[1] * x + coefficients[2]

            x_vals = np.linspace(z, z + h, 400)
            y_vals = parabola(x_vals)

            
            parabola_plot, = self.ax.plot(x_vals, y_vals, color='black', linewidth=2)
            

            verts = [(z, 0)] + [(xi, parabola(xi)) for xi in x_vals] + [(z + h, 0)]
            poly = plt.Polygon(verts, closed=True, facecolor='lightblue', alpha=0.3)
            self.ax.add_patch(poly)
            line1, = self.ax.plot([p1[0], p2[0]], [0, 0] ,color='#39FF14', linewidth=2)
            line2, = self.ax.plot([p1[0], p3[0]], [0, p3[1]], color='#39FF14', linewidth=2)
            line3, = self.ax.plot([p2[0], p5[0]], [p2[1], p5[1]], color='#39FF14', linewidth=2)
            

            self.lista.extend([parabola_plot, line1, line2, line3, poly])
            return self.lista
    
    def animate(self):
        
        self.anim = FuncAnimation(self.figure, self.update_frame, frames=self.n, interval=350, repeat=False)
        return self.canvas
         
            
    def save_animation(self):
        root = tk.Tk()
        root.withdraw()  
        
        
        file_path = filedialog.asksaveasfilename(defaultextension='.mp4',
                                                 filetypes=[('MP4 files', '*.mp4')],
                                                 title="Save the animation as...")
        if file_path:
            self.anim.save(file_path, writer='ffmpeg', fps= 1000/400)
            

        root.destroy()
            
class Plot3D:
    def __init__(self, f, a, b, c, d):
       
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
        
        self.x, self.y = sp.symbols('x y')
        self.f_symbol = sp.sympify(f)
        self.f_lambda = sp.lambdify((self.x, self.y), f, 'numpy')
        
        
        self.figure = plt.figure(figsize=(10, 10), facecolor='#1a1a1a')
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.figure.suptitle('Zona de plotare și animare', fontsize=25, color='white')
        self.ax.set_xlabel('Axa x', fontsize=15, color='grey')
        self.ax.set_ylabel('Axa y', fontsize=15, color='grey')
        self.ax.set_zlabel('Axa z', fontsize=15, color='grey')

        
        self.ax.xaxis.pane.set_edgecolor('red')
        self.ax.yaxis.pane.set_edgecolor('red')
        self.ax.zaxis.pane.set_edgecolor('red')
        self.ax.xaxis.pane.set_facecolor('#1a1a1a')
        self.ax.yaxis.pane.set_facecolor('#1a1a1a')
        self.ax.zaxis.pane.set_facecolor('#1a1a1a')
        self.ax.xaxis.pane.fill = True
        self.ax.yaxis.pane.fill = True
        self.ax.zaxis.pane.fill = True

        
        self.ax.tick_params(axis='x', colors='red', direction='inout', length=14, labelsize=15)
        self.ax.tick_params(axis='y', colors='red', direction='inout', length=14, labelsize=15)
        self.ax.tick_params(axis='z', colors='red', direction='inout', length=14, labelsize=15)

        
        self.puncte_x = np.linspace(self.a, self.b, 30)
        self.puncte_y =np.linspace(self.c, self.d, 30)
        X, Y = np.meshgrid(self.puncte_x, self.puncte_y)
        Z=self.f_lambda(X,Y)
       
        x_fata,y_fata=(np.full(30,self.b),self.puncte_y)
        z_fata=self.f_lambda(x_fata,y_fata)
        
        
        self.ax.plot(x_fata, y_fata, z_fata, color='lightblue', alpha=0.2)
        self.ax.plot_surface(X, Y, Z, edgecolor='#39FF14', alpha=0.2)
        
        self.ax.legend(['f(x, y)'])
        self.canvas = FigureCanvas(self.figure)
    
    def save_plot(self):
       
       root = tk.Tk()
       root.withdraw()  

       
       file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                filetypes=[('PNG files', '*.png'),
                                                           ('All files', '*.*')],
                                                title="Save the plot as...")
       if file_path:  
           self.figure.savefig(file_path, dpi=300)
       root.destroy() 
    
class animate_rectangle():
    def __init__(self,f,a,b,vector,vector_h,n):
        
        self.a=a
        self.b=b
        self.vector=vector
        self.vector_h=vector_h
        self.x=sp.symbols('x')
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        self.n=n
        
   
        plt.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)
        self.figure=plt.figure(figsize=(10,10), facecolor='#1a1a1a')
        self.figure.suptitle('Zona de plotare si animare', fontsize=25, color='white')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Axa x', fontsize=15,color='grey')
        self.ax.set_ylabel('Axa y', fontsize=15,color='grey')
        self.ax.grid(True,linestyle='--', linewidth=1, color='lightgrey')
        self.ax.set_facecolor('#1a1a1a')
        self.ax.spines['bottom'].set_color('lightgrey')  
        self.ax.spines['left'].set_color('lightgrey') 
        self.ax.spines['bottom'].set_linewidth(2)
        self.ax.spines['left'].set_linewidth(2)
        self.ax.xaxis.label.set_color('lightgrey')  
        self.ax.yaxis.label.set_color('lightgrey')
        self.ax.tick_params(axis='x', colors='red',direction='inout',length=14,labelsize=15)
        self.ax.tick_params(axis='y', colors='red',direction='inout',length=14,labelsize=15) 
        
        
        self.puncte_x=np.linspace(self.a,self.b,100)
        self.puncte_y=self.f_lambda(self.puncte_x)
        self.ax.plot(self.puncte_x,self.puncte_y,'.-',color='red',label='f(x)',linewidth=3)
        self.ax.plot([self.a, self.a], [0, self.f_lambda(self.a)], color='blue', linewidth=2)
        self.ax.plot([self.b, self.b], [0, self.f_lambda(self.b)], color='blue', linewidth=2)
        self.ax.plot([self.a, self.b], [0, 0], color='blue', linewidth=2)
        
        self.ax.set_xticks(list(self.ax.get_xticks()) + [self.a]+[self.b])
        self.ax.set_yticks(list(self.ax.get_yticks()) + [self.f_lambda(self.a)]+[self.f_lambda(self.b)])
        self.ax.legend()
        self.canvas=FigureCanvas(self.figure)
        self.lista = []
    def update_frame(self,frame):
        if frame < self.n:
            z = self.vector[frame]
            
            h = self.vector_h[frame]
            width=abs(self.vector[1]-self.vector[0])
            rect = plt.Rectangle((z, 0),width,0+h , edgecolor='#39FF14', facecolor='lightblue', alpha=0.3, linewidth=2)
            self.lista.append(rect)
            self.ax.add_patch(rect)
            return self.lista
    
    def animate(self):
        self.anim = FuncAnimation(self.figure, self.update_frame, frames=self.n, interval=350, repeat=False)
        
        return self.canvas
    
         
            
    def save_animation(self):
        root = tk.Tk()
        root.withdraw()  
        
        
        file_path = filedialog.asksaveasfilename(defaultextension='.mp4',
                                                 filetypes=[('MP4 files', '*.mp4')],
                                                 title="Save the animation as...")
        if file_path:
            self.anim.save(file_path, writer='ffmpeg', fps= 1000/400)
            

        root.destroy()
class animate_trapeze():
    def __init__(self,f,a,b,n):
        
        self.a=a
        self.b=b
        
        
        self.x=sp.symbols('x')
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        self.n=n
        
   
        plt.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)
        self.figure=plt.figure(figsize=(10,10), facecolor='#1a1a1a')
        self.figure.suptitle('Zona de plotare si animare', fontsize=25, color='white')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Axa x', fontsize=15,color='grey')
        self.ax.set_ylabel('Axa y', fontsize=15,color='grey')
        self.ax.grid(True,linestyle='--', linewidth=1, color='lightgrey')
        self.ax.set_facecolor('#1a1a1a')
        self.ax.spines['bottom'].set_color('lightgrey')  
        self.ax.spines['left'].set_color('lightgrey') 
        self.ax.spines['bottom'].set_linewidth(2)
        self.ax.spines['left'].set_linewidth(2)
        self.ax.xaxis.label.set_color('lightgrey')  
        self.ax.yaxis.label.set_color('lightgrey')
        self.ax.tick_params(axis='x', colors='red',direction='inout',length=14,labelsize=15)
        self.ax.tick_params(axis='y', colors='red',direction='inout',length=14,labelsize=15) 
        
        
        self.puncte_x=np.linspace(self.a,self.b,100)
        self.puncte_y=self.f_lambda(self.puncte_x)
        self.ax.plot(self.puncte_x,self.puncte_y,'.-',color='red',label='f(x)',linewidth=3)
        self.ax.plot([self.a, self.a], [0, self.f_lambda(self.a)], color='blue', linewidth=2)
        self.ax.plot([self.b, self.b], [0, self.f_lambda(self.b)], color='blue', linewidth=2)
        self.ax.plot([self.a, self.b], [0, 0], color='blue', linewidth=2)
        
        self.ax.set_xticks(list(self.ax.get_xticks()) + [self.a]+[self.b])
        self.ax.set_yticks(list(self.ax.get_yticks()) + [self.f_lambda(self.a)]+[self.f_lambda(self.b)])
        self.ax.legend()
        self.canvas=FigureCanvas(self.figure)
        self.lista = []
    def update_frame(self, frame):
        if frame < self.n:
            h = (self.b - self.a) / self.n
            z = self.a + frame * h

            p1 = (z, 0)
            p2 = (z + h, 0)
            p3 = (z, self.f_lambda(z))
            p4 = (z + h, self.f_lambda(z + h))

            line1, = self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#39FF14', linewidth=2)
            line2, = self.ax.plot([p1[0], p3[0]], [p1[1], p3[1]], color='#39FF14', linewidth=2)
            line3, = self.ax.plot([p2[0], p4[0]], [p2[1], p4[1]], color='#39FF14', linewidth=2)
            line4, = self.ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'o-', color='black', linewidth=2)

            self.lista.extend([line1, line2, line3, line4])

            fill = self.ax.fill_between([z, z + h], [self.f_lambda(z), self.f_lambda(z + h)], color='lightblue', alpha=0.3)
            self.lista.append(fill)

            return self.lista
    
    def animate(self):
        
        self.anim = FuncAnimation(self.figure, self.update_frame, frames=self.n, interval=350, repeat=False)
        return self.canvas
    
    
         
   
    def save_animation(self):
        root = tk.Tk()
        root.withdraw()  
        
        
        file_path = filedialog.asksaveasfilename(defaultextension='.mp4',
                                                 filetypes=[('MP4 files', '*.mp4')],
                                                 title="Save the animation as...")
        if file_path:
            self.anim.save(file_path, writer='ffmpeg', fps= 1000/400)
            

        root.destroy()
