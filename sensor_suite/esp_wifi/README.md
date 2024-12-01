## Flash PCB

In order to flash the program code to the pcb, attach the outputs of the Programmer like follows:<br>



| Programmer | PCB  |
|---|---|
| 3.3V | V_in |
| GND  | GND  |
| RX  | TX  |
| TX  | RX  |

At the beginning of the flashing process, push the IO0 button once. <br>
(Note that normal operation does **not** work with this connection, because Programmer does not deliver enough current!)

## Normal operation
To have the pcb work normally, just attach 3.3V and GND to an external power supply. Once connected, push the EN button once to reboot the system. 



## Serial Window
To have access to the serial window, connect the pins the following way:<br>

| Programmer | PCB  | Power Supply |
|---|---|---|
| - | V_in | 3.3V |
| GND  | GND  | GND |
| RX  | TX  |-|
| TX  | RX  |-|