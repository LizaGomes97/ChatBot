# src/bot/whatsapp_bot.py

from ..config.messages import Messages
from .browser_manager import BrowserManager
from .message_handler import MessageHandler
import time

class WhatsAppBot:
    def __init__(self):
        self.browser = BrowserManager()
        self.message_handler = None
        self.is_monitoring = False
        
    def start(self):
        """Inicializa o bot"""
        if self.browser.initialize_browser():
            self.message_handler = MessageHandler(self.browser)
            self.browser.open_whatsapp()
            return True
        return False
        
    def wait_for_login(self):
        """Aguarda o login no WhatsApp Web"""
        return self.browser.is_logged_in()
    
    def start_service(self, contact):
        """Inicia o atendimento automático"""
        try:
            if self.message_handler.send_message(contact, Messages.WELCOME_MESSAGE):
                self.is_monitoring = True
                print("\nAtendimento iniciado. Pressione Ctrl+C para parar.")
                return True
            return False
        except Exception as e:
            print(f"Erro ao iniciar serviço: {e}")
            return False
    
    def monitor_messages(self, callback=None):
        """Monitora as mensagens recebidas"""
        try:
            while self.is_monitoring:
                try:
                    message = self.message_handler.get_latest_message()
                    if message:
                        if callback:
                            callback(f"Nova mensagem: {message}")
                            
                        if message in ["1", "2", "3", "4"]:
                            response = Messages.get_response(message)
                            self.message_handler.send_message(None, response)
                            if callback:
                                callback(f"Resposta enviada para opção {message}")
                    
                    time.sleep(2)
                    
                except KeyboardInterrupt:
                    print("\nMonitoramento interrompido!")
                    self.stop_monitoring()
                    return
                    
                except Exception as e:
                    if callback:
                        callback(f"Erro ao processar mensagem: {e}")
                    time.sleep(2)
                    
        except KeyboardInterrupt:
            print("\nMonitoramento interrompido!")
            self.stop_monitoring()
            return
    
    def stop_monitoring(self):
        """Para o monitoramento de mensagens"""
        self.is_monitoring = False
        print("Voltando ao menu principal...")
    
    def quit(self):
        """Encerra o bot"""
        self.stop_monitoring()
        self.browser.quit()