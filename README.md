🖥️ Central Computer Controller (SCC)
This project allows remote control of a Windows-based main computer through a Raspberry Pi, using a Telegram bot as the interface. It enables the user to power on and shut down the computer remotely, ensuring efficient and secure control.

🔧 How it works
When the main Windows PC is off, the Raspberry Pi listens for commands via Telegram.

Upon receiving a command, the Pi communicates with an ESP-based microcontroller through HTTP, which sends a short pulse via a GPIO pin to trigger a transistor that simulates the PC’s power button.

Once the PC is powered on, the Raspberry Pi detects its availability via ping, and then disables its own bot polling.

At this point, the main PC takes over Telegram bot communication, allowing it to respond to commands — including a shutdown command that powers it off remotely.

When the PC shuts down, the Raspberry Pi automatically resumes listening for new activation commands.

This setup provides a smart and energy-efficient server control system, ideal for remote environments or shared usage.
