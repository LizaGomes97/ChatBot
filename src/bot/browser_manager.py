# src/bot/browser_manager.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BrowserManager:
    def __init__(self):
        self.driver = None

    def initialize_browser(self):
        """Inicializa o navegador Chrome"""
        try:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=options)
            return True
        except Exception as e:
            print(f"Erro ao inicializar navegador: {e}")
            return False

    def open_whatsapp(self):
        """Abre o WhatsApp Web"""
        if self.driver:
            self.driver.get("https://web.whatsapp.com")
            return True
        return False

    def is_logged_in(self):
        """Verifica se está logado no WhatsApp Web"""
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#pane-side'))
            )
            return True
        except Exception:
            return False

    def find_unread_chats(self):
        """Procura chats não lidos"""
        try:
            unread_chats = self.driver.find_elements(By.CSS_SELECTOR, 'span[data-icon="unread-count"]')
            
            if unread_chats:
                chats = []
                for chat in unread_chats:
                    try:
                        chat_element = chat.find_element(By.XPATH, "./../../..")
                        chat_title = chat_element.get_attribute('title')
                        chats.append({
                            'element': chat_element,
                            'title': chat_title
                        })
                    except Exception:
                        continue
                return chats
            return []
            
        except Exception as e:
            print(f"Erro ao procurar chats não lidos: {e}")
            return []

    def open_chat(self, chat_element):
        """Abre um chat específico"""
        try:
            chat_element.click()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Erro ao abrir chat: {e}")
            return False

    def wait_for_element(self, by, value, timeout=10):
        """Espera um elemento aparecer na página"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception:
            return None

    def quit(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()