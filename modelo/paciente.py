# modelo/paciente.py
from modelo.conexion_bd import db_connection
from datetime import datetime

class Paciente:
    def __init__(self, nombre="", apellido="", cedula="", telefono="", email="", 
                 fecha_nacimiento=None, genero="", categoria_paciente="CAT002"):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.telefono = telefono
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero  # Agregado campo genero
        self.categoria_paciente = categoria_paciente  # CAT001: Afiliado, CAT002: Particular, CAT003: Convenio
        self.deuda = 0.0
        self.activo = True
        
    def nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        return f"{self.nombre} {self.apellido}"

    def obtener_citas(self):
        """Obtiene las citas del paciente desde la base de datos con información completa"""
        try:
            print(f"🔍 DEBUG: Obteniendo citas para paciente {self.cedula}")
            
            # Importar aquí para evitar importaciones circulares
            from modelo.cita import Modelo_citas
            from modelo.medico import Modelo_medicos
            from modelo.catalogos import Modelo_catalogos
            
            # Obtener citas del paciente desde la BD
            citas_bd = Modelo_citas.obtener_citas_por_paciente(self.cedula)
            print(f"🔍 DEBUG: Se encontraron {len(citas_bd) if citas_bd else 0} citas en BD")
            
            if not citas_bd:
                print(f"⚠️ DEBUG: No hay citas para el paciente {self.cedula}")
                return []
            
            # Convertir a formato que espera la vista
            citas_formateadas = []
            
            for i, cita in enumerate(citas_bd):
                print(f"🔍 DEBUG: Procesando cita {i+1}: ID={cita.id_cita}, Médico={cita.id_medico}")
                try:
                    # Obtener información del médico
                    medico = Modelo_medicos.obtener_medico_por_id(cita.id_medico)
                    nombre_medico = f"Dr. {medico.nombre} {medico.apellido}" if medico else f"Médico #{cita.id_medico}"
                    
                    # Obtener tipo de consulta
                    tipo_consulta = Modelo_catalogos.obtener_tipo_consulta_por_id(cita.id_tipo_consulta)
                    tipo_consulta_nombre = tipo_consulta.get('nombre', 'Consulta General') if tipo_consulta else 'Consulta General'
                    
                    # Formatear fecha y hora
                    fecha_str = cita.fecha.strftime("%Y-%m-%d") if hasattr(cita.fecha, 'strftime') else str(cita.fecha)
                    hora_str = str(cita.hora)
                    
                    # Calcular costo total
                    costo_total = cita.total_neto if cita.total_neto > 0 else cita.costo_consulta
                    
                    cita_formateada = {
                        "id_cita": cita.id_cita,
                        "fecha": fecha_str,
                        "hora": hora_str,
                        "estado": cita.estado,
                        "tipo": tipo_consulta_nombre,
                        "costo": float(costo_total),
                        "doctor": nombre_medico,
                        "observaciones": cita.observaciones or ""
                    }
                    
                    citas_formateadas.append(cita_formateada)
                    
                except Exception as e:
                    print(f"⚠️ Error procesando cita {cita.id_cita}: {e}")
                    # Agregar cita con datos básicos si hay error
                    citas_formateadas.append({
                        "id_cita": cita.id_cita,
                        "fecha": str(cita.fecha),
                        "hora": str(cita.hora),
                        "estado": cita.estado,
                        "tipo": "Consulta",
                        "costo": float(cita.costo_consulta),
                        "doctor": f"Médico #{cita.id_medico}",
                        "observaciones": ""
                    })
            
            return citas_formateadas
            
        except Exception as e:
            print(f"❌ Error al obtener citas del paciente {self.cedula}: {e}")
            return []

    def calcular_deuda_actual(self):
        """Calcula la deuda actual del paciente desde facturas pendientes"""
        try:
            print(f"🔍 DEBUG: Calculando deuda actual para paciente {self.cedula}")
            
            # Calcular deuda real desde facturas pendientes/vencidas
            query = """
                SELECT COALESCE(SUM(total_neto), 0) as deuda_total
                FROM facturas 
                WHERE cedula_paciente = %s 
                AND estado IN ('Pendiente', 'Vencida');
            """
            
            resultado = db_connection.ejecutar_consulta(query, (self.cedula,))
            
            if resultado and len(resultado) > 0:
                self.deuda = float(resultado[0][0]) if resultado[0][0] else 0.0
                print(f"🔍 DEBUG: Deuda desde facturas: ${self.deuda:.2f}")
            else:
                self.deuda = 0.0
                print(f"🔍 DEBUG: No hay facturas pendientes, deuda = $0.00")
            
            return self.deuda
            
        except Exception as e:
            print(f"❌ Error al calcular deuda del paciente {self.cedula}: {e}")
            self.deuda = 0.0
            return self.deuda

    def obtener_deuda_detallada(self):
        """Obtiene un desglose detallado de la deuda del paciente desde facturas pendientes"""
        try:
            print(f"🔍 DEBUG: Obteniendo deuda detallada para paciente {self.cedula}")
            
            # Inicializar desglose
            desglose = {
                "total": 0.0,
                "deuda_citas": 0.0,
                "deuda_servicios": 0.0,
                "citas_pendientes": [],
                "servicios_pendientes": []
            }
            
            # FUENTE PRINCIPAL: Obtener facturas pendientes/vencidas desde tabla facturas
            query_facturas = """
                SELECT f.id_factura, f.numero_factura, f.id_cita, f.fecha_emision,
                       f.subtotal_consulta, f.subtotal_servicios, f.total_neto, f.estado,
                       c.fecha as fecha_cita, c.hora as hora_cita, tc.nombre as tipo_consulta
                FROM facturas f
                INNER JOIN citas c ON f.id_cita = c.id_cita
                LEFT JOIN tipos_consulta tc ON c.id_tipo_consulta = tc.id_tipo_consulta
                WHERE f.cedula_paciente = %s 
                AND f.estado IN ('Pendiente', 'Vencida')
                ORDER BY f.fecha_emision DESC;
            """
            
            resultado_facturas = db_connection.ejecutar_consulta(query_facturas, (self.cedula,))
            print(f"🔍 DEBUG: Se encontraron {len(resultado_facturas) if resultado_facturas else 0} facturas pendientes")
            
            if resultado_facturas:
                # Hay facturas pendientes - calcular deuda real
                for factura_data in resultado_facturas:
                    subtotal_consulta = float(factura_data[4]) if factura_data[4] else 0.0
                    subtotal_servicios = float(factura_data[5]) if factura_data[5] else 0.0
                    total_neto = float(factura_data[6]) if factura_data[6] else 0.0
                    
                    desglose["deuda_citas"] += subtotal_consulta
                    desglose["deuda_servicios"] += subtotal_servicios
                    desglose["total"] += total_neto
                    
                    desglose["citas_pendientes"].append({
                        "id_factura": factura_data[0],
                        "numero_factura": factura_data[1],
                        "id_cita": factura_data[2],
                        "fecha": str(factura_data[8]),  # fecha_cita
                        "hora": str(factura_data[9]),   # hora_cita
                        "costo": total_neto,
                        "tipo": factura_data[10] or "Consulta",
                        "estado": f"Factura {factura_data[7]}"
                    })
                
                print(f"🔍 DEBUG: Deuda real desde facturas - Citas: ${desglose['deuda_citas']:.2f}, Servicios: ${desglose['deuda_servicios']:.2f}, Total: ${desglose['total']:.2f}")
                
            else:
                # No hay facturas pendientes - verificar citas completadas sin facturar
                print(f"🔍 DEBUG: No hay facturas pendientes, verificando citas sin facturar")
                
                query_citas_sin_factura = """
                    SELECT c.id_cita, c.fecha, c.hora, c.costo_consulta, 
                           c.costo_servicios_adicionales, c.total_neto, c.estado,
                           tc.nombre as tipo_consulta
                    FROM citas c
                    LEFT JOIN tipos_consulta tc ON c.id_tipo_consulta = tc.id_tipo_consulta
                    LEFT JOIN facturas f ON c.id_cita = f.id_cita
                    WHERE c.cedula_paciente = %s 
                    AND c.estado IN ('Confirmada', 'Completada', 'En_Proceso')
                    AND f.id_factura IS NULL
                    AND c.total_neto > 0
                    ORDER BY c.fecha DESC;
                """
                
                resultado_citas = db_connection.ejecutar_consulta(query_citas_sin_factura, (self.cedula,))
                print(f"🔍 DEBUG: Se encontraron {len(resultado_citas) if resultado_citas else 0} citas sin facturar")
                
                if resultado_citas:
                    for cita_data in resultado_citas:
                        costo_consulta = float(cita_data[3]) if cita_data[3] else 0.0
                        costo_servicios = float(cita_data[4]) if cita_data[4] else 0.0
                        total_neto = float(cita_data[5]) if cita_data[5] else 0.0
                        
                        # Usar total_neto si está disponible, sino sumar componentes
                        costo_total = total_neto if total_neto > 0 else (costo_consulta + costo_servicios)
                        
                        desglose["deuda_citas"] += costo_consulta
                        desglose["deuda_servicios"] += costo_servicios
                        desglose["total"] += costo_total
                        
                        desglose["citas_pendientes"].append({
                            "id_cita": cita_data[0],
                            "fecha": str(cita_data[1]),
                            "hora": str(cita_data[2]),
                            "costo": costo_total,
                            "tipo": cita_data[7] or "Consulta",
                            "estado": f"{cita_data[6]} (Sin facturar)"
                        })
                
                print(f"🔍 DEBUG: Deuda estimada desde citas - Total: ${desglose['total']:.2f}")
            
            # Actualizar campo deuda en tabla pacientes para mantener sincronización
            if desglose["total"] != self.deuda:
                try:
                    query_update = "UPDATE pacientes SET deuda = %s WHERE cedula = %s;"
                    db_connection.ejecutar_actualizacion(query_update, (desglose["total"], self.cedula))
                    self.deuda = desglose["total"]
                    print(f"🔍 DEBUG: Campo deuda actualizado en tabla pacientes: ${desglose['total']:.2f}")
                except Exception as e:
                    print(f"⚠️ DEBUG: Error al actualizar campo deuda: {e}")
            
            return desglose
            
        except Exception as e:
            print(f"❌ Error al obtener deuda detallada del paciente {self.cedula}: {e}")
            import traceback
            traceback.print_exc()
            return {
                "total": 0.0,
                "deuda_citas": 0.0,
                "deuda_servicios": 0.0,
                "citas_pendientes": [],
                "servicios_pendientes": []
            }

    def pagar_deuda(self, monto):
        """Procesa un pago parcial o total de la deuda del paciente"""
        try:
            if monto <= 0:
                return False
            
            # Calcular deuda actual
            deuda_actual = self.calcular_deuda_actual()
            
            if deuda_actual <= 0:
                print("El paciente no tiene deuda pendiente")
                return False
            
            # Calcular nueva deuda
            nueva_deuda = max(0, deuda_actual - monto)
            
            # Actualizar en la base de datos
            query = "UPDATE pacientes SET deuda = %s WHERE cedula = %s;"
            filas_afectadas = db_connection.ejecutar_actualizacion(query, (nueva_deuda, self.cedula))
            
            if filas_afectadas and filas_afectadas > 0:
                self.deuda = nueva_deuda
                print(f"✅ Pago procesado. Deuda anterior: ${deuda_actual:.2f}, Pago: ${monto:.2f}, Nueva deuda: ${nueva_deuda:.2f}")
                return True
            else:
                print("❌ No se pudo procesar el pago")
                return False
                
        except Exception as e:
            print(f"❌ Error al procesar pago: {e}")
            return False

    def agregar_cita(self, cita_data):
        """Método de compatibilidad - agrega una cita al paciente"""
        # Este método se mantiene para compatibilidad, pero las citas se manejan en Modelo_citas
        try:
            print(f"✅ Cita agregada al paciente {self.nombre_completo()}: {cita_data.get('tipo', 'Consulta')}")
            # Actualizar deuda si la cita tiene costo
            if 'costo' in cita_data and cita_data['costo'] > 0:
                nueva_deuda = self.deuda + cita_data['costo']
                query = "UPDATE pacientes SET deuda = %s WHERE cedula = %s;"
                db_connection.ejecutar_actualizacion(query, (nueva_deuda, self.cedula))
                self.deuda = nueva_deuda
            return True
        except Exception as e:
            print(f"❌ Error al agregar cita: {e}")
            return False

    def simular_citas(self):
        """Método de compatibilidad mejorado - verifica si ya tiene citas reales"""
        try:
            # Verificar si ya tiene citas en la BD
            citas_reales = self.obtener_citas()
            
            if citas_reales:
                print(f"✅ Paciente {self.nombre_completo()} tiene {len(citas_reales)} citas en la BD")
                return
            
            print(f"📋 Paciente {self.nombre_completo()} no tiene citas registradas en la BD")
            print("💡 Para agregar citas, use el sistema de agendamiento o inserte datos en la tabla 'citas'")
            
        except Exception as e:
            print(f"⚠️ Error verificando citas: {e}")
    
    def to_dict(self):
        """Convierte el paciente a diccionario"""
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "nombre_completo": self.nombre_completo(),
            "telefono": self.telefono,
            "email": self.email,  # correo en BD
            "fecha_nacimiento": self.fecha_nacimiento,
            "genero": self.genero,  # Agregado campo genero
            "categoria_paciente": self.categoria_paciente,
            "deuda": self.deuda,
            "activo": self.activo
        }

class Modelo_pacientes:
    """Modelo para manejar operaciones CRUD de pacientes"""
    
    @staticmethod
    def obtener_todos_los_pacientes():
        """Retorna todos los pacientes desde la base de datos"""
        query = """
            SELECT cedula, nombre, apellido, telefono, correo, 
                   fecha_nacimiento, genero, categoria_paciente, deuda, activo
            FROM pacientes 
            ORDER BY apellido, nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        pacientes = []
        
        if resultado:
            for paciente_data in resultado:
                paciente = Paciente(
                    cedula=paciente_data[0],
                    nombre=paciente_data[1],
                    apellido=paciente_data[2],
                    telefono=paciente_data[3],
                    email=paciente_data[4],  # correo en BD
                    fecha_nacimiento=paciente_data[5],
                    genero=paciente_data[6],
                    categoria_paciente=paciente_data[7]
                )
                paciente.deuda = float(paciente_data[8]) if paciente_data[8] else 0.0
                paciente.activo = paciente_data[9]
                pacientes.append(paciente)
        
        return pacientes

    @staticmethod
    def obtener_paciente_por_cedula(cedula):
        """Obtiene un paciente específico por su cédula"""
        query = """
            SELECT cedula, nombre, apellido, telefono, correo, 
                   fecha_nacimiento, genero, categoria_paciente, deuda, activo
            FROM pacientes 
            WHERE cedula = %s;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (cedula,))
        
        if resultado and len(resultado) > 0:
            paciente_data = resultado[0]
            paciente = Paciente(
                cedula=paciente_data[0],
                nombre=paciente_data[1],
                apellido=paciente_data[2],
                telefono=paciente_data[3],
                email=paciente_data[4],  # Mapear correo a email internamente
                fecha_nacimiento=paciente_data[5],
                genero=paciente_data[6],
                categoria_paciente=paciente_data[7]
            )
            # Agregar campos adicionales
            paciente.deuda = float(paciente_data[8]) if paciente_data[8] else 0.0
            paciente.activo = paciente_data[9] if paciente_data[9] is not None else True
            return paciente
        return None

    @staticmethod
    def obtener_pacientes_activos():
        """Retorna solo los pacientes activos"""
        query = """
            SELECT cedula, nombre, apellido, telefono, correo, 
                   fecha_nacimiento, genero, categoria_paciente, deuda, activo
            FROM pacientes 
            WHERE activo = TRUE
            ORDER BY apellido, nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        pacientes = []
        
        if resultado:
            for paciente_data in resultado:
                paciente = Paciente(
                    cedula=paciente_data[0],
                    nombre=paciente_data[1],
                    apellido=paciente_data[2],
                    telefono=paciente_data[3],
                    email=paciente_data[4],
                    fecha_nacimiento=paciente_data[5],
                    genero=paciente_data[6],
                    categoria_paciente=paciente_data[7]
                )
                paciente.deuda = float(paciente_data[8]) if paciente_data[8] else 0.0
                paciente.activo = paciente_data[9]
                pacientes.append(paciente)
                
        return pacientes

    @staticmethod
    def obtener_pacientes_por_categoria(categoria):
        """Obtiene pacientes filtrados por categoría"""
        query = """
            SELECT cedula, nombre, apellido, telefono, correo, 
                   fecha_nacimiento, genero, categoria_paciente, deuda, activo
            FROM pacientes 
            WHERE categoria_paciente = %s AND activo = TRUE
            ORDER BY apellido, nombre;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (categoria,))
        pacientes = []
        
        if resultado:
            for paciente_data in resultado:
                paciente = Paciente(
                    cedula=paciente_data[0],
                    nombre=paciente_data[1],
                    apellido=paciente_data[2],
                    telefono=paciente_data[3],
                    email=paciente_data[4],
                    fecha_nacimiento=paciente_data[5],
                    genero=paciente_data[6],
                    categoria_paciente=paciente_data[7]
                )
                paciente.deuda = float(paciente_data[8]) if paciente_data[8] else 0.0
                paciente.activo = paciente_data[9]
                pacientes.append(paciente)
                
        return pacientes

    @staticmethod
    def obtener_pacientes_con_deuda():
        """Obtiene pacientes que tienen deuda pendiente"""
        query = """
            SELECT cedula, nombre, apellido, telefono, correo, 
                   fecha_nacimiento, genero, categoria_paciente, deuda, activo
            FROM pacientes 
            WHERE deuda > 0 AND activo = TRUE
            ORDER BY deuda DESC;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        pacientes = []
        
        if resultado:
            for paciente_data in resultado:
                paciente = Paciente(
                    cedula=paciente_data[0],
                    nombre=paciente_data[1],
                    apellido=paciente_data[2],
                    telefono=paciente_data[3],
                    email=paciente_data[4],
                    fecha_nacimiento=paciente_data[5],
                    genero=paciente_data[6],
                    categoria_paciente=paciente_data[7]
                )
                paciente.deuda = float(paciente_data[8]) if paciente_data[8] else 0.0
                paciente.activo = paciente_data[9]
                pacientes.append(paciente)
                
        return pacientes

    @staticmethod
    def agregar_paciente(datos_paciente):
        """Agrega un nuevo paciente a la base de datos"""
        try:
            # Verificar que no exista ya un paciente con esa cédula
            if Modelo_pacientes.obtener_paciente_por_cedula(datos_paciente.get("cedula")):
                print("❌ Ya existe un paciente with that ID")
                return False
            
            query = """
                INSERT INTO pacientes (cedula, nombre, apellido, telefono, correo, 
                                     fecha_nacimiento, genero, categoria_paciente, deuda, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            params = (
                datos_paciente.get("cedula", ""),
                datos_paciente.get("nombre", ""),
                datos_paciente.get("apellido", ""),
                datos_paciente.get("telefono", ""),
                datos_paciente.get("correo", ""),  # Cambiado de email a correo
                datos_paciente.get("fecha_nacimiento", None),
                datos_paciente.get("genero", ""),  # Agregado campo genero
                datos_paciente.get("categoria_paciente", "CAT002"),
                datos_paciente.get("deuda", 0.0),
                datos_paciente.get("activo", True)  # Agregado campo activo
            )
            
            filas_afectadas = db_connection.ejecutar_insercion(query, params)
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Paciente registrado exitosamente: {datos_paciente['cedula']}")
                return True
            else:
                print("❌ No se pudo registrar el paciente")
                return False
                
        except Exception as e:
            print(f"❌ Error al agregar paciente: {e}")
            return False
            
    @staticmethod
    def actualizar_paciente(cedula, datos_actualizados):
        """Actualiza los datos de un paciente existente"""
        try:
            # Verificar que el paciente existe
            paciente_existente = Modelo_pacientes.obtener_paciente_por_cedula(cedula)
            if not paciente_existente:
                print(f"❌ No se encontró el paciente con cédula: {cedula}")
                return False

            # Crear consulta dinámica solo con los campos que se van a actualizar
            campos_actualizables = ['nombre', 'apellido', 'telefono', 'correo', 
                                  'fecha_nacimiento', 'genero', 'categoria_paciente', 'deuda', 'activo']
            
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
                UPDATE pacientes 
                SET {', '.join(campos_a_actualizar)}
                WHERE cedula = %s;
            """
            
            filas_afectadas = db_connection.ejecutar_actualizacion(query, tuple(valores))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Paciente actualizado exitosamente: {cedula}")
                return True
            else:
                print(f"❌ No se pudo actualizar el paciente: {cedula}")
                return False
                
        except Exception as e:
            print(f"❌ Error al actualizar paciente: {e}")
            return False

    @staticmethod
    def eliminar_paciente(cedula):
        """Elimina (desactiva) un paciente de la base de datos"""
        try:
            # Verificar que el paciente existe
            paciente_existente = Modelo_pacientes.obtener_paciente_por_cedula(cedula)
            if not paciente_existente:
                print(f"❌ No se encontró el paciente con cédula: {cedula}")
                return False

            # En lugar de eliminar, desactivamos el paciente
            query = "UPDATE pacientes SET activo = FALSE WHERE cedula = %s;"
            
            filas_afectadas = db_connection.ejecutar_actualizacion(query, (cedula,))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Paciente desactivado exitosamente: {cedula}")
                return True
            else:
                print(f"❌ No se pudo desactivar el paciente: {cedula}")
                return False
                
        except Exception as e:
            print(f"❌ Error al eliminar paciente: {e}")
            return False

    @staticmethod
    def buscar_pacientes(termino_busqueda):
        """Busca pacientes por nombre, apellido o cédula"""
        try:
            query = """
            SELECT cedula, nombre, apellido, telefono, correo, 
                   fecha_nacimiento, genero, categoria_paciente, deuda, activo
            FROM pacientes 
            WHERE (LOWER(nombre) LIKE LOWER(%s) 
                   OR LOWER(apellido) LIKE LOWER(%s) 
                   OR cedula LIKE %s) 
                  AND activo = TRUE
            ORDER BY apellido, nombre;
            """
            
            termino = f"%{termino_busqueda}%"
            resultado = db_connection.ejecutar_consulta(query, (termino, termino, termino))
            pacientes = []
            
            if resultado:
                for paciente_data in resultado:
                    paciente = Paciente(
                        cedula=paciente_data[0],
                        nombre=paciente_data[1],
                        apellido=paciente_data[2],
                        telefono=paciente_data[3],
                        email=paciente_data[4],
                        fecha_nacimiento=paciente_data[5],
                        genero=paciente_data[6],
                        categoria_paciente=paciente_data[7]
                    )
                    paciente.deuda = float(paciente_data[8]) if paciente_data[8] else 0.0
                    paciente.activo = paciente_data[9]
                    pacientes.append(paciente)
                    
            return pacientes
            
        except Exception as e:
            print(f"❌ Error al buscar pacientes: {e}")
            return []

    @staticmethod
    def contar_pacientes():
        """Retorna el número total de pacientes activos"""
        try:
            query = "SELECT COUNT(*) FROM pacientes WHERE activo = TRUE;"
            resultado = db_connection.ejecutar_consulta(query)
            
            if resultado and len(resultado) > 0:
                return resultado[0][0]
            return 0
            
        except Exception as e:
            print(f"❌ Error al contar pacientes: {e}")
            return 0

    @staticmethod
    def obtener_estadisticas_pacientes():
        """Retorna estadísticas generales de pacientes"""
        try:
            query = """
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN activo = TRUE THEN 1 END) as activos,
                COUNT(CASE WHEN activo = FALSE THEN 1 END) as inactivos,
                COUNT(CASE WHEN deuda > 0 THEN 1 END) as con_deuda,
                COALESCE(SUM(deuda), 0) as deuda_total
            FROM pacientes;
            """
            
            resultado = db_connection.ejecutar_consulta(query)
            
            if resultado and len(resultado) > 0:
                stats = resultado[0]
                return {
                    'total': stats[0],
                    'activos': stats[1], 
                    'inactivos': stats[2],
                    'con_deuda': stats[3],
                    'deuda_total': float(stats[4]) if stats[4] else 0.0
                }
            return {}
            
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return {}
    
    def generar_factura_desde_cita(self, id_cita):
        """Genera una factura automáticamente desde una cita (si no existe)"""
        try:
            # Verificar si ya existe una factura para esta cita
            query_verificar = """
                SELECT id_factura FROM facturas WHERE id_cita = %s;
            """
            resultado = db_connection.ejecutar_consulta(query_verificar, (id_cita,))
            
            if resultado and len(resultado) > 0:
                print(f"🔍 DEBUG: Ya existe factura para cita {id_cita}")
                return True
            
            # Obtener información de la cita
            from modelo.cita import Modelo_citas
            cita = Modelo_citas.obtener_cita_por_id(id_cita)
            
            if not cita:
                print(f"❌ No se encontró la cita {id_cita}")
                return False
            
            # Generar número de factura único
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            numero_factura = f"FAC-{timestamp[-8:]}"
            
            # Crear la factura
            query_factura = """
                INSERT INTO facturas (
                    numero_factura, id_cita, cedula_paciente,
                    subtotal_consulta, subtotal_servicios, descuentos_aplicados,
                    total_bruto, total_neto, estado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            params = (
                numero_factura,
                cita.id_cita,
                cita.cedula_paciente,
                cita.costo_consulta,
                cita.costo_servicios_adicionales,
                cita.descuento_aplicado,
                cita.costo_consulta + cita.costo_servicios_adicionales,
                cita.total_neto,
                'Pendiente'
            )
            
            filas_afectadas = db_connection.ejecutar_insercion(query_factura, params)
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Factura {numero_factura} generada para cita {id_cita}")
                return True
            else:
                print(f"❌ Error al generar factura para cita {id_cita}")
                return False
                
        except Exception as e:
            print(f"❌ Error al generar factura: {e}")
            return False

    def generar_facturas_pendientes(self):
        """Genera facturas para todas las citas del paciente que no tengan factura"""
        try:
            print(f"🔧 DEBUG: Generando facturas pendientes para paciente {self.cedula}")
            
            # Obtener citas sin factura
            query = """
                SELECT c.id_cita, c.estado, c.total_neto
                FROM citas c
                LEFT JOIN facturas f ON c.id_cita = f.id_cita
                WHERE c.cedula_paciente = %s 
                AND f.id_factura IS NULL
                AND c.estado IN ('Confirmada', 'Completada')
                AND c.total_neto > 0;
            """
            
            resultado = db_connection.ejecutar_consulta(query, (self.cedula,))
            
            if resultado:
                print(f"🔧 DEBUG: Se encontraron {len(resultado)} citas sin factura")
                
                for cita_data in resultado:
                    id_cita = cita_data[0]
                    self.generar_factura_desde_cita(id_cita)
            else:
                print(f"🔧 DEBUG: No hay citas sin factura para generar")
                
        except Exception as e:
            print(f"❌ Error al generar facturas pendientes: {e}")
