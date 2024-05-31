#include <iostream>
#include <iomanip>
#include <vector>
#include <map>
#include <ctime>
#include <fstream>
#include "user.h"


User* login(std::vector<User> &users) {
    std::string username, password;
    std::cout << "Username: ";
    std::cin >> username;
    std::cout << "Password: ";
    std::cin >> password;
    for (auto& user : users) {
        if (user.getUsername() == username && user.getPassword() == password) {
            return &user;
        }
    }
    return nullptr;
}


void signUp(std::vector<User> &users) {
    std::string username, password, password2;
    bool isSigned, success = 0;
    while (true) {
        std::cout << "Username: ";
        std::cin >> username;
        std::cout << "Password: ";
        std::cin >> password;
        std::cout << "Repeat password: ";
        std::cin >> password2;
        if (password != password2)
        {
            char tryAgain;
            while (true) {
                std::cout << "Passwords did not match. Do you want to try again? Y/N: ";
                std::cin >> tryAgain;
                if (tolower(tryAgain) == 'n') return;
                else if (tolower(tryAgain) != 'y') std::cout << "I don't understand your answer";
                else break;
            }
        }
        else break;
    }
        std::cout << "User registered successfully.\n";
        int id = users.size();
        User newUser = User(id, username, password);
        users.push_back(newUser);
        std::ofstream usersFile;
        usersFile.open("usersData\\users.txt", std::ios::app);
        usersFile << id << ',' << username << ',' << password << std::endl;
        usersFile.close();
        
        std::string command = "mkdir usersData\\ && mkdir userData\\expenses && mkdir userData\\budgets" + username;
        system(command.c_str());
}

std::vector<std::string> splitString(std::string& string)
{
    std::string placeholder;
    std::vector<std::string> userData;
    int i = 0;
    for (i; i <= string.length(); i++)
    {
        if (string[i] != ',' && string.length() != i) placeholder += string[i];
        else
        {
            userData.push_back(placeholder);
            placeholder = "";
        }
    }
    return userData;
}

std::vector<User> loadUsers()
{
    std::vector<User> output;
    std::ifstream usersFile("usersData\\users.txt");
    if (usersFile.is_open())
    {
        std::string data;
        while (usersFile >> data)
        {
            std::vector<std::string> user = splitString(data);
            User newUser(stoi(user[0]), user[1], user[2]);
            output.push_back(newUser);
        }
    }
    return output;

}

void main_Menu(User* usrptr)
{
    system("cls");
    int choice;
    while (true) {
        int choice;
        std::cout << "Welcome back, " + usrptr->getUsername() << "\nBalance: " << std::fixed << std::setprecision(2) << usrptr->getBalance() << std::endl;
        std::cout << "1. Update balance\n2. Add expense\n3. Set Budget\n4. Change password\n5. Sign out\n";
        std::cin >> choice;
        switch (choice)
        {
        case 1:
            usrptr->update_balance();
            break;
        case 2:
            usrptr->add_expense();
            break;
        case 3:
            usrptr->add_expense();
            break;
        case 4:
            usrptr->change_Password();
            break;
        case 5:
            system("cls");
            std::cout << "User succesfully signed out.\n";
            return;
        }
    }
}



int main() {    
    User* userPtr = nullptr;
    std::vector<User> users = loadUsers();
    int choice;

    while (true) {
        std::cout << "1. Login\n2. Sign Up\n3. Exit\n";
        std::cin >> choice;
        switch (choice)
        {
        case 1:
            userPtr = login(users);
            if (userPtr == nullptr)
            {
                system("cls");
                std::cout << "User not found.\n";
                break;
            }
            main_Menu(userPtr);

            /*std::cout << userPtr->getUsername() << std::endl;*/
            break;

        case 2:
            signUp(users);
            break;
        case 3:
            return false;
        }
    }

    
}

