#include <stdio.h>
#include <iostream>
#define N 10
#define K 8
using namespace std;

/* 1    2    3    4    5    6    7    8    9   10
|  A    B    C    D    E    F    G    H    I    J
-- - +----------------------------------------------------
1 A | 0    374  200  223  108  178  252  285  240  356
2 B | 374  0    255  166  433  199  135  95   136  17
3 C | 200  255  0    128  277  821  180  160  131  247
4 D | 223  166  128  0    430  47   52   84   40   155
5 E | 108  433  277  430  0    453  478  344  389  423
6 F | 178  199  821  47   453  0    91   110  64   181
7 G | 252  135  180  52   478  91   0    114  83   117
8 H | 285  95   160  84   344  110  114  0    47   78
9 I | 240  136  131  40   389  64   83   47   0    118
10J | 356  17   247  155  423  181  117  78   118  0   */

int matrica[11][11] = {
	0,0,0,0,0,0,0,0,0,0,0,
	0,0,374,200,223,108,178,252,285,240,356,
	0,374,0,255,166,433,199,135,95,136,17,
	0,200,255,0,128,277,821,180,160,131,247,
	0,223,166,128,0,430,47,52,84,40,155,
	0,108,433,277,430,0,453,478,344,389,423,
	0,178,199,821,47,453,0,91,110,64,181,
	0,252,135,180,52,478,91,0,114,83,117,
	0,285,95,160,84,344,110,114,0,47,78,
	0,240,136,131,40,389,64,83,47,0,118,
	0,356,17,247,155,423,181,117,78,118,0
};

char dohvati_grad(int pozicija) {
	char slovo;
	switch (pozicija) {
	case 1:
		slovo = 'A';
		break;
	case 2:
		slovo = 'B';
		break;
	case 3:
		slovo = 'C';
		break;
	case 4:
		slovo = 'D';
		break;
	case 5:
		slovo = 'E';
		break;
	case 6:
		slovo = 'F';
		break;
	case 7:
		slovo = 'G';
		break;
	case 8:
		slovo = 'H';
		break;
	case 9:
		slovo = 'I';
		break;
	case 10:
		slovo = 'J';
		break;
	default:
		slovo = 'Q';
	}
	return slovo;
}

int min = -1; 
int sum = 0;
int* stablo = new int[2 * (K + 1)];
int* min_stablo = new int[2 * (K + 1)]; 

class Stabla {
public:

	class Elem {
	public:
		int* stablo;
		Elem* sled;

		Elem(int* s) {
			stablo = new int[18];
			for (int i = 0; i < 18; i++)
				stablo[i] = s[i];
			sled = nullptr;
		}

		~Elem() {
			delete[] stablo;
		} 
	};

	Elem* prvi = 0;

	~Stabla() {
		obrisi_stabla();
	}

	void dodaj_stablo(int* s) {
		Elem* novi = new Elem(s);
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

	void obrisi_stabla() {
		Elem* tek = prvi;
		Elem* stari = nullptr;
		while (tek) {
			stari = tek;
			tek = tek->sled;
			delete stari;
		}
		prvi = nullptr;
	}
};

Stabla* lista = new Stabla();

void prebaci_sekvencu_u_stablo(int* P, int len, int* T) {

	int i, j;
	int q = 0;
	int n = len + 2;
	int* V = new int[n];

	for (int i = 0; i < n; i++) V[i] = 0;
	
	for (int i = 0; i < len; i++) V[P[i] - 1] += 1;
	
	for (int i = 0; i < len; i++) {
		for (int j = 0; j < n; j++) {
			if (V[j] == 0)
			{
				V[j] = -1;
				T[q++] = j + 1;
				T[q++] = P[i];
				V[P[i] - 1]--;
				break;
			}
		}
	}
	j = 0;
	for (int i = 0; i < n; i++) 
	{
		if (V[i] == 0 && j == 0)
		{
			T[q++] = i + 1;
			j++;
		}
		else if (V[i] == 0 && j == 1) 
		{
			T[q++] = i + 1;
			break;
		}
	}
	delete[] V;
}

void varijacije_sa_ponavljanjem(int n, int k) {
	int q;
	int *P = new int[k];
	bool iskoci = false;

	for (int i = 0; i < k; i++) P[i] = 0;
	
	int sekvenca[K];
	for (int i = 0; i < K; i++) sekvenca[i] = 0;

	int duzina = sizeof(sekvenca) / sizeof(sekvenca[0]);
	
	int* brojaci = new int[N + 1];
	for (int i = 0; i < N + 1; i++) brojaci[i] = 0;

	do {
		for (int i = 0; i < k; i++) sekvenca[i] = P[i] + 1;
		
		prebaci_sekvencu_u_stablo(sekvenca, duzina, stablo);

		if (min == -1) 
		{
			int i = -1;
			while (i < 2 * (duzina + 1) - 1) {
				sum += matrica[stablo[i + 1]][stablo[i + 2]];
				brojaci[stablo[i + 1]]++;
				brojaci[stablo[i + 2]]++;
				i += 2;
			}
			for (int i = 0; i < N + 1; i++) {
				if (brojaci[i] >= 4) sum += (brojaci[i] - 3) * 100;
			}
			min = sum;
			for (int i = 0; i < 2 * (duzina + 1); i++) min_stablo[i] = stablo[i];
		}
		else 
		{
			sum = 0;
			int i = -1;
			iskoci = false;
			for (int i = 0; i < N + 1; i++) brojaci[i] = 0;
			
			while (i < 2 * (duzina + 1) - 1) {
				sum += matrica[stablo[i + 1]][stablo[i + 2]];
				if (sum > min) {
					iskoci = true;
					break;
				}
				brojaci[stablo[i + 1]]++;
				brojaci[stablo[i + 2]]++;
				i += 2;
			}
			if (iskoci == false) {
				for (int i = 0; i < N + 1; i++) {
					if (brojaci[i] >= 4) sum += (brojaci[i] - 3) * 100;
				}
				if (sum == min) lista->dodaj_stablo(stablo);
				else if (sum < min) {
					min = sum;
					lista->obrisi_stabla();
					lista->dodaj_stablo(stablo);
				}
			}
		}
		q = k - 1;
		while (q >= 0) 
		{
			P[q]++;
			if (P[q] == n) 
			{
				P[q] = 0;
				q--;
			}
			else break;
		}
	} while (q >= 0);

	delete[]P;
	delete[]brojaci;
}

/*int main() {
	cout << "Povezivanje gradova u mrezu je zapocelo...\n";
	varijacije_sa_ponavljanjem(N, K);
	int len = K;
	cout << "Putanja: \n";

	Stabla::Elem* tek = lista->prvi;

	while (tek != nullptr) {
		for (int i = 0; i < 2 * (len + 1); i++) {
			char grad = dohvati_grad(tek->stablo[i]);
			cout << grad;
			if ((i + 1) % 2 == 0 && i < 2 * len)
				cout << "-";
		}
		cout << "\n";
		tek = tek->sled;
	}
	cout << "\n";
	cout << "Minimalna cena mreze za povezivanje je: " << min << "\n";
	delete stablo;
	delete min_stablo;
	delete lista;
	system("pause");
	return 0;
} */

