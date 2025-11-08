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
            print(f"Ingreso inválido, usted ingreso un valor NO entero.")
        except AssertionError:
            print(f"\nIngreso invalido, usted ingreso un valor fuera de los rangos establecidos, ")    
        print(f'Recuerde que debe ser un entero entre {rango1} y {rango2}\n')
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
            lista_numeros = f"{d}/{m}/{y} {hora}:{minuto}"
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

def separar_campos(linea):
    linea = linea.strip() 
    campos = linea.split(";")
    return campos

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

    provincia = input("\nIngrese la provincia de destino: ").title()

    provincias = ("Buenos Aires", "Catamarca", "Chaco", "Chubut", "Cordoba", "Corrientes", "Entre Rios", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquen", "Ro Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucuman")

    while provincia not in provincias:
        provincia = input("\nIngreso invalido, reintente\nIngrese la provincia de destino: ").title()

    estado  = "Pendiente"

    fecha_sin_formato = formato_fechas()

    registro = [contador1, codigo2, cliente, direccion,provincia, estado, fecha_sin_formato]
    guardar_archivo_append(registro)
    
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
    tipo_de_consulta = ("Volver al menu", "Por codigo", "Por cliente", "Por fecha")
    
    tipo_elegido = input(f"\n🔎​  --- Consultar envío ---\n0️⃣  Volver al menú anterior\n1️⃣  Por codigo\n2️⃣  Por cliente\n3️⃣  ​Por fecha\n\nIngrese un numero para el tipo de consulta: ")
    tipo_elegido = validar_opciones(tipo_elegido, 0, 3)
    tipo_elegido = tipo_de_consulta[tipo_elegido]
    
    try:
        arch = open("pedidos.txt", "rt")
        
        
        if tipo_elegido == "Por codigo":
            consulta = (input("Ingrese el codigo de tracking que desee consultar: ")).upper()
            print()
            while consulta[ :5] != "ENV00":
                print("Ingreso incorrecto, intente nuevamente")
                consulta = (input("Ingrese el codigo de tracking que desee consultar: ")).upper()
            encontrado = False
            for linea in arch:
                if linea.strip() != "":
                    linea = separar_campos(linea)
                    if linea[1] == consulta:
                        encontrado = True
                        print("✅ Pedido encontrado:")
                        print(f"{linea[1]:^10} | {linea[2]:^15} | {linea[3]:^15} | {linea[4]:^15} | {linea[5]:^15} | {linea[6]:^15}")
                        break
            if encontrado == False:
                print("\n No hay pedidos con ese codigo de envio")
            consultar_envio()
        elif tipo_elegido == "Por cliente":
            consulta = input("\nIngrese el nombre del cliente: ").title()
            print()
            encontrado = False
            for linea in arch:
                if linea.strip() != "":
                    linea = separar_campos(linea)
                    if linea[2] == consulta:
                        encontrado = True
                        print("✅ Pedido encontrado:")
                        print(f"{linea[1]:^10} | {linea[2]:^15} | {linea[3]:^15} | {linea[4]:^15} | {linea[5]:^15} | {linea[6]:^15}")
            if encontrado == False:
                print("\n No hay pedidos con ese nombre de cliente")
            consultar_envio()
        elif tipo_elegido == "Por fecha": 
            cadena_fecha = validar_horario(msj="\nIngrese la fecha a consultar (formato: DD/MM/AAAA hh:mm o DD-MM-AAAA hh:mm): ")
            print()
            
            encontrado = False
            for linea in arch:
                if linea.strip() != "":
                    linea = separar_campos(linea)
                    if linea[6] == cadena_fecha:
                        print("✅ Pedido encontrado:")
                        encontrado = True
                        print(f"{linea[1]:^10} | {linea[2]:^15} | {linea[3]:^15} | {linea[4]:^15} | {linea[5]:^15} | {linea[6]:^15}")
            if encontrado == False:
                print("\n No hay pedidos con esa fecha")
            consultar_envio()
        else:
            pass
    except FileNotFoundError as mensaje:
        print("No se pudo abrir el archivo", mensaje)
    except  OSError as mensaje:
        print("No se pudo abrir el archivo", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

def historial_envios():
    """
    Muestra todos los envíos registrados en el sistema, filtra por estado de pedido o fecha.
    Si no hay envíos registrados muestra un mensaje informativo.
    Si hay envíos, los lista todos mostrando código, cliente, dirección y estado.    
    """
    
    print("\n📦 --- Listar envios ---\n0️⃣  Volver al menu\n1️⃣  Listar todos\n2️⃣  Listar por fecha\n3️⃣  Listar por estado de envio\n4️⃣​  Listar por provincias\n5️⃣  Mostrar estadisticas")
    opcion = input("\nEscoja una opcion:")
    opcion = validar_opciones(opcion,1,5)
    
    try:
        arch = open("pedidos.txt","rt")
        
        #se inicializa fuera del match case ya que sera usado en mas de dos cases#
        estados = ("Pendiente", "Despachado", "En camino", "Entregado", "Cancelado", "Devuelto")
        provincias = ("Buenos Aires", "Catamarca", "Chaco", "Chubut", "Cordoba", "Corrientes", "Entre Rios", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquen", "Rio Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucuman")
        total = 0

        match opcion:
            case 1: #LISTAR TODO#
                print("Lista de envíos 📦:")
                print("-" * 100)
                ultima_linea1 = "" 
                for linea in arch:
                    if linea.strip() != "":
                        campos = separar_campos(linea)
                        print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^10} | {campos[6]:^10}")
                        total += 1
                        ultima_linea1 = linea

                if ultima_linea1 == "":
                    print("Actualmente no existen pedidos en el sistema")
                print("-" * 100)
                print(f"Total de Pedidos: {total}")
                    
            case 2: ###POR FECHA###
                print("Lista de pedidos segun fecha 📦 ")
                print("-" * 100)
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
                    if linea.strip() != "":
                        campos = separar_campos(linea)
                        if campos[6][rango1:rango2] == f"{valor:02d}":
                            print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^12} | {campos[5]:^10} | {campos[6]:^10}")
                            encontrado = True
                            
                if not encontrado:
                    print(f"\nNo hay pedidos para el {seleccion} seleccionado.")
                print("-" * 100)

            case 3:#LISTAR POR ESTADO# 
                seleccion = input("1 - Pendiente\n2 - Despachado\n3 - En camino \n4 - Entregado\n5 - Cancelado \n6 - Devuelto\n\nIngrese el valor que representa el estado el cual desea ver el listado: ")

                seleccion = validar_opciones(seleccion,1,6)

                seleccion = estados[seleccion-1]
                
                encontrado = False

                print(f"\nLista de pedidos con el estado {seleccion} 📦 : ")
                print("-"*100)

                #caso Excepcional para devuelto ya que tiene un motivo y no es solo el estado#
                for linea in arch:
                    if linea.strip() != "":
                        campos = separar_campos(linea)
                        if seleccion == "Devuelto":
                            if "Devuelto" in campos[5]:  # captura Devuelto aunque tenga motivo
                                print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^12} | {campos[5]:^10} | {campos[6]:^10}")
                                encontrado = True

                        elif campos[5] == seleccion:
                            print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^12} | {campos[5]:^10} | {campos[6]:^10}")
                            encontrado = True

                if not encontrado:
                    print(f"\nNo hay pedidos con estado {seleccion}.")
                print("-"*100)
                
            #listar por provincia#
            case 4:
                seleccion = input("Ingrese el nombre de la provincia que desea listar: ").title()

                while seleccion not in provincias:
                    seleccion = input("Ingreso invalido, reintente\nIngrese el nombre de la provincia que desea listar: ").title()
                
                encontrado = False
                
                print(f"\nLista de pedidos provenientes de {seleccion} 📦 : ")
                print("-"*100)
                
                for linea in arch:
                    if linea.strip() != "":
                        campos = separar_campos(linea)
                        if campos[4] == seleccion:
                            print(f"{campos[1]:^10} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^12} | {campos[5]:^10} | {campos[6]:^10}")
                            encontrado = True
                
                print("-"*100)
                
                if not encontrado:
                    print(f"No hay pedidos de la provincia {seleccion}")

            case 5:
                conteo_provincias = {provincia: 0 for provincia in provincias}
                conteo_estados = {estado: 0 for estado in estados}

                for linea in arch:
                    if linea.strip()!="":
                        campos = separar_campos(linea)
                        #conteo para provincias#
                        conteo_provincias[campos[4]] += 1
                        #conteo para estados#
                        if "Devuelto" in campos[5]:
                            conteo_estados["Devuelto"] += 1
                        elif campos[5] in conteo_estados:
                            conteo_estados[campos[5]] += 1
                        total += 1

                if total > 0:
                    print("\n📊 Estadísticas generales por provincia:")
                    print("-" * 100)
                    for provincia in provincias:
                        cantidad = conteo_provincias[provincia]
                        porcentaje = (cantidad / total) * 100
                        print(f"{provincia:<25} | {cantidad:>3} pedidos | Porcentaje: {porcentaje:5.1f}%")
                    print("-" * 100)
                    print("\n\n📊 Estadísticas generales por estado de envio:")
                    print("-" * 100)
                    for estado1 in estados:
                        cantidad1 = conteo_estados[estado1]
                        porcentaje1 = (cantidad1 / total) * 100
                        print(f"{estado1:<12} | {cantidad1:>3} pedidos | Porcentaje: {porcentaje1:5.1f}%")
                    print("-" * 100)
                    print(f"Total de Pedidos: {total}")
                else:
                    print("No se encuentran pedidos en el sistema para poder realizar estadisticas")

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
    codigo_objetivo = input("🔄 --- Cambiar estado ---\nIngrese el código de envío a modificar: ").upper()
    encontrado = False

    try:
        original = open("pedidos.txt", "rt")
        temporal = open("pedidostemp.txt", "wt")

        for linea in original:
            if not linea.strip():
                continue  # salta líneas vacías

            partes = linea.strip().split(";")
            codigo = partes[1]  # el código está en la posición 1
            estado_actual = partes[5]

            if codigo == codigo_objetivo:
                encontrado = True
                print(f"Estado actual: {estado_actual}")
                print("\nOpciones de nuevo estado:")
                print("1️⃣ - Pendiente")
                print("2️⃣ - Despachado")
                print("3️⃣ - En camino")
                print("4️⃣ - Entregado")
                print("5️⃣ - Cancelar pedido")
                print("0️⃣ - Volver al menú")

                opcion = input("Seleccione una opción: ")
                opcion = validar_opciones(opcion, 0, 5)

                if opcion == 0:
                    print("Volviendo al menú principal...")
                    temporal.write(linea)
                    continue

                estados_a_modificar = ("Pendiente", "Despachado", "En camino", "Entregado", "Cancelar pedido")
                nuevo_estado = estados_a_modificar[opcion - 1]

                seguridad = input(f"Usted seleccionó '{nuevo_estado}' para el pedido {codigo}. ¿Desea confirmar? [Si/No]: ").lower()
                if seguridad != "si":
                    print("Acción cancelada. No se realizaron cambios.")
                    temporal.write(linea)
                    continue

                # Reglas de validación
                if "Devuelto" in estado_actual:
                    print("❌ No se puede cambiar el estado de un pedido que ya fue devuelto.")
                    temporal.write(linea)
                    continue

                if estado_actual == "Entregado" and nuevo_estado == "Cancelar pedido":
                    print("❌ No se puede cancelar un pedido que ya fue entregado.")
                    temporal.write(linea)
                    continue

                # Actualización del estado
                if nuevo_estado == "Cancelar pedido":
                    nuevo_estado = "Cancelado"

                partes[5] = nuevo_estado
                linea_modificada = ";".join(partes)
                temporal.write(linea_modificada + "\n")

                print(f"✅ Pedido {codigo} actualizado a estado: {nuevo_estado}")
            else:
                temporal.write(linea)

        original.close()
        temporal.close()

        if encontrado:
            os.replace("pedidostemp.txt", "pedidos.txt")
        else:
            os.remove("pedidostemp.txt")
            print("❌ No se encontró un pedido con ese código.")

    except FileNotFoundError:
        print("⚠️ No se encontró el archivo 'pedidos.txt'.")
    except OSError as e:
        print(f"Error al acceder al archivo: {e}")
    finally:
        try:
            original.close()
            temporal.close()
        except NameError:
            pass

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
        salida = open("pedidostemp.txt","wt")  
        
        for linea in archivo:
            if linea.strip() == "":
                continue
        
            campos = separar_campos(linea)

            if campos[1].upper() == codigo_devolucion:
                encontrado = True
                if "Devuelto" in campos[5]:
                    print("\nEste pedido ya ha sido devuelto anteriormente")
                elif campos[5] == "Entregado":
                    motivo = input("Ingrese el motivo de devolucion: ").capitalize()
                    campos[5] = f"Devuelto, causa: {motivo}"
                    print("-"*100)
                    print(f"Devolucion registrada: {campos[5]}")
                    print("-"*100)             
                else:
                    print("\nEl envio todavia no ha sido entregado por lo que no se puede realizar la devolucion")
                
                salida.write(";".join(campos) + "\n")
            
            else:
                salida.write(linea + "\n")
                
        if encontrado == False:
            print("Pedido no encontrado ")
    

        os.rename("pedidostemp.txt", "pedidos.txt") 

    except FileNotFoundError as mensaje:
        print("No se pudo encontrar el archivo", mensaje)
    except OSError as mensaje:
        print("No se pudo abrir el archivo", mensaje)
    finally:
        try:
            archivo.close()
            salida.close()
        except OSError:
            print("No se pudo cerrar el archivo", mensaje)
        except NameError:
            print("No se pudo cerrar el archivo ya que no existe", mensaje)

#PROGRAMA PRINCIPAL#

try:
    archivo = open("pedidos.txt", "rt")
    ultima_linea = ""
    
    for linea in archivo:
        linea_limpia = linea.strip()
        if linea_limpia != "":
            ultima_linea = linea_limpia
    
    if ultima_linea == "":  # Archivo vacío
        n = 0 #se incializa el contador de envios (para tracking) en 0 ya que no existen pedidos#
    else:
        campos = ultima_linea.split(";")
        n = int(campos[0]) #se incializa el contador de envios desde el ultimo envio encontrado en el archivo#

except FileNotFoundError:
    print("⚠️ No se encontró 'pedidos.txt'.")
    n = 0

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
    