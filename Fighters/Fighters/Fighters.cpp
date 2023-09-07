// Fighters.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include <iostream>
#include <stdlib.h>
#include <time.h> 
#include <string>

class Entity {
    private:
        int MaxHealth;
        int Health;
        int Strength;
        int Accuracy;
        std::string Name;
        

    public:
        Entity(std::string name, int health, int strength, int accuracy) {
            Name = name;
            Health = health;
            MaxHealth = health;
            Strength = strength;
            Accuracy = accuracy;
            std::cout << "Utworzono postac\n" << "Imie: " << Name << "\nIlosc zdrowia: " << Health << "\nSila: " << Strength << "\nCelnosc: " << Accuracy << std::endl;
    }
        std::string getName() {
            return Name;
        }

        int getDmg() {
            if (rand() % 20 < Accuracy) {
                int dmg = rand() % Strength + 1;
                std::cout << std::endl << Name << " uderzyl przeciwnika z sila " << dmg;
                return dmg;
            }
            else
                std::cout << std::endl << Name << " nie trafil!";
                return 0;
        }

        void getHit(int dmg) {
            Health -= dmg;
        }

        void heal(){
            int heal = rand() % 30 + 15;
            Health += heal;
            std::cout << std::endl << Name << " uleczyl sie o " << heal << " punkty zdrowia!";
        }

        int getHealth() {
            return Health;
        }

        bool isAlive() {
            if (Health > 0)
                return true;
            else 
                return false;
        }

        int action() {
            if (Health < MaxHealth - 30 && rand() % 4 == 3) {
                heal();
                return 0;
            }
            else
                getDmg();
        }
};


int main()
{
    srand(time(NULL));
    Entity Gawel("Gawel", 100, 20, 13);
    std::string name;
    int health, strength, accuracy;
    
    std::cout << "Podaj imie swojej postaci: ";
    std::cin >> name;
    std::cout << "Ilosc zdrowia: ";
    std::cin >> health;
    std::cout << "Sila: ";
    std::cin >> strength;
    std::cout << "Celnosc: ";
    std::cin >> accuracy;


    Entity Player(name, health, strength, accuracy);
    int turn = 0;
    while (Gawel.isAlive() && Player.isAlive()) {
        turn++;
        std::cout << std::endl << "Turn " << turn << ".";
        Gawel.getHit(Player.action());
        Player.getHit(Gawel.action());
        
        std::cout << "\nPlayer health: " << Player.getHealth() << "\nGawel health: " << Gawel.getHealth() << std::endl;
    }
    std::string loser;
    if (!Player.isAlive())
        loser = Player.getName();
    else
        loser = Gawel.getName();
    std::cout << loser << " przegral pojedynek!" << std::endl;;

}

// Uruchomienie programu: Ctrl + F5 lub menu Debugowanie > Uruchom bez debugowania
// Debugowanie programu: F5 lub menu Debugowanie > Rozpocznij debugowanie

// Porady dotyczące rozpoczynania pracy:
//   1. Użyj okna Eksploratora rozwiązań, aby dodać pliki i zarządzać nimi
//   2. Użyj okna programu Team Explorer, aby nawiązać połączenie z kontrolą źródła
//   3. Użyj okna Dane wyjściowe, aby sprawdzić dane wyjściowe kompilacji i inne komunikaty
//   4. Użyj okna Lista błędów, aby zobaczyć błędy
//   5. Wybierz pozycję Projekt > Dodaj nowy element, aby utworzyć nowe pliki kodu, lub wybierz pozycję Projekt > Dodaj istniejący element, aby dodać istniejące pliku kodu do projektu
//   6. Aby w przyszłości ponownie otworzyć ten projekt, przejdź do pozycji Plik > Otwórz > Projekt i wybierz plik sln
