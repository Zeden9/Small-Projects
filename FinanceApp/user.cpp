#include <vector>
#include <ios>
#include <iostream>
#include <fstream>
#include <string>
#include "user.h"
#pragma once

User::User(int id, const std::string& username, const std::string& password)
{
    this->username = username;
    this->password = password;
    this->balance = 0;
    this->id = id;
};


std::string User::getUsername() { return this->username; }
std::string User::getPassword() { return this->password; }


void User::change_Password()
{
    std::string passwordInput;
    std::cout << "Enter your password: ";
    std::cin >> passwordInput;
    if (passwordInput == this->getPassword())
    {

        std::string fileContent;
        std::cout << "Enter your new password: ";
        std::cin >> this->password;
        std::ifstream usersFileIn("usersData\\users.txt");
        if (usersFileIn.is_open())
        {
            std::string data;
            while (usersFileIn >> data)
            {
                if (data[0] == static_cast<char>(this->id + '0'))
                {
                    std::string newData = std::to_string(this->id) + ',' + this->getUsername() + ',' + this->getPassword();
                    fileContent += newData;
                }
                else fileContent += data;
                fileContent += '\n';
            }
        }
        usersFileIn.close();
        std::ofstream usersFileOut("usersData\\users.txt");
        if (usersFileOut.is_open())
        {
            usersFileOut << fileContent;
        }
        usersFileOut.close();
        


    }
}

double User::getBalance() {
    return this->balance;
};
void User::add_expense() {};
void User::set_budget() {};
void User::update_balance() {};






    //void AddExpense() 
    //{
    //    system("cls");
    //    int choice, category = 0;
    //    double amount = 0;
    //    while (category == 0)
    //    {
    //        std::cout << "What's the category of the expense?" << std::endl;
    //        for (int i = 0; )
    //            std::cin >> choice;
    //        if (choice > 0 && choice < 10) category = choice;
    //        else std::cout << "Invalid data" << std::endl;
    //    }
    //    while ()
    //        std::cout << "What's the amount?\n";
    //    std::cin >> amount;
    //}
