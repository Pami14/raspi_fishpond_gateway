Project Documentation: Fischteich (Fishpond) Surveillance Gateway

1. Project Overview
This project transforms a Raspberry Pi into an autonomous security gateway for an external IP camera. The Pi acts as a network hub that provides a DHCP address to the camera, establishes a secure VPN tunnel to a home base, and sends real-time motion alerts via Telegram.

2. Core Features
Network Master: The Pi acts as a dedicated DHCP server (isc-dhcp-server), assigning the fixed IP 192.168.14.60 to the camera.
Motion Detection: A hardware PIR sensor connected to GPIO 23 triggers the system logic.
Hardware Control: Upon motion detection, a relay or LED connected to GPIO 18 is toggled.
Smart Streaming: To save CPU resources, the motion service is only started when the PIR sensor detects activity.
Secure Remote Access: Establishes an OpenVPN connection (tun0) automatically, making the camera stream accessible via the home network IP (10.8.0.x).
Instant Messaging: Sends status updates and direct stream links via a Telegram Bot.

3. System Components & File Paths
Component	Path / Details
Main Logic	        /home/pi/surveillance_system.py (Python 3)
Startup Script	        /home/pi/Surveillance.sh (includes 60s boot delay)
Systemd Service	        /etc/systemd/system/Surveillance.service
DHCP Configuration	/etc/dhcp/dhcpd.conf
VPN Profile	        /home/pi/Fischteich.ovpn
Streaming Engine	motion software (default port 8081)

4. Hardware Pinout (BCM)
GPIO 23 (Input): PIR Motion Sensor (configured with Pull-Up).
GPIO 18 (Output): Control output (Relay/LED), active LOW.

5. Script Logic & Resilience
Self-Healing: The Python script continuously pings the camera. If unreachable, it proactively restarts the dhcpd service to re-establish the connection.
VPN Awareness: Before alerting, the script verifies if the tun0 interface is active and pings the VPN gateway to ensure the notification can be sent.
Efficiency: The motion service (used for the web stream) is stopped when no motion is detected to keep the Pi's temperature and power consumption low.