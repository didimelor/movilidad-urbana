# Movilidad Urbana
#### Integrantes del Equipo: 
Diana Karen Melo, Miguel Medina y Andrés Briseño.
___
#### Descripción del Reto: 
En este reto se pretende modelar el comportamiento de los automoviles en un mapa en la ciudad. Para esto se utiliza Mesa para el comportamiento multiagente en Python. Y los gráficos se modelan en Unity a partir de Flask.
___
#### Agentes Involucrados: 
* Obstáculos:

> Osbtáculos, Semaforos en rojo y otros coches

* Semáforos:

> Pasó el tiempo máximo en estado rojo &rarr; Se cambia a estado verde

* Coches:
Sensado | Condiciones | Acciones |
--- | --- | --- | 
Estoy en destino |  | No se mueve por que ya llegó | 
Mi destino esta en Possible_steps |  | Se mueve hacia el destino |
Hay un obstáculo |  | No me muevo hacia el obstáculo |
No hay un obstáculo | Elige la posisión más cercana por cada possible_step. La dirección de la calle tiene que ser congrunte con la dirección elegida para acercarse al destino. | Decide si le conviene moverse ahí con base en las condiciones anteriores|
___
#### Explicación en video:
> https://youtu.be/vANPKpjw-lY
