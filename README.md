# quadrature_py
A Gui with 11 quadrature methods for R and R**2

@ciofu_dragos_ioan author
Informatii program-aproximare cu metode 
de quadratura pe R si R**2.


PENTRU DOWNLOAD VIDEO/FOTO TREBUIE FFMPEG

Programul are si un MINI GHID integrat
pentru utilizator , dar voi incerca sa 
scriu niste detalii despre anumite functii
si clase.





Programul are 4 fisiere:
gui 
csv_and_txt
plotting_anim
logica


Programul este facut utilizand conceptele
programarii orientate pe obiect.

Fiecare fisier py contine mai multe clase ,care 
comunica intre ele.

Din Fisierul  se ruleaza
programul si se afla in legatura
toate celelalte clase.


fisierul logica: clasa logica si logica_R2 care contin doar metodele de quadratura.

Cate un obiect pentru fiecare metoda ( clasa)care preia in constructor datele necesare rezolvarii functiei cu acea metoda .


fisierul csv_txt_etc: clasele de load,save csv si txt (tkinter) pentru citirea fisiere de input , si apoi producerea fisierelor rezolvate ( scriere intr un fisier gol txt existent in sistem sau in caz csv downloadare csv cu rezolvarile)

fisierul plotting_anim:
Clase pentru animare pentru TRAPEZ,SIMPSON,DREPTUNGHI.

Clase de plotare a ariei de sub functie ( integrala=arie) , si pentru R**2 plotarea functiei f(x,y) ( volumul de sub f(x,y)==integrala.

fisierul Gui: 
Gestionarea majoritatii claselor progamului, integrarea lor cu butoane , etc . Metode care apeleaza clase din celelalte fisiere ,etc .interfata grafica a programului evident

Programul ne permite sa :
inputam o singura functie/csv/txt pentru a o aproxima 
cu una din cele 11 metode de quadratura disponibile, 8 valabile pentru o singura dimensiune iar 3 valabile pentru R**2.

Vorbim mai intai de cazul unei singure functii pentru a intelege optiunile  checboxurile si butoanele.

Sa zicem ca inputam o functie prin intermediul textboxului.
Programul stie daca este o functie pe R sau pe R**2 prin verificarea utilizand metode sympy de nr de free_symbols deci daca free_Symbols==2 inseamna a avem functie pe R**2 f(x,y) ,altfel avem f(x) . Se foloseste syntagma sympy pentru a inputa functia in program.

Dupa caz daca avem f(x):
se pune interval sub forma a,b/a b/a;b/ ,iteratii,eroare

Daca avem f(x,y):
interval sub forma a b c d despartite valorile
prin virgule sau spatii ,programul stie, (se foloseste libraria re pentru formatarea inputurilor interval si iteratii), APOI iteratiile care pot fi de forma n m , adica 2 valori , una pentru x alta pentru y , sau o singura valoare, in acest caz n=m( programul ia decizia adecvata conform inputului) si Eroarea cu care se doreste aproximarea.

TRECEM la selectarea metodei din cele disponibile de quadratura.
Apoi selectam optiuni extra cum ar  fi: 
animarea metodei daca este disponibila pentru metoda selectata ,plotarea integralei, includerea erorilor ( abs si max daca este cazul) , a rezultatului dat de scipy(exact) , a timpului de executie.

Apasarea butonului REZOLVA VA afisa in boxul pentru rezultat APROXIMAREA impreuna cu celallte detalii sau optiuni ,daca se selecteaza animatie sau plotare se va plota /anima in canvas corespunzator.

Apasarea butonului REZOLVA MP4/IMG face acelasi lucru doar de asemenea permite descarcarea mp4 a videoclipului, pozei dupa checkboxul selectat, DACA ESTE SELECTATA ACEASTA OPTIUNE.

IN CAZ DE EROARE ,UTILIZATORUL VA PRIMI UN POP UP WINDOW CU EROAREA DEFINITA FIE CLAR ( EXEMPLU: FUNCTIA NU POATE FI APROXIMATA CORESPUNZATOR CU metoda..( in general daca functia nu este continua , am implemnetat de asemenea metode pentru verificarea compatibilitatii unei functii cu metoda de quadratura selectata) sau : ,,nu poti aproxima cu eroarea Dorita, mareste interatiile''

sau ,, functia ta are prea multe variabile''

PRECUM SI ERORI DE SISTEM ( in engleza) . Programul ar TREBUI SA NU SE BLOCHEZE IN CAZUL ERORII .

CATEVA ASPECTE GUI : 

Aplicam stiluri csv pentru designul widgeturilor .


Apasarea butonului hid deschide un pop up window cu cateva informatii utile.

checkboxul animatie metoda este unchecked si facut indisponibil pentru metodele care nu permit animatie.

checkboxul animatie si plotare nu pot fi selectate in acelasi timp, programul gestionand correct acest aspect.

1...incarcarea unui csv sau txt , blocheaza incarcarea altui fisier pana la rezolvarea acestuia ex : daca am incarcat cu success un txt/csv , butoanele incarca csv si incarca txt nu mai fac nimic, pana la rezolvare.

Daca utilizatorul cu success un fisier , va fi intampinat cu un pop up window care il informeaza ca incarcarea a avut success 
si ii da cateva informatii .In cazul in care abandoneaza incarcarea utilizatorul, va primi un pop up care il informeaza ca nu s a incarcat nimic (NOTA: IN ACEST CAZ , BUTOANELE DE INCARCARE CSV SI TXT NU SE BLOCHEAZA CONFORM PARAGRAFULUI DE MAI SUS.).

DE ASEMENEA,DACA UTILIZATORUL A INCARCAT CU SUCCES UN FISIER(BUTOANE INCARCARE BLOCATE) SI APASA PE REZOLVARE ,DAR ABANDONEAZA DESCARCAREA/SCRIEREA FISIERULUI REZOLVAT, BUTOANELE DE INCARCARE RAMAN BLOCATE .





REZOLVARE FISIERE TEXT SI CSV:

informatii apasand butonul GHID din program.(Programul gestioneaza toate erorile linie cu linie in cazul unei erori la o linei utilizatorul este INFORMAT DE CE REZUTLATUL SI OPTIUNILE(daca au fost selectate) sunt NAN . 
Ex eroare: La functia ,,x**3'' ai eroarea:
nu poti aproxima cu eroarea setata.

Mai multe detalii verbal , atasez in arhgiva si un fisier text si 2 csv , unul cu 4 coloane altul cu 5 col(informatii in ghid program) 






