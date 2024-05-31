#ifndef USER_H
#define USER_H

#include <string>
#include <vector>

class User {
private:
    int id;
    std::string username, password;
    double balance;

public:
    User(int id, const std::string& username, const std::string& password);

    std::string getUsername();
    std::string getPassword();
    double getBalance();
    void change_Password();
    void add_expense();
    void set_budget();
    void update_balance();
};

#endif