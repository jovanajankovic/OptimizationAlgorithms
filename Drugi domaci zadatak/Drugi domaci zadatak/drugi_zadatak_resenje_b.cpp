#include <iostream>
#include <algorithm>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#define epsilon 0.0005
using namespace std;

int globalni_id = 0;

struct Rupa {
	int id = ++globalni_id;
	double x, y;
	Rupa(double xx, double yy) {
		x = xx;
		y = yy;
	}
};

class Putanja {
public:
	double duzina_putanje;
	Rupa** rupe = new Rupa*[12];

	Putanja(double r, Rupa** rupe) {
		duzina_putanje = r;
		for (int i = 0; i < 12; i++) {
			this->rupe[i] = rupe[i];
		}
	}

	~Putanja() {
		for (int i = 0; i < 12; i++)
			delete rupe[i];
		delete rupe;
	}
};

class ListaPutanja {
public:

	class Elem {
	public:
		Putanja * putanja;
		Elem* sled;
		Elem(Putanja* p) {
			putanja = p;
			sled = 0;
		}
	};

	Elem* prvi = 0;

	~ListaPutanja() {
		Elem* tek = prvi;
		Elem* stari = nullptr;
		while (tek) {
			stari = tek;
			tek = tek->sled;
			delete stari;
		}
	}

	void dodaj_putanju(Putanja* p) {
		Elem* novi = new Elem(p);
		if (prvi) {
			Elem* tek;
			for (tek = prvi; tek != nullptr; tek = tek->sled) {
				if (tek->sled == nullptr)
					break;
			}
			tek->sled = novi;
		}
		else {
			prvi = novi;
		}
	}
};

double rastojanje(Rupa* r1, Rupa* r2) {
	double rastojanje = sqrt((pow((r1->x - r2->x), 2) + pow((r1->y - r2->y), 2)));
	return rastojanje;
}

void main() {
	ListaPutanja* lista = new ListaPutanja();
	Rupa* rupe[12];
	double zbir;
	double min = 0;
	bool iskoci;

	rupe[0] = new Rupa(62.0, 58.4);
	rupe[1] = new Rupa(57.5, 56.0);
	rupe[2] = new Rupa(51.7, 56.0);
	rupe[3] = new Rupa(67.9, 19.6);
	rupe[4] = new Rupa(57.7, 42.1);
	rupe[5] = new Rupa(54.2, 29.1);
	rupe[6] = new Rupa(46.0, 45.1);
	rupe[7] = new Rupa(34.7, 45.1);
	rupe[8] = new Rupa(45.7, 25.1); 
	rupe[9] = new Rupa(34.7, 26.4); 
	rupe[10] = new Rupa(28.4, 31.7);
	rupe[11] = new Rupa(33.4, 60.5);

	cout << "Pretraga najkrace putanje je zapocela: \n";
	do {
		iskoci = false;
		zbir = 0; //resetuje se vrednost zbira, zbog sledece iteracije petlje
		for (int i = 0; i < 11; i++) {
			zbir += rastojanje(rupe[i], rupe[i + 1]);
			if (min> 0 && zbir > (min + epsilon)) { //to znaci da nema potrebe dalje prolaziti kroz petlju i racunati zbir, jer nece biti minimalni put
				iskoci = true;
				break;
				}
		}
		if (min == 0) { //ulazi se prvi put u ovaj uslov, kada je jos uvek min=0
			min = zbir;
			lista->dodaj_putanju(new Putanja(zbir, rupe));
		}
		else if (iskoci==false) { //ili je pronadjen novi minimum ili je pronadjena putanja u suprotnom smeru
			if ((zbir <= (min + epsilon)) && (zbir >= (min - epsilon))) { //uradjeno zbog mogucnosti da kompjuter ne uzme u obzir iste putanje koje su iste, a to moze da uradi zbog preciznosti
			//radi se o istoj putanji, ali u suprotnom smeru, ali moze biti i nova putanja iste duzine
			lista->dodaj_putanju(new Putanja(zbir, rupe));
			} 
			else { //definitivno smo pronasli novi minimum, moramo da obrisemo stari zapamceni i da u listu putanja zapamtimo novu vrednost
					min = zbir;
					delete lista;
					lista = new ListaPutanja();
					lista->dodaj_putanju(new Putanja(zbir, rupe));
			}
		}
	} while (next_permutation(rupe, rupe + 12));

	cout<< "Najkrace moguce putanje su: \n";

	ListaPutanja::Elem* tek = lista->prvi;
	while (tek) {
		int i = 0;
		while (i < 12) {
			cout << tek->putanja->rupe[i]->id;
			if (i < 11) cout << "-";
			else cout << "\n";
			i++;
		}
		tek = tek->sled;
	}
	cout << "Duzina najkrace putanje je: " << lista->prvi->putanja->duzina_putanje << "\n";
	system("pause");
}