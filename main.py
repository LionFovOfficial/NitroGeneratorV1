import os
import time
import random
import string
import requests

class NitroGen:
    def __init__(self):
        self.fileName = "Nitro Codes.txt"

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""_   _ _ _                                     
| \ | (_) |_ _ __ ___                          
|  \| | | __| '__/ _ \                         
| |\  | | |_| | | (_) |                        
|_|_\_|_|\__|_|  \___/           _             
 / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
| |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
| |_| |  __/ | | |  __/ | | (_| | || (_) | |   
 \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
""")
        time.sleep(2)

        self.slowType("Nitro Generator and Checker - Made by LionFov", .02)
        time.sleep(1)

        self.slowType("\nWie viele Codes sollen generiert und geprüft werden? ", .02, newLine=False)
        num = int(input(''))

        self.slowType("\nWebhook-URL eingeben (oder Enter zum Überspringen): ", .02, newLine=False)
        url = input('')
        webhook = url if url != "" else None

        if webhook:
            test_data = {"content": "✅ Webhook funktioniert! - Testnachricht von LionFov"}
            response = requests.post(webhook, json=test_data)
            if response.status_code != 204:
                print("❌ Webhook ungültig oder nicht erreichbar.")
            else:
                print("✅ Webhook erfolgreich getestet!")

        valid = []
        invalid = 0
        delay = 0.5  # Geschwindigkeit einstellen (Sekunden)

        for i in range(num):
            try:
                code = "".join(random.choices(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase,
                    k=16
                ))
                url = f"https://discord.gift/{code}"

                result = self.quickChecker(url, webhook)

                if result:
                    valid.append(url)
                else:
                    invalid += 1

                time.sleep(delay)

            except Exception as e:
                print(f"❌ Fehler bei {url} | {str(e)}")

            if os.name == "nt":
                os.system(f"title Nitro Generator and Checker - {len(valid)} Valid | {invalid} Invalid - Made by LionFov")
            else:
                print(f'\33]0;Nitro Generator and Checker - {len(valid)} Valid | {invalid} Invalid - Made by LionFov\a', end='', flush=True)

        print(f"""
Ergebnisse:
 ✅ Gültig: {len(valid)}
 ❌ Ungültig: {invalid}
 🎁 Gültige Codes: {', '.join(valid)}""")

        input("\nFertig! Drücke 5x Enter zum Schließen.")
        [input(i) for i in range(4, 0, -1)]

    def slowType(self, text, speed, newLine=True):
        for i in text:
            print(i, end="", flush=True)
            time.sleep(speed)
        if newLine:
            print()

    def quickChecker(self, nitro, notify=None):
        url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"✅ Gültig | {nitro}", flush=True)

            with open(self.fileName, "w") as file:
                file.write(nitro)

            if notify:
                requests.post(notify, json={"content": f"🎉 Gültiger Nitro-Code gefunden! @everyone\n{nitro}"})

            return True

        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 5)
            print(f"⚠️ Rate Limit erreicht! Warte {retry_after} Sekunden...")
            if notify:
                requests.post(notify, json={"content": f"⚠️ Rate Limit erreicht! Warte {retry_after} Sekunden..."})
            time.sleep(retry_after)
            return self.quickChecker(nitro, notify)

        else:
            print(f"❌ Ungültig | {nitro}", flush=True)
            return False

if __name__ == '__main__':
    Gen = NitroGen()
    Gen.main()
