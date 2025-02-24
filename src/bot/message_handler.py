# src/bot/message_handler.py

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

class MessageHandler:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.last_processed_message = ""
    
    def send_message(self, contact, message):
        try:
            # Se tiver contato, precisamos procurar e abrir a conversa
            if contact:
                # Buscar contato
                search_box = self.browser.wait_for_element(
                    By.XPATH, 
                    '//div[@contenteditable="true"][@data-tab="3"]',
                    timeout=20
                )
                if not search_box:
                    return False
                    
                search_box.clear()
                time.sleep(2)
                search_box.send_keys(contact)
                time.sleep(3)
                
                # Clicar no contato
                contact_element = self.browser.wait_for_element(
                    By.XPATH,
                    f"//span[@title='{contact}']",
                    timeout=10
                )
                if not contact_element:
                    return False
                    
                contact_element.click()
                time.sleep(2)
            
            # Enviar mensagem na conversa atual
            message_box = self.browser.wait_for_element(
                By.XPATH,
                '//div[@contenteditable="true"][@data-tab="10"]',
                timeout=10
            )
            if not message_box:
                return False
            
            lines = message.split('\n')
            for i, line in enumerate(lines):
                message_box.send_keys(line)
                if i < len(lines) - 1:
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            message_box.send_keys(Keys.ENTER)
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False
    
    def get_latest_message(self):
        try:
            messages = self.browser.driver.find_elements(
                By.CSS_SELECTOR, 
                'div.message-in, div._1Gy50, div[data-pre-plain-text]'
            )
            
            if messages:
                latest_message = messages[-1].text.strip()
                if latest_message != self.last_processed_message:
                    self.last_processed_message = latest_message
                    return latest_message
            return None
            
        except Exception:
            return None