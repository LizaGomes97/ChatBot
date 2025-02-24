# src/ui/main_window.py

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLineEdit, QTextEdit, QLabel,
                           QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ..bot.whatsapp_bot import WhatsAppBot

class BotThread(QThread):
    message_received = pyqtSignal(str)
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    def run(self):
        self.bot.monitor_messages(callback=self.message_received.emit)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bot = None
        self.bot_thread = None
        self.init_ui()
        
    def init_ui(self):
        # Configurar janela principal
        self.setWindowTitle('WhatsApp Bot - Drogasil')
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Status do Bot
        self.status_label = QLabel('Bot Desconectado')
        layout.addWidget(self.status_label)
        
        # Campo de contato
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText('Nome do contato')
        layout.addWidget(self.contact_input)
        
        # Botões
        self.start_button = QPushButton('Iniciar Bot')
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)
        
        self.service_button = QPushButton('Iniciar Atendimento')
        self.service_button.clicked.connect(self.start_service)
        self.service_button.setEnabled(False)
        layout.addWidget(self.service_button)
        
        self.stop_button = QPushButton('Parar Atendimento')
        self.stop_button.clicked.connect(self.stop_service)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)
        
        # Log de mensagens
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
    def log_message(self, message):
        self.log_text.append(message)
        
    def start_bot(self):
        try:
            self.bot = WhatsAppBot()
            if self.bot.start():
                self.log_message("Aguardando login no WhatsApp Web...")
                if self.bot.wait_for_login():
                    self.status_label.setText('Bot Conectado')
                    self.start_button.setEnabled(False)
                    self.service_button.setEnabled(True)
                    self.log_message("Bot iniciado com sucesso!")
                else:
                    self.log_message("Erro ao fazer login!")
            else:
                self.log_message("Erro ao iniciar o bot!")
        except Exception as e:
            self.log_message(f"Erro: {e}")
            
    def start_service(self):
        contact = self.contact_input.text().strip()
        if not contact:
            QMessageBox.warning(self, 'Aviso', 'Digite o nome do contato!')
            return
            
        if self.bot.start_service(contact):
            self.service_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.contact_input.setEnabled(False)
            
            # Iniciar thread de monitoramento
            self.bot_thread = BotThread(self.bot)
            self.bot_thread.message_received.connect(self.log_message)
            self.bot_thread.start()
            
    def stop_service(self):
        if self.bot:
            self.bot.stop_monitoring()
            self.service_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.contact_input.setEnabled(True)
            self.log_message("Atendimento parado!")
            
    def closeEvent(self, event):
        if self.bot:
            self.bot.quit()
        event.accept()