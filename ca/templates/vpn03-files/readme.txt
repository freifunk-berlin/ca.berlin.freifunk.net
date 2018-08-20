Dieses TGZ enthält die Zugangsdateien für 
den Freifunk-Community-Tunnel.
---------------------------------------------------------

VPN03_*.key, VPN03_*.crt
  Schlüsseldateien, bitte nicht veröffentlichen. Schlüssel nur einmal
  gleichzeitig verwendbar. Neues Gerät, neuer Schlüssel!
  
Diese Dateien könnt Ihr mithilfe des Freifunk-Assistenten in Euer Gerät
einspielen (oder erneuern): auf der zweiten Seite des Assistenten
"Freifunk anbieten und Internet teilen" wählen und dann die *.crt und die
*.key-Dateien in den entsprechenden Feldern auswählen und hochladen.

Nach den Neustart sollte im Systemlog das Zustandekommen der Verbindung
über das ffuplink-Interface zu sehen sein, hier ein Beispiel:

Tue Jul 10 17:03:08 2018 daemon.notice openvpn(ffuplink)[2222]: [freifunk-gw01.xxxxxxxxx.de] Peer Connection Initiated with [AF_INET]XXX.XXX.83.193:1194
Tue Jul 10 17:03:09 2018 daemon.notice netifd: Interface 'ffuplink' is enabled
Tue Jul 10 17:03:09 2018 daemon.notice netifd: Network device 'ffuplink' link is up
Tue Jul 10 17:03:09 2018 daemon.notice netifd: Interface 'ffuplink' has link connectivity 
Tue Jul 10 17:03:09 2018 daemon.notice netifd: Interface 'ffuplink' is setting up now
Tue Jul 10 17:03:09 2018 daemon.notice netifd: Interface 'ffuplink' is now up
Tue Jul 10 17:03:09 2018 daemon.notice openvpn(ffuplink)[2222]: TUN/TAP device ffuplink opened
Tue Jul 10 17:03:09 2018 daemon.notice openvpn(ffuplink)[2222]: do_ifconfig, tt->did_ifconfig_ipv6_setup=0
Tue Jul 10 17:03:09 2018 daemon.notice openvpn(ffuplink)[2222]: /sbin/ifconfig ffuplink XXX.XXX.241.121 netmask 255.255.255.0 mtu 1500 broadcast XXX.XXX.241.255
Tue Jul 10 17:03:09 2018 daemon.notice openvpn(ffuplink)[2222]: /lib/freifunk/ffvpn-up.sh ffuplink 1500 1553 XXX.XXX.241.121 255.255.255.0 init
Tue Jul 10 17:03:10 2018 user.debug up-down-ffvpn: no route_net_gateway env var from openvpn!
Tue Jul 10 17:03:11 2018 daemon.warn openvpn(ffuplink)[2222]: WARNING: this configuration may cache passwords in memory -- use the auth-nocache option to prevent this
Tue Jul 10 17:03:11 2018 daemon.notice openvpn(ffuplink)[2222]: Initialization Sequence Completed
Tue Jul 10 17:31:48 2018 user.notice up-down-ffvpn: ugw: 192.168.XXX.XXX dev: ffuplink remote: 255.255.255.0 gw: XXX.XXX.241.1 src: XXX.XXX.241.121 mask: 255.255.255.0

Bei Fragen schaut ins Wiki oder meldet Euch auf der Berliner Mailing-Liste,
die Links findet Ihr in der Begleitmail zu diesem Archiv.

Viel Spaß mit Freifunk!
