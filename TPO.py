import datetime
import os

#-----------------------------------------------------
#FUNCIONES PARA RESTRICCIONES
#-----------------------------------------------------

def validar_opciones(seleccion,rango1,rango2):
    """
    Función creada para validar la selección de opciones dentro de un rango, ideal para los menus
    """
    while True:
        try:
            seleccion = int(seleccion) #ya que el input es un string se intenta pasar a int para verificar si es correcto el ingreso
            assert rango1<=seleccion<=rango2 #debe estar detro del rango
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
        if nombre.strip() == "": #si no se ingresa nombre dara false, restriccion para que se ingrese de manera obligatoria un nombre
            valido = False
        else:
            for c in nombre:
                if (not c.isalpha()) and (c != " "): #en caso de que ambos sean falsos es invalido ya que no es una letra ni un espacio
                    valido = False
                    break
        if valido:
            break
        else:
            nombre = input("Ingreso inválido, recuerde que no se permite ingresar números ni símbolos. \nIngrese el nombre del cliente: ")
    return nombre.title()

def validar_direccion(direc):
    """
    Función para validar que se haya ingresado una dirección y no un espacio vacío
    """
    while True:
        valido = True
        if direc.strip() == "": #si no se ingresa direccion dara false, restriccion para que se ingrese de manera obligatoria una direccion
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
        try: #intenta validar la entrada para que sea una fecha real
            d, m, y, hora, minuto = map(int, fecha.split())
            valido = True
            
            if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
                n = 29
            else:
                n = 28
            
            dias_posibles = (31,n,31,30,31,30,31,31,30,31,30,31)
            
            if y <= 0 or y > 9999:
                valido = False
            elif m <= 0 or m > 12:
                valido = False
            elif (d < 1) or (d > dias_posibles[m - 1]):
                valido = False
            elif hora < 0 or hora > 23:
                valido = False
            elif minuto < 0 or minuto > 59:
                valido = False
            if not valido:
                raise ValueError
            lista_numeros = f"{d:02d}/{m:02d}/{y} {hora:02d}:{minuto:02d}" #formatea el string para que coincida con el formato del archivo
            break
        except ValueError:
            print("ingreso invalido, debe ser una fecha del estilo (DD/MM/AAAA hh:mm), o (DD-MM-AAAA hh:mm)")
            print("Intente nuevamente")
    return lista_numeros

def formato_fechas():
    """ Funcion para sacar cada parametro de fecha y horario, cargarlo como string para luego que se cargue bien en el archivo """
    fecha_original = datetime.datetime.now()
    fecha_final = f"{fecha_original.day:02d}/{fecha_original.month:02d}/{fecha_original.year} {fecha_original.hour:02d}:{fecha_original.minute:02d}"
    return fecha_final

def guardar_archivo_append(registro):
    """ agrega un pedido al archivo de forma que no se eliminen los anteriores """
    try: #intenta abrir el archivo donde estan los pedidos
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
    """ Separa los campos de una línea del archivo pedidos.txt """
    linea = linea.strip() 
    campos = linea.split(";")
    return campos

def preguntar_continuar():
    """ Pregunta al usuario si desea continuar """
    ingreso = input(f"\n¿Desea continuar en dicha operación? Si/No: ").lower()
    while ingreso != "si" and ingreso != "no":
        ingreso = input("Ingreso inválido. Debe ser Si/No: ").lower()
    return ingreso == "si"

def sacar_acentos(entrada):
    """ formatea las entradas para que no se carguen acentos """
    acentos = (
    ("á", "a"),
    ("é","e"),
    ("í","i"),
    ("ó","o"),
    ("ú","u"),
    ("Á", "A"),
    ("É","E"),
    ("Í","I"),
    ("Ó","O"),
    ("Ú","U")
    )
    for i, j in acentos:
        entrada = entrada.replace(i,j)
    return entrada

#-----------------------------------------------------
#FUNCIONES PRINCIPALES
#-----------------------------------------------------

def codigo_envio(numero):
    """ Genera un código de envío único incrementando el contador para proximos pedidos """
    numero += 1
    codigo1 = f"ENV{numero:03d}"
    return codigo1, numero

def agregar_envio(contador1): 
    """ Se agrega un nuevo pedido en forma de registro, para luego ser cargado en el archivo, el pedido tiene el codigo de tracking, nombre del cliente, direccion, provincia de destino, estado del pedido y la fecha en la que se emite el mismo """
    
    # Se inicializan las variables para la carga del pedido
    
    codigo2, contador1 = codigo_envio(contador1)
    
    cliente = input("📨​  --- Crear envío ---\nIngrese el nombre del cliente: ").title()
    cliente = validar_nombre(cliente)
    cliente = sacar_acentos(cliente)
    
    direccion= input("\nIngrese la direccion del cliente: ").title()
    direccion = validar_direccion(direccion)
    direccion = sacar_acentos(direccion)
    
    provincia = input("\nIngrese la provincia de destino: ").title()
    provincia = sacar_acentos(provincia)
    provincias = ("Buenos Aires", "Catamarca", "Chaco", "Chubut", "Cordoba", "Corrientes", "Entre Rios", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquen", "Rio Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucuman")
    while provincia not in provincias:
        provincia = input("\nIngreso invalido, reintente\nIngrese la provincia de destino: ").title()
        provincia = sacar_acentos(provincia)
    
    estado  = "Pendiente"
    
    fecha_sin_formato = formato_fechas()
    
    registro = [str(contador1), codigo2, cliente, direccion,provincia, estado, fecha_sin_formato]
    guardar_archivo_append(registro)
    
    # Se imprime el pedido recien agregado
    print()
    print("-" * 100)
    for i in range(len(registro)):
        print(registro[i], end=" | ")
    print()
    print("-" * 100)
    print("✅ Envio agregado con exito")
    print(f"\n👥 Total clientes (filas): {contador1}") 
    
    return contador1 

def consultar_envio():
    """ Busca y muestra la información de un envío específico por su código de tracking, por cliente o por fecha.
    Solicita al usuario el código de tracking, busca en el archivo y muestra
    los datos del envío si existe, o un mensaje de error si no se encuentra """
    
    while True: #para repetir la entrada si se responde que si a la confirmacion
        tipo_de_consulta = ("Salida","Por codigo", "Por cliente", "Por fecha")
        tipo_elegido = input(f"\n🔎​  --- Consultar envío ---\n0️⃣  Volver al menú anterior\n1️⃣  Por codigo\n2️⃣  Por cliente\n3️⃣  ​Por fecha\n\nescoja una opcion: ") # se pregunta que pedido se desea consultar
        
        tipo_elegido = validar_opciones(tipo_elegido, 0, 3)
        tipo_elegido = tipo_de_consulta[tipo_elegido]
        
        try: #intenta abrir el archivo
            arch = open("pedidos.txt", "rt")
            if tipo_elegido == "Por codigo":
                consulta = (input("Ingrese el codigo de tracking que desee consultar: ")).upper()
                
                # Validacion de formato
                while consulta[ :3] != "ENV" or not consulta[3: ].isdigit() or len(consulta[3: ]) < 3:
                    print("Ingreso incorrecto (debe tener al menos 3 digitos), intente nuevamente")
                    consulta = (input("Ingrese el codigo de tracking que desee consultar: ")).upper()
                
                encontrado = False
                ultima_linea = ""
                for linea in arch: #Se recorren las lineas del archivo, luego se descarta la anterior
                    if linea.strip() != "":
                        campos = separar_campos(linea)
                        if campos[1] == consulta: #Si se encuentra el codigo de tracking
                            encontrado = True
                            print("✅ Pedido encontrado:")
                            print("-"*100)
                            print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^{25 if campos[5][ :8] == "Devuelto" else 10}} | {campos[6]:^15}")
                            print("-"*100)
                            break
                        ultima_linea = linea
                    
                if encontrado == False:
                    print("-"*100)
                    print(" No hay pedidos con ese codigo de envio")
                    print("-"*100)
            elif tipo_elegido == "Por cliente":
                consulta = input("\nIngrese el nombre del cliente: ").title()
                consulta = sacar_acentos(consulta)
                print()
                encontrado = False
                ultima_linea = ""
                for linea in arch: #Se recorren las lineas del archivo, luego se descarta la anterior
                    if linea.strip() != "":
                        campos = separar_campos(linea)
                        if campos[2] == consulta: #Si se encuentra el nombre del cliente
                            print("✅ Pedido encontrado:")
                            encontrado = True
                            print("-"*100)
                            print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^{25 if campos[5][ :8] == "Devuelto" else 10}} | {campos[6]:^15}")
                            print("-"*100)
                        ultima_linea = linea
                if ultima_linea == "":
                    print("\nActualmente no hay pedidos cargados")
                    print("-"*100)
                    encontrado = True
                    
                if encontrado == False:
                    print("-"*100)
                    print(" No hay pedidos con ese nombre de cliente")
                    print("-"*100)
            elif tipo_elegido == "Por fecha": 
                cadena_fecha = validar_horario(msj="\nIngrese la fecha a consultar (formato: DD/MM/AAAA hh:mm o DD-MM-AAAA hh:mm): ") #Se valida directamente la fecha ingresada
                print()
                
                encontrado = False
                ultima_linea = ""
                for linea in arch: #Se recorren las lineas del archivo, luego se descarta la anterior
                    if linea.strip() != "":
                        campos = separar_campos(linea)
                        if campos[6] == cadena_fecha: #Si se encuentra el pedido emitido con dicha fecha y horario
                            print("✅ Pedido encontrado:")
                            print("-"*100)
                            encontrado = True
                            print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^{25 if campos[5][ :8] == "Devuelto" else 10}} | {campos[6]:^15}")
                            print("-"*100)
                        ultima_linea = linea
                if ultima_linea == "":
                    print("\nActualmente no hay pedidos cargados")
                    print("-"*100)
                    encontrado = True
                    
                if encontrado == False:
                    print("-"*100)
                    print(" No hay pedidos con esa fecha")
                    print("-"*100)
            elif tipo_elegido == "Salida":
                print("\nVolviendo al menu principal...")
                break

            repetir = preguntar_continuar() #Pregunta para consultar otro envio

            if not repetir:
                break

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
    """ Muestra todos los envíos registrados en el sistema, filtra por provincia, estado de pedido o fecha. Se imprimen las estadisticas de los estados de envio y de pedidos de distintas provincias """
    while True:
        print("📦 --- Listar envios ---\n0️⃣  Volver al menú anterior\n1️⃣  Listar todos\n2️⃣  Listar por fecha\n3️⃣  Listar por estado de envio\n4️⃣​  Listar por provincias\n5️⃣  Mostrar estadisticas")
        opcion = input("\nEscoja una opcion: ")
        opcion = validar_opciones(opcion,0,5)
        try:
            arch = open("pedidos.txt","rt")
            
            #se inicializa fuera del match case ya que sera usado en mas de dos cases
            estados = ("Pendiente", "Despachado", "En camino", "Entregado", "Cancelado", "Devuelto")
            provincias = ("Buenos Aires", "Catamarca", "Chaco", "Chubut", "Cordoba", "Corrientes", "Entre Rios", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquen", "Rio Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucuman")
            total = 0

            match opcion:
                case 0:
                    print("\nVolviendo al menu principal...")
                    break
                case 1: #listar todo
                    print("Lista de envíos 📦:")
                    print("-" * 100)
                    for linea in arch:
                        if linea.strip() != "":
                            campos = separar_campos(linea)
                            print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^{25 if campos[5][ :8] == "Devuelto" else 10}} | {campos[6]:^15}")
                            total += 1
                    print("-" * 100)
                    print(f"Total de Pedidos: {total}")
                    print()
                case 2: #listar por fecha
                    print("Lista de pedidos segun fecha 📦 ")
                    print("-" * 100)
                    fechas = ("año","mes", "dia", "hora")
                    
                    seleccion = input("1 - año \n2 - mes\n3 - dia\n4 - hora\nIngrese el parametro por el cual desea listar: ")
                    
                    seleccion = validar_opciones(seleccion,1,4)
                    seleccion = fechas[seleccion - 1]
                    encontrado=False
                    
                    if seleccion == "año": #Segun el año de emision
                        año_actual = datetime.datetime.now().year
                        valor = input("Ingrese el año: ")
                        valor = validar_opciones(valor,2025,año_actual)
                        rango1, rango2 = 6,10 #indices de la rebanada donde se encuentra el año
                        
                    elif seleccion == "mes": #Segun el mes de emision
                        valor = input("Ingrese el número del mes (1-12): ")
                        valor = validar_opciones(valor,1,12)
                        rango1, rango2 = 3,5 #indices de la rebanada donde se encuentra el mes
                    
                    elif seleccion == "dia": #Segun el dia de emision
                        valor = input("Ingrese el número del día (1-31): ")
                        valor = validar_opciones(valor,1,31)
                        rango1, rango2 = 0,2 #indices de la rebanada donde se encuentra el dia#
                    
                    else: #Segun la hora de emision
                        valor = input("Ingrese la hora (0hs-23hs): ")
                        valor = valor.replace("hs","")
                        valor = validar_opciones(valor,0,23)
                        rango1, rango2 = 11,13 #indices de la rebanada donde se encuentra la hora
                    
                    print("-"*100)
                    for linea in arch:
                        if linea.strip() != "":
                            campos = separar_campos(linea)
                            if campos[6][rango1:rango2] == f"{valor:02d}": #Imprime segun el filtro de fecha igualando a lo que ingresa el usuario
                                print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^{25 if campos[5][ :8] == "Devuelto" else 10}} | {campos[6]:^15}")
                                encontrado = True
                                
                    if not encontrado:
                        print(f"No hay pedidos para {seleccion} seleccionado.")
                    print("-" * 100)
                    
                case 3: #listar por estado
                    seleccion = input("1 - Pendiente\n2 - Despachado\n3 - En camino \n4 - Entregado\n5 - Cancelado \n6 - Devuelto\n\nIngrese el valor que representa el estado el cual desea ver el listado: ")
                    
                    seleccion = validar_opciones(seleccion,1,6)
                    seleccion = estados[seleccion-1]
                    encontrado = False
                    
                    print(f"\nLista de pedidos con el estado {seleccion} 📦 : ")
                    print("-"*100)

                    for linea in arch:
                        if linea.strip() != "":
                            campos = separar_campos(linea)
                            # Para la excpecion "Devuelto"
                            if seleccion == "Devuelto":
                                if campos[5][:8] == "Devuelto": 
                                    print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^25} | {campos[6]:^15}") 
                                    encontrado = True
                            # Para los demás estados
                            elif campos[5] == seleccion:
                                print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^10} | {campos[6]:^15}")
                                encontrado = True

                    if not encontrado:
                        print(f"No hay pedidos con estado {seleccion}.")
                    print("-"*100)
                    
                case 4: #listar por provincia
                    seleccion = input("Ingrese el nombre de la provincia que desea listar: ").title()
                    seleccion = sacar_acentos(seleccion)

                    while seleccion not in provincias: #Validacion de provincia
                        seleccion = input("Ingreso invalido, reintente\nIngrese el nombre de la provincia que desea listar: ").title()
                        seleccion = sacar_acentos(seleccion)
                    
                    encontrado = False
                    
                    print(f"\nLista de pedidos provenientes de {seleccion} 📦 : ")
                    
                    print("-"*100)
                    
                    for linea in arch:
                        if linea.strip() != "":
                            campos = separar_campos(linea)
                            if campos[4] == seleccion: #iguala al ingreso del usuario
                                print(f"{campos[1]:^7} | {campos[2]:^15} | {campos[3]:^15} | {campos[4]:^15} | {campos[5]:^{25 if campos[5][ :8] == "Devuelto" else 10}} | {campos[6]:^15}")
                                encontrado = True
                    if not encontrado:
                        print(f"No hay pedidos de la provincia {seleccion}")
                    
                    print("-"*100)
                    
                case 5: #estadisticas
                    conteo_provincias = {provincia: 0 for provincia in provincias}
                    conteo_estados = {estado: 0 for estado in estados}

                    for linea in arch:
                        if linea.strip()!="":
                            campos = separar_campos(linea)
                            #conteo para provincias
                            conteo_provincias[campos[4]] += 1
                            #conteo para estados
                            if campos[5][:8]=="Devuelto":
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
                        print("-"*100)
                        
                        print(f"Total de Pedidos: {total}")
                    else:
                        print("-"*100)
                        print("No se encuentran pedidos en el sistema para poder realizar estadisticas")
                        print("-"*100)
                        
            repetir = preguntar_continuar()
            
            if not repetir:
                    break
            
        except OSError as error:
            print(f"Error al intentar manipular el archivo: {error}")
            
        finally:
            try:
                arch.close()
            except OSError as error:
                print(f"Error al intentar cerrar el archivo: {error}")


def cambiar_estado():
    """ Permite modificar el estado de un envío existente.
    Valida que no se pueda cancelar un pedido ya entregado """

    while True:
        codigo_objetivo = input("\n🔄 --- Cambiar estado ---\nIngrese el código de tracking que desee modificar: ").upper()

        while codigo_objetivo[ :3] != "ENV" or not codigo_objetivo[3: ].isdigit() or len(codigo_objetivo[3: ]) < 3:
            print("Ingreso incorrecto. Debe ser formato ENVXXX, intente nuevamente")
            codigo_objetivo = (input("\nIngrese el codigo de tracking que desee modificar: ")).upper()

        encontrado = False
        try:
            original = open("pedidos.txt", "rt")
            temporal = open("pedidostemp.txt", "wt")
            volver = True
            
            for linea in original:
                if linea.strip() == "":
                    continue  # salta líneas vacías

                partes = separar_campos(linea)
                codigo = partes[1]  # el código está en la posición 1
                estado_actual = partes[5]    # el estado actual está en la posición 5

                if codigo == codigo_objetivo:
                    encontrado = True
                    print("-"*100)
                    print(f"Estado actual: {estado_actual}")
                    
                    print("\nOpciones de nuevo estado:")
                    print("1️⃣ - Pendiente")
                    print("2️⃣ - Despachado")
                    print("3️⃣ - En camino")
                    print("4️⃣ - Entregado")
                    print("5️⃣ - Cancelar pedido")
                    print("0️⃣ - Volver al menú")

                    opcion = input("\nEscoja una opción: ")
                    opcion = validar_opciones(opcion, 0, 5)

                    #Si elige volver al menu, no se modifica más
                    if opcion == 0:
                        print("Volviendo al menú principal...")
                        volver = False
                        temporal.write(linea)
                        continue

                    estados_a_modificar = ("Pendiente", "Despachado", "En camino", "Entregado", "Cancelar pedido")
                    nuevo_estado = estados_a_modificar[opcion - 1]

                    # Confirmación de cambio de estado
                    seguridad = input(f"\nUsted seleccionó '{nuevo_estado}' para el pedido {codigo}. ¿Desea confirmar? [Si/No]: ").lower()
                    print("-"*100)
                    if seguridad != "si":
                        print("Acción cancelada. No se realizaron cambios.")
                        temporal.write(linea) 
                        continue

                    # Restriccion: si el pedido fue devuelto no se puede cambiar su estado
                    if estado_actual[:8] == "Devuelto":
                        print("❌ No se puede cambiar el estado de un pedido que ya fue devuelto.")
                        temporal.write(linea)
                        continue
                    # Restriccion: no se puede cancelar un pedido ya entregado
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

            # Reemplazo del archivo original por el temporal si se encontró el pedido
            if encontrado:
                os.replace("pedidostemp.txt", "pedidos.txt")
            else:
                #Si no se encontró el pedido, se elimina el archivo temporal
                os.remove("pedidostemp.txt")
                print("❌ No se encontró un pedido con ese código.")
            
            repetir = preguntar_continuar()
            if not repetir:
                break

        except FileNotFoundError:
            print("⚠️ No se encontró el archivo 'pedidos.txt'.")
        except OSError as e:
            print(f"Error al acceder al archivo: {e}")
        finally:
            try:
                original.close() ## esto cierra el archivo
                temporal.close()
            except NameError:
                pass

def devoluciones(): 
    """ Procesa la devolución de un pedido ya entregado. """
    
    codigo_devolucion = input("\n↩️  --- Devoluciones ---\nIngrese el codigo del pedido a devolver: ").upper()
    while codigo_devolucion[ :3] != "ENV" or not codigo_devolucion[3: ].isdigit() or len(codigo_devolucion[3: ]) < 3:
            print("Ingreso incorrecto. Debe ser formato ENVXXX, intente nuevamente")
            codigo_devolucion = (input("\nIngrese el codigo de tracking del pedido a devolver: ")).upper()

    encontrado = False  
    try:#apertura de archivos
        archivo = open("pedidos.txt", "rt")
        salida = open("pedidostemp.txt","wt")  
        
        for linea in archivo: #lectura linea por linea, descartando la anterior
            if linea.strip() == "":
                continue
        
            campos = separar_campos(linea) 

            if campos[1].upper() == codigo_devolucion: #comparacion del codigo ingresado con el del archivo
                encontrado = True
                # Se verifica que el pedido este en condiciones de devolverse
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
                
                salida.write(";".join(campos) + "\n") #escritura en el archivo temporal
            
            else:
                salida.write(linea)

    except FileNotFoundError as mensaje: 
        print("No se pudo encontrar el archivo", mensaje)
    except OSError as mensaje:
        print("No se pudo abrir el archivo", mensaje)
    finally:
        try:
            archivo.close()
            salida.close()
        except OSError as mensaje:
            print("No se pudo cerrar el archivo", mensaje)
        except NameError as mensaje:
            print("No se pudo cerrar el archivo ya que no existe", mensaje)

    if encontrado: #reemplazo del archivo original por el temporal
        os.replace("pedidostemp.txt", "pedidos.txt")
    else: #elimina el archivo temporal si no se encuentra ninguna coincidencia
        os.remove("pedidostemp.txt")
        print("❌ No se encontró un pedido con ese código.")

    repetir = preguntar_continuar() 
    if repetir:
        try:
            devoluciones() #se utiliza recursividad para volver a entrar al menu de devoluciones
        except RecursionError as e:
            print(f"Maximo de operaciones alcanzadas en Devoluciones {e}") #manejo de error en caso de muchas devoluciones

#-----------------------------------------------------
#PROGRAMA PRINCIPAL
#-----------------------------------------------------

#inicializacion del contador de envíos "n"
while True:
    try:
        archivo = open("pedidos.txt", "rt")
        try:
            ultima_linea = ""
            for linea in archivo:
                linea_limpia = linea.strip()
                if linea_limpia != "":
                    ultima_linea = linea_limpia
            
            if ultima_linea == "":
                n = 0  # no hay pedidos
            else:
                campos = ultima_linea.split(";")
                n = int(campos[0])  # tomar el ultimo indice de envío
        finally:
            try:
                archivo.close()
            except OSError:
                pass
        break

    except FileNotFoundError: #si no se encuentra el archivo, se crea uno y se cierra para poder usar el programa
        try:
            archivo = open("pedidos.txt", "wt")
            try:
                print()
                print("-" * 100)
                print("Archivo creado como pedidos.txt")
                print("-" * 100)
            finally:
                try:
                    archivo.close()
                except OSError:
                    pass
            n = 0
        except OSError as mensaje:
            print("No se puede leer el archivo:", mensaje)
            n = 0
        continue
    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)
        n = 0

# --------------
# MENU PRINCIPAL
# --------------

archivo_verificado = False
archivo_tiene_datos = False

while True:
    print("\n📦 --- Sistema de Envíos ---")
    print("\n1️⃣  Crear envío")
    print("2️⃣  Consultar envío")
    print("3️⃣  Listar los envíos")
    print("4️⃣  Cambiar estado de un envío")
    print("5️⃣  Realizar devolución del cliente")
    print("0️⃣  Salir")

    opcion = input("\nEscoja una opción: ")
    print()
    opcion = validar_opciones(opcion, 0, 5)

    if opcion in [2, 3, 4, 5]: #cualquier opcion que no sea agregar pedido o salir
        if not archivo_verificado:
            try:
                archivo = open("pedidos.txt", "rt")
                try:
                    archivo_tiene_datos = False
                    for linea in archivo:
                        if linea.strip() != "":
                            archivo_tiene_datos = True
                            break
                finally:
                    try:
                        archivo.close()
                        archivo_verificado = True
                    except OSError:
                        pass
            except (FileNotFoundError, OSError) as mensaje:
                print("\nNo se pudo abrir el archivo:", mensaje)
                archivo_tiene_datos = False

        if not archivo_tiene_datos: # Se debe primero crear un pedido para usar el resto de funciones
            print("\n⚠️  No hay ningún pedido en el archivo para usar esta función, cree uno primero.\n")
            continue

# SE LLAMAN A TODAS LAS FUNCIONES PARA CARGAR LOS DISTINTOS MENUS

    match opcion:
        case 0:
            print("Nos vemos! 👋")
            break
        case 1:
            n = agregar_envio(n)
            archivo_verificado = False  # se invalida la verificación
        case 2:
            consultar_envio()
        case 3:
            historial_envios()
        case 4:
            cambiar_estado()
        case 5:
            devoluciones()

