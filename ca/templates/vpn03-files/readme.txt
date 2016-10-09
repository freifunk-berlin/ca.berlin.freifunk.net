Dieses TGZ enthält eine VPN-Konfiguration für Freifunker.
---------------------------------------------------------

Ausprobieren: sudo openvpn VPN03-udp.opvn
dann einfach http://google.com/search?q=my+ip nutzen

VPN03-udp.ovpn
  Standard-Konfiguration über UDP, unverschlüsselt, optimiert für Tempo

VPN03-tcp.ovpn
  Ausweich-Konfiguration über TCP, verschlüsselt, für Proxy + Regimes
  Hinweis: TCP-über-TCP führt häufig zu hängenden Downloads

VPN03_*.key, VPN03_*.crt
  Schlüsseldateien, bitte nicht veröffentlichen

freifunk-ca.crt
  Bestätigt beim Verbindungsaufbau ausgetauschte Schlüssel

%SERVER%_%NAME%-android.p12
  Schlüsseldateien zum Import für Win, Android: experimentelles IPSec/L2TP
  Kennwort ist "freifunc". IPSec ist kompliziert und Buggy -> nicht benutzen

Die Regeln sind einfach:

* Ungewöhnlich viele Verbindungen zu verschiedenen Rechnern -> Zwangsproxy(4h)
* Kein NAT auf den Routern, sonst Zwangsproxy für alle wegen einem DHCP-Benutzer
* NAT passiert grundsätzlich auf dem VPN-Gateway. Outgoing IP aus einem Pool
* Rückroute über Tunnel gibts automatisch wenn eine Incoming-IP entdeckt wird
* Generell: IPs (auch DHCP-IPs) nur aus 104.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12
* Doppelte IPs vermeiden (sonst togglen die Rückrouten). Berlin -> IPVergabe(104)
* Tunnel sind nicht (nur) für Road-Warrior, sondern für Router mit Netzen dahinter
* Schlüssel nur einmal gleichzeitig verwendbar. Neues Gerät, neuer Schlüssel
* Tipp: VPN-Server hostet Opkg's (OpenVPN+SSL) für OpenWRT-Router mit wenig Platz

Bei Fragen schaut ins Wiki oder meldet Euch auf der Berliner Mailing-Liste:
http://wiki.freifunk.net/Vpn03
http://lists.berlin.freifunk.net/cgi-bin/mailman/listinfo/berlin

Bitte denkt auch an die Betriebskosten: http://freifunkstattangst.de/
