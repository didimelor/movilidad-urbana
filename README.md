# Movilidad Urbana
#### Integrantes del Equipo: 
Diana Karen Melo, Miguel Medina y Andrés Briseño.
___
#### Descripción del Reto: 
En este reto se pretende modelar el comportamiento de los automoviles en un mapa en la ciudad. Para esto se utiliza Mesa para el comportamiento multiagente en Python. Y los gráficos se modelan en Unity a partir de Flask.
___
#### Explicación en video:
> https://youtu.be/vANPKpjw-lY
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
Hay un obstáculo |  | No se muevo hacia el obstáculo |
No hay un obstáculo | Elige la posisión más cercana por cada possible_step. La dirección de la calle tiene que ser congrunte con la dirección elegida para acercarse al destino. | Decide si le conviene moverse ahí con base en las condiciones anteriores|
___
#### ¿Cómo funcionan los coches?:
___
#### ¿Cómo se puede optimizar el comportamiento de los coches?:

> El indicador de la optimización del comportamiento son los steps que tarda el coche en llegar a su destino. Tomando esto en cuenta, una mejora importante sería calcular la ruta antes de que el coche avance para evitar vueltas inecesarias y le tome más pasos llegar al destino.

> Otra optimización es la comunicación entre agentes. Se pueden utlizar mensajes con las luces de los coches. La direccional para saber que el coche va a dar vuelta, la de freno para saber que se va a parar por semáforo y las que va a avanzar. Esto ayudaría a evitar que un coche no se mueva porque el otro no le da el paso o que crea que se va a mover a una dirección que al final decidió moverse a otra.
