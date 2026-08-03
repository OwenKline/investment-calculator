import csv
import matplotlib.pyplot as plt

def main():

    initial_principal, monthly_contribution, rate, years, inflation_rate, choice = get_user_input()

    monthly_rate = get_monthly_rate(rate, choice)

    balance = initial_principal
    total_interest = 0

    balance, total_interest, years_graph, interest_graph, balances_graph = calculate_growth(initial_principal, monthly_contribution, monthly_rate, years)

    display_summary(balance, total_interest, initial_principal, monthly_contribution, years, inflation_rate)

    save_to_csv(years_graph, interest_graph, balances_graph)

    plot_graph(years_graph, balances_graph)

def get_user_input():
    initial_principal = float(input("Enter the principal amount: "))
    monthly_contribution = float(input("Enter the monthly contribution: "))
    rate = float(input("Enter the annual interest rate (in %): ")) / 100
    years = int(input("Enter the number of years: "))
    inflation_rate = float(input("Enter the annual inflation rate (in %): ")) / 100

    print("\nCompounding Frequency")
    print("1. Annual")
    print("2. Quarterly")
    print("3. Monthly")
    print("4. Daily")
    
    choice = int(input("Choose an option (1-4): "))

    return initial_principal, monthly_contribution, rate, years, inflation_rate, choice

def get_monthly_rate(rate, choice):
    if choice == 1:
        return (1 + rate) ** (1/12) - 1
    elif choice == 2:
        return (1 + rate / 4) ** (1/3) - 1
    elif choice == 3:
        return rate / 12
    elif choice == 4:
        return (1 + rate / 365) ** (365/12) - 1

def calculate_growth(initial_principal, monthly_contribution, monthly_rate, years):
    years_graph = []
    interest_graph = []
    balances_graph = []
    balance = initial_principal
    total_interest = 0
    for year in range(1, years + 1):
        yearly_interest = 0
        for month in range(1, 13):
            interest = balance * monthly_rate
            balance += interest
            yearly_interest += interest
            total_interest += interest
            balance += monthly_contribution
        years_graph.append(year)
        interest_graph.append(yearly_interest)
        balances_graph.append(balance)
        print(f"{year:<5}{f'${yearly_interest:.2f}':>15}{f'${balance:.2f}':>18}")
    return balance, total_interest, years_graph, interest_graph, balances_graph

def display_summary(balance, total_interest, initial_principal, monthly_contribution, years, inflation_rate):
    print("\nYear\tInterest Earned\t  Ending Balance")

    total_principal = initial_principal + monthly_contribution * years * 12
    principal_percentage = (total_principal / balance) * 100
    interest_percentage = (total_interest / balance) * 100
    real_balance = balance / ((1 + inflation_rate) ** years)

    print(f"\nEnding Balance: ${balance:.2f}")
    print(f"Total Principal: ${total_principal:.2f}")
    print(f"Total Interest Earned: ${total_interest:.2f}")
    print(f"Principal %: {principal_percentage:.2f}%")
    print(f"Interest %: {interest_percentage:.2f}%")
    print(f"Real Ending Balance (adjusted for inflation): ${real_balance:.2f}")

def save_to_csv(years_graph, interest_graph, balances_graph):
    with open("investment_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Interest", "Balance"])
        for year, interest, balance in zip(years_graph, interest_graph, balances_graph):
            writer.writerow([year, f"{interest:.2f}", f"{balance:.2f}"])

def plot_graph(years_graph, balances_graph):
    plt.plot(years_graph, balances_graph)
    plt.xlabel("Year")
    plt.ylabel("Balance ($)")
    plt.title("Investment Growth")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()