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
	Rupa** rupe=new Rupa*[8];

	Putanja(double r, Rupa** rupe) {
		duzina_putanje = r;
		for (int i = 0; i < 8; i++) {
			this->rupe[i] = rupe[i];
		}
	}

	~Putanja() {
		for (int i = 0; i < 8; i++)
			delete rupe[i];
		delete rupe;
	}
};

class ListaPutanja {
public:

	class Elem {
	public:
		Putanja* putanja;
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
	Rupa* rupe[8];
	double zbir = 0;
	double min = 0;
	
	rupe[0] = new Rupa(62.0, 58.4);
	rupe[1] = new Rupa(57.5, 56.0);
	rupe[2] = new Rupa(51.7, 56.0);
	rupe[3] = new Rupa(67.9, 19.6);
	rupe[4] = new Rupa(57.7, 42.1);
	rupe[5] = new Rupa(54.2, 29.1);
	rupe[6] = new Rupa(46.0, 45.1);
	rupe[7] = new Rupa(34.7, 45.1);

	cout << "Pretraga najkrace putanje je zapocela: \n";

	do {
		zbir = 0; //resetuje se vrednost zbira, zbog sledece iteracije petlje
		for (int i = 0; i < 7; i++) zbir += rastojanje(rupe[i], rupe[i+1]);
	
		if (min == 0) { //ulazi se prvi put u ovaj uslov, kada je jos uvek min=0
			min = zbir;
			lista->dodaj_putanju(new Putanja(zbir, rupe));
		}
		else if (zbir <= min) { 
			if ((zbir <= (min + epsilon)) && (zbir >= (min - epsilon))) { //uradjeno zbog mogucnosti da kompjuter ne uzme u obzir iste putanje, a to moze da uradi zbog (ne)preciznosti
				lista->dodaj_putanju(new Putanja(zbir, rupe));
			}
			else { //definitivno smo pronasli novi minimum, moramo da obrisemo stari zapamceni i da u listu putanja zapamtimo novu vrednost
				min = zbir;
				delete lista;
				lista = new ListaPutanja();
				lista->dodaj_putanju(new Putanja(zbir, rupe));
			}
		}
	} while (next_permutation(rupe, rupe + 8));

	cout << "Najkrace moguce putanje su: \n";
	ListaPutanja::Elem* tek = lista->prvi;
	while (tek) {
		int i = 0;
		while (i < 8) {
			cout << tek->putanja->rupe[i]->id;
			if (i < 7) cout << "-";
			else cout << "\n";
			i++;
		}
		tek = tek->sled;
	}

	cout << "Duzina najkrace putanje je: " << lista->prvi->putanja->duzina_putanje << "\n";
	system("pause");
}