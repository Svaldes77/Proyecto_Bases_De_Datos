# modelo/facturacion.py
"""
Modelo de facturación para el Centro Médico "Salud Vital"
Maneja el cálculo de costos, descuentos y generación de facturas con integración BD
"""
from datetime import datetime
from modelo.conexion_bd import db_connection

class Factura:
    def __init__(self, id_factura=None, numero_factura="", id_cita=None, cedula_paciente="", 
                 fecha_emision=None, subtotal_consulta=0.0, subtotal_servicios=0.0, 
                 descuentos_aplicados=0.0, total_bruto=0.0, total_neto=0.0, 
                 estado="Pendiente", metodo_pago=None, fecha_pago=None, observaciones=""):
        self.id_factura = id_factura
        self.numero_factura = numero_factura
        self.id_cita = id_cita
        self.cedula_paciente = cedula_paciente
        self.fecha_emision = fecha_emision or datetime.now()
        self.subtotal_consulta = subtotal_consulta
        self.subtotal_servicios = subtotal_servicios
        self.descuentos_aplicados = descuentos_aplicados
        self.total_bruto = total_bruto
        self.total_neto = total_neto
        self.estado = estado
        self.metodo_pago = metodo_pago
        self.fecha_pago = fecha_pago
        self.observaciones = observaciones
        self.detalles = []  # Lista de items de detalle

    def agregar_detalle(self, tipo_item, descripcion, cantidad=1, precio_unitario=0.0, 
                       descuento=0.0, subtotal=0.0):
        """Agrega un detalle a la factura"""
        detalle = {
            "tipo_item": tipo_item,
            "descripcion": descripcion,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "descuento": descuento,
            "subtotal": subtotal
        }
        self.detalles.append(detalle)

    def calcular_totales(self):
        """Recalcula los totales de la factura basado en los detalles"""
        self.subtotal_consulta = 0.0
        self.subtotal_servicios = 0.0
        
        for detalle in self.detalles:
            if detalle["tipo_item"] == "CONSULTA":
                self.subtotal_consulta += detalle["subtotal"]
            elif detalle["tipo_item"] == "SERVICIO_ADICIONAL":
                self.subtotal_servicios += detalle["subtotal"]
        
        self.total_bruto = self.subtotal_consulta + self.subtotal_servicios
        self.total_neto = self.total_bruto - self.descuentos_aplicados

    def to_dict(self):
        """Convierte la factura a diccionario"""
        return {
            "id_factura": self.id_factura,
            "numero_factura": self.numero_factura,
            "id_cita": self.id_cita,
            "cedula_paciente": self.cedula_paciente,
            "fecha_emision": self.fecha_emision,
            "subtotal_consulta": self.subtotal_consulta,
            "subtotal_servicios": self.subtotal_servicios,
            "descuentos_aplicados": self.descuentos_aplicados,
            "total_bruto": self.total_bruto,
            "total_neto": self.total_neto,
            "estado": self.estado,
            "metodo_pago": self.metodo_pago,
            "fecha_pago": self.fecha_pago,
            "observaciones": self.observaciones,
            "detalles": self.detalles
        }

class Modelo_facturacion:
    """Modelo para manejar operaciones CRUD de facturas con la base de datos"""
    
    @staticmethod
    def generar_numero_factura():
        """Genera un número único de factura"""
        try:
            # Obtener el último número de factura
            query = """
                SELECT numero_factura 
                FROM facturas 
                ORDER BY id_factura DESC 
                LIMIT 1;
            """
            resultado = db_connection.ejecutar_consulta(query)
            
            if resultado and len(resultado) > 0:
                ultimo_numero = resultado[0][0]
                # Extraer el número secuencial (ej: FAC-2025-001 -> 001)
                try:
                    numero_secuencial = int(ultimo_numero.split("-")[-1]) + 1
                except:
                    numero_secuencial = 1
            else:
                numero_secuencial = 1
            
            # Generar nuevo número de factura
            año_actual = datetime.now().year
            numero_factura = f"FAC-{año_actual}-{numero_secuencial:03d}"
            
            return numero_factura
            
        except Exception as e:
            print(f"Error generando número de factura: {e}")
            # Número de respaldo
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            return f"FAC-{timestamp}"

    @staticmethod
    def crear_factura_para_cita(id_cita, cedula_paciente, tipo_consulta, precio_consulta, 
                               servicios_adicionales=None, descuento_aplicado=0.0, observaciones=""):
        """Crea una factura completa para una cita médica"""
        try:
            # Generar número de factura
            numero_factura = Modelo_facturacion.generar_numero_factura()
            
            # Calcular totales
            subtotal_consulta = precio_consulta
            subtotal_servicios = 0.0
            
            if servicios_adicionales:
                for servicio in servicios_adicionales:
                    subtotal_servicios += servicio.get("precio", 0.0)
            
            total_bruto = subtotal_consulta + subtotal_servicios
            total_neto = total_bruto - descuento_aplicado
            
            # Insertar factura principal
            query_factura = """
                INSERT INTO facturas (numero_factura, id_cita, cedula_paciente, 
                                    subtotal_consulta, subtotal_servicios, descuentos_aplicados,
                                    total_bruto, total_neto, estado, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_factura;
            """
            
            parametros_factura = (
                numero_factura, id_cita, cedula_paciente,
                subtotal_consulta, subtotal_servicios, descuento_aplicado,
                total_bruto, total_neto, 'Pendiente', observaciones
            )
            
            # Usamos ejecutar_consulta porque necesitamos el ID retornado
            resultado_factura = db_connection.ejecutar_consulta(query_factura, parametros_factura)
            
            if not resultado_factura:
                return None
            
            id_factura = resultado_factura[0][0]
            
            # Insertar detalle de consulta
            query_detalle = """
                INSERT INTO facturas_detalle (id_factura, tipo_item, descripcion, 
                                            cantidad, precio_unitario, descuento, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            
            parametros_consulta = (
                id_factura, 'CONSULTA', f'Consulta médica - {tipo_consulta}',
                1, precio_consulta, descuento_aplicado, subtotal_consulta
            )
            
            db_connection.ejecutar_insercion(query_detalle, parametros_consulta)
            
            # Insertar detalles de servicios adicionales
            if servicios_adicionales:
                for servicio in servicios_adicionales:
                    parametros_servicio = (
                        id_factura, 'SERVICIO_ADICIONAL', servicio.get('nombre', ''),
                        1, servicio.get('precio', 0.0), 0.0, servicio.get('precio', 0.0)
                    )
                    
                    db_connection.ejecutar_insercion(query_detalle, parametros_servicio)
            
            # Retornar la factura creada
            return Modelo_facturacion.obtener_factura_por_id(id_factura)
            
        except Exception as e:
            print(f"Error creando factura: {e}")
            return None

    @staticmethod
    def obtener_factura_por_id(id_factura):
        """Obtiene una factura completa por su ID con sus detalles"""
        try:
            # Consultar factura principal
            query_factura = """
                SELECT id_factura, numero_factura, id_cita, cedula_paciente, 
                       fecha_emision, subtotal_consulta, subtotal_servicios,
                       descuentos_aplicados, total_bruto, total_neto, estado,
                       metodo_pago, fecha_pago, observaciones
                FROM facturas
                WHERE id_factura = %s;
            """
            
            resultado_factura = db_connection.ejecutar_consulta(query_factura, (id_factura,))
            
            if not resultado_factura:
                return None
            
            factura_data = resultado_factura[0]
            
            # Crear objeto factura
            factura = Factura(
                id_factura=factura_data[0],
                numero_factura=factura_data[1],
                id_cita=factura_data[2],
                cedula_paciente=factura_data[3],
                fecha_emision=factura_data[4],
                subtotal_consulta=float(factura_data[5]),
                subtotal_servicios=float(factura_data[6]),
                descuentos_aplicados=float(factura_data[7]),
                total_bruto=float(factura_data[8]),
                total_neto=float(factura_data[9]),
                estado=factura_data[10],
                metodo_pago=factura_data[11],
                fecha_pago=factura_data[12],
                observaciones=factura_data[13] or ""
            )
            
            # Consultar detalles de la factura
            query_detalles = """
                SELECT tipo_item, descripcion, cantidad, precio_unitario, descuento, subtotal
                FROM facturas_detalle
                WHERE id_factura = %s
                ORDER BY id_detalle_factura;
            """
            
            resultado_detalles = db_connection.ejecutar_consulta(query_detalles, (id_factura,))
            
            if resultado_detalles:
                for detalle_data in resultado_detalles:
                    factura.agregar_detalle(
                        tipo_item=detalle_data[0],
                        descripcion=detalle_data[1],
                        cantidad=detalle_data[2],
                        precio_unitario=float(detalle_data[3]),
                        descuento=float(detalle_data[4]),
                        subtotal=float(detalle_data[5])
                    )
            
            return factura
            
        except Exception as e:
            print(f"Error obteniendo factura: {e}")
            return None

    @staticmethod
    def obtener_facturas_por_paciente(cedula_paciente, limite=None):
        """Obtiene las facturas de un paciente específico"""
        try:
            query = """
                SELECT id_factura, numero_factura, fecha_emision, total_neto, estado
                FROM facturas
                WHERE cedula_paciente = %s
                ORDER BY fecha_emision DESC
            """
            
            if limite:
                query += f" LIMIT {limite}"
            
            resultado = db_connection.ejecutar_consulta(query, (cedula_paciente,))
            facturas = []
            
            if resultado:
                for factura_data in resultado:
                    facturas.append({
                        "id_factura": factura_data[0],
                        "numero_factura": factura_data[1],
                        "fecha_emision": factura_data[2],
                        "total_neto": float(factura_data[3]),
                        "estado": factura_data[4]
                    })
            
            return facturas
            
        except Exception as e:
            print(f"Error obteniendo facturas del paciente: {e}")
            return []

class Calculadora_costos:
    def __init__(self, catalogo_tipos_consulta, catalogo_aseguradoras, catalogo_servicios):
        self.catalogo_tipos_consulta = catalogo_tipos_consulta
        self.catalogo_aseguradoras = catalogo_aseguradoras
        self.catalogo_servicios = catalogo_servicios

    def calcular_costo_consulta(self, tipo_consulta_id, categoria_paciente="CAT002", id_aseguradora=None):
        """Calcula el costo de una consulta con descuentos aplicables"""
        # Obtener precio base
        precio_base = self.catalogo_tipos_consulta.obtener_precio(tipo_consulta_id)
        
        # Calcular descuentos según la aseguradora
        if id_aseguradora:
            porcentaje_descuento = self.catalogo_aseguradoras.obtener_descuento(id_aseguradora)
            descuento = precio_base * (porcentaje_descuento / 100)
            
            return {
                "precio_base": precio_base,
                "descuento": descuento,
                "porcentaje_descuento": porcentaje_descuento,
                "precio_final": precio_base - descuento,
                "tipo_descuento": f"Aseguradora {id_aseguradora}"
            }
        
        return {
            "precio_base": precio_base,
            "descuento": 0.0,
            "precio_final": precio_base,
            "tipo_descuento": "Ninguno"
        }

    def calcular_total_con_servicios(self, tipo_consulta_id, categoria_paciente, 
                                   lista_servicios_ids, id_aseguradora=None):
        """Calcula el total incluyendo consulta y servicios adicionales"""
        # Costo de consulta
        consulta = self.calcular_costo_consulta(tipo_consulta_id, categoria_paciente, id_aseguradora)
        
        # Costo de servicios adicionales
        total_servicios = self.catalogo_servicios.calcular_total(lista_servicios_ids)
        
        return {
            "consulta": consulta,
            "servicios_adicionales": total_servicios,
            "total_general": consulta["precio_final"] + total_servicios
        }
