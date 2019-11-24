import Pyro4

class AtmCheck:
    @staticmethod
    def withdrawCheck():

        flag = True
        while flag:
            print("Please enter the amount of money you want to withdraw: ", end="")
            withdrawMoney = int(input())

            if withdrawMoney > 0:
                if withdrawMoney % 50 == 0:
                    flag = False
                elif withdrawMoney % 20 == 0:
                    flag = False
                else:
                    remainder = withdrawMoney % 50
                    if remainder % 20 == 0:
                        flag = False

            if flag:
                print("Make sure your withdraw is a positive number and a multiple of 50 or 20!")

        return withdrawMoney

    @staticmethod
    def depositCheck():
        flag = True
        while flag:
            print("Please enter the amount of money you want to deposit: ", end="")
            depositMoney = int(input())

            if depositMoney > 0 and depositMoney % 5 == 0:
                flag = False
            else:
                print("Make sure your deposit is a positive number and a multiple of 5!")

        return depositMoney

class CustomerInterface:
    @staticmethod
    def menu():

        flag = True
        while flag:
            print("Transactions available:")
            print("- Balance  => Press 0")
            print("- Deposit  => Press 1")
            print("- Withdraw => Press 2")
            choice = input("Please choose a transaction: ")
            if int(choice) >= 0 and int(choice) <= 2:
                flag = False
            else:
                print("Choose a valid transaction")
            print("")

        return choice

    @staticmethod
    def choosingTransaction(atmOperationsCall):
        flag = True
        while flag:
            choice = CustomerInterface.menu()

            print("Please enter your name: ", end="")
            name = input()

            if choice == '0':
                print("Your account balance is: ", end="")
                print(atmOperationsCall.getBalance(name))
            elif choice == '1':
                depositMoney = AtmCheck.depositCheck()

                print("Your account balance is: ", end="")
                print(atmOperationsCall.deposit(name, depositMoney))
            elif choice == '2':
                withdrawMoney = AtmCheck.withdrawCheck()

                print("Your account balance is: ", end="")
                print(atmOperationsCall.withdraw(name, withdrawMoney))

            print("\nDo you want to perform any more actions? (y / n): ", end="")
            answer = input()
            if answer == 'n' or answer == 'N':
                flag = False

def main():
    atmOperationsCall = Pyro4.Proxy("PYRONAME:atmOperations")

    CustomerInterface.choosingTransaction(atmOperationsCall)


if __name__ == '__main__':
    main()
