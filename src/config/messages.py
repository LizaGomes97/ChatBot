# src/config/messages.py

class Messages:
    WELCOME_MESSAGE = """Ola! Bem-vindo ao atendimento da Drogasil.

Por favor, escolha uma opcao:

• Digite 1 - Consultar precos
• Digite 2 - Verificar disponibilidade
• Digite 3 - Horario de funcionamento
• Digite 4 - Falar com atendente"""

    RESPONSES = {
        "1": "Para consultar precos, por favor me informe o nome do medicamento:",
        "2": "Para verificar disponibilidade, me informe o produto que procura:",
        "3": "Nossa loja esta aberta:\nSeg-Sab: 07h as 22h\nDomingo: 08h as 20h",
        "4": "Transferindo para um atendente...\n\nLizandra: Ola! Como posso ajudar voce hoje?"
    }

    @classmethod
    def get_response(cls, option):
        return cls.RESPONSES.get(option, "Opcao invalida. Por favor, escolha uma opcao valida.")