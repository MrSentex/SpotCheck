# SpotCheck v0.1-Beta
  
## ¿Que es SpotCheck?  
SpotCheck es un chequeador  de cuentas escrito en Python. SpotCheck consigue evadir la seguridad de Spotify para conseguir probar cuentas a una velocidad decente.  SpotCheck nació por un reto entre amigos y no debe ser usado para cometer ningún tipo de delito. Si decides cometer un delito con SpotCheck lo haces bajo tu responsabilidad.  
## ¿Como funciona?  
SpotCheck realiza requests a spotify desde la libreria `PySocks` y no usa ningun tipo de libreria externa como podria ser `urllib2` o el conocido `requests`.
`PySocks` es una libreria que usa `socket` como base. Pero `PySocks` da la posibilidad de configurar un proxy para realizar conexiones.    

Ejemplo de una web request con `PySocks` y `ssl`:  
```python
no_ssl_socket = socks.socksocket()
ssl_socket = ssl.wrap_socket(no_ssl_socket, ssl_version=ssl.PROTOCOL_SSLv23)
ssl_socket.connect(('accounts.spotify.com', 443))
ssl_socket.sendall(b'GET / HTTP/1.1\r\nHost: accounts.spotify.com\r\n\r\n')
```
