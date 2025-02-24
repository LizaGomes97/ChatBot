from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class WhatsAppBot:
    def __init__(self):
        print("Iniciando o bot...")
        # Carregar configurações
        self.carregar_configuracoes()
        
        try:
            # Configurar o Chrome
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # Inicializar o driver com o serviço
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Abrir WhatsApp Web
            self.driver.get("https://web.whatsapp.com")
            print("Por favor, escaneie o QR Code...")
            
            # Aguardar login
            self.wait_for_login()
        except Exception as e:
            print(f"Erro ao inicializar o Chrome: {e}")
            raise e

    def carregar_configuracoes(self):
        self.config = {
            "boas_vindas": """Ola! Bem-vindo ao atendimento da Drogasil.

Por favor, escolha uma opcao:

• Digite 1 - Consultar precos
• Digite 2 - Verificar disponibilidade
• Digite 3 - Horario de funcionamento
• Digite 4 - Falar com atendente""",
            "respostas": {
                "1": "Para consultar precos, por favor me informe o nome do medicamento:",
                "2": "Para verificar disponibilidade, me informe o produto que procura:",
                "3": "Nossa loja esta aberta:\nSeg-Sab: 07h as 22h\nDomingo: 08h as 20h",
                "4": "Transferindo para um atendente...\n\nLizandra: Ola! Como posso ajudar voce hoje?"
            }
        }

    def wait_for_login(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#pane-side'))
            )
            print("Login realizado com sucesso!")
        except Exception as e:
            print("Erro ao fazer login:", e)
            self.driver.quit()

    def enviar_mensagem(self, contato, mensagem):
        try:
            # Buscar contato
            search_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            time.sleep(2)
            search_box.send_keys(contato)
            time.sleep(3)
            
            # Clicar no contato
            contato_elemento = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//span[@title='{contato}']"))
            )
            contato_elemento.click()
            time.sleep(2)
            
            # Enviar mensagem
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Dividir mensagem em linhas
            linhas = mensagem.split('\n')
            for i, linha in enumerate(linhas):
                message_box.send_keys(linha)
                if i < len(linhas) - 1:
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            message_box.send_keys(Keys.ENTER)
            
            print(f"Mensagem enviada para {contato}!")
            return True
            
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False

    def iniciar_atendimento(self, contato):
        # Enviar menu inicial
        if self.enviar_mensagem(contato, self.config["boas_vindas"]):
            print("\nMenu inicial enviado. Iniciando monitoramento automatico...")
            print("IMPORTANTE: Use Ctrl + C para parar o monitoramento e voltar ao menu")
            self.monitorar_mensagens()
        else:
            print("Não foi possível iniciar o atendimento automático.")
        
    def monitorar_mensagens(self):
        print("\nMonitorando mensagens...")
        print("Pressione Ctrl + C para parar o monitoramento e voltar ao menu principal")
        print("\nAguardando mensagens...\n")
        
        ultima_mensagem_processada = ""  # Variável para guardar a última mensagem
        
        try:
            while True:
                try:
                    # Tentar encontrar mensagens
                    mensagens = self.driver.find_elements(By.CSS_SELECTOR, 'div.message-in, div._1Gy50, div[data-pre-plain-text]')
                    
                    if mensagens:
                        mensagem_atual = mensagens[-1].text.strip()
                        
                        # Só processa se for uma mensagem nova
                        if mensagem_atual != ultima_mensagem_processada:
                            print(f"Nova mensagem detectada: {mensagem_atual}")
                            ultima_mensagem_processada = mensagem_atual
                            
                            # Verificar se é uma opção válida
                            if mensagem_atual in ["1", "2", "3", "4"]:
                                resposta = self.config["respostas"].get(mensagem_atual)
                                print(f"Enviando resposta para opção {mensagem_atual}")
                                
                                # Enviar resposta
                                message_box = WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                                )
                                
                                linhas = resposta.split('\n')
                                for i, linha in enumerate(linhas):
                                    message_box.send_keys(linha)
                                    if i < len(linhas) - 1:
                                        message_box.send_keys(Keys.SHIFT + Keys.ENTER)
                                message_box.send_keys(Keys.ENTER)
                                print("Resposta enviada com sucesso!")
                                time.sleep(1)
                    
                    time.sleep(2)
                
                except KeyboardInterrupt:
                    print("\nMonitoramento interrompido!")
                    print("Voltando ao menu principal...")
                    return
                    
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")
                    time.sleep(2)
                    
        except KeyboardInterrupt:
            print("\nMonitoramento interrompido!")
            print("Voltando ao menu principal...")
            return
            
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
            print("Voltando ao menu principal...")

if __name__ == "__main__":
    try:
        bot = WhatsAppBot()
        time.sleep(5)
        
        while True:
            print("\n=== WhatsApp Bot ===")
            print("1. Iniciar atendimento automatico")
            print("2. Enviar mensagem manual")
            print("3. Sair")
            
            opcao = input("\nEscolha uma opcao: ")
            
            if opcao == "1":
                contato = input("Digite o nome do contato: ")
                bot.iniciar_atendimento(contato)
            elif opcao == "2":
                contato = input("Digite o nome do contato: ")
                mensagem = input("Digite a mensagem: ")
                bot.enviar_mensagem(contato, mensagem)
            elif opcao == "3":
                print("Encerrando o bot...")
                bot.driver.quit()
                break
            else:
                print("Opcao invalida!")
                
    except Exception as e:
        print(f"Erro inesperado: {e}")
        try:
            bot.driver.quit()
        except:
            pass