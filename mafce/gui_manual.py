#GUI Manual

##############################

inicio='''¡Bienvenido a MAFCE (Mecanismo para la Aplicación de Fuerzas Controladas Electrónicamente)!
Puede acceder a las distintas pestañas del programa pulsando en el menú de la izquierda.
Y si tiene alguna duda sobre el funcionamiento, aquí puede leer el manual de cada pestaña.'''


sim_peso='''Simular Peso es la pestaña principal de MAFCE.
Aquí se selecciona el peso que se quiere simular y cuando se pulsa el botón INICIAR, el motor se pone en marcha. Hay tres maneras de simular el peso: arrastrando el control deslizante, introduciéndolo en el teclado numérico y pulsando ENTER o sumando o restando los valores predeterminados. La resolución del controlador deslizante se puede cambiar en la pestaña Ajustes.
Una vez comienza la simulación el botón INICIAR se convierte en el botón PARAR. En la pantalla se muestra el peso simulado en cada momento y el error con respecto al peso que se quiere simular. Cuando el error actual es mayor que el error admisible, el recuadro es de color amarillo y cuando es menor, el recuadro es verde. El valor del error admisible se puede modificar en la pestaña Ajustes.'''


motor='''La pestaña Motor permite controlar directamente el movimiento del motor.
Hay un control deslizante para ajustar la velocidad de giro. En la pestaña Ajustes se puede determinar el valor máximo y mínimo de la velocidad, así como el número de divisiones del deslizante.
El motor se puede girar en los dos sentidos y en dos modos: el primero es girar mientras el botón se mantiene pulsado y el segundo, pulsar el botón y que el motor gire automáticamente hasta que se vuelva a pulsar el botón y entonces para.
En la parte de abajo de la pantalla se muestra la velocidad en revoluciones por minuto y en revoluciones por segundo. Este valor es una aproximación bastante precisa, pero no exacta.
En la parte superior se muestra el peso mientras el motor está girando. Cuando se para, el valor del peso es el último medido cuando el motor estaba en marcha.'''


bascula='''En la pestaña Báscula se muestra el peso simulado en todo momento. Este peso es igual al peso colgado de la célula de carga más el peso de la propia célula de carga. El valor del peso de la célula de carga se puede modificar desde la pestaña Ajustes o pulsando el botón 'Cambiar peso de la célula de carga'.
Esta pestaña también permite calibrar la célula de carga. Para ello, se pulsa el botón 'Calibrar célula de carga' y se siguen las instrucciones que aparecen en el recuadro negro, que incluyen colgar un peso conocido e introducir el valor de dicho peso mediante el teclado numérico.
También permite obtener una aproximación de la rigidez del sistema. La estimación de k se mostrará en la pantalla, pero el valor deberá ser guardado por el usuario en la pestaña Ajustes.''' 


ajustes='''La pestaña Ajustes ofrece la posibilidad de cambiar los valores de algunos parámetros con los que funciona la máquina. Para ello se selecciona una propiedad de la lista y se introduce el valor deseado en el teclado numérico y al pulsar ENTER se convertirá en el valor actual de dicha propiedad.
El botón 'Aplicar cambios solo a esta sesión' lleva al usuario a la pestaña Simular Peso para utilizar el programa con los cambios realizados. El botón 'Guardar esta configuración' hace que todos los valores guardados pasen a ser iguales que los valores actuales. Los valores guardados son los que el programa asigna a cada propiedad cada vez que se inicia. El botón 'Deshacer cambios' hace que los valores actuales pasen a ser iguales que los valores guardados. Y el botón 'Restaurar valores por defecto' hace que los valores actuales pasen a ser iguales que los valores por defecto.'''
