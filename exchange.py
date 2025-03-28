#import httpx
#
#URL = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt;jsessionid=189EF7A03CFCE3D9CF6F43DC0F7928A0?date=13.02.2025"
#
#def get_exchange_rate():
#    try:
#        response = httpx.get(URL, timeout=10)
#        response.raise_for_status()
#        
#        for line in response.text.split("\n"):
#            if "|EUR|" in line:
#                parts = line.split("|")
#                return float(parts[4].replace(",", "."))
#    except (httpx.RequestError, ValueError, IndexError) as e:
#        print(f"Chyba: {e}")
#        return None
#
#def convert_currency(amount, rate, direction):
#    if direction == "CZK->EUR":
#        return amount / rate
#    elif direction == "EUR->CZK":
#        return amount * rate
#    else:
#        return None
#
#def main():
#    print("Online převodník EUR a CZK")
#    
#    rate = get_exchange_rate()
#    if rate is None:
#        print("Aktuální kurz nenalezen")
#        return
#    
#    print(f"Aktuální kurz EUR/CZK: {rate}")
#    
#    while True:
#        direction = input("Zvolte typ převodu (CZK->EUR nebo EUR->CZK): ").strip()
#        if direction in ("CZK->EUR", "EUR->CZK"):
#            break
#        print("Neplatná volba. Zadejte 'CZK->EUR' nebo 'EUR->CZK'.")
#    
#    while True:
#        try:
#            amount = float(input("Zadejte částku: ").strip())
#            if amount < 0:
#                raise ValueError("Částka musí být kladná.")
#            break
#        except ValueError as e:
#            print(f"Neplatný vstup: {e}")
#    
#    result = convert_currency(amount, rate, direction)
#    print(f"Výsledek převodu: {result:.2f} {'EUR' if direction == 'CZK->EUR' else 'CZK'}")
#
#if __name__ == "__main__":
#    main()
#