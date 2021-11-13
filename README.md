# Movilidad Urbana
#### Integrantes del Equipo: 
Diana Karen Melo, Miguel Medina y Andrés Briseño.
___
#### Descripción del Reto: 
En este reto se pretende modelar el comportamiento de los automoviles en un mapa en la ciudad. Para esto se utiliza Mesa para el comportamiento multiagente en Python. Y los gráficos se modelan en Unity a partir de Flask.
___
#### Agentes Involucrados: 
* Automoviles: 
  > El semáforo se encuentra en rojo &rarr; Quedarse en el mismo lugar 
  
  > Hay un coche en la dirección en la que se dirije  &rarr; Quedarse en el mismo lugar 
  
  > Hay un obstáculo en la dirección en la que se dirije  &rarr; Moverse hacia la dirección de la calle y "rodearlo" siempre intentando regresar a la dirección que lo lleve al destino.
  
  > Iteraciones intentando ir a la dirección deseada se excedieron -> ir a dirección random.
* Obstáculos
* Semáforos:
> Pasó el tiempo máximo en estado rojo &rarr; Se cambia a estado verde
