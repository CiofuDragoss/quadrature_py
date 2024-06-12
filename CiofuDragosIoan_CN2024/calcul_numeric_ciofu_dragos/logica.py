# -*- coding: utf-8 -*-
"""
Created on Fri May 17 18:24:36 2024

@author: drago
"""
from scipy.special import roots_legendre
import math as m
import numpy as np
from scipy.integrate import quad,quadrature,trapz,simps
import scipy.integrate as integrate
import time
import decimal
from decimal import Decimal
import sympy as sp
from scipy.optimize import minimize_scalar

from scipy.integrate import dblquad
class Logica_R():
    
    ###metode de verificare a conditiilor ce trebuie respectate de functiile
    ### ce vor fi aproximate prin simpson,dreptunghi,,gaussiene
    
    def verify_continuity_R(f,a,b):
        x = sp.symbols('x')
        f=sp.sympify(f)
        
        if(sp.singularities(f, x,sp.Interval(a,b))):
            return False
        else:
            
            return True
    
    
     
    def verify_Gauss_Chebyshev_R(f,num_points=1000,epsilon=1e-18):
        x_points = np.linspace(-1 + epsilon, 1 - epsilon, num_points)
        old_settings = np.seterr(divide='ignore')
        f_values = f(x_points)
        
        if np.any(np.isnan(f_values)) or np.any(np.isinf(f_values)):
            return False
        else:
            return True
    
    
    def erorr_rectangle_R_maj(f,a,b,n):
        x=sp.Symbol('x')
        result = minimize_scalar(lambda x: -f(x), bounds=(a, b), method='bounded')
        supremum = -result.fun 
        return (((b-a)**2)/(4*n))*supremum
    def erorr_trapeze_R_maj(f,a,b,n):
        x=sp.Symbol('x')
        result = minimize_scalar(lambda x: -f(x), bounds=(a, b), method='bounded')
        supremum = -result.fun 
        return (((b-a)**3)/(12*(n**2)))*supremum

    def erorr_simpson_R_maj(f,a,b,n):
        x=sp.Symbol('x')
        result = minimize_scalar(lambda x: -f(x), bounds=(a, b), method='bounded')
        supremum = -result.fun 
        return (((b-a)**5)/(2880*(n**4)))*supremum
        
    
    
    def rectangle_R(f,a,b,n):
        start_time= time.time()
        h=(b-a)/n
        summ=0
        vector=[]
        vector_h=[]
        z=a
        vector.append(z)
        for _ in range(n):
            summ+=f((z+z+h)/2)
            vector_h.append(f((z+z+h)/2))
            z+=h
            vector.append(z)
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return h*summ,time_complet,vector,vector_h
    def trapeze_R(f,a,b,n):
        start_time= time.time()
        h=(b-a)/n
        summ=0
        z=a
        for _ in range(n):
            summ+=(f(z)+f(z+h))/2
            z+=h
        
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return h*summ,time_complet
    def simpson_R(f,a,b,n):
        start_time= time.time()
        h=(b-a)/n
        summ=0
        z=a
        for _ in range(n):
            summ+=(f(z)+4*f((z+z+h)/2)+f(z+h))
            z+=h
        
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return (h*(1/6))*summ,time_complet
   
    
    def composite_rectangle_R(f,a,b,n):
        start_time= time.time()
        h=(b-a)/n
        summ=0
        
        for i in range(n):
            summ+=f(a+(i+1/2)*h)
            
        
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return h*summ,time_complet
    def composite_trapeze_R(f,a,b,n):
        
        start_time= time.time()
        h=(b-a)/n
        summ=0
            
        for i in range(1,n):
            summ+=f(a+i*h)
        
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return (h/2)*(f(a)+2*summ+f(b)),time_complet
    def composite_simpson_R(f,a,b,n):
        
    
        
            
        start_time= time.time()
        h=(b-a)/n
        summ=0
        summ2=0        
        for i in range(1,n,2):
            summ+=f(a+i*h)
        for i in range(2,n,2):
            summ2+=f(a+i*h)
            
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return (h/3)*(f(a)+4*summ+2*summ2+f(b)),time_complet
    def Gauss_Legendre(f,a,b,n):
        start_time= time.time()
        nodes, weights = roots_legendre(n)
        transformed_nodes = 0.5 * (nodes + 1) * (b - a) + a
        scaled_weights = weights * 0.5 * (b - a)
        integral = np.sum(scaled_weights * f(transformed_nodes))
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return integral,time_complet
    def Gauss_Chebyshev_R(f,a,b,n):
        start_time= time.time()
        summ=0
        w=np.pi/n
        h=(b-a)/2
        for i in range(1,n):
            x_i = np.cos((2 * i - 1) * np.pi / (2 * n))
            summ+=f((x_i+1)*h+a)*(1-x_i**2)**(1/2)
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return (np.pi*h*1/n )*summ,time_complet

    
class Logica_R2():
    
    def simpson_R2(f, a, b, c, d, n, m):
        start_time= time.time()
        hx = (b - a) / n
        hy = (d - c) / m
        s = 0
        
        for i in range(m+1):
            if i==0 or i==m:
                p=1
            elif i%2!=0:
                p=4
            else:
                p=2
              
            for j in range(n+1):
                if j==0 or j==n:
                    q=1
                elif j%2!=0:
                    q=4
                else:
                    q=2
                x=a+j*hx
                y=c+i*hy
                s+=p*q*f(x,y)
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return hx*hy/9*s,time_complet

    def trapeze_R2(f,a,b,c,d,n,m):
        start_time= time.time()
        h=(b-a)/n
        h1=(d-c)/m
        suma=0
        suma2=0
        suma3=0
        for i in range(1,n):
            suma+=f(a+i*h,c)+f(a+i*h,d)
        for i in range(1,m):
            suma2+=f(a,c+i*h1)+f(b,c+i*h1)
        for i in range(1,n):
            for j in range(1,m):
                suma3+=f(a+i*h,c+j*h1)
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return ((h*h1)/4)*(f(a,d)+f(a,c)+f(b,d)+f(b,c)+2*suma+2*suma2+4*suma3),time_complet
    def trapeze_R2_v2(f,a,b,c,d,n,m):
        start_time= time.time()
        h=(b-a)/n
        h1=(d-c)/m
        suma=0
            
        for i in range(n):
            for j in range (m):
                suma+=f(a+i*h,c+j*h1)+f(a+(i+1)*h,c+j*h1)+f(a+i*h,c+(j+1)*h1)+f(a+(i+1)*h,c+(j+1)*h1)
        end_time = time.time()
        time_complet=Decimal(end_time) - Decimal(start_time)
        return ((h*h1)/4)*suma,time_complet


class solve_simpson_R2():
    
    def __init__(self,f,a,b,c,d,n,m):
        self.x,self.y=sp.symbols('x,y')
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.n=n
        self.m=m
        self.log=Logica_R2
        
        self.f_lambda=sp.lambdify([self.x,self.y],f)
        self.aprox=self.log.simpson_R2(self.f_lambda,self.a,self.b,self.c, self.d,self.n, self.m)[0]
        self.timp=str(self.log.simpson_R2(self.f_lambda,self.a,self.b,self.c, self.d,self.n, self.m)[1])
        self.rez_scipy=dblquad(self.f_lambda,self.a,self.b,lambda x: self.c,lambda x: self.d)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        
class solve_Trapeze_R2_v2():
    
    def __init__(self,f,a,b,c,d,n,m):
        self.x,self.y=sp.symbols('x,y')
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.n=n
        self.m=m
        self.log=Logica_R2
        
        self.f_lambda=sp.lambdify([self.x,self.y],f)
        self.aprox=self.log.trapeze_R2_v2(self.f_lambda,self.a,self.b,self.c, self.d,self.n, self.m)[0]
        self.timp=str(self.log.trapeze_R2_v2(self.f_lambda,self.a,self.b,self.c, self.d,self.n, self.m)[1])
        self.rez_scipy=dblquad(self.f_lambda,self.a,self.b,lambda x: self.c,lambda x: self.d)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
    
class solve_Trapeze_R2_v1():
    
    def __init__(self,f,a,b,c,d,n,m):
        self.x,self.y=sp.symbols('x,y')
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.n=n
        self.m=m
        self.log=Logica_R2
        
        self.f_lambda=sp.lambdify([self.x,self.y],f)
        self.aprox=self.log.trapeze_R2(self.f_lambda,self.a,self.b,self.c, self.d,self.n, self.m)[0]
        self.timp=str(self.log.trapeze_R2(self.f_lambda,self.a,self.b,self.c, self.d,self.n, self.m)[1])
        self.rez_scipy=dblquad(self.f_lambda,self.a,self.b,lambda x: self.c,lambda x: self.d)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        
class solve_Gauss_Legendre ():
    def __init__(self,f,a,b,n):
        
        self.x = sp.symbols('x')
        self.a = a
        self.b = b
        self.n = n
        self.log = Logica_R
        
        self.f_symbol = sp.sympify(f)
        self.f_lambda = sp.lambdify(self.x, f)
        if self.log.verify_Gauss_Chebyshev_R(self.f_lambda)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu chebyshev")
        self.aprox = self.log.Gauss_Legendre(self.f_lambda, self.a, self.b, self.n)[0]
        self.timp = str(self.log.Gauss_Legendre(self.f_lambda, self.a, self.b, self.n)[1])
        self.rez_scipy = quadrature(self.f_lambda, self.a, self.b)[0]
        self.eroare = Decimal(abs(self.rez_scipy - self.aprox))
        
class solve_Gauss_Chebyshev ():
    def __init__(self,f,a,b,n):
        
        
        self.x = sp.symbols('x')
        self.a = a
        self.b = b
        self.n = n
        self.log = Logica_R
        
        self.f_symbol = sp.sympify(f)
        self.f_lambda = sp.lambdify(self.x, f)
        if self.log.verify_Gauss_Chebyshev_R(self.f_lambda)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu chebyshev")
        self.aprox = self.log.Gauss_Chebyshev_R(self.f_lambda, self.a, self.b, self.n)[0]
        self.timp = str(self.log.Gauss_Chebyshev_R(self.f_lambda, self.a, self.b, self.n)[1])
        self.rez_scipy = quadrature(self.f_lambda, self.a, self.b)[0]
        self.eroare = Decimal(abs(self.rez_scipy - self.aprox))
        
        
        
            
class solve_composite_simpson():
    def __init__(self,f,a,b,n):
        self.x=sp.symbols('x')
        self.a=a
        self.b=b
        self.n=n
        self.log=Logica_R
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        self.f_diff2=sp.sympify(sp.diff(f,self.x,4))
        if self.log.verify_continuity_R(self.f_diff2, self.a, self.b)==False or self.log.verify_continuity_R(self.f_symbol, self.a, self.b)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu simpson")
        
        self.aprox=self.log.composite_simpson_R(self.f_lambda,self.a,self.b,self.n)[0]
        self.timp=self.log.composite_simpson_R(self.f_lambda,self.a,self.b,self.n)[1]
        self.rez_scipy=quadrature(self.f_lambda,self.a,self.b)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        self.eroare_maj=self.log.erorr_simpson_R_maj(self.f_lambda,self.a,self.b,self.n)


class solve_composite_rectangle():
    def __init__(self,f,a,b,n):
        self.x=sp.symbols('x')
        self.a=a
        self.b=b
        self.n=n
        self.log=Logica_R
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        
        if self.log.verify_continuity_R(self.f_symbol, self.a, self.b)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu metoda dreptunghiului.")
        
        self.aprox=self.log.composite_rectangle_R(self.f_lambda,self.a,self.b,self.n)[0]
        self.timp=self.log.composite_rectangle_R(self.f_lambda,self.a,self.b,self.n)[1]
        self.rez_scipy=quadrature(self.f_lambda,self.a,self.b)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        self.eroare_maj=self.log.erorr_rectangle_R_maj(self.f_lambda,self.a,self.b,self.n)
        
class solve_rectangle():
    
    def __init__(self,f,a,b,n):
        self.x=sp.symbols('x')
        self.a=a
        self.b=b
        self.n=n
        self.log=Logica_R
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        
        if self.log.verify_continuity_R(self.f_symbol, self.a, self.b)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu metoda dreptunghiului.")
        
        self.aprox=self.log.rectangle_R(self.f_lambda,self.a,self.b,self.n)[0]
        self.timp=self.log.rectangle_R(self.f_lambda,self.a,self.b,self.n)[1]
        self.rez_scipy=quadrature(self.f_lambda,self.a,self.b)[0]
        self.vector=self.log.rectangle_R(self.f_lambda,self.a,self.b,self.n)[2]
        self.vector2=self.log.rectangle_R(self.f_lambda,self.a,self.b,self.n)[3]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        self.eroare_maj=self.log.erorr_rectangle_R_maj(self.f_lambda,self.a,self.b,self.n)

class solve_composite_trapeze():
    def __init__(self,f,a,b,n):
        self.x=sp.symbols('x')
        self.a=a
        self.b=b
        self.n=n
        self.log=Logica_R
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        self.f_diff2=sp.sympify(sp.diff(f,self.x,2))
        if self.log.verify_continuity_R(self.f_diff2, self.a, self.b)==False or self.log.verify_continuity_R(self.f_symbol, self.a, self.b)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu metoda trapezelor.")
        
        self.aprox=self.log.composite_trapeze_R(self.f_lambda,self.a,self.b,self.n)[0]
        self.timp=self.log.composite_trapeze_R(self.f_lambda,self.a,self.b,self.n)[1]
        self.rez_scipy=quadrature(self.f_lambda,self.a,self.b)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        self.eroare_maj=self.log.erorr_trapeze_R_maj(self.f_lambda,self.a,self.b,self.n)
        
class solve_trapeze ():
    def __init__(self,f,a,b,n):
        self.x=sp.symbols('x')
        self.a=a
        self.b=b
        self.n=n
        self.log=Logica_R
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        self.f_diff2=sp.sympify(sp.diff(f,self.x,2))
        if self.log.verify_continuity_R(self.f_diff2, self.a, self.b)==False or self.log.verify_continuity_R(self.f_symbol, self.a, self.b)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu trapez")
        
        self.aprox=self.log.trapeze_R(self.f_lambda,self.a,self.b,self.n)[0]
        self.timp=self.log.trapeze_R(self.f_lambda,self.a,self.b,self.n)[1]
        self.rez_scipy=quadrature(self.f_lambda,self.a,self.b)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        self.eroare_maj=self.log.erorr_trapeze_R_maj(self.f_lambda,self.a,self.b,self.n)
            
        
    
        
class solve_simpson():
    def __init__(self,f,a,b,n):
        self.x=sp.symbols('x')
        self.a=a
        self.b=b
        self.n=n
        self.log=Logica_R
        self.f_symbol=sp.sympify(f)
        self.f_lambda=sp.lambdify(self.x,f)
        self.f_diff2=sp.sympify(sp.diff(f,self.x,4))
        if self.log.verify_continuity_R(self.f_diff2, self.a, self.b)==False or self.log.verify_continuity_R(self.f_symbol, self.a, self.b)==False:
            raise ValueError("Functia nu se poate aproxima corespunzator cu simpson")
        
        self.aprox=self.log.simpson_R(self.f_lambda,self.a,self.b,self.n)[0]
        self.timp=self.log.simpson_R(self.f_lambda,self.a,self.b,self.n)[1]
        self.rez_scipy=quadrature(self.f_lambda,self.a,self.b)[0]
        self.eroare=Decimal(abs(self.aprox-self.rez_scipy))
        self.eroare_maj=self.log.erorr_simpson_R_maj(self.f_lambda,self.a,self.b,self.n)
            
    
