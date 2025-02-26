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
        self.auto_welcome = False
        
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
            
    def monitor_new_chats(self, callback=None):
        """Monitora novos chats e envia mensagem de boas-vindas"""
        try:
            # Procura por chats não lidos
            unread_chats = self.browser.find_unread_chats()
            
            for chat in unread_chats:
                if callback:
                    callback(f"Nova mensagem detectada de: {chat['title']}")
                
                # Abre o chat
                if self.browser.open_chat(chat['element']):
                    # Envia mensagem de boas-vindas
                    if self.message_handler.send_message(None, Messages.WELCOME_MESSAGE):
                        if callback:
                            callback(f"Mensagem de boas-vindas enviada para: {chat['title']}")
                    time.sleep(2)
                    
        except Exception as e:
            if callback:
                callback(f"Erro ao monitorar novos chats: {e}")
    
    def toggle_auto_welcome(self, state):
        """Ativa/desativa o envio automático de boas-vindas"""
        self.auto_welcome = state
    
    def monitor_messages(self, callback=None):
        """Monitora as mensagens recebidas"""
        while self.is_monitoring:
            try:
                # Monitora novos chats se auto_welcome estiver ativado
                if self.auto_welcome:
                    self.monitor_new_chats(callback)
                
                # Monitora mensagens do chat atual
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
                    
            except Exception as e:
                if callback:
                    callback(f"Erro ao processar mensagem: {e}")
                time.sleep(2)
    
    def stop_monitoring(self):
        """Para o monitoramento de mensagens"""
        self.is_monitoring = False
        print("Voltando ao menu principal...")
    
    def quit(self):
        """Encerra o bot"""
        self.stop_monitoring()
        if self.browser:
            self.browser.quit()