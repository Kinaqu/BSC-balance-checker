from web3 import Web3

def load_wallets(file_path):
    """Загрузка адресов кошельков из файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            wallets = [line.strip() for line in file if line.strip()]
        return wallets
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []

def check_balance(wallet_address, web3):
    """Проверка баланса кошелька."""
    try:
        if not web3.is_address(wallet_address):
            print(f"Некорректный адрес кошелька: {wallet_address}")
            return wallet_address, None

        balance_wei = web3.eth.get_balance(wallet_address)
        balance_bnb = web3.from_wei(balance_wei, 'ether')
        return wallet_address, balance_bnb
    except Exception as e:
        print(f"Ошибка при проверке баланса {wallet_address}: {e}")
        return wallet_address, None

def main():
    # Подключение к узлу Binance Smart Chain
    bsc_rpc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc_rpc))
    
    if not web3.is_connected():
        print("Ошибка подключения к сети Binance Smart Chain")
        return
    
    # Загрузка адресов кошельков из файла
    wallet_file = "wallets.txt"
    wallets = load_wallets(wallet_file)
    
    if not wallets:
        print("Файл кошельков пуст или не найден.")
        return
    
    # Проверка балансов
    results = []
    for wallet in wallets:
        print(f"Проверяется кошелек: {wallet}")
        address, balance = check_balance(wallet, web3)
        if balance is not None:
            print(f"Баланс кошелька {address}: {balance} BNB")
        else:
            print(f"Ошибка при проверке баланса {address}")
        results.append((address, balance))
    
    # Сохранение результатов в файл
    output_file = "balances.txt"
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for address, balance in results:
            if balance is not None:
                out_file.write(f"{address}: {balance} BNB\n")
            else:
                out_file.write(f"{address}: Ошибка проверки\n")
    
    print(f"Результаты сохранены в файл: {output_file}")

# Запуск программы
if __name__ == "__main__":
    main()
