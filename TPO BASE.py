#FUNCIONES PARA RESTRICCIONES#

def validar_opciones(seleccion):
    """
    Función creada para validar la selección de opciones en el menú
    """
    while not (seleccion.isdigit() and 0 <= int(seleccion) <= 5):
        print("Ingreso inválido, debe ser un número entre 0 y 5.")
        seleccion = input("Escoja una opcion: ")
    return int(seleccion)

def validar_nombre(nombre):
    """
    Función para validar que se ingresen caracteres de cadena y no números
    """
    while True:
        valido = True
        if nombre.strip() != '': #si no se ingresa nombre dara false, restriccion para que se ingrese de manera obligatoria un nombre#
            valido = False
        for c in nombre:
            if not (c.isalpha() or c == ' '): #en caso de que ambos sean falsos es invalido ya que no es una letra ni un espacio# queda false or false = false
                valido = False
                break
        if valido:
            break
        else:
            nombre = input("Ingreso inválido, recuerde que no se permite ingresar números ni símbolos. Ingrese el nombre del cliente: ")
    return nombre

def validar_direccion(direc):
    """
    Función para validar que se haya ingresado una dirección y no un espacio vacío
    """
    while direc.strip() != '': #si no se ingresa nombre dara false, restriccion para que se ingrese de manera obligatoria un nombre#
        direc = input("No se ha ingresado ninguna direccion, Reintente: ").capitalize()
    return direc

#FUNCIONES PRINCIPALES#

def codigo_envio(numero):
    """
    Genera un código de envío único incrementando el contador para proximos pedidos.
    """
    numero += 1
    codigo1 = f"ENV{numero:03d}"
    
    return codigo1, numero

def agregar_envio(contador, matriz1): #Contador sirve para q se hagan las iteraciones, las toma cuando llama a codigo_envio
    """
    Agrega un nuevo envío al sistema solicitando datos del cliente.
    Valida el nombre del cliente (solo letras y espacios) y la dirección.
    Crea un nuevo registro con estado "Pendiente" y lo añade a la matriz1.
    """
    columnas = 4
    codigo2, contador = codigo_envio(contador)

    cliente = input("Ingrese el nombre del cliente: ")    

    cliente = validar_nombre(cliente)

    direccion= input("Ingrese la direccion del cliente: ").capitalize()

    direccion = validar_direccion(direccion)

    estado  = "Pendiente"

    # Se crea una fila con los datos de un pedido
    fila1 = [""] * columnas
    fila1[0] = codigo2
    fila1[1] = cliente.title()
    fila1[2] = direccion.title()
    fila1[3] = estado

    # Se agrega el pedido al total de pedidos
    matriz1.append(fila1)

    # total_clientes = filas actuales
    total_clientes = len(matriz1)
    
    #Se imprime el envio agregado de forma estetica
    print("-" * 60)
    print(" 📦 Envío agregado:", " | ".join(fila1))
    #Se informa el total de los clientes
    print("\n 👥 Total clientes (filas):", total_clientes)
    
    return contador # devolvemos contador actualizado 

def consultar_envio(matriz2):
    """
    Busca y muestra la información de un envío específico por su código de tracking.
    Solicita al usuario el código de tracking, busca en la matriz2 y muestra
    los datos del envío si existe, o un mensaje de error si no se encuentra.     
    """
    #Pide el numero del pedido que se desea consultar
    consulta = (input('Ingrese el codigo de tracking que desee consultar: ')).upper()
    print()
    #Utiliza el primer valor de la fila, que es el codigo del envío, para verificar si esta o no en la lista total de clientes
    
    encontrado = False
    for fila2 in matriz2:
        if fila2[0] == consulta:
            print(" ✅ Pedido encontrado:")
            print()
            print(" | ".join(fila2))
            encontrado = True
            break
    
    if not encontrado:
        print("Codigo de envio incorrecto u inexistente ❌ ")

def historial_envios(matriz3):
    """
    Muestra todos los envíos registrados en el sistema.
    Si no hay envíos registrados muestra un mensaje informativo.
    Si hay envíos, los lista todos mostrando código, cliente, dirección y estado.    
    """
    if not matriz3:
        print("No Hay pedidos aun")
    else:
        print("Lista de pedidos totales 📦 : ")
        print("-"*60)
        for f in range(len(matriz3)):
            for c in range(len(matriz3[0])):
                print(matriz3[f][c], end=' | ') #imprime todos los pedidos del sistema de forma estetica
            print()

def cambiar_estado(matriz4):
    """
    Permite modificar el estado de un envío existente.
    Valida que no se pueda cancelar un pedido ya entregado.
    """
    codigo3 = input("Ingrese el código de envío a modificar: ").upper()
    
    encontrado = False
    #Recorre cada fila de la matriz4
    for fila3 in matriz4:
        if fila3[0] == codigo3: #si el codigo ingresado esta dentro de la lista de codigos de la matriz4, entonces se encontró el numero de pedido
            encontrado = True
            print("Estado actual:", fila3[3])
            print("\nOpciones de nuevo estado:")
            print("1 - Pendiente")
            print("2 - Despachado")
            print("3 - En camino")
            print("4 - Entregado")
            print("5 - Cancelar pedido")
            print("0 - Cancelar operación")
            print()
            
            opcion = input("Seleccione una opción: ") #Pide al usuario que ingrese una de las opciones anteriores
            opcion = validar_opciones(opcion) #Valida que la entrada este entre 0 y 5
            
            #Se le asigna el nuevo estado al pedido solicitado, si es 0 se sale de la operacion y el pedido queda con el estado original
            if opcion == 0:
                print("Operación cancelada.")
            elif "Devuelto" in fila3[3]:  
                print('No se puede cambiar el estado de un pedido que ya ha sido devuelto')

            elif opcion == 1:
                fila3[3] = "Pendiente"
            elif opcion == 2:
                fila3[3] = "Despachado"
            elif opcion == 3:
                fila3[3] = "En camino"
            elif opcion == 4:
                fila3[3] = "Entregado"
            elif opcion == 5:
                if fila3[3] == "Entregado":
                    print('No se puede marcar como cancelado el pedido ya que ha sido entregado')
                else:
                    fila3[3] = "Cancelado"
            if opcion != 0 and "Devuelto" not in fila3[3]:  # Solo mostrar si no se canceló o no fue devuelto
                print(f"Pedido marcado como {fila3[3]}.")
                print(f" ✅ Pedido actualizado: {' | '.join(fila3)}")
            break
    
    if not encontrado:
        print("No se encontró un pedido con ese código. ❌ ")

def devoluciones(matriz5): 
    """
    Procesa la devolución de un pedido ya entregado.
    Busca el pedido por código, verifica que esté en estado "Entregado",
    solicita el motivo de la devolución y actualiza el estado.
    Solo permite devoluciones de pedidos entregados.    
    """
    codigo_devolucion = input("Ingrese el codigo del pedido a devolver: ").upper()
    
    encontrado = False
    for fila4 in matriz5: #Recorre la matriz de pedidos
        if fila4[0] == codigo_devolucion: # Si el codigo esta en la lista de pedidos significa que existe dicho pedido
            encontrado = True
            if "Devuelto" in fila4[3]: #para evitar que se devuelva nuevamente un producto ya devuelto#
                print('Este pedido ya ha sido devuelto anteriormente')
            elif fila4[3] == "Entregado":
                motivo = input("Ingrese el motivo de porque le han devuelto el pedido: ").capitalize()
                fila4[3] = f"Devuelto, causa: {motivo}"
                print(f"Devolucion registrada: {' | '.join(fila4)}")
            else:
                print('El envio todavia no ha sido entregado por lo que no se puede realizar la devolucion')
            break
    
    if not encontrado:
        print("Pedido no encontrado ❌ ")

#PROGRAMA PRINCIPAL#

sistema = []
n = 0

while True:
    print("\n📦 --- Sistema de Envíos ---")
    print("\n1️⃣  Crear envío")
    print("2️⃣  Consultar envío")
    print("3️⃣  Listar todos los envíos")
    print("4️⃣  Cambiar estado de un envío")
    print("5️⃣  Realizar devolución del cliente")
    print("0️⃣  Salir")
    
    opcion = input('\nEscoja una opcion: ')
    print()
    
    opcion = validar_opciones(opcion)
        
    match opcion:
        case 0:
            print('Nos vemos! 👋 ')
            break
        case 1:
            n = agregar_envio(n, sistema)
        case 2:
            consultar_envio(sistema)
        case 3:
            historial_envios(sistema)
        case 4:
            cambiar_estado(sistema)  
        case 5:
            devoluciones(sistema)
