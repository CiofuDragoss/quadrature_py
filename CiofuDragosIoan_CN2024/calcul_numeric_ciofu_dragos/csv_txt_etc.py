import tkinter as tk
from tkinter import filedialog
import pandas as pd
from logica import Logica_R,Logica_R2,solve_simpson
from logica import solve_simpson,solve_rectangle,solve_trapeze,solve_Gauss_Chebyshev,solve_Trapeze_R2_v1,solve_Trapeze_R2_v2,solve_simpson_R2,solve_Gauss_Legendre,solve_composite_rectangle,solve_composite_simpson,solve_composite_trapeze
import re
import sympy as sp


   
        
        
class ReadCSV:
    def load_csv(self):
        df=None
        
        root = tk.Tk()
        
        root.withdraw() 
        
        
        file_path = filedialog.askopenfilename(defaultextension='.csv',
                                               filetypes=[('CSV files', '*.csv')],
                                               title="Open CSV file")
        
        
        root.destroy()  
        
        
        if file_path:
            df = pd.read_csv(file_path)
            
            if df.shape[1]<4 or df.shape[1]>5:
                raise ValueError("Fisier csv incompatibil, verifica ghidul programului.")
            
        else:
            raise ValueError('Incarcare nereusita.Foloseste inputul pentru o singura functie sau incearca din nou.')
        
        return df
class SaveCSV:
    def __init__(self, df):
        self.df = df
        
    def save_csv(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                 filetypes=[('CSV files', '*.csv')],
                                                 title="Save CSV file")
        
        
        root.destroy()  
        if file_path:
            
            self.df.to_csv(file_path, index=False)
                
            
        else:
            raise ValueError("Nu ai salvat fisierul cu raspunsul !")
        

class ReadTXT:
    def load_txt(self):
        
        
        root = tk.Tk()
        root.withdraw() 
        
        file_path = filedialog.askopenfilename(defaultextension='.txt',
                                               filetypes=[('Text files', '*.txt')],
                                               title="Open TXT file")
        
        root.destroy()  
        
        if file_path:
            return file_path
            
            
        else:
            raise ValueError('Incarcare nereusita. Foloseste inputul pentru o singura functie sau incearca din nou.')
        
        

class SaveTXT:
   
        
        
    def save_txt(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(defaultextension='.txt',
                                                 filetypes=[('Text files', '*.txt')],
                                                 title="Save TXT file")
        
        root.destroy()
        if file_path:
            self.filepath=file_path
            return self.filepath
                
        else:
            raise ValueError("Nu ai salvat fisierul cu raspunsul! ")
        

class SolveTXT:
    def __init__(self,vector,path_fisier_derez):
        
        self.vector=vector
        self.bool=True
        self.functii=[]
        self.path_fisier=path_fisier_derez
        self.data = open(self.path_fisier, 'r')
        self.interval=[]
        self.eroare=[]
        self.iteratii=[]   
        self.index_met=[]
        self.i=0
        self.erori_exec=[]
        
        self.rezolva2()
    def rezolva(self):
        while self.bool:
            line = self.data.readline()
            if not line:
                # End of file
                self.bool = False
                break

            line = line.strip()
            if line:  # If the line is not empty
                self.functii.append(line)
                for i in range(4):
                    line = self.data.readline().strip()
                    if i == 0:
                        self.interval.append(line if line else 'NaN')
                    elif i == 1:
                        self.iteratii.append(line if line else 'NaN')
                    elif i == 2:
                        self.eroare.append(line if line else 'NaN')
                    elif i == 3:
                        self.index_met.append(line if line else 'NaN')
        self.data.close( )
    def get_metoda_rez(self, index, f, a, b, c, d, n, m):
        if index == 0:
            simp = solve_simpson(f, a, b, n)
    
        if index == 1:
            simp = solve_rectangle(f, a, b, n)
        
        if index == 2:
            simp = solve_trapeze(f, a, b, n)
        
        if index == 3:
            simp = solve_composite_simpson(f, a, b, n)
        
        if index == 4:
            simp = solve_composite_rectangle(f, a, b, n)
        
        if index == 5:
            simp = solve_composite_trapeze(f, a, b, n)
        
        if index == 6:
            simp = solve_Gauss_Legendre(f, a, b, n)
        
        if index == 7:
            simp = solve_Gauss_Chebyshev(f, a, b, n)
        
        if index == 8:
            simp = solve_Trapeze_R2_v1(f, a, b, c, d, n, m)
        
        if index == 9:
            simp = solve_Trapeze_R2_v1(f, a, b, c, d, n, m)
        
        if index == 10:
            simp = solve_simpson_R2(f, a, b, c, d, n, m)
        
        return simp
                        
            
    def rezolva2(self):
        self.rezolva()
        self.rezultat=[]
        self.erori=[]
        self.timp_exec=[]
        self.rez_scipy=[]
        
        
        
        for i in range(len(self.functii)):
            
            try:
                f_txt=self.functii[i]
                f_simbol=sp.sympify(f_txt)
                print(f_simbol)
                if len(f_simbol.free_symbols)==1 :
                   
                    interval_text = self.interval[i]
                    interval=re.split(r'[;,\s]\s*', interval_text)
                
                    a=int(float(interval[0]))
                    b=int(float(interval[1]))
                    c=None
                    d=None
                    iter1=int(float(self.iteratii[i]))
                    iter2=None
                    eroare=int(float(self.eroare[i]))
                    
                elif len(f_simbol.free_symbols)==1 and self.index_utilizator in [8,9,10]:
                     raise ValueError("Pentru aceasta metoda ai nevoie de o functie cu 2 variabile x,y")
                elif len(f_simbol.free_symbols)==2:
                   
                    interval_text = self.interval[i]
                    interval=re.split(r'[;,\s]\s*', interval_text)
                
                    a=int(float(interval[0]))
                    b=int(float(interval[1]))
                    c=int(float(interval[2]))
                    d=int(float(interval[3]))
                    text_iter=self.iteratii[i]
                    iter_interval=re.split(r'[;,\s]\s*', text_iter)
                    if len(iter_interval)==1:
                        iter1=int(float(iter_interval[0]))
                        iter2=int(float(iter_interval[0]))
                    elif len(iter_interval)==2:
                        iter1=int(float(iter_interval[0]))
                        iter2=int(float(iter_interval[1]))
                    else:
                        raise ValueError("Doar 2 valori de iteratie n si m")
                    
                
                    eroare=int(float(self.eroare[i]))
                    
                
                elif len(f_simbol.free_symbols)>2:
                    raise ValueError("Functia ta are prea multe variabile ,maxim 2")
            
                
                simp=self.get_metoda_rez(int(float(self.index_met[i])),f_txt,a,b,c,d,iter1,iter2)
                if eroare<simp.eroare:
                    raise ValueError('Nu poti aproxima cu eroarea setata.')
                self.rezultat.append(simp.aprox)
                    
                self.erori.append(simp.eroare)
                    
                self.timp_exec.append(simp.timp)
                self.rez_scipy.append(simp.rez_scipy)
                
            except Exception as e:
                self.rezultat.append('nan')
                self.erori.append('nan')
                self.timp_exec.append('nan')
                self.rez_scipy.append('nan')
                self.erori_exec.append(f"La functia '{f_txt}' ai primit erorile: {e}")
        
        file_path=SaveTXT().save_txt()
        with open(file_path, 'w') as file:
            for i in range(len(self.functii)):
                file.write(f"functie : {self.functii[i]}\n")
                file.write(f"interval : {self.interval[i]}\n")
                file.write(f"iteratii : {self.iteratii[i]}\n")
                file.write(f"eroare : {self.eroare[i]}\n")
                file.write(f"index met : {self.index_met[i]}\n\n")
                
                
                file.write(f"aproximare : {self.rezultat[i]}\n")
                if 1 in self.vector:
                    file.write(f"eroare_abs : {self.erori[i]}\n")
                if 2 in self.vector:
                    file.write(f"timp_exec : {self.timp_exec[i]}\n")
                if 3 in self.vector:
                    file.write(f"rez_scipy : {self.rez_scipy[i]}\n")
                
                file.write("\n\n")
            for i in range(len(self.erori_exec)):
                file.write(f"eroare : {self.erori_exec[i]}\n")
                
                file.write("\n\n")
        file.close()
            
class Rez_CSV:
    
    
    def __init__(self,index,vector,df):
        self.vector=vector
        self.df=df
        self.index_utilizator=index
        self.erori_exec=[]
        
            
            
        if self.df.shape[1]==4:
           self.functii=self.df.iloc[:,0].astype(str).to_numpy()
           self.interval=self.df.iloc[:,1].astype(str).to_numpy()
           self.eroare=self.df.iloc[:,3].astype(str).to_numpy()
           self.iteratii=self.df.iloc[:,2].astype(str).to_numpy()
           self.rezolva()
           
        elif self.df.shape[1]==5:
            self.functii=self.df.iloc[:,0].astype(str).to_numpy()
            
            self.interval=self.df.iloc[:,1].astype(str).to_numpy()
            self.eroare=self.df.iloc[:,3].astype(str).to_numpy()
            self.iteratii=self.df.iloc[:,2].astype(str).to_numpy()    
            self.index_met=self.df.iloc[:,4].astype(str).to_numpy()
            self.rezolva2()
        
    

    def rezolva(self):
        rezultat=[]
        erori=[]
        timp_exec=[]
        rez_scipy=[]
        
        
        
        for i in range(len(self.functii)):
            
            try:
                f_txt=self.functii[i]
                f_simbol=sp.sympify(f_txt)
                print(f_simbol)
                if len(f_simbol.free_symbols)==1 :
                   
                    interval_text = self.interval[i]
                    interval=re.split(r'[;,\s]\s*', interval_text)
                
                    a=int(float(interval[0]))
                    b=int(float(interval[1]))
                    c=None
                    d=None
                    iter1=int(float(self.iteratii[i]))
                    iter2=None
                    eroare=int(float(self.eroare[i]))
                    
                elif len(f_simbol.free_symbols)==1 and self.index_utilizator in [8,9,10]:
                     raise ValueError("Pentru aceasta metoda ai nevoie de o functie cu 2 variabile x,y")
                elif len(f_simbol.free_symbols)==2:
                   
                    interval_text = self.interval[i]
                    interval=re.split(r'[;,\s]\s*', interval_text)
                
                    a=int(float(interval[0]))
                    b=int(float(interval[1]))
                    c=int(float(interval[2]))
                    d=int(float(interval[3]))
                    text_iter=self.iteratii[i]
                    iter_interval=re.split(r'[;,\s]\s*', text_iter)
                    if len(iter_interval)==1:
                        iter1=int(float(iter_interval[0]))
                        iter2=int(float(iter_interval[0]))
                    elif len(iter_interval)==2:
                        iter1=int(float(iter_interval[0]))
                        iter2=int(float(iter_interval[1]))
                    else:
                        raise ValueError("Doar 2 valori de iteratie n si m")
                    
                
                    eroare=int(float(self.eroare[i]))
                    
                
                elif len(f_simbol.free_symbols)>2:
                    raise ValueError("Functia ta are prea multe variabile ,maxim 2")
            
                
                simp=self.get_metoda_rez(self.index_utilizator,f_txt,a,b,c,d,iter1,iter2)
                if eroare<simp.eroare:
                    raise ValueError('Nu poti aproxima cu eroarea setata.')
                rezultat.append(simp.aprox)
                    
                erori.append(simp.eroare)
                    
                timp_exec.append(simp.timp)
                rez_scipy.append(simp.rez_scipy)
                
            except Exception as e:
                rezultat.append('nan')
                erori.append('nan')
                timp_exec.append('nan')
                rez_scipy.append('nan')
                self.erori_exec.append(f"La functia '{f_txt}' ai primit erorile: {e}")
        self.df = self.df.assign(
            rezultat=rezultat,
            )
        if 1 in self.vector:
            
            self.df = self.df.assign(
            eroare_abs=erori
            )
        if 2 in self.vector:
            self.df=self.df.assign(
                timp_exec=timp_exec
                )
        if 3 in self.vector:
            self.df=self.df.assign(
                rez_scipy=rez_scipy
                )
                        

                        
            
    def rezolva2(self):
         rezultat=[]
         erori=[]
         timp_exec=[]
         rez_scipy=[]
         
         
         
         for i in range(len(self.functii)):
             
             try:
                 f_txt=self.functii[i]
                 f_simbol=sp.sympify(f_txt)
                 print(f_simbol)
                 if len(f_simbol.free_symbols)==1 :
                    
                     interval_text = self.interval[i]
                     interval=re.split(r'[;,\s]\s*', interval_text)
                 
                     a=int(float(interval[0]))
                     b=int(float(interval[1]))
                     c=None
                     d=None
                     iter1=int(float(self.iteratii[i]))
                     iter2=None
                     eroare=int(float(self.eroare[i]))
                     
                 elif len(f_simbol.free_symbols)==1 and self.index_utilizator in [8,9,10]:
                      raise ValueError("Pentru aceasta metoda ai nevoie de o functie cu 2 variabile x,y")
                 elif len(f_simbol.free_symbols)==2:
                    
                     interval_text = self.interval[i]
                     interval=re.split(r'[;,\s]\s*', interval_text)
                 
                     a=int(float(interval[0]))
                     b=int(float(interval[1]))
                     c=int(float(interval[2]))
                     d=int(float(interval[3]))
                     text_iter=self.iteratii[i]
                     iter_interval=re.split(r'[;,\s]\s*', text_iter)
                     if len(iter_interval)==1:
                         iter1=int(float(iter_interval[0]))
                         iter2=int(float(iter_interval[0]))
                     elif len(iter_interval)==2:
                         iter1=int(float(iter_interval[0]))
                         iter2=int(float(iter_interval[1]))
                     else:
                         raise ValueError("Doar 2 valori de iteratie n si m")
                     
                 
                     eroare=int(float(self.eroare[i]))
                     
                 
                 elif len(f_simbol.free_symbols)>2:
                     raise ValueError("Functia ta are prea multe variabile ,maxim 2")
             
                 
                 simp=self.get_metoda_rez(int(float(self.index_met[i])),f_txt,a,b,c,d,iter1,iter2)
                 if eroare<simp.eroare:
                     raise ValueError('Nu poti aproxima cu eroarea setata.')
                 rezultat.append(simp.aprox)
                     
                 erori.append(simp.eroare)
                     
                 timp_exec.append(simp.timp)
                 rez_scipy.append(simp.rez_scipy)
                 
             except Exception as e:
                 rezultat.append('nan')
                 erori.append('nan')
                 timp_exec.append('nan')
                 rez_scipy.append('nan')
                 self.erori_exec.append(f"La functia '{f_txt}' ai primit erorile: {e}")
         self.df = self.df.assign(
             rezultat=rezultat,
             )
         if 1 in self.vector:
             
             self.df = self.df.assign(
             eroare_abs=erori
             )
         if 2 in self.vector:
             self.df=self.df.assign(
                 timp_exec=timp_exec
                 )
         if 3 in self.vector:
             self.df=self.df.assign(
                 rez_scipy=rez_scipy
                 )
             
            
    def get_metoda_rez(self, index, f, a, b, c, d, n, m):
        if index == 0:
            simp = solve_simpson(f, a, b, n)
    
        if index == 1:
            simp = solve_rectangle(f, a, b, n)
        
        if index == 2:
            simp = solve_trapeze(f, a, b, n)
        
        if index == 3:
            simp = solve_composite_simpson(f, a, b, n)
        
        if index == 4:
            simp = solve_composite_rectangle(f, a, b, n)
        
        if index == 5:
            simp = solve_composite_trapeze(f, a, b, n)
        
        if index == 6:
            simp = solve_Gauss_Legendre(f, a, b, n)
        
        if index == 7:
            simp = solve_Gauss_Chebyshev(f, a, b, n)
        
        if index == 8:
            simp = solve_Trapeze_R2_v1(f, a, b, c, d, n, m)
        
        if index == 9:
            simp = solve_Trapeze_R2_v1(f, a, b, c, d, n, m)
        
        if index == 10:
            simp = solve_simpson_R2(f, a, b, c, d, n, m)
        
        return simp
                
            
        

    
