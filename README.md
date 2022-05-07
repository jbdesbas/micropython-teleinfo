# microPython Teleinfo
Read teleinfo from France EDF 🇫🇷 electricty provider. 🔌

A lib used to read _teleinformation_ from electirc meter. Basically, the I1 and I2 port provide a serial signal with some usefull informations.
Tested only with ESP8266, but should work with other boards using [MicroPython](http://micropython.org).

⚠️ Since ESP8266 has only 1 UART (https://docs.micropython.org/en/latest/esp8266/quickref.html#uart-serial-bus), we need to detach Python REPL in order to record provider's data.
On the exemple below, the UART is detached from REPL, configured for telemetry, then reconfired with defaults parameters.
You can leave UART detached from REPL, but be aware that you will no longer be able to use it for debug or put files, and maybe need to reflash the board. (But you can style use webREPL if configured).

You can below find an exemple with UART immediatly reconfigured and re-attached to REPL after data record. 

Exemple on ESP8266:

```python
from utime import sleep
from machine import UART
from teleinfo import Teleinfo

ti_uart = UART(0) # Some board have many UART, use UART0 for ESP8266
telei = Teleinfo(ti_uart)

 try : 
      print('Detach REPL, see you soon')
      sleep(3)
      dupterm(None, 1) #  Detach REPL from UART
      t = telei.get_next_trame() #  Configure REPL for telemetry and record data
  finally : #  make sure that REPL is re-attached if something would go wrong
      ti_uart.init(baudrate=115200, parity=None, bits=8, stop=1) #reinit uart with default value
      dupterm(ti_uart, 1) #  Re-attach REPL
      print('REPL reattached')

print(t.infos_dict['BASE']) # Print index

```
if you don't care about REPL :


```python
from utime import sleep
from machine import UART
from teleinfo import Teleinfo

ti_uart = UART(0) # Some board have many UART, use UART 0 for ESP8266
telei = Teleinfo(ti_uart)

while True:
  trame = telei.get_next_trame()

  for k, v in t.infos_dict.items():
     # to some stuff, like MQTT post
   
  sleep(30)
```


Not tested with ESP32, should be work with UART1 or UART2 

See https://www.magdiblog.fr/gpio/teleinfo-edf-suivi-conso-de-votre-compteur-electrique/ for all labels definition


## Hardware
![image](https://user-images.githubusercontent.com/6163107/167256147-e408ef1a-be4b-4785-8748-59fffaf949ca.png)

Schema from : http://hallard.me/pitinfov12/

ℹ️ With _linky_ meter, I had to **change the value of R1 resistor** 4,7kΩ --> 1kΩ to make it work.

## TODO 
🚧 Add checksum control
