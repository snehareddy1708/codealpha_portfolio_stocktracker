import http.client
import json

# Function to retrieve stock data from Alpha Vantage using http.client
def get_stock_data(symbol, api_key):
    conn = http.client.HTTPSConnection("www.alphavantage.co")
    conn.request("GET", f"/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}")
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    stock_data = json.loads(data)
    if 'Global Quote' in stock_data:
        return stock_data
    return None

class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] += quantity
        else:
            self.stocks[symbol] = quantity

    def remove_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] -= quantity
            if self.stocks[symbol] <= 0:
                del self.stocks[symbol]

    def get_portfolio_value(self, api_key):
        total_value = 0
        for symbol, quantity in self.stocks.items():
            stock_data = get_stock_data(symbol, api_key)
            if stock_data and 'Global Quote' in stock_data:
                price = float(stock_data['Global Quote']['05. price'])
                total_value += price * quantity
        return total_value

def calculate_gain_loss(initial_value, current_value):
    return current_value - initial_value

def calculate_diversification(portfolio, api_key):
    sector_weights = {}
    total_value = portfolio.get_portfolio_value(api_key)

    
    if total_value == 0:
        return {}  

    for symbol, quantity in portfolio.stocks.items():
        stock_data = get_stock_data(symbol, api_key)
        if stock_data and 'Global Quote' in stock_data:
            sector = 'USD'  # Mock sector as USD for diversification
            if sector in sector_weights:
                sector_weights[sector] += quantity * float(stock_data['Global Quote']['05. price'])
            else:
                sector_weights[sector] = quantity * float(stock_data['Global Quote']['05. price'])

    diversification = {sector: (value / total_value) * 100 for sector, value in sector_weights.items()}
    return diversification

def main():
    api_key = '3A89Q8KRTTJVWW9O'  
    portfolio = Portfolio()
    initial_value = float(input("Enter initial portfolio value: "))

    while True:
        print("\n1. Add stock to portfolio")
        print("2. Remove stock from portfolio")
        print("3. View portfolio value")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            portfolio.add_stock(symbol, quantity)
        elif choice == '2':
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            portfolio.remove_stock(symbol, quantity)
        elif choice == '3':
            value = portfolio.get_portfolio_value(api_key)
            print(f"\nPortfolio value: ${value:.2f}")
            print(f"Gains/Losses: ${calculate_gain_loss(initial_value, value):.2f}")
            print("Diversification:")
            for sector, weight in calculate_diversification(portfolio, api_key).items():
                print(f"{sector}: {weight:.2f}%")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
