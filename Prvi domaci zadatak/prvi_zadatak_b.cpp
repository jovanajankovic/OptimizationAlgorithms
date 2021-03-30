#include <iostream>
#include <math.h>
#include <cstdlib>

using namespace std;

class Lista {
public:

	class Elem {
	public:
		double* cetvorka;
		Elem* sled;

		Elem(double a, double b, double c, double d) {
			cetvorka = new double[4];
			cetvorka[0] = a;
			cetvorka[1] = b;
			cetvorka[2] = c;
			cetvorka[3] = d;
			sled = nullptr;
		}

		~Elem() {
			delete[] cetvorka;
		}
	};

	Elem * prvi;
	int duzina;

	Lista() {
		prvi = nullptr;
		duzina = 0;
	}

	~Lista() {
		Elem* tek = prvi, *stari = nullptr;
		while (tek != nullptr) {
			stari = tek;
			tek = tek->sled;
			delete stari;
		}
	}

	int duz() {
		return duzina;
	}

	void dodaj(double i, double j, double k, double l) {
		Elem* novi = new Elem(i, j, k, l);
		if (prvi) {
			Elem* tek;
			for (tek = prvi; tek != nullptr; tek = tek->sled) {
				if (tek->sled == nullptr)
					break;
			}
			tek->sled = novi;
			duzina++;
			return;
		}
		else {
			prvi = novi;
			duzina++;
			return;
		}
	}

	static void provera(double i, double j, double k, double l);

};

Lista* lista = new Lista();

void Lista::provera(double i, double j, double k, double l) {
		double proizvod = i * j * k * l;
		if ((proizvod == (7.11*pow(100, 4))) && (l>k)) lista->dodaj(i,j,k,l);
}


/*void main() {

	unsigned long broj_poziva=0;

	cout << "Program pretrazuje uredjene cetvorke... \n";
	for (int i = 1; i <= 711; i++) {
		for (int j = i; j <= 711; j++) {
			for (int k = j; k <= 711; k++) {
				int l = 711 - i - k - j;
				Lista::provera(i, j, k, l);
				broj_poziva++;
			}
		}
	}

	cout << "Uredjene cetvorke su:\n";
	for (Lista::Elem* tek = lista->prvi; tek != nullptr; tek = tek->sled)
		cout << "(" << tek->cetvorka[0] / 100 << ", " << tek->cetvorka[1] / 100 << ", " << tek->cetvorka[2] / 100 << ", " << tek->cetvorka[3] / 100 << ")\n";

	cout << "Broj poziva optimizacione funkcije je: " << broj_poziva << "\n";

	system("pause");
	delete lista;
} */



