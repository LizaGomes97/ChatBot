# src/bot/browser_manager.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BrowserManager:
    def __init__(self):
        self.driver = None
        
    def initialize_browser(self):
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
        if self.driver:
            self.driver.get("https://web.whatsapp.com")
            return True
        return False
    
    def wait_for_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception:
            return None
    
    def is_logged_in(self):
        return self.wait_for_element(By.CSS_SELECTOR, '#pane-side', timeout=60) is not None
    
    def quit(self):
        if self.driver:
            self.driver.quit()