import httpx

print("online prevodnik men dle kurzu cnb")

url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt;jsessionid=189EF7A03CFCE3D9CF6F43DC0F7928A0?date=13.02.2025"

r = httpx.get(url)

in_array = r.text.split("\n") 

print(in_array)

for line in in_array:
    if "|EUR|" in line:
        print(line)

castka = input("Zadej castku v CZK: ")
result = int(castka) * 25
print(f"To je v EUR: {result}")