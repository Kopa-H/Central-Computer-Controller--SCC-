import os
import subprocess
import tkinter as tk
from telegram import Update # type: ignore
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext # type: ignore
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Acceder al token como harías con process.env en Node.js
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("El token de Telegram no está definido en el archivo .env")

class ShutdownApp:
    def __init__(self, bot, chat_id):
        self.root = tk.Tk()
        self.root.title("Aviso de apagado del sistema")
        self.root.geometry("800x250")
        self.root.attributes("-topmost", True)  # Hace que la ventana esté en primer plano
        self.root.resizable(False, False)

        # Etiqueta de mensaje
        self.message_label = tk.Label(self.root, text="El sistema se apagará en breve.\nEscoja una opción. En caso contrario, en 5 minutos se apagará automáticamente.",
                                      font=("Helvetica", 14), justify="center")
        self.message_label.pack(pady=20)

        # Variables de control
        self.shut_down = False
        self.timer = None
        self.bot = bot
        self.chat_id = chat_id

        # Estilo de los botones
        boton_estilo = {
            "font": ("Helvetica", 16),  # Fuente más grande
            "width": 20,  # Ancho del botón
            "height": 2,  # Altura del botón
            "bd": 5,  # Borde más grueso
            "relief": "raised",  # Efecto de relieve para hacerlo más atractivo
            "fg": "white",  # Color del texto
            "bg": "#4CAF50",  # Color de fondo (verde)
            "activebackground": "#45a049",  # Color de fondo cuando se presiona
            "activeforeground": "white"  # Color del texto cuando se presiona
        }

        # Botones de acción
        self.btn_evitar = tk.Button(self.root, text="Evitar", command=self.evitar, **boton_estilo)
        self.btn_evitar.pack(side="left", padx=20)

        self.btn_apagar = tk.Button(self.root, text="Apagar", command=self.apagar, **boton_estilo)
        self.btn_apagar.pack(side="right", padx=20)

        # Iniciar el temporizador de 5 minutos
        self.start_timer()

    def start_timer(self):
        # Si no se hace nada en 5 minutos, apaga el sistema
        self.timer = self.root.after(1 * 60 * 1000, self.apagar)

    def evitar(self):
        # Cancelar el temporizador si está activo
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None  # Limpia la variable del temporizador

        # Cerrar la ventana de tkinter y terminar el bucle
        self.root.quit()
        self.root.destroy()  # Asegura que la ventana se destruya completamente

        # Enviar mensaje al bot
        message = "Apagado cancelado por el usuario."
        self.bot.send_message(self.chat_id, message)  # Informar al bot

    def apagar(self):
        # Si se presiona "Apagar", apaga el sistema
        message = "El sistema se está apagando..."
        self.bot.send_message(self.chat_id, message)  # Informar al bot
        subprocess.run(["shutdown", "/s", "/f", "/t", "0"])
        self.root.quit()
        self.root.destroy()

    def run(self):
        # Ejecutar la ventana tkinter
        self.root.mainloop()

class TelegramBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()

        # Guardamos el bot y chat_id como atributos
        self.bot = self.application.bot

        # Añadir manejadores de comandos
        self.application.add_handler(CommandHandler("shutdown", self.shutdown))

        # Añadir manejador para /info
        self.application.add_handler(CommandHandler("info", self.info))

        # Añadir un manejador para los mensajes no reconocidos
        self.application.add_handler(MessageHandler(filters.Regex('^.*'), self.unknown_command))
    async def start(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("¡Hola! Soy un bot destinado a hacer uso del Computador Principal de Kopa a modo de servidor. Usa /info para ver los comandos disponibles.")

    async def unknown_command(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("Comando no reconocido. Usa /info para ver los comandos disponibles.")

    async def info(self, update: Update, context: CallbackContext) -> None:
        comandos = (
            "/shutdown - Apaga el sistema en 5 minutos"
        )
        await update.message.reply_text(comandos)

    async def shutdown(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("El sistema se apagará en 5 minutos. Preparando...")

        # Ahora podemos usar directamente self.bot y el chat_id del mensaje
        app = ShutdownApp(self.bot, update.message.chat_id)
        app.run()

    def run(self):
        # Iniciar el bot
        self.application.run_polling()

if __name__ == '__main__':
    # Crear y ejecutar el bot
    telegram_bot = TelegramBot(TOKEN)
    telegram_bot.run()
