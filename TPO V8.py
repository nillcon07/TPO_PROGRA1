#FUNCIONES PARA RESTRICCIONES#

import datetime

def validar_opciones(seleccion,rango1,rango2):
    """
    Función creada para validar la selección de opciones en el menú
    """

    while True:

        try:
            seleccion = int(seleccion) #ya que el input es un string se intenta pasar a int para verificar si es correcto el ingreso#
            assert rango1<=seleccion<=rango2 #debe estar detro del rango#
            break

        except (ValueError, AssertionError):
            print(f"Ingreso inválido, debe ser un número entre {rango1} y {rango2}.")
            seleccion = input("Escoja una opcion: ")
        
    return seleccion

def validar_nombre(nombre):
    """
    Función para validar que se ingresen caracteres de cadena y no números
    """
    while True:
        valido = True
        if nombre.strip() == "": #si no se ingresa nombre dara false, restriccion para que se ingrese de manera obligatoria un nombre#
            valido = False
        else:
            for c in nombre:
                if (not c.isalpha()) and (c != " "): #en caso de que ambos sean falsos es invalido ya que no es una letra ni un espacio# queda false or false = false
                    valido = False
                    break
        if valido:
            break
        else:
            nombre = input("Ingreso inválido, recuerde que no se permite ingresar números ni símbolos. Ingrese el nombre del cliente: ")
    return nombre.title()

def validar_direccion(direc):
    """
    Función para validar que se haya ingresado una dirección y no un espacio vacío
    """

    while True:
        valido = True
    
        if direc.strip() == "": #si no se ingresa nombre dara false, restriccion para que se ingrese de manera obligatoria un nombre#
            valido = False

        else:
            for c in direc:
                if (not c.isalnum()) and (c != " "): 
                    valido = False
                    break
                
        if valido:
            break

        else:
            direc = input("Direccion invalida, reintente: ")


    return direc.title()

def formato_fechas():
    fecha_final = []
    fecha_original = datetime.datetime.now()
    fecha_final.append(fecha_original.day)
    fecha_final.append(fecha_original.month)
    fecha_final.append(fecha_original.year)
    fecha_final.append(fecha_original.hour)
    fecha_final.append(fecha_original.minute)
    fecha = "/".join(map(str, fecha_final[ :3]))
    hora = ":".join(map(str, fecha_final[3: ]))
    fecha_con_formato = (fecha, hora)
    return fecha, hora, fecha_final

#FUNCIONES PRINCIPALES#

def codigo_envio(numero):
    """
    Genera un código de envío único incrementando el contador para proximos pedidos.
    """
    numero += 1
    codigo1 = f"ENV{numero:03d}"
    
    return codigo1, numero

def agregar_envio(contador1, matriz1): #Contador sirve para q se hagan las iteraciones, las toma cuando llama a codigo_envio
    """
    Agrega un nuevo envío al sistema solicitando datos del cliente.
    Valida el nombre del cliente (solo letras y espacios) y la dirección.
    Crea un nuevo registro con estado "Pendiente" y lo añade a la matriz1.
    """
    
    codigo2, contador1 = codigo_envio(contador1)

    cliente = input("Ingrese el nombre del cliente: ").title()

    cliente = validar_nombre(cliente)

    direccion= input("Ingrese la direccion del cliente: ").title()

    direccion = validar_direccion(direccion)

    estado  = "Pendiente"

    fecha1, horario, fecha_sin_formato = formato_fechas()

    matriz1[0].append(codigo2)
    matriz1[1].append(cliente)
    matriz1[2].append(direccion)
    matriz1[3].append(estado)
    matriz1[4].append(fecha_sin_formato)
    

    # total_clientes = filas actuales
    total_clientes = len(matriz1[1])
    
    print()
    for fila in matriz1[ :-1]:
        print(fila[contador1 - 1], end=" | ")
    print(f"{fecha1} Horario: {horario}")
    print()
    print("✅ Envio agregado con exito")
    print("-" * 100)
    #Se informa el total de los clientes
    print("\n 👥 Total clientes (filas):", total_clientes)
    
    return contador1 # devolvemos contador actualizado 

def consultar_envio(matriz2):
    """
    Busca y muestra la información de un envío específico por su código de tracking.
    Solicita al usuario el código de tracking, busca en la matriz2 y muestra
    los datos del envío si existe, o un mensaje de error si no se encuentra.     
    """
    
    tipo_de_consulta = ("por codigo", "por cliente", "por fecha")
    
    tipo_elegido = int(input(f"1 - por codigo\n2 - por cliente\n3 - por fecha\nIngrese un numero para el tipo de consulta: "))
    validar_opciones(tipo_elegido,1,3)
    if tipo_elegido == 1:
        #Pide el numero del pedido que se desea consultar
        consulta = (input("Ingrese el codigo de tracking que desee consultar: ")).upper()
        print()
        #Utiliza el primer valor de la fila, que es el codigo del envío, para verificar si esta o no en la lista total de clientes
        encontrado = False
        if matriz2[0] == []:
            print("No hay pedidos cargados aun, pulse 1 para añadir un pedido nuevo")
        else:
            for fila2 in range(len(matriz2[0])):
                if matriz2[0][fila2] == consulta:
                    encontrado = True
                    indice = fila2
                    break
            if encontrado:
                print("✅ Pedido encontrado:")
                print()
                for fila in matriz2:
                    print(fila[indice], end=" | ")
                print()
            else:
                print("❌ Código de envío incorrecto o inexistente")
    elif tipo_elegido == 2:
        consulta = input("Ingrese el nombre del cliente: ").capitalize()
        print()
        cantidad_del_cliente = []
        encontrado = False
        if matriz2[1] == []:
            print("No hay pedidos cargados aun, pulse 1 para añadir un pedido nuevo")
        else:
            for fila2 in range(len(matriz2[1])):
                if matriz2[1][fila2] == consulta:
                    encontrado = True
                    indice = fila2
                    print("✅ Pedido encontrado:")
                    print()
                    for fila in matriz2:
                        print(fila[indice], end=" | ")
                    print()
                    print()
                    
            if encontrado == False:
                print("❌ nombre del cliente incorrecto o inexistente")
    else: #Resolver esto
        pass
        consulta = input("Ingrese la fecha que quiere consultar: ")
        
        
        print()
        
        encontrado = False
        if matriz2[4] == []:
            print("No hay pedidos cargados aun, pulse 1 para añadir un pedido nuevo")
        else:
            for fila2 in range(len(matriz2[4])):
                fecha_str = matriz2[4][fila2]
                fecha3 = datetime.strptime(fecha_str, "%d/%m/%y %h:%M")
                valores = [fecha3.year , fecha3.month , fecha3.day , fecha3.hour , fecha3.minute]
                
                if valores[ :len(consulta_dividida)] == consulta_dividida:
                    encontrado = True
                    
                    print("✅ Pedido encontrado:")
                    print()
                    print(f"{matriz2[0][fila2]} | {matriz2[1][fila2]} | {matriz2[2][fila2]} | {matriz2[3][fila2]} | {matriz2[4]}")
                    print()
                    
            if encontrado == False:
                print("❌ nombre del cliente incorrecto o inexistente")

def historial_envios(matriz3,opcion):
    """
    Muestra todos los envíos registrados en el sistema.
    Si no hay envíos registrados muestra un mensaje informativo.
    Si hay envíos, los lista todos mostrando código, cliente, dirección y estado.    
    """
    dia, hora, fecha = formato_fechas()
    if matriz3[0] == []:
                print("No Hay pedidos aun")
    else:
        match int(opcion):
            case 1: #LISTAR TODo#
                print("Lista de envíos 📦:")
                print("-" * 100)
                total = len(matriz3[0])  # cantidad de envíos registrados
                
                
                
                for i in range(total):
                    print(f"{matriz3[0][i]:^10} | {matriz3[1][i]:^15} | {matriz3[2][i]:^20} | {matriz3[3][i]:^10} | {dia} Horario: {hora}")

                print("-" * 100)
                print(f"Total de Pedidos: {total}")


            case 2: ###FALTA###
                print("Lista de pedidos segun fecha 📦 : ")
                print("-"*100)
                print("-" * 100)
                print(f"Total de Pedidos: {total}")
                pass
            
            case 3:#LISTAR POR ESTADO# 
                estados = ("Pendiente","Despachado","En camino","Entregado","Cancelado","Devuelto")

                seleccion = input("1 - Pendiente\n2 - Despachado\n3 - En camino \n4 - Entregado\n5 - Cancelado \n6 - Devuelto\n\nIngrese el nombre estado el cual desea ver el listado: ")

                seleccion = validar_opciones(seleccion,1,6)

                seleccion = estados[seleccion-1]

                print(f"Lista de pedidos con el estado {seleccion} 📦 : ")
                print("-"*100)
                
                #caso unico para devuelto ya que tiene un motivo y no es solo el estado#
                if seleccion == "Devuelto":
                    total_estado=[]
                    for i in range (len(matriz3[3])): # se usa for in range para obtener el indice#
                        if "Devuelto" in matriz3[3][i]: 
                            total_estado.append(i) #se guarda el indice en la lista#
                else:
                    total_estado = [i for i in range(len(matriz3[3])) if matriz3[3][i] == seleccion] 
                    # guardo en una lista de compresion cada indice del pedido que tenga el estado seleccionado# #se usa in range para tener los indices#

                if len(total_estado) == 0:
                    print("No se encuentran pedidos con el estado seleccionado")

                else:
                    for i in total_estado:
                            print(f"{matriz3[0][i]} | {matriz3[1][i]} | {matriz3[2][i]} | {matriz3[3][i]} | {dia} Horario: {hora}")
                    print("-" * 100)
                    print(f"Total de Pedidos en ese estado: {len(total_estado)}")
                    
def cambiar_estado(matriz4):
    """
    Permite modificar el estado de un envío existente.
    Valida que no se pueda cancelar un pedido ya entregado.
    """
    codigo3 = input("Ingrese el código de envío a modificar: ").upper()
    
    encontrado = False
    # Recorremos las columnas (cada envío)
    for i in range(len(matriz4[0])):
        if matriz4[0][i] == codigo3:
            encontrado = True
            print("Estado actual:", matriz4[3][i])
            
            while True:
                print("\nOpciones de nuevo estado:")
                print("1 - Pendiente")
                print("2 - Despachado")
                print("3 - En camino")
                print("4 - Entregado")
                print("5 - Cancelar pedido")
                print("0 - Volver al menu")
                print()
                
                
                opcion = input("Seleccione una opción: ") #Pide al usuario que ingrese una de las opciones anteriores
                opcion = validar_opciones(opcion,0,5) #Valida que la entrada este entre 0 y 5
                if opcion == 0:
                    print("Volviendo al menu principal...")
                    break
                estados_a_modificar = ("Pendiente","Despachado","En camino","Entregado","Cancelar pedido")
                estados_a_modificar = estados_a_modificar[opcion - 1]

                seguridad = input(f"Usted seleccionó la opción {estados_a_modificar} y el codigo {codigo3}. ¿Desea confirmar esta opción? [Si/No]: ").lower()

                if seguridad == "si":
                    #Se le asigna el nuevo estado al pedido solicitado, si es 0 se sale de la operacion y el pedido queda con el estado original14
                    
                    if opcion == 0:
                        print("Operación cancelada.")

                    elif "Devuelto" in matriz4[3][i]:  
                        print("No se puede cambiar el estado de un pedido que ya ha sido devuelto")

                    elif opcion == 1:
                        matriz4[3][i] = "Pendiente"
                    elif opcion == 2:
                        matriz4[3][i] = "Despachado"
                    elif opcion == 3:
                        matriz4[3][i] = "En camino"
                    elif opcion == 4:
                        matriz4[3][i] = "Entregado"
                    elif opcion == 5:
                        if matriz4[3][i] == "Entregado":
                            print("No se puede marcar como cancelado el pedido ya que ha sido entregado")
                        else:
                            matriz4[3][i] = "Cancelado"
                    if opcion != 0 and "Devuelto" not in matriz4[3][i]:  # Solo mostrar si no se canceló o no fue devuelto
                        dia2, hora2 = formato_fechas()
                        print(f"Pedido marcado como {matriz4[3][i]}.")
                        print(f" ✅ Pedido actualizado: {matriz4[0][i]} | {matriz4[1][i]} | {matriz4[2][i]} | {matriz4[3][i]} | {dia2} Horario: {hora2}")
                    break
                elif seguridad == "no":
                    print("Acción cancelada por decisión del usuario, volviendo al menú interno...")
                    continue
                else:
                    while seguridad != "no" and seguridad != "si":
                        print("Opción incorrecta, seleccione Si o No")
                        seguridad = input(f"Usted seleccionó la opción {estados_a_modificar}. ¿Desea confirmar esta opción? [Si/No]: ").lower()
            break
    if not encontrado:
        print("No se encontró un pedido con ese código. ❌")


def devoluciones(matriz5): 
    """
    Procesa la devolución de un pedido ya entregado.
    Busca el pedido por código, verifica que esté en estado "Entregado",
    solicita el motivo de la devolución y actualiza el estado.
    Solo permite devoluciones de pedidos entregados.    
    """
    codigo_devolucion = input("Ingrese el codigo del pedido a devolver: ").upper()
    
    encontrado = False
    for c in range(len(matriz5) - 1):
        if matriz5[0][c] == codigo_devolucion:
            encontrado = True
            if "Devuelto" in matriz5[3][c]: #para evitar que se devuelva nuevamente un producto ya devuelto#
                print("Este pedido ya ha sido devuelto anteriormente")
            elif matriz5[3][c] == "Entregado":
                motivo = input("Ingrese el motivo de porque le han devuelto el pedido: ").capitalize()
                matriz5[3][c] = f"Devuelto, causa: {motivo}"
                print(f"Devolucion registrada: {matriz5[3][c]}")
                
            else:
                print("El envio todavia no ha sido entregado por lo que no se puede realizar la devolucion")
        break

    if not encontrado:
        print("Pedido no encontrado ❌ ")

#PROGRAMA PRINCIPAL#

sistema = [[], [], [], [],[]]
n = 0

while True:
    print("\n📦 --- Sistema de Envíos ---")
    print("\n1️⃣  Crear envío")
    print("2️⃣  Consultar envío")
    print("3️⃣  Listar los envíos")
    print("4️⃣  Cambiar estado de un envío")
    print("5️⃣  Realizar devolución del cliente")
    print("0️⃣  Salir")
    
    opcion = input("\nEscoja una opcion: ")
    print()
    
    opcion = validar_opciones(opcion,0,5)
        
    match opcion:
        case 0:
            print("Nos vemos! 👋 ")
            break
        case 1:
            n = agregar_envio(n, sistema)
        case 2:
            consultar_envio(sistema)
        case 3:
            print("1. Listar todos\n2. Listar por fecha\n3. Listar por estado de envio")
            listar = input("\nEscoja una opcion: ")
            listar = validar_opciones(listar,1,3)
            historial_envios(sistema,listar)
        case 4:
            cambiar_estado(sistema)  
        case 5:
            devoluciones(sistema)