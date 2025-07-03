# modelo/Recepcionista.py
from modelo.conexion_bd import db_connection

class Recepcionista:
    def __init__(self, cedula, nombre, apellido, numero_documento, telefono="", email="", 
                 turno="Mañana", fecha_contratacion=None, activo=True):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.numero_documento = numero_documento
        self.telefono = telefono
        self.email = email
        self.turno = turno  # Mañana, Tarde, Noche
        self.fecha_contratacion = fecha_contratacion
        self.activo = activo

    def nombre_completo(self):
        """Retorna el nombre completo del recepcionista"""
        return f"{self.nombre} {self.apellido}"

    def to_dict(self):
        """Convierte el recepcionista a diccionario"""
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "nombre_completo": self.nombre_completo(),
            "numero_documento": self.numero_documento,
            "telefono": self.telefono,
            "email": self.email,
            "turno": self.turno,
            "fecha_contratacion": self.fecha_contratacion,
            "activo": self.activo
        }

class Modelo_recepcionista:
    """Modelo para manejar operaciones CRUD de recepcionistas con la base de datos"""
    
    @staticmethod
    def obtener_todos_los_recepcionistas():
        """Retorna todos los recepcionistas desde la base de datos"""
        query = """
            SELECT cedula, nombre, apellido, numero_documento, telefono, email, 
                   turno, fecha_contratacion
            FROM recepcionistas
            ORDER BY apellido, nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        recepcionistas = []
        
        if resultado:
            for recep_data in resultado:
                recepcionista = Recepcionista(
                    cedula=recep_data[0],
                    nombre=recep_data[1],
                    apellido=recep_data[2],
                    numero_documento=recep_data[3],
                    telefono=recep_data[4] or "",
                    email=recep_data[5] or "",
                    turno=recep_data[6] or "Mañana",
                    fecha_contratacion=recep_data[7]
                )
                recepcionistas.append(recepcionista)
        
        return recepcionistas

    @staticmethod
    def obtener_recepcionista_por_cedula(cedula):
        """Obtiene un recepcionista específico por su cédula"""
        query = """
            SELECT cedula, nombre, apellido, numero_documento, telefono, email, 
                   turno, fecha_contratacion
            FROM recepcionistas
            WHERE cedula = %s;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (cedula,))
        
        if resultado and len(resultado) > 0:
            recep_data = resultado[0]
            return Recepcionista(
                cedula=recep_data[0],
                nombre=recep_data[1],
                apellido=recep_data[2],
                numero_documento=recep_data[3],
                telefono=recep_data[4] or "",
                email=recep_data[5] or "",
                turno=recep_data[6] or "Mañana",
                fecha_contratacion=recep_data[7]
            )
        return None

    @staticmethod
    def obtener_recepcionistas_por_turno(turno):
        """Obtiene recepcionistas filtrados por turno"""
        query = """
            SELECT cedula, nombre, apellido, numero_documento, telefono, email, 
                   turno, fecha_contratacion
            FROM recepcionistas
            WHERE turno = %s
            ORDER BY apellido, nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (turno,))
        recepcionistas = []
        
        if resultado:
            for recep_data in resultado:
                recepcionista = Recepcionista(
                    cedula=recep_data[0],
                    nombre=recep_data[1],
                    apellido=recep_data[2],
                    numero_documento=recep_data[3],
                    telefono=recep_data[4] or "",
                    email=recep_data[5] or "",
                    turno=recep_data[6] or "Mañana",
                    fecha_contratacion=recep_data[7]
                )
                recepcionistas.append(recepcionista)
        
        return recepcionistas

    @staticmethod
    def agregar_recepcionista(datos_recepcionista):
        """Agrega un nuevo recepcionista a la base de datos"""
        try:
            # Verificar que no exista ya un recepcionista con esa cédula
            if Modelo_recepcionista.obtener_recepcionista_por_cedula(datos_recepcionista.get("cedula")):
                print("❌ Ya existe un recepcionista con esa cédula")
                return False
            
            query = """
                INSERT INTO recepcionistas (cedula, nombre, apellido, numero_documento, 
                                          telefono, email, turno, fecha_contratacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            params = (
                datos_recepcionista.get("cedula", ""),
                datos_recepcionista.get("nombre", ""),
                datos_recepcionista.get("apellido", ""),
                datos_recepcionista.get("numero_documento", ""),
                datos_recepcionista.get("telefono", ""),
                datos_recepcionista.get("email", ""),
                datos_recepcionista.get("turno", "Mañana"),
                datos_recepcionista.get("fecha_contratacion", None)
            )
            
            filas_afectadas = db_connection.ejecutar_insercion(query, params)
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Recepcionista registrado exitosamente: {datos_recepcionista['cedula']}")
                return True
            else:
                print("❌ No se pudo registrar el recepcionista")
                return False
                
        except Exception as e:
            print(f"❌ Error al agregar recepcionista: {e}")
            return False

    @staticmethod
    def actualizar_recepcionista(cedula, datos_actualizados):
        """Actualiza los datos de un recepcionista existente"""
        try:
            # Verificar que el recepcionista existe
            recepcionista_existente = Modelo_recepcionista.obtener_recepcionista_por_cedula(cedula)
            if not recepcionista_existente:
                print(f"❌ No se encontró el recepcionista con cédula: {cedula}")
                return False

            # Crear consulta dinámica solo con los campos que se van a actualizar
            campos_actualizables = ['nombre', 'apellido', 'numero_documento', 'telefono', 
                                  'email', 'turno', 'fecha_contratacion']
            
            campos_a_actualizar = []
            valores = []
            
            for campo in campos_actualizables:
                if campo in datos_actualizados:
                    campos_a_actualizar.append(f"{campo} = %s")
                    valores.append(datos_actualizados[campo])
            
            if not campos_a_actualizar:
                print("❌ No hay campos para actualizar")
                return False
            
            # Agregar la cédula al final para el WHERE
            valores.append(cedula)
            
            query = f"""
                UPDATE recepcionistas 
                SET {', '.join(campos_a_actualizar)}
                WHERE cedula = %s;
            """
            
            filas_afectadas = db_connection.ejecutar_actualizacion(query, tuple(valores))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Recepcionista actualizado exitosamente: {cedula}")
                return True
            else:
                print(f"❌ No se pudo actualizar el recepcionista: {cedula}")
                return False
                
        except Exception as e:
            print(f"❌ Error al actualizar recepcionista: {e}")
            return False

    def _generar_recepcionistas_ejemplo(self):
        """Genera recepcionistas de ejemplo"""
        recepcionistas_data = [
            ("REC001", "Laura", "Martínez", "555-0301", "laura.martinez@hospital.com"),
            ("REC002", "Carlos", "Jiménez", "555-0302", "carlos.jimenez@hospital.com"),
            ("REC003", "Patricia", "Morales", "555-0303", "patricia.morales@hospital.com"),
        ]

        for data in recepcionistas_data:
            recepcionista = Recepcionista(*data)
            self.recepcionistas.append(recepcionista)

    def obtener_todos_los_recepcionistas(self):
        """Retorna todos los recepcionistas"""
        return self.recepcionistas

    def obtener_recepcionista_por_id(self, id_recepcionista):
        """Busca un recepcionista por su ID"""
        for recepcionista in self.recepcionistas:
            if recepcionista.id_recepcionista == id_recepcionista:
                return recepcionista
        return None

    # ===================================================================
    # MÉTODOS ESPECÍFICOS PARA FUNCIONALIDADES DE RECEPCIONISTA CON BD
    # ===================================================================
    
    @staticmethod
    @staticmethod
    def obtener_citas_del_dia_bd(fecha=None):
        """Obtiene las citas del día desde la base de datos"""
        from datetime import date
        
        if fecha is None:
            fecha = date.today()
            
        query = """
            SELECT c.id_cita, c.cedula_paciente, c.id_medico, c.id_tipo_consulta,
                   c.fecha, c.hora, c.estado, c.total_neto,
                   p.nombre as nombre_paciente, p.apellido as apellido_paciente,
                   m.nombre as nombre_medico, m.apellido as apellido_medico,
                   tc.nombre as tipo_consulta
            FROM citas c
            INNER JOIN pacientes p ON c.cedula_paciente = p.cedula
            INNER JOIN medicos m ON c.id_medico = m.id_medico
            INNER JOIN tipos_consulta tc ON c.id_tipo_consulta = tc.id_tipo_consulta
            WHERE c.fecha = %s
            ORDER BY c.hora;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (fecha,))
        citas = []
        
        if resultado:
            for cita_data in resultado:
                citas.append({
                    "id_cita": cita_data[0],
                    "cedula_paciente": cita_data[1],
                    "id_medico": cita_data[2],
                    "fecha": cita_data[4],
                    "hora": cita_data[5],
                    "estado": cita_data[6],
                    "total": float(cita_data[7]) if cita_data[7] else 0.0,
                    "paciente": f"{cita_data[8]} {cita_data[9]}",
                    "medico": f"{cita_data[10]} {cita_data[11]}",
                    "tipo_consulta": cita_data[12]
                })
        
        return citas
    
    @staticmethod
    @staticmethod
    def registrar_llegada_paciente_bd(id_cita, cedula_paciente=None):
        """Registra la llegada de un paciente actualizando el estado de su cita a 'Confirmada'"""
        try:
            print(f"🔍 DEBUG: Registrando llegada para cita ID: {id_cita}, cédula: {cedula_paciente}")
            
            # Verificar que la cita existe y está en estado 'Pendiente'
            query_buscar = """
                SELECT id_cita, cedula_paciente, estado, fecha, hora
                FROM citas 
                WHERE id_cita = %s 
                AND estado = 'Pendiente';
            """
            
            resultado = db_connection.ejecutar_consulta(query_buscar, (id_cita,))
            
            if resultado and len(resultado) > 0:
                cita_data = resultado[0]
                cedula_encontrada = cita_data[1]
                estado_actual = cita_data[2]
                
                # Validar cédula si se proporciona
                if cedula_paciente and cedula_paciente != cedula_encontrada:
                    print(f"❌ DEBUG: Cédula no coincide. Esperada: {cedula_paciente}, Encontrada: {cedula_encontrada}")
                    return {
                        "exito": False,
                        "mensaje": "La cédula del paciente no coincide con la cita seleccionada."
                    }
                
                print(f"🔍 DEBUG: Cita encontrada - Paciente: {cedula_encontrada}, Estado actual: {estado_actual}")
                
                # Actualizar estado a 'Confirmada' (llegada registrada)
                query_update = """
                    UPDATE citas 
                    SET estado = 'Confirmada',
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE id_cita = %s;
                """
                
                filas_afectadas = db_connection.ejecutar_actualizacion(query_update, (id_cita,))
                
                if filas_afectadas and filas_afectadas > 0:
                    print(f"✅ DEBUG: Estado de cita {id_cita} actualizado a 'Confirmada'")
                    return {
                        "exito": True,
                        "mensaje": "Llegada registrada exitosamente. Estado de cita actualizado a 'Confirmada'.",
                        "id_cita": id_cita,
                        "cedula_paciente": cedula_paciente
                    }
                else:
                    print(f"❌ DEBUG: No se pudo actualizar el estado de la cita {id_cita}")
                    return {
                        "exito": False,
                        "mensaje": "Error al actualizar el estado de la cita"
                    }
            else:
                print(f"❌ DEBUG: No se encontró cita pendiente con ID {id_cita}")
                return {
                    "exito": False,
                    "mensaje": "No se encontró una cita pendiente con ese ID"
                }
                
        except Exception as e:
            print(f"❌ Error registrando llegada: {e}")
            return {
                "exito": False,
                "mensaje": f"Error interno: {str(e)}"
            }
            
            return {"exito": False, "mensaje": "No se encontró cita pendiente para hoy"}
            
        except Exception as e:
            print(f"❌ Error al registrar llegada: {e}")
            return {"exito": False, "mensaje": f"Error: {str(e)}"}
    
    @staticmethod
    @staticmethod
    def procesar_atencion_sin_cita_bd(datos_atencion):
        """Procesa una atención sin cita previa creando paciente, cita y factura"""
        try:
            from datetime import date, datetime, time
            import random
            
            print(f"🔍 DEBUG Modelo: Procesando atención sin cita para {datos_atencion.get('nombre_paciente')}")
            
            # 1. VERIFICAR/REGISTRAR PACIENTE
            cedula = datos_atencion.get("cedula_paciente")
            nombre_completo = datos_atencion.get("nombre_paciente", "")
            
            # Separar nombre y apellido (simplificado)
            nombres = nombre_completo.split()
            nombre = nombres[0] if nombres else "Sin Nombre"
            apellido = " ".join(nombres[1:]) if len(nombres) > 1 else "Sin Apellido"
            
            # Verificar si el paciente ya existe
            query_verificar = "SELECT cedula FROM pacientes WHERE cedula = %s;"
            resultado_paciente = db_connection.ejecutar_consulta(query_verificar, (cedula,))
            
            if not resultado_paciente:
                # Primero verificar si existe como usuario
                query_usuario_existe = "SELECT id_usuario FROM usuarios WHERE id_usuario = %s;"
                resultado_usuario = db_connection.ejecutar_consulta(query_usuario_existe, (cedula,))
                
                if not resultado_usuario:
                    # Registrar nuevo usuario primero
                    print(f"📝 DEBUG Modelo: Registrando nuevo usuario - {cedula}")
                    query_usuario = """
                        INSERT INTO usuarios (id_usuario, contrasena, rol)
                        VALUES (%s, %s, %s);
                    """
                    
                    # Generar contraseña temporal (puede ser la cédula)
                    contrasena_temporal = cedula  # Se puede cambiar después
                    rol = 'Paciente'
                    
                    params_usuario = (cedula, contrasena_temporal, rol)
                    
                    filas_usuario = db_connection.ejecutar_insercion(query_usuario, params_usuario)
                    if filas_usuario <= 0:
                        return {"exito": False, "mensaje": "No se pudo registrar el usuario"}
                    
                    print(f"✅ DEBUG Modelo: Usuario registrado exitosamente")
                
                # Registrar nuevo paciente
                print(f"📝 DEBUG Modelo: Registrando nuevo paciente - {nombre} {apellido}")
                query_paciente = """
                    INSERT INTO pacientes (cedula, nombre, apellido, correo, telefono, fecha_nacimiento, genero, categoria_paciente, deuda, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                
                # Datos aleatorios para campos requeridos según estructura real
                telefono = datos_atencion.get("telefono_paciente", f"300{random.randint(1000000, 9999999)}")
                correo = f"{nombre.lower()}.{apellido.lower()}@email.com"
                fecha_nacimiento = date(random.randint(1960, 2000), random.randint(1, 12), random.randint(1, 28))
                genero = random.choice(['Masculino', 'Femenino', 'Otro'])
                categoria_paciente = 'CAT002'  # Valor por defecto
                deuda = 0.00
                activo = True
                
                params_paciente = (cedula, nombre, apellido, correo, telefono, fecha_nacimiento, genero, categoria_paciente, deuda, activo)
                
                filas_paciente = db_connection.ejecutar_insercion(query_paciente, params_paciente)
                if filas_paciente <= 0:
                    return {"exito": False, "mensaje": "No se pudo registrar el paciente"}
                
                print(f"✅ DEBUG Modelo: Paciente registrado exitosamente")
            else:
                print(f"ℹ️ DEBUG Modelo: Paciente ya existe en el sistema")
            
            # 2. CREAR CITA DE URGENCIA
            print(f"📝 DEBUG Modelo: Creando cita de urgencia...")
            
            query_cita = """
                INSERT INTO citas (cedula_paciente, id_medico, id_tipo_consulta, id_aseguradora,
                                 fecha, hora, estado, costo_consulta, descuento_aplicado, 
                                 costo_servicios_adicionales, total_neto, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_cita;
            """
            
            # Datos de la cita
            fecha_cita = date.today()
            hora_cita = datetime.now().time()
            id_medico = datos_atencion.get("id_medico")
            id_tipo_consulta = "TC003"  # Urgencias (según tabla tipos_consulta)
            id_aseguradora = None  # Sin aseguradora para urgencias
            estado = "Confirmada"  # Estado para atención inmediata
            costo_consulta = 75000.00  # Costo estándar de urgencia
            descuento = 0.00
            costo_servicios = 0.00
            total_neto = costo_consulta
            observaciones = f"Atención sin cita previa - {datos_atencion.get('tipo_atencion', 'Urgencia')}"
            
            params_cita = (
                cedula, id_medico, id_tipo_consulta, id_aseguradora,
                fecha_cita, hora_cita, estado, costo_consulta, descuento,
                costo_servicios, total_neto, observaciones
            )
            
            resultado_cita = db_connection.ejecutar_consulta(query_cita, params_cita)
            
            if not resultado_cita or len(resultado_cita) == 0:
                return {"exito": False, "mensaje": "No se pudo crear la cita"}
            
            id_cita = resultado_cita[0][0]  # RETURNING id_cita
            print(f"✅ DEBUG Modelo: Cita creada con ID: {id_cita}")
            
            # 3. CREAR FACTURA AUTOMÁTICAMENTE
            print(f"📝 DEBUG Modelo: Creando factura para la cita...")
            
            query_factura = """
                INSERT INTO facturas (numero_factura, id_cita, cedula_paciente, fecha_emision,
                                    subtotal_consulta, subtotal_servicios, descuentos_aplicados, 
                                    total_bruto, total_neto, estado, metodo_pago, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_factura;
            """
            
            # Datos de la factura según estructura real
            numero_factura = f"FAC-{date.today().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            fecha_emision = datetime.now()
            subtotal_consulta = costo_consulta  # 75000.00
            subtotal_servicios = 0.00  # Sin servicios adicionales
            descuentos_aplicados = 0.00  # Sin descuentos
            total_bruto = subtotal_consulta + subtotal_servicios - descuentos_aplicados
            total_neto = total_bruto  # Sin impuestos adicionales en este caso
            estado_factura = "Pendiente"  # Estado inicial
            metodo_pago_factura = "Efectivo"  # Método por defecto
            observaciones_factura = f"Factura atención sin cita - Cita ID: {id_cita} - Urgencia"
            
            params_factura = (
                numero_factura, id_cita, cedula, fecha_emision,
                subtotal_consulta, subtotal_servicios, descuentos_aplicados,
                total_bruto, total_neto, estado_factura, metodo_pago_factura, observaciones_factura
            )
            
            resultado_factura = db_connection.ejecutar_consulta(query_factura, params_factura)
            
            if not resultado_factura or len(resultado_factura) == 0:
                print("⚠️ DEBUG Modelo: No se pudo crear la factura, pero la cita se creó")
                return {
                    "exito": True,
                    "mensaje": f"Atención sin cita registrada exitosamente. Cita ID: {id_cita}. (Factura pendiente)"
                }
            
            id_factura = resultado_factura[0][0]
            print(f"✅ DEBUG Modelo: Factura creada con ID: {id_factura}, Número: {numero_factura}")
            
            return {
                "exito": True,
                "mensaje": f"Atención sin cita registrada exitosamente.\nCita ID: {id_cita}\nFactura: {numero_factura}",
                "id_cita": id_cita,
                "numero_factura": numero_factura,
                "id_factura": id_factura
            }
                
        except Exception as e:
            print(f"❌ Error al procesar atención sin cita: {e}")
            import traceback
            traceback.print_exc()
            return {"exito": False, "mensaje": f"Error: {str(e)}"}
    
    @staticmethod
    def obtener_pacientes_en_espera_bd():
        """Obtiene los pacientes que están en espera (con citas En_Proceso)"""
        from datetime import date
        
        query = """
            SELECT c.id_cita, c.cedula_paciente, c.hora,
                   p.nombre, p.apellido, p.telefono,
                   m.nombre as nombre_medico, m.apellido as apellido_medico,
                   tc.nombre as tipo_consulta
            FROM citas c
            INNER JOIN pacientes p ON c.cedula_paciente = p.cedula
            INNER JOIN medicos m ON c.id_medico = m.id_medico
            INNER JOIN tipos_consulta tc ON c.id_tipo_consulta = tc.id_tipo_consulta
            WHERE c.fecha = %s 
            AND c.estado = 'En_Proceso'
            ORDER BY c.hora;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (date.today(),))
        pacientes_espera = []
        
        if resultado:
            for paciente_data in resultado:
                pacientes_espera.append({
                    "id_cita": paciente_data[0],
                    "cedula": paciente_data[1],
                    "hora_cita": paciente_data[2],
                    "nombre": f"{paciente_data[3]} {paciente_data[4]}",
                    "telefono": paciente_data[5],
                    "medico": f"{paciente_data[6]} {paciente_data[7]}",
                    "tipo_consulta": paciente_data[8]
                })
        
        return pacientes_espera
    
    @staticmethod
    def obtener_estadisticas_diarias_bd(fecha=None):
        """Obtiene estadísticas del día desde la base de datos"""
        from datetime import date
        
        if fecha is None:
            fecha = date.today()
            
        query = """
            SELECT 
                COUNT(*) as total_citas,
                COUNT(CASE WHEN estado = 'Completada' THEN 1 END) as completadas,
                COUNT(CASE WHEN estado = 'En_Proceso' THEN 1 END) as en_proceso,
                COUNT(CASE WHEN estado IN ('Pendiente', 'Confirmada') THEN 1 END) as pendientes,
                COUNT(CASE WHEN estado = 'Cancelada' THEN 1 END) as canceladas,
                COALESCE(SUM(total_neto), 0) as ingresos_dia
            FROM citas
            WHERE fecha = %s;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (fecha,))
        
        if resultado and len(resultado) > 0:
            stats = resultado[0]
            return {
                "fecha": fecha,
                "total_citas": stats[0],
                "completadas": stats[1],
                "en_proceso": stats[2],
                "pendientes": stats[3],
                "canceladas": stats[4],
                "ingresos_dia": float(stats[5]) if stats[5] else 0.0
            }
        
        return {
            "fecha": fecha,
            "total_citas": 0,
            "completadas": 0,
            "en_proceso": 0,
            "pendientes": 0,
            "canceladas": 0,
            "ingresos_dia": 0.0
        }