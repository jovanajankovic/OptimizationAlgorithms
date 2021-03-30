#include <iostream>
#include <cmath>
#include <stdio.h>
#define epsilon 0.0000000000001
#define nula 0.0
using namespace std;

int brojac;
int red;

//funkcija za ispis pronadjenih nula funkcije
void ispis(double nula_fje) {
	if (brojac == 1) cout << "Prva nula funkcije reda n = 1 : " << nula_fje << endl;
	else if (brojac == 2) cout << "Druga nula funkcije reda n = 1 : " << nula_fje << endl;
	else if (brojac == 3) cout << "Prva nula funkcije reda n = 2 : " << nula_fje << endl;
	else cout << "Druga nula funkcije reda n = 2 : " << nula_fje << endl;
}

//funkcija za pronalazenje nula funkcije na intervalu [a,b]
void polovljenje_intervala(double a, double b) {
	bool zavrsi = false;
    double polovina_intervala = a;
    double y;
    double y1,y2;
    
    y1 = std::sph_bessel(red, a);
    y2 = std::sph_bessel(red, b);
    if(y1 * y2 >= 0) return; 
    
	while (zavrsi == false) {
        if((b - a) <= epsilon){
            zavrsi = true;
        }
        else {  
         polovina_intervala = (a + b) / 2;
		 y = std::sph_bessel(red, polovina_intervala);
        if (y == nula) {
          zavrsi = true; 
        }
		else {
            y1 = std::sph_bessel(red, polovina_intervala);
            y2 = std::sph_bessel(red, a);
            if(y1 * y2 > 0) a = polovina_intervala;
            else b = polovina_intervala;
        }
      }
	}
	brojac++;
	if (brojac == 2) red = 2;
	ispis(polovina_intervala);
}

int main() {
	brojac = 0;
	red = 1;
	cout.precision(13);
	polovljenje_intervala(0.5, 5); //prva nula reda n = 1
	polovljenje_intervala(5.0, 8.0); //druga nula reda n = 1
	polovljenje_intervala(4.0, 7.0); //prva nula reda n = 2
	polovljenje_intervala(6.0, 11.0); //druga nula reda n = 2
	system("pause");
	return 0;
}
