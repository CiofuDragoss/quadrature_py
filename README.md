# quadratura.py  
Autor: Dragos Ioan Ciofu  



Descriere: Aplicatie GUI pentru aproximarea integralei pe R si R^2, care ofera 11 metode de cuadratura (8 pentru o variabila, 3 pentru doua variabile). Include optiuni de animatie, plotare, export MP4/PNG si salvare rezultate in CSV/TXT.

Structura proiectului

- **gui.py**  
  Interfata grafica si gestionarea evenimentelor (buton Solve, incarcare fisiere, optiuni)
- **logica.py**  
  Clasele de cuadratura pentru R (Logica) si R^2 (LogicaR2) – fiecare metoda intr‑o clasa separata
- **csv_and_txt.py**  
  Clase pentru incarcare si salvare date in format CSV/TXT folosind tkinter
- **plotting_anim.py**  
  Clase pentru animatie (Trapez, Simpson, Dreptunghi) si plotare grafice 2D/3D

Parametri input:

- **R:** interval a,b; numar subdiviziuni sau eroare dorita
- **R^2:** interval a,b,c,d; n,m (sau un singur numar pentru ambele axe); eroare dorita
- metoda dorita (din cele 11)
- animatie (daca e disponibila)
- plotare
- eroare absoluta si maxima
- timp executie
- 
Functionalitati principale

- Detectarea automata a functiei pe R (o variabila) sau R^2 (doua variabile)
- salvare CSV/TXT
- plotare/animare
- export imagine PNG sau video MP4 (necesita FFMPEG)

Gestionarea erorilor:

- Verifica compatibilitatea functiei cu metoda selectata
- Afiseaza mesaje clare in ferestre pop‑up
- Nu blocheaza aplicatia in caz de eroare; rezultatul este NaN acolo unde nu se poate calcula ex csv.

Aspecte GUI

- Stil consistent,folosirea de stiluri css.
- Butoanele “Incarca CSV/TXT” se blocheaza dupa incarcare pana la rezolvare.
- Checkbox‑urile pentru animatie si plotare sunt inactive pentru metode fara animatie.
- Butonul GHID afiseaza instructiuni detaliate

Proces rezolvare fisiere CSV/TXT

- Fisierele sunt procesate linie cu linie
- Erorile pe linie sunt raportate SI rezultatul invalid este NaN
- Dupa incarcare cu succes, utilizatorul primeste o notificare pop






