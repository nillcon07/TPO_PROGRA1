#FUNCIONES PARA RESTRICCIONES#

import datetime
import os

def validar_opciones(seleccion,rango1,rango2):
    """
    Función creada para validar la selección de opciones en el menú
    """
    while True:
        try:
            seleccion = int(seleccion) #ya que el input es un string se intenta pasar a int para verificar si es correcto el ingreso#
            assert rango1<=seleccion<=rango2 #debe estar detro del rango#
            break
        
        except ValueError:
            print(f"\nIngreso inválido, usted ingreso un valor NO entero.")
        except AssertionError:
            print(f"\nIngreso invalido, usted ingreso un valor fuera de los rangos establecidos, ")
            
        print(f'\nRecuerde que debe ser un entero entre {rango1} y {rango2}\n')
        seleccion = input("Escoja una opcion (recuerde que sigue en la misma seccion): ")
        
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

def validar_horario(msj="Ingrese la consulta: "):
    """ Funcion para formatear el ingreso de una fecha a traves de / o - """
    while True:
        consulta = input(msj)
        fecha = consulta.replace("/", " ").replace(":", " ").replace("-", " ")
        try:
            d, m, y, hora, minuto = map(int, fecha.split())  
            lista_numeros = [d, m, y, hora, minuto] 
            break
        except ValueError:
            print("ingreso invalido, debe ser una fecha del estilo (DD/MM/AAAA hh:mm), o (DD-MM-AAAA hh:mm)")
            print("Intente nuevamente")
            print()
    return lista_numeros

def formato_fechas():
    """ Funcion para sacar cada parametro de fecha y horario y que se agregue a una lista para agregarlo a la matriz principal """
    fecha_original = datetime.datetime.now()
    fecha_final = f"{fecha_original.day:02d}/{fecha_original.month:02d}/{fecha_original.year} {fecha_original.hour:02d}:{fecha_original.minute:02d}"
    return fecha_final


def guardar_archivo_append(registro):
    try:
        pedido = open("pedidos.txt", "at")
        registro = ";".join(registro)
        pedido.write(f"{registro}\n")
    
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:" , mensaje)

    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
    
    finally:
        try:
            pedido.close()
        except NameError:
            pass 

#lambda para separar cada campo de la linea del archivo#
separar_campos = lambda pedido: pedido.split(";")

#FUNCIONES PRINCIPALES#

def codigo_envio(numero):
    """
    Genera un código de envío único incrementando el contador para proximos pedidos.
    """
    numero += 1
    codigo1 = f"ENV{numero:03d}"
    
    return codigo1, numero

def agregar_envio(contador1): #Contador sirve para q se hagan las iteraciones, las toma cuando llama a codigo_envio
    """
    Agrega un nuevo envío al sistema solicitando datos del cliente.
    Valida el nombre del cliente (solo letras y espacios) y la dirección.
    Crea un nuevo registro con estado "Pendiente" y lo añade a la matriz.
    """
    
    codigo2, contador1 = codigo_envio(contador1)
    contador1 = str(contador1)

    cliente = input("📨​  --- Crear envío ---\nIngrese el nombre del cliente: ").title()

    cliente = validar_nombre(cliente)

    direccion= input("\nIngrese la direccion del cliente: ").title()

    direccion = validar_direccion(direccion)

    estado  = "Pendiente"
    

    fecha_sin_formato = formato_fechas()

    registro = [contador1, codigo2, cliente, direccion, estado, fecha_sin_formato]
    guardar_archivo_append(registro)
    
    # total_clientes = filas actuales
    total_clientes = contador1
    
    print()
    print("-" * 100)
    for i in range(len(registro)):
        print(registro[i], end=" | ")
    print()
    print("-" * 100)
    print("✅ Envio agregado con exito")
    print(f"\n👥 Total clientes (filas): {contador1}") #Se informa el total de los clientes
    
    
    return contador1 # devolvemos contador actualizado 

def consultar_envio():
    """
    Busca y muestra la información de un envío específico por su código de tracking, por cliente o por fecha.
    Solicita al usuario el código de tracking, busca en el archivo y muestra
    los datos del envío si existe, o un mensaje de error si no se encuentra.     
    """
    tipo_de_consulta = ("Por codigo", "Por cliente", "Por fecha")
    
    tipo_elegido = input(f"\n🔎​  --- Consultar envío ---\n1️⃣  Por codigo\n2️⃣  Por cliente\n3️⃣  ​Por fecha\n\nIngrese un numero para el tipo de consulta: ")
    tipo_elegido = validar_opciones(tipo_elegido, 1, 3)
    tipo_elegido = tipo_de_consulta[tipo_elegido - 1]

    encontrado = False

    if tipo_elegido == 'Por codigo':
        consulta = (input("Ingrese el codigo de tracking que desee consultar: ")).upper()
        print()
        for linea in arch:
            if linea[1] == consulta:
                encontrado = True
                linea = separar_campos(linea)
                print(f"{linea[1]:^10} | {linea[2]:^15} | {linea[3]:^15} | {linea[4]:^15} | {linea[5]:^15}")
    elif tipo_elegido == 'Por cliente':
        consulta = input("\nIngrese el nombre del cliente: ").title()
        print()
        for linea in arch:
            linea = linea.strip()
            if linea == "":
                continue

            campos = separar_campos(linea)
            if campos[2].title() == consulta:
                print("✅ Pedido encontrado:")
                print(f"Índice: {indice}")
                print(f"{campos[1]:^10} | {campos[2]:^12} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:15}")
                encontrado = True
                break
            indice += 1
    
    else: 
        lista_fecha = validar_horario(msj="\nIngrese la fecha a consultar (formato: DD/MM/AAAA hh:mm o DD-MM-AAAA hh:mm): ")
        print()
        encontrado = False
        for fila in range(len(matriz2[4])):
            if matriz2[4][fila] == lista_fecha:
                encontrado = True
                indice = fila
                break

    if encontrado:
        print("✅ Pedido encontrado:")
        print("-" * 100)
        for fila in matriz2[:-1]:
            print(fila[indice], end=" | ")
        print("/".join(map(str, matriz2[4][indice][:3])), end=" ")
        print(":".join(f"{x:02d}" for x in matriz2[4][indice][3:]))
        print("-" * 100)


def historial_envios():
    """
    Muestra todos los envíos registrados en el sistema, filtra por estado de pedido o fecha.
    Si no hay envíos registrados muestra un mensaje informativo.
    Si hay envíos, los lista todos mostrando código, cliente, dirección y estado.    
    """
    
    print("1. Listar todos\n2. Listar por fecha\n3. Listar por estado de envio")
    opcion = input("\nEscoja una opcion:")
    opcion = validar_opciones(opcion,1,3)
    
    try:
        arch = open("pedidos.txt","rt")
        match opcion:
            case 1: #LISTAR TODO#
                estados = ("Pendiente", "Despachado", "En camino", "Entregado", "Cancelado", "Devuelto")
                conteo = {estado: 0 for estado in estados}
                total = 0

                print("Lista de envíos 📦:")
                print("-" * 100)
                for linea in arch:
                    linea = separar_campos(linea)
                    print(f"{linea[1]:^10} | {linea[2]:^15} | {linea[3]:^15} | {linea[4]:^12} | {linea[5]:^10}")    
                    total += 1
                    if linea[4] in conteo:
                        conteo[linea[4]] += 1

                print("-" * 100)
                print(f"Total de Pedidos: {total}")

                print("\nEstadisticas de envios")
                print("-" * 100)
                for e, cantidad in conteo.items():
                    porcentaje = ((cantidad / total) * 100)if total > 0 else 0 
                    print(f"{e:<12} | {cantidad:>3} pedidos | Porcentaje: {porcentaje:5.1f}%")
                print("-"*100)

            case 2: ###POR FECHA###
                print("Lista de pedidos segun fecha 📦 ")
                
                fechas = ("año","mes", "dia", "hora")
                
                seleccion = input("1 - año \n2 - mes\n3 - dia\n4 - hora\nIngrese el parametro por el cual desea listar: ")
                
                seleccion = validar_opciones(seleccion,1,4)
                
                seleccion = fechas[seleccion - 1]

                encontrado=False

                if seleccion == "año":
                    año_actual = datetime.datetime.now().year
                    valor = input("Ingrese el año: ")
                    valor = validar_opciones(valor,año_actual,9999)
                    rango1, rango2 = 6,10 #rebanada donde se encuentra el año#

                elif seleccion == "mes":
                    valor = input("Ingrese el número del mes (1-12): ")
                    valor = validar_opciones(valor,1,12)
                    rango1, rango2 = 3,5 #rebanada donde se encuentra el mes#
                
                elif seleccion == "dia":
                    valor = input("Ingrese el número del día (1-31): ")
                    valor = validar_opciones(valor,1,31)
                    rango1, rango2 = 0,2 #rebanada donde se encuentra el dia#
                
                else:  
                    valor = input("Ingrese la hora (0hs-23hs): ")
                    valor = validar_opciones(valor,0,23)
                    rango1, rango2 = 11,13 #rebanada donde se encuentra la hora#
                
                for linea in arch:
                    campos = separar_campos(linea)
                    if campos[5][rango1:rango2] == str(valor):
                        print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^12} | {campos[5]:^10}")
                        encontrado = True
                            
                if not encontrado:
                    print(f"\nNo hay pedidos para el {seleccion} seleccionado.")

            case 3:#LISTAR POR ESTADO# 
                estados = ("Pendiente","Despachado","En camino","Entregado","Cancelado","Devuelto")

                seleccion = input("1 - Pendiente\n2 - Despachado\n3 - En camino \n4 - Entregado\n5 - Cancelado \n6 - Devuelto\n\nIngrese el valor que representa el estado el cual desea ver el listado: ")

                seleccion = validar_opciones(seleccion,1,6)

                seleccion = estados[seleccion-1]
                
                encontrado = False

                print(f"\nLista de pedidos con el estado {seleccion} 📦 : ")
                print("-"*100)

                #caso Excepcional para devuelto ya que tiene un motivo y no es solo el estado#
                for linea in arch:
                    campos = separar_campos(linea)
                    if seleccion == "Devuelto":
                        if "Devuelto" in campos[4]:  # captura Devuelto aunque tenga motivo
                            print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^12} | {campos[5]:^10}")
                            encontrado = True

                    elif campos[4] == seleccion:
                        print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^12} | {campos[5]:^10}")
                        encontrado = True

                if not encontrado:
                    print(f"\nNo hay pedidos con estado {seleccion}.")

                print("-"*100)
                
        ingreso = input("¿Desea continuar listando envios? Si / No: ").lower()
        while ingreso != "si" and ingreso != "no":
            ingreso = input("Ingreso invalido, ¿Desea continuar listando envios? Si / No: ").lower()
        if ingreso == "no":
            pass
        else:
            historial_envios()

    except OSError as error:
        print(f"Error al intentar manipular el archivo: {error}")
        
    finally:
        try:
            arch.close()
        except OSError as error:
            print(f"Error al intentar cerrar el archivo: {error}")


def cambiar_estado():
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
                        print(f"Pedido marcado como {matriz4[3][i]}.")
                        print("✅ Pedido actualizado: ")
                        for fila in matriz4[ :-1]:
                            print(fila[i], end=" | ")
                        print("/".join(map(str, matriz4[4][i][ :3])), end=" ")
                        print(":".join(f"{x:02d}" for x in matriz4[4][i][3: ]))
                        print()
                        break
                elif seguridad == "no":
                    print("Acción cancelada por decisión del usuario, volviendo al menú interno...")
                    continue
                else:
                    while seguridad != "no" and seguridad != "si":
                        print("Opción incorrecta, seleccione Si o No")
                        seguridad = input(f"Usted seleccionó la opción {estados_a_modificar}. ¿Desea confirmar esta opción? [Si/No]: ").lower()
                    break
            break

    if not encontrado:
        print("No se encontró un pedido con ese código. ❌")


def devoluciones(): 
    """
    Procesa la devolución de un pedido ya entregado.
    Busca el pedido por código, verifica que esté en estado "Entregado",
    solicita el motivo de la devolución y actualiza el estado.
    Solo permite devoluciones de pedidos entregados.    
    """
    codigo_devolucion = input("Ingrese el codigo del pedido a devolver: ").upper()
    
    encontrado = False
   
    try:
        archivo = open("pedidos.txt", "rt")
        salida = open("pedidostemp.txt","wt")  #nueva version
        k = 0
        for linea in archivo:
            salida.write(linea.upper())
            k += 1
    except FileNotFoundError as mensaje:
        print("No se pudo abrir el archivo", mensaje)
    except  OSError as mensaje:
        print("No se pudo abrir el archivo", mensaje)
    else:
        print("Copia finalizada. Líneas copiadas:", k)
    finally:
        try:
            archivo.close( )
        except NameError:
            pass

        if matriz5[0][c] == codigo_devolucion:
            encontrado = True
            if "Devuelto" in matriz5[3][c]: #para evitar que se devuelva nuevamente un producto ya devuelto#
                print("\nEste pedido ya ha sido devuelto anteriormente")
            elif matriz5[3][c] == "Entregado":
                motivo = input("Ingrese el motivo de porque le han devuelto el pedido: ").capitalize()
                matriz5[3][c] = f"Devuelto, causa: {motivo}"

                print("-"*100)
                print(f"Devolucion registrada: {matriz5[3][c]}")
                print("-"*100)             
            else:
                print("\nEl envio todavia no ha sido entregado por lo que no se puede realizar la devolucion")


    if not encontrado:
        print("Pedido no encontrado ❌ ")

#PROGRAMA PRINCIPAL#

try:
    archivo = open("pedidos.txt", "rt")
    ultima_linea = ""
    vacio = False
    
    for linea in archivo:
        linea_limpia = linea.strip()
        if linea_limpia != "":
            ultima_linea = linea_limpia
    
    if ultima_linea == "":  # Archivo vacío
        vacio = True
        n = 0
    else:
        campos = ultima_linea.split(";")
        n = int(campos[0])
        #se define para continuar el indice de pedidos desde la ultima apertura#
except FileNotFoundError:
    print("⚠️ No se encontró 'pedidos.txt'. Se creará un nuevo archivo.")
    open("pedidos.txt", "wt").close()
    n = 0
    print(f"🔢 Contador inicial (archivo nuevo): {n}")  # Debug

except OSError as mensaje:
    print("No se puede leer el archivo:", mensaje)
    n = 0
    
else:
    try:
        archivo.close()
    except OSError:
        pass

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
        
        opcion = validar_opciones(opcion, 0, 5)
            
        if opcion != 1 and opcion != 0 and vacio: #si el archivo se encuentra vacio el unico ingreso valido seria agregar o salir#
            print("El archivo se encuentra vacio")

        else:
            match opcion:
                case 0:
                    print("Nos vemos! 👋 ")
                    break
                case 1:
                    n = int(agregar_envio(n))  
                case 2:
                    consultar_envio()
                case 3:
                    historial_envios()
                case 4:
                    cambiar_estado()
                case 5:
                    devoluciones()
    