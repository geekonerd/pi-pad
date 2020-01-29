# pi-pad
*a simple GAMEPAD controlled by a Raspberry Pi that can control remote devices*

### Intro
**pi-pad** è un gamepad capace di controllare da remoto altri dispositivi Raspberry Pi. Per far ciò offre uno Stick, un Rotary Encoder, due bottoni ed un LED RGB di stato. Grazie all'uso delle librerie GPIOZeroLib e PiGPIO può inviare comandi da remoto ai PIN della testata GPIO di un altro Raspberry Pi, in questo caso il Pi Zero Wireless che controlla #RoPi. Per maggiori dettagli rimando alla *serie* di focus ad esso dedicati pubblicati sul mio blog (https://geekonerd.blogspot.com/p/gli-esperimenti.html).

#### Contenuto
Sono presenti i file python contenenti il codice di controllo per i vari sensori collegati al gamepad, la configurazione generale, uno script di reset dei PIN utilizzati, ed ovviamente il programma principale che fa da collante a tutte le librerie utilizzate. In più ci sono tutti i file python contenenti il codice di controllo dei vari sensori collegati a RoPi, visto che anche quel codice va eseguito sul controller.

###### Nota bene
Il codice presente in questo repository funziona su un Raspberry Pi configurato come descritto nei tutorial. Nella versione attuale, si tratta di una *demo* che funziona ma che può sicuramente essere migliorata ed integrata. Attualmente c'è qualche inghippo nella comunicazione tra le librerie GPIOZero e PiGPIO e manca un workaround che consenta di superarli.
