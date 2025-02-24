# main.py

from src.bot.whatsapp_bot import WhatsAppBot
import time

def main():
    bot = WhatsAppBot()
    
    try:
        # Iniciar bot
        if not bot.start():
            print("Erro ao iniciar o bot")
            return
            
        print("Aguardando login no WhatsApp Web...")
        if not bot.wait_for_login():
            print("Erro ao fazer login")
            return
            
        print("Login realizado com sucesso!")
        
        while True:
            print("\n=== WhatsApp Bot ===")
            print("1. Iniciar atendimento automatico")
            print("2. Enviar mensagem manual")
            print("3. Sair")
            
            opcao = input("\nEscolha uma opcao: ")
            
            if opcao == "1":
                contato = input("Digite o nome do contato: ")
                if bot.start_service(contato):
                    print("\nAtendimento iniciado. Pressione Ctrl+C para parar.")
                    try:
                        bot.monitor_messages(callback=print)
                    except KeyboardInterrupt:
                        bot.stop_monitoring()
                        print("\nMonitoramento interrompido!")
                else:
                    print("Erro ao iniciar atendimento")
                    
            elif opcao == "2":
                contato = input("Digite o nome do contato: ")
                mensagem = input("Digite a mensagem: ")
                if bot.message_handler.send_message(contato, mensagem):
                    print("Mensagem enviada com sucesso!")
                else:
                    print("Erro ao enviar mensagem")
                    
            elif opcao == "3":
                print("Encerrando o bot...")
                break
                
            else:
                print("Opcao invalida!")
                
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        bot.quit()

if __name__ == "__main__":
    main()