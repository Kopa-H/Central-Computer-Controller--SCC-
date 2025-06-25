import TelegramBot from 'node-telegram-bot-api';
import { exec } from 'child_process';
import axios from 'axios';  // Para hacer peticiones HTTP
import dotenv from 'dotenv';

dotenv.config(); // Cargar las variables del archivo .env

// Obtener valores del .env
const token = process.env.TELEGRAM_BOT_TOKEN;
const ipPC = process.env.IP_PC;
const esp8266Ip = process.env.ESP8266_IP;

if (!token || !ipPC || !esp8266Ip) {
    console.error("Faltan variables de entorno. Verifica el archivo .env");
    process.exit(1);
}

const bot = new TelegramBot(token, { polling: true });

// Función para hacer ping a la IP de tu PC
function pingPC(ip) {
    return new Promise((resolve, reject) => {
        exec(`ping -c 1 ${ip}`, (error, stdout, stderr) => {
            if (error) {
                reject("Error en ping");
            } else {
                resolve(stdout);
            }
        });
    });
}

// Función para controlar el ESP8266 y activar el pin GPIO
async function startPC() {
    try {
        await axios.get(esp8266Ip);  // Enviar una solicitud HTTP GET al ESP8266
        return "El Computador Principal se está encendiendo correctamente. No olvide usar /shutdown al abandonar la sesión.";
    } catch (error) {
        return "Error al intentar iniciar el Computador Principal, el control del ESP8266 ha fallado. Contacte con Kopa para obtener asistencia.";
    }
}

// Verificar continuamente si el PC está encendido
async function checkPCStatus() {
    let pcEncendido = false;

    while (true) {
        try {
            await pingPC(ipPC);
            if (!pcEncendido) {
                pcEncendido = true;
                bot.stopPolling();  // Detiene temporalmente el polling
            }
        } catch (error) {
            if (pcEncendido) {
                pcEncendido = false;
                bot.startPolling();  // Vuelve a habilitar el polling
            }
        }

        // Verifica el estado cada 5 segundos
        await new Promise(resolve => setTimeout(resolve, 5000));
    }
}

// Manejar mensajes generales
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text.trim();

    if (text.startsWith('/')) {
        // Intentar hacer ping y si falla, proceder a encender el PC
        try {
            await pingPC(ipPC);
        } catch (error) {
            bot.sendMessage(chatId, "El Computador Principal se encuentra apagado. Procediendo a encender el sistema...");
            const startPcResponse = await startPC();
            bot.sendMessage(chatId, startPcResponse);
        }
    }
});

// Iniciar la verificación continua del estado del PC
checkPCStatus();