# SpotCheck v0.3-Stable
  
## ¿Que es SpotCheck?  
SpotCheck es un chequeador  de cuentas escrito en Python. SpotCheck consigue evadir la seguridad de Spotify para conseguir probar cuentas a una velocidad decente.  SpotCheck nació por un reto entre amigos y no debe ser usado para cometer ningún tipo de delito. Si decides cometer un delito con SpotCheck lo haces bajo tu responsabilidad. SpotCheck no necesita ningun tipo de proxy a menos que especifiques el uso de TOR.  
## ¿Como funciona?  
SpotCheck realiza requests a spotify desde la libreria `PySocks` y no usa ningun tipo de libreria externa como podria ser `urllib2` o el conocido `requests`.
`PySocks` es una libreria que usa `socket` como base. Pero `PySocks` da la posibilidad de configurar un proxy para realizar conexiones.    

Ejemplo de una web request con `PySocks` y `ssl`:  
```python
no_ssl_socket = socks.socksocket()
ssl_socket = ssl.wrap_socket(no_ssl_socket, ssl_version=ssl.PROTOCOL_SSLv23)
ssl_socket.connect(('accounts.spotify.com', 443)) y
ssl_socket.sendall(b'GET / HTTP/1.1\r\nHost: accounts.spotify.com\r\n\r\n')
```    
El funcionamiento interno de SpotCheck es sencillo. Se realiza un *GET* a **accounts.spotify.com** para conseguir la *csrf_token*, la cual nos ayudara a tener acceso a la API de autentificación de Spotify: **accounts.spotify.com/api/login**. La API de autentificación se puede ver en el AJAX de Spotify (Publico).  

Parte de código de Spotify (https://accounts.scdn.co/js/index.5b565fd7cb445ad46542.js):  
```javascript
var o=n({method:"POST",url:"/api/login",data:r,headers:{"Content-Type":"application/x-www-form-urlencoded"},transformRequest:u.objToFormData})
```
  Una vez conseguida la *csrf_token* se realizara un *POST* a la API **accounts.spotify.com/api/login**.
   
   Ejemplo de *POST* a la API:  
 
 ```
POST /api/login HTTP/1.0
Host: accounts.spotify.com
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4
Accept: application/json, text/plain
Content-Type: application/x-www-form-urlencoded
Content-Length: 80
Cookie: fb_continue=https%3A%2F%2Fwww.spotify.com%2Fid%2Faccount%2Foverview%2F; sp_landing=play.spotify.com%2F; sp_landingref=https%3A%2F%2Fwww.google.com%2F; user_eligible=0; spot=%7B%22t%22%3A1498061345%2C%22m%22%3A%22id%22%2C%22p%22%3Anull%7D; sp_t=ac1439ee6195be76711e73dc0f79f894; sp_new=1; csrf_token=<token>; __bon=MHwwfDE1MTEzNzE0OTl8NjM0Nzc2MDI5NTh8MXwxfDF8MQ==; remember=true@true.com; _ga=GA1.2.153026989.1498061376; _gid=GA1.2.740264023.1498061376

remember=true&username=test@test.com&password=thisisatest1234&csrf_token=<token>
 ```
 
 ## Instalación
 
 Lo primero qué se necesita es clonar o descargar el repositorio.
 
 SpotCheck al ser un script en Python es necesario la instalación del mismo. Para ello solo se necesita una busqueda en google.
 
 SpotCheck es compatible con Python 2.7 y Python 3.x.
 Despues de instalar Python es necesario la instalación de varios modulos/paquetes los cuales son `PySocks` y `colorama`. Los cuales se instalan con pip o pip3 con el siguiente comando: 
 
 ```
 pip install <paquete>
 ```
 
 Si eres demasiado vago para instalar dos paquetes se pueden instalar con un solo comando:
 ```
 pip install -r requeriments.txt
 ```
 Este comando se tiene que ejecutar desde la carpeta de SpotCheck.
 
 
 ## Utilización
 
 Ya que SpotCheck es un script automatizado su uso es muy sencillo.
 Los argumentos obligatorios son:
 
 ### combo
 ### output
 
 Estos dos argumentos determinan el fichero donde se tienen listas de emails y contraseñas en formato combo (email:password) y el archivo donde se almacenaran las cuentas que funcionen correctamente.
 
 Argumentos opcionales:
 
 ### --tor
 Si se especifica este argumento en el comando de ejecución de SpotCheck obligara al programa a realizar las peticiones a traves de TOR. (Impacto en el rendimiento)
 
 ### --nothreads
  Si se especifica este argumento en el comando de ejecución de SpotCheck obligara al programa a chequear las cuentas en el proceso principal de SpotCheck (Impacto en el rendimiento)
  
  ## Ejemplo de uso sin TOR
  ```
  python SpotCheck.py combo.txt accounts.txt
  ```
  
  ## Ejemplo de uso con TOR
  ```
  python SpotCheck.py combo.txt accounts.txt --tor
  ```
  
  ## Ejemplo de uso sin threads
   ```
  python SpotCheck.py combo.txt accounts.txt --nothreads
  ```
  
# Changelog  
### 13/09/2018 v0.1-Beta
```
 Creación del proyecto.
```  
### 14/09/2018 v0.2-Beta
```
Mejora en el sistema de adquisición de la csrf_token.
```
### 09/10/2018 v0.3-Stable
```
Mejora en el rendimiento (Calcula el numero de threads necesarios).
Añadida barra de progreso (Solo en multi-thread).
```
