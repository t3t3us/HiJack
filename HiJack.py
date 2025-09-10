import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

#banner e menu

def banner():
    os.system('clear')
    print("\033[1;31m" + """
 ██░ ██  ██▓    ▄▄▄██▀▀▀▄▄▄       ▓█████▄ ▓██   ██▓
▓██░ ██▒▓██▒      ▒██  ▒████▄    ▒██▀ ██▌ ▒██  ██▒
▒██▀▀██░▒██▒      ░██  ▒██  ▀█▄  ░██   █▌  ▒██ ██░
░▓█ ░██ ░██░   ▓████▓ ░██▄▄▄▄██ ░▓█▄   ▌  ░ ▐██▓░
░▓█▒░██▓░██░    ▓███▒   ▓█   ▓██▒░▒████▓   ░ ██▒▓░
 ▒ ░░▒░▒░▓      ▒▓▒▒░   ▒▒   ▓▒█░ ▒▒▓  ▒    ██▒▒▒
 ▒ ░▒░ ░ ▒ ░    ▒ ░▒░    ▒   ▒▒ ░ ░ ▒  ▒   ▓██ ░▒░
 ░  ░░ ░ ▒ ░    ░ ░ ░    ░   ▒    ░ ░  ░   ▒ ▒ ░░
 ░   ░ ░      ░   ░        ░  ░   ░      ░ ░
                                 ░        ░ ░
    Ferramenta de Testes de Segurança Web
    \033[0m
""")

def mostrar_menu():
    print("\n\033[1;33mSelecione uma opção:\033[0m")
    print("🛡️  \033[1;32m1 - Testar vulnerabilidade a Clickjacking\033[0m")
    print("🔍  \033[1;34m2 - Exibir principais headers de segurança\033[0m")
    print("🪓  \033[1;31m3 - Testar vulnerabilidade a XSS (Cross-Site Scripting)\033[0m")
    print("🚪  \033[1;37m0 - Sair\033[0m")

def linha():
    print("\033[1;30m" + "="*60 + "\033[0m")

def toma_jack():
    mensagens = [
        "Toma jack Toma jack Toma jack",
        "Toma jack na via gaúcha",
        "Toma jack toda vida",
        "Toma jack dos menor que tem ódio",
    ]
    print(f"\n\033[1;35m{random.choice(mensagens)}\033[0m\n")
    time.sleep(1)

#testes de segurança 

def clickjacking_test(url):
    linha()
    print(f"\033[1;36m[•] Testando Clickjacking em:\033[0m {url}")
    html_content = f'''
    <html>
      <body>
        <iframe src="{url}" width="500" height="500"></iframe>
      </body>
    </html>
    '''
    html_path = os.path.abspath('test_clickjacking.html')
    try:
        with open(html_path, 'w') as f:
            f.write(html_content)
        options = Options()
        options.headless = True
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.get("file://" + html_path)
        time.sleep(2)
        try:
            iframe = driver.find_element("tag name", "iframe")
            driver.switch_to.frame(iframe)
            driver.find_element("tag name", "body")
            print("\033[1;32m[+] Vulnerável a Clickjacking! O site carregou no iframe.\033[0m")
        except Exception:
            print("\033[1;31m[-] Protegido contra Clickjacking (iframe bloqueado).\033[0m")
        finally:
            driver.quit()
    except Exception as e:
        print(f"\033[1;31m[ERRO] Falha no teste: {e}\033[0m")
    finally:
        if os.path.exists(html_path):
            os.remove(html_path)
    linha()
    toma_jack()

def headers_info(url):
    linha()
    print(f"\033[1;34m[•] Verificando headers de segurança em:\033[0m {url}")
    try:
        #ignora avisos de ssl invalido pra ambientes de teste
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, timeout=10, verify=False)
        headers = response.headers
        security_headers = {
            'X-Frame-Options': headers.get('X-Frame-Options', 'NÃO PRESENTE'),
            'Content-Security-Policy': headers.get('Content-Security-Policy', 'NÃO PRESENTE'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'NÃO PRESENTE'),
            'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'NÃO PRESENTE'),
            'Referrer-Policy': headers.get('Referrer-Policy', 'NÃO PRESENTE'),
            'Permissions-Policy': headers.get('Permissions-Policy', 'NÃO PRESENTE'),
            'X-XSS-Protection': headers.get('X-XSS-Protection', 'NÃO PRESENTE'),
            'Set-Cookie': headers.get('Set-Cookie', 'NÃO PRESENTE'),
            'Server': headers.get('Server', 'NÃO INFORMADO')
        }
        print("\n\033[1;34m--- Principais Headers de Segurança ---\033[0m")
        for header, valor in security_headers.items():
            if valor != 'NÃO PRESENTE' and valor != 'NÃO INFORMADO':
                print(f"\033[1;32m{header}:\033[0m {valor}")
            else:
                print(f"\033[1;31m{header}:\033[0m {valor}")
        print()
    except Exception as e:
        print(f"\033[1;31m[ERRO] Falha ao obter headers: {e}\033[0m")
    linha()
    toma_jack()

def xss_test(url):
    linha()
    print("\033[1;31m[!] Função de teste XSS em breve...\033[0m")
    linha()
    toma_jack()

#loop principal do script

def main():
    banner()
    while True:
        mostrar_menu()
        opcao = input("\n\033[1;33mDigite sua opção:\033[0m ").strip()
        if opcao == '1':
            url = input("\033[1;36mInforme a URL a ser testada:\033[0m ").strip()
            clickjacking_test(url)
        elif opcao == '2':
            url = input("\033[1;34mInforme a URL para análise de headers:\033[0m ").strip()
            headers_info(url)
        elif opcao == '3':
            url = input("\033[1;31mInforme a URL para teste XSS:\033[0m ").strip()
            xss_test(url)
        elif opcao == '0':
            print("\033[1;37mSaindo... Até logo!\033[0m")
            toma_jack()
            break
        else:
            print("\033[1;31mOpção inválida. Tente novamente.\033[0m")

if __name__ == "__main__":
    main()
