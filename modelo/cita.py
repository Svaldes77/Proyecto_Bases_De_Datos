# modelo/cita.py
from modelo.conexion_bd import db_connection
from datetime import datetime, timedelta
import random

class Cita:
    def __init__(self, id_cita=None, cedula_paciente=None, id_medico=None, fecha=None, 
                 hora=None, id_tipo_consulta=None, id_aseguradora=None, estado="Pendiente", 
                 costo_consulta=0.0, descuento_aplicado=0.0, costo_servicios_adicionales=0.0, 
                 total_neto=0.0, observaciones=""):
        self.id_cita = id_cita
        self.cedula_paciente = cedula_paciente
        self.id_medico = id_medico
        self.fecha = fecha
        self.hora = hora
        self.id_tipo_consulta = id_tipo_consulta
        self.id_aseguradora = id_aseguradora
        # Asegurarnos que siempre use valores válidos del enum estado_cita
        # Los valores válidos son: 'Pendiente', 'Confirmada', 'En_Proceso', 'Completada', 'Cancelada'
        if estado not in ['Pendiente', 'Confirmada', 'En_Proceso', 'Completada', 'Cancelada']:
            self.estado = 'Pendiente'  # valor predeterminado si el estado no es válido
        else:
            self.estado = estado
        self.costo_consulta = costo_consulta
        self.descuento_aplicado = descuento_aplicado
        self.costo_servicios_adicionales = costo_servicios_adicionales
        self.total_neto = total_neto
        self.observaciones = observaciones

    def to_dict(self):
        """Convierte la cita a diccionario para facilitar el manejo en las vistas"""
        return {
            "id_cita": self.id_cita,
            "cedula_paciente": self.cedula_paciente,
            "id_medico": self.id_medico,
            "fecha": self.fecha.strftime("%Y-%m-%d") if isinstance(self.fecha, datetime) else str(self.fecha),
            "hora": str(self.hora),
            "id_tipo_consulta": self.id_tipo_consulta,
            "id_aseguradora": self.id_aseguradora,
            "estado": self.estado,
            "costo_consulta": self.costo_consulta,
            "descuento_aplicado": self.descuento_aplicado,
            "costo_servicios_adicionales": self.costo_servicios_adicionales,
            "total_neto": self.total_neto,
            "observaciones": self.observaciones
        }

class Modelo_citas:
    """Modelo para manejar operaciones CRUD de citas con la base de datos"""
    
    @staticmethod
    def obtener_todas_las_citas():
        """Retorna todas las citas desde la base de datos"""
        query = """
            SELECT id_cita, cedula_paciente, id_medico, id_tipo_consulta, id_aseguradora,
                   fecha, hora, estado, costo_consulta, descuento_aplicado,
                   costo_servicios_adicionales, total_neto, observaciones
            FROM citas
            ORDER BY fecha DESC, hora DESC;
        """
        
        resultado = db_connection.ejecutar_consulta(query)
        citas = []
        
        if resultado:
            for cita_data in resultado:
                cita = Cita(
                    id_cita=cita_data[0],
                    cedula_paciente=cita_data[1],
                    id_medico=cita_data[2],
                    id_tipo_consulta=cita_data[3],
                    id_aseguradora=cita_data[4],
                    fecha=cita_data[5],
                    hora=cita_data[6],
                    estado=cita_data[7],
                    costo_consulta=float(cita_data[8]) if cita_data[8] else 0.0,
                    descuento_aplicado=float(cita_data[9]) if cita_data[9] else 0.0,
                    costo_servicios_adicionales=float(cita_data[10]) if cita_data[10] else 0.0,
                    total_neto=float(cita_data[11]) if cita_data[11] else 0.0,
                    observaciones=cita_data[12] or ""
                )
                citas.append(cita)
        
        return citas

    @staticmethod
    def obtener_cita_por_id(id_cita):
        """Obtiene una cita específica por su ID"""
        query = """
            SELECT id_cita, cedula_paciente, id_medico, id_tipo_consulta, id_aseguradora,
                   fecha, hora, estado, costo_consulta, descuento_aplicado,
                   costo_servicios_adicionales, total_neto, observaciones
            FROM citas
            WHERE id_cita = %s;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (id_cita,))
        
        if resultado and len(resultado) > 0:
            cita_data = resultado[0]
            return Cita(
                id_cita=cita_data[0],
                cedula_paciente=cita_data[1],
                id_medico=cita_data[2],
                id_tipo_consulta=cita_data[3],
                id_aseguradora=cita_data[4],
                fecha=cita_data[5],
                hora=cita_data[6],
                estado=cita_data[7],
                costo_consulta=float(cita_data[8]) if cita_data[8] else 0.0,
                descuento_aplicado=float(cita_data[9]) if cita_data[9] else 0.0,
                costo_servicios_adicionales=float(cita_data[10]) if cita_data[10] else 0.0,
                total_neto=float(cita_data[11]) if cita_data[11] else 0.0,
                observaciones=cita_data[12] or ""
            )
        return None

    @staticmethod
    def obtener_citas_por_paciente(cedula_paciente):
        """Obtiene todas las citas de un paciente específico"""
        query = """
            SELECT id_cita, cedula_paciente, id_medico, id_tipo_consulta, id_aseguradora,
                   fecha, hora, estado, costo_consulta, descuento_aplicado,
                   costo_servicios_adicionales, total_neto, observaciones
            FROM citas
            WHERE cedula_paciente = %s
            ORDER BY fecha DESC, hora DESC;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (cedula_paciente,))
        citas = []
        
        if resultado:
            for cita_data in resultado:
                cita = Cita(
                    id_cita=cita_data[0],
                    cedula_paciente=cita_data[1],
                    id_medico=cita_data[2],
                    id_tipo_consulta=cita_data[3],
                    id_aseguradora=cita_data[4],
                    fecha=cita_data[5],
                    hora=cita_data[6],
                    estado=cita_data[7],
                    costo_consulta=float(cita_data[8]) if cita_data[8] else 0.0,
                    descuento_aplicado=float(cita_data[9]) if cita_data[9] else 0.0,
                    costo_servicios_adicionales=float(cita_data[10]) if cita_data[10] else 0.0,
                    total_neto=float(cita_data[11]) if cita_data[11] else 0.0,
                    observaciones=cita_data[12] or ""
                )
                citas.append(cita)
        
        return citas

    @staticmethod
    def obtener_citas_por_medico(id_medico):
        """Obtiene todas las citas de un médico específico"""
        query = """
            SELECT id_cita, cedula_paciente, id_medico, id_tipo_consulta, id_aseguradora,
                   fecha, hora, estado, costo_consulta, descuento_aplicado,
                   costo_servicios_adicionales, total_neto, observaciones
            FROM citas
            WHERE id_medico = %s
            ORDER BY fecha DESC, hora DESC;
        """
        
        resultado = db_connection.ejecutar_consulta(query, (id_medico,))
        citas = []
        
        if resultado:
            for cita_data in resultado:
                cita = Cita(
                    id_cita=cita_data[0],
                    cedula_paciente=cita_data[1],
                    id_medico=cita_data[2],
                    id_tipo_consulta=cita_data[3],
                    id_aseguradora=cita_data[4],
                    fecha=cita_data[5],
                    hora=cita_data[6],
                    estado=cita_data[7],
                    costo_consulta=float(cita_data[8]) if cita_data[8] else 0.0,
                    descuento_aplicado=float(cita_data[9]) if cita_data[9] else 0.0,
                    costo_servicios_adicionales=float(cita_data[10]) if cita_data[10] else 0.0,
                    total_neto=float(cita_data[11]) if cita_data[11] else 0.0,
                    observaciones=cita_data[12] or ""
                )
                citas.append(cita)
        
        return citas

    @staticmethod
    def agendar_cita(datos_cita):
        """Agenda una nueva cita en la base de datos"""
        try:
            query = """
                INSERT INTO citas (cedula_paciente, id_medico, id_tipo_consulta, id_aseguradora,
                                 fecha, hora, estado, costo_consulta, descuento_aplicado,
                                 costo_servicios_adicionales, total_neto, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            params = (
                datos_cita.get("cedula_paciente"),
                datos_cita.get("id_medico"),
                datos_cita.get("id_tipo_consulta"),
                datos_cita.get("id_aseguradora"),
                datos_cita.get("fecha"),
                datos_cita.get("hora"),
                datos_cita.get("estado", "Pendiente"),
                datos_cita.get("costo_consulta", 0.0),
                datos_cita.get("descuento_aplicado", 0.0),
                datos_cita.get("costo_servicios_adicionales", 0.0),
                datos_cita.get("total_neto", 0.0),
                datos_cita.get("observaciones", "")
            )
            
            filas_afectadas = db_connection.ejecutar_insercion(query, params)
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Cita agendada exitosamente")
                return True
            else:
                print("❌ No se pudo agendar la cita")
                return False
                
        except Exception as e:
            print(f"❌ Error al agendar cita: {e}")
            return False

    @staticmethod
    def actualizar_estado_cita(id_cita, nuevo_estado):
        """Actualiza el estado de una cita"""
        try:
            query = "UPDATE citas SET estado = %s WHERE id_cita = %s;"
            filas_afectadas = db_connection.ejecutar_actualizacion(query, (nuevo_estado, id_cita))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Estado de cita {id_cita} actualizado a {nuevo_estado}")
                return True
            else:
                print(f"❌ No se pudo actualizar el estado de la cita {id_cita}")
                return False
                
        except Exception as e:
            print(f"❌ Error al actualizar estado de cita: {e}")
            return False

    @staticmethod
    def cancelar_cita(id_cita, motivo=""):
        """Cancela una cita"""
        try:
            observaciones_actualizadas = f"CANCELADA: {motivo}" if motivo else "CANCELADA"
            
            query = """
                UPDATE citas 
                SET estado = 'Cancelada', observaciones = %s 
                WHERE id_cita = %s;
            """
            
            filas_afectadas = db_connection.ejecutar_actualizacion(query, (observaciones_actualizadas, id_cita))
            
            if filas_afectadas and filas_afectadas > 0:
                print(f"✅ Cita {id_cita} cancelada exitosamente")
                return True
            else:
                print(f"❌ No se pudo cancelar la cita {id_cita}")
                return False
                
        except Exception as e:
            print(f"❌ Error al cancelar cita: {e}")
            return False

    @staticmethod
    @staticmethod
    def crear_cita_bd(datos_cita):
        """Crea una nueva cita en la base de datos"""
        try:
            # ✅ QUERY ACTUALIZADA SEGÚN TABLA_CITAS.txt
            query = """
                INSERT INTO citas (cedula_paciente, id_medico, id_tipo_consulta, 
                                 fecha, hora, estado, costo_consulta, total_neto, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_cita;
            """
            
            costo_consulta = datos_cita.get("costo_consulta", 0.0)
            
            # Asegurarse de que el estado sea válido según el enum
            estado = datos_cita.get("estado", "Pendiente")
            if estado not in ['Pendiente', 'Confirmada', 'En_Proceso', 'Completada', 'Cancelada']:
                estado = 'Pendiente'  # Usar valor predeterminado si no es válido
                
            parametros = (
                datos_cita.get("cedula_paciente"),
                datos_cita.get("id_medico"),
                datos_cita.get("tipo_consulta"),  # Se mapea a id_tipo_consulta
                datos_cita.get("fecha"),
                datos_cita.get("hora"),
                estado,  # Estado validado para que coincida con el enum
                costo_consulta,
                costo_consulta,  # total_neto igual a costo_consulta inicialmente
                datos_cita.get("observaciones", "")
            )
            
            resultado = db_connection.ejecutar_consulta(query, parametros)
            
            if resultado and len(resultado) > 0:
                id_cita = resultado[0][0]
                
                # Retornar objeto Cita creado
                cita = Cita(
                    id_cita=id_cita,
                    cedula_paciente=datos_cita.get("cedula_paciente"),
                    id_medico=datos_cita.get("id_medico"),
                    fecha=datos_cita.get("fecha"),
                    hora=datos_cita.get("hora"),
                    id_tipo_consulta=datos_cita.get("tipo_consulta"),
                    estado=datos_cita.get("estado", "Pendiente"),  # Cambiado de "Programada" a "Pendiente" para que coincida con los valores del enum en la BD
                    costo_consulta=datos_cita.get("costo_consulta", 0.0),
                    observaciones=datos_cita.get("observaciones", "")
                )
                
                return cita
            
            return None
            
        except Exception as e:
            print(f"Error creando cita en BD: {e}")
            return None

    def _generar_citas_ejemplo(self):
        """Genera citas de ejemplo para demostración"""
        tipos_consulta = ["General", "Especialista", "Pediatría", "Cardiología", "Dermatología"]
        estados = ["Confirmada", "Pendiente", "Cancelada"]
        
        for i in range(10):
            fecha = datetime.today() + timedelta(days=random.randint(-30, 30))
            hora = f"{random.randint(8, 17)}:{random.choice(['00', '30'])}"
            
            cita = Cita(
                id_cita=self.contador_id,
                id_paciente=f"PAC{random.randint(100, 999)}",
                id_medico=f"MED{random.randint(1, 10)}",
                fecha=fecha,
                hora=hora,
                tipo_consulta=random.choice(tipos_consulta),
                estado=random.choice(estados),
                costo=round(random.uniform(50, 200), 2)
            )
            
            self.citas.append(cita)
            self.contador_id += 1

    def obtener_todas_las_citas(self):
        """Retorna todas las citas"""
        return self.citas



    def obtener_citas_por_fecha(self, fecha):
        """Retorna las citas de una fecha específica"""
        return [cita for cita in self.citas if cita.fecha == fecha]

    def crear_cita(self, id_paciente, id_medico, fecha, hora, tipo_consulta, costo=0.0):
        """Crea una nueva cita"""
        nueva_cita = Cita(
            id_cita=self.contador_id,
            id_paciente=id_paciente,
            id_medico=id_medico,
            fecha=fecha,
            hora=hora,
            tipo_consulta=tipo_consulta,
            estado="Pendiente",
            costo=costo
        )
        
        self.citas.append(nueva_cita)
        self.contador_id += 1
        return nueva_cita

    def actualizar_estado_cita(self, id_cita, nuevo_estado):
        """Actualiza el estado de una cita"""
        for cita in self.citas:
            if cita.id_cita == id_cita:
                cita.estado = nuevo_estado
                return True
        return False

    def cancelar_cita(self, id_cita):
        """Cancela una cita"""
        return self.actualizar_estado_cita(id_cita, "Cancelada")

    def confirmar_cita(self, id_cita):
        """Confirma una cita"""
        return self.actualizar_estado_cita(id_cita, "Confirmada")
