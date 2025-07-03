from vista.Menu_recepcionista import  Menu_recepcionista_vista
from vista.agendamiento_citas import  Vista_agendamiento_citas
from vista.registrar_llegada_paciente import Registrar_llegada_paciente_vista
from vista.atencion_sin_cita import Vista_atencion_sin_cita
from modelo.servicio import Modelo_servicios_adicionales, Modelo_citas_servicios
from modelo.Recepcionista import Modelo_recepcionista
from modelo.paciente import Modelo_pacientes
from modelo.medico import Modelo_medicos
from modelo.cita import Modelo_citas
from modelo.catalogos import (Catalogo_especialidades, Catalogo_tipos_consulta, 
                             Catalogo_aseguradoras, Catalogo_servicios_adicionales)
from modelo.facturacion import Modelo_facturacion, Calculadora_costos
import tkinter as tk

class Controlador_recepcionista:
    def __init__(self, root, usuario_actual=None, login_controlador=None):
        self.root = root
        self.usuario_actual = usuario_actual
        self.login_controlador = login_controlador
        
        # Inicializar catálogos
        self.cat_especialidades = Catalogo_especialidades()
        self.cat_tipos_consulta = Catalogo_tipos_consulta()
        self.cat_aseguradoras = Catalogo_aseguradoras()
        self.cat_servicios = Catalogo_servicios_adicionales()
        
        # Los modelos tienen métodos estáticos, no necesitan instanciación
        # Se acceden directamente por la clase
        
        # Calculadora de costos
        self.calculadora_costos = Calculadora_costos(
            self.cat_tipos_consulta,
            self.cat_aseguradoras, 
            self.cat_servicios
        )

    def mostrar(self):
        """Muestra la vista principal del menú de recepcionista"""
        self.vista = Menu_recepcionista_vista(self, self.root)

    def abrir_ventana_agendamiento(self):
        """Abre la ventana de agendamiento de citas"""
        # Ya no necesitamos destroy() porque todos usan el mismo root
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Vista_agendamiento_citas(self, self.root))

    def registrar_llegada_paciente(self):
        """Abre la ventana para registrar llegada de paciente"""
        # Ya no necesitamos destroy() porque todos usan el mismo root
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Registrar_llegada_paciente_vista(self, self.root))

    def atencion_sin_cita(self):
        """Abre la ventana para atención sin cita previa"""
        # Ya no necesitamos destroy() porque todos usan el mismo root
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Vista_atencion_sin_cita(self, self.root))

    def volver_menu_recepcionista(self):
        """Regresa al menú principal de recepcionista"""
        # Ya no hay ventanas Toplevel que cerrar, solo limpiar root
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, self._crear_menu_recepcionista)
    
    def _crear_menu_recepcionista(self):
        """Método auxiliar para crear el menú de recepcionista"""
        self.vista = Menu_recepcionista_vista(self, self.root)

    # Métodos para interactuar con los modelos
    def obtener_medicos_disponibles(self):
        """Retorna la lista de médicos disponibles"""
        try:
            # ✅ USAR EL MÉTODO ESTÁTICO CORRECTO DEL MODELO
            medicos_objs = Modelo_medicos.obtener_medicos_disponibles()
            if not medicos_objs:
                return []
            
            # ✅ CONVERTIR OBJETOS MÉDICO A DICCIONARIOS PARA LA VISTA
            medicos_dict = []
            for medico in medicos_objs:
                medicos_dict.append({
                    'id_medico': medico.id_medico,
                    'nombre': medico.nombre,
                    'apellido': medico.apellido,
                    'nombre_completo': medico.nombre_completo(),
                    'especialidad': medico.especialidad,
                    'horario_disponible': f"{medico.horario_inicio}-{medico.horario_fin}",
                    'disponible': medico.disponible,
                    'telefono': medico.telefono,
                    'email': medico.email
                })
            
            return medicos_dict
        except Exception as e:
            print(f"Error obteniendo médicos: {e}")
            return []

    def obtener_pacientes(self):
        """Retorna la lista de pacientes"""
        return self.modelo_pacientes.obtener_todos_los_pacientes()

    def obtener_pacientes(self):
        """Retorna la lista de pacientes"""
        return Modelo_pacientes.obtener_todos_los_pacientes()

    def buscar_paciente(self, criterio_busqueda):
        """Busca un paciente por nombre, apellido o cédula"""
        return Modelo_pacientes.buscar_pacientes(criterio_busqueda)

    def obtener_especialidades(self):
        """Retorna la lista de especialidades médicas"""
        return Modelo_medicos.obtener_especialidades()

    def obtener_servicios_disponibles(self):
        """Retorna la lista de servicios disponibles desde la BD"""
        try:
            # ✅ USAR EL NUEVO MODELO PARA SERVICIOS ADICIONALES
            servicios_objs = Modelo_servicios_adicionales.obtener_todos_los_servicios()
            if not servicios_objs:
                return []
            
            # ✅ CONVERTIR OBJETOS SERVICIO A DICCIONARIOS PARA LA VISTA
            servicios_dict = []
            for servicio in servicios_objs:
                servicios_dict.append({
                    'id': servicio.id_servicio,
                    'id_servicio': servicio.id_servicio,
                    'nombre': servicio.nombre,
                    'categoria': servicio.categoria,
                    'precio': servicio.precio,
                    'descripcion': servicio.descripcion,
                    'activo': servicio.activo
                })
            
            return servicios_dict
        except Exception as e:
            print(f"Error obteniendo servicios disponibles: {e}")
            return []

    def agendar_cita_paciente(self, datos_cita):
        """Agenda una nueva cita para un paciente y genera automáticamente la factura"""
        try:
            # ✅ EXTRAER DATOS CON NOMBRES CORRECTOS DE LA VISTA
            cedula_paciente = datos_cita.get("id_paciente", "").strip()  # Vista usa "id_paciente"
            id_medico = datos_cita.get("id_medico")  # Vista ahora pasa id_medico
            fecha = datos_cita.get("fecha")
            hora = datos_cita.get("hora")
            tipo_consulta = datos_cita.get("tipo_consulta", "").strip()  # Vista ahora pasa ID
            servicios_ids = datos_cita.get("servicios_ids", [])
            
            if not all([cedula_paciente, id_medico, fecha, hora, tipo_consulta]):
                return {"exito": False, "mensaje": "Faltan datos obligatorios para agendar la cita"}
            
            # Validar que el paciente existe
            paciente = Modelo_pacientes.obtener_paciente_por_cedula(cedula_paciente)
            if not paciente:
                return {"exito": False, "mensaje": "Paciente no encontrado"}
            
            # Validar que el médico esté disponible
            medico = Modelo_medicos.obtener_medico_por_id(id_medico)
            if not medico:
                return {"exito": False, "mensaje": "Médico no encontrado"}
            
            # Calcular costos usando la calculadora
            calculo_costo = self.calculadora_costos.calcular_costo_consulta(
                tipo_consulta_id=tipo_consulta,  # Ahora es ID real
                categoria_paciente=paciente.categoria_paciente,
                id_aseguradora=getattr(paciente, 'id_aseguradora', None)
            )
            
            # Obtener servicios adicionales si existen
            servicios_adicionales = []
            costo_servicios = 0.0
            
            if servicios_ids:
                for servicio_id in servicios_ids:
                    # ✅ USAR EL NUEVO MODELO PARA OBTENER SERVICIOS DESDE LA BD
                    servicio_bd = Modelo_servicios_adicionales.obtener_servicio_por_id(servicio_id)
                    if servicio_bd:
                        servicios_adicionales.append({
                            "id": servicio_bd.id_servicio,
                            "nombre": servicio_bd.nombre,
                            "precio": servicio_bd.precio
                        })
                        costo_servicios += servicio_bd.precio
            
            # ✅ CREAR LA CITA CON DATOS CORRECTOS PARA LA BD
            datos_cita_bd = {
                "cedula_paciente": cedula_paciente,
                "id_medico": id_medico,
                "fecha": fecha,
                "hora": hora,
                "tipo_consulta": tipo_consulta,  # Campo correcto para el método crear_cita_bd
                "estado": "Pendiente",  # Cambiado de "Programada" a "Pendiente" para que coincida con los valores del enum en la BD
                "costo_consulta": calculo_costo.get("precio_final", 25000) if isinstance(calculo_costo, dict) else (calculo_costo if calculo_costo else 25000),
                "observaciones": datos_cita.get("observaciones", f"Agendamiento desde recepción - Servicios: {len(servicios_ids)} servicios")
            }
            
            # ✅ USAR MÉTODO ESTÁTICO CORRECTO
            cita_creada = Modelo_citas.crear_cita_bd(datos_cita_bd)
            
            if not cita_creada:
                return {"exito": False, "mensaje": "Error al crear la cita en la base de datos"}
            
            # ✅ PERSISTIR SERVICIOS ADICIONALES EN LA BD
            servicios_agregados_exitosos = 0
            if servicios_ids:
                for servicio_id in servicios_ids:
                    # Verificar que el servicio existe y obtener su precio desde la BD
                    servicio_bd = Modelo_servicios_adicionales.obtener_servicio_por_id(servicio_id)
                    if servicio_bd:
                        # Agregar el servicio a la tabla citas_servicios_adicionales
                        exito_servicio = Modelo_citas_servicios.agregar_servicio_a_cita(
                            id_cita=cita_creada.id_cita,
                            id_servicio=servicio_id,
                            cantidad=1,
                            precio_unitario=servicio_bd.precio
                        )
                        if exito_servicio:
                            servicios_agregados_exitosos += 1
                
                # Actualizar el costo de servicios en la tabla citas
                if servicios_agregados_exitosos > 0:
                    Modelo_citas_servicios.actualizar_costo_servicios_en_cita(cita_creada.id_cita)
            
            # Recalcular costo de servicios desde la BD
            costo_servicios_bd = Modelo_citas_servicios.calcular_total_servicios_cita(cita_creada.id_cita)
            
            # Generar factura automáticamente
            factura_creada = Modelo_facturacion.crear_factura_para_cita(
                id_cita=cita_creada.id_cita,
                cedula_paciente=cedula_paciente,
                tipo_consulta=tipo_consulta,
                precio_consulta=calculo_costo["precio_final"],
                servicios_adicionales=servicios_adicionales,
                descuento_aplicado=calculo_costo.get("descuento", 0.0),
                observaciones=f"Factura generada automáticamente para cita del {fecha} a las {hora}"
            )
            
            # ✅ OBTENER SERVICIOS FINALES DESDE LA BD
            servicios_finales_bd = Modelo_citas_servicios.obtener_servicios_de_cita(cita_creada.id_cita) if cita_creada else []
            
            return {
                "exito": True, 
                "cita": cita_creada, 
                "factura": factura_creada,
                "mensaje": f"Cita agendada exitosamente. Servicios agregados: {servicios_agregados_exitosos}/{len(servicios_ids) if servicios_ids else 0}",
                "costo_total": calculo_costo["precio_final"] + costo_servicios_bd,  # Usar el costo real de la BD
                "costo_servicios": costo_servicios_bd,  # Agregar desglose de servicios
                "numero_factura": factura_creada.numero_factura if factura_creada else None,
                "servicios_procesados": servicios_agregados_exitosos,
                "servicios_adicionales": servicios_adicionales,  # ✅ Agregar lista de servicios con nombres
                "servicios_agregados_bd": servicios_finales_bd  # ✅ Servicios desde BD
            }
            
        except Exception as e:
            print(f"Error agendando cita: {e}")
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def registrar_llegada(self, id_cita, cedula_paciente):
        """Registra la llegada de un paciente usando el ID de la cita"""
        try:
            print(f"🔍 DEBUG Controlador: Registrando llegada - ID Cita: {id_cita}, Cédula: {cedula_paciente}")
            # ✅ USAR MÉTODO ESTÁTICO CORRECTO CON ID DE CITA
            llegada = Modelo_recepcionista.registrar_llegada_paciente_bd(id_cita, cedula_paciente)
            print(f"✅ DEBUG Controlador: Resultado registro: {llegada}")
            return llegada  # Ya retorna dict con "exito" y "mensaje"
        except Exception as e:
            print(f"❌ ERROR Controlador registrar_llegada: {e}")
            return {"exito": False, "mensaje": f"Error en controlador: {str(e)}"}

    def obtener_pacientes_en_espera(self):
        """Retorna la lista de pacientes en espera"""
        return Modelo_recepcionista.obtener_pacientes_en_espera_bd()

    def procesar_atencion_sin_cita(self, datos_atencion):
        """Procesa la atención de un paciente sin cita previa"""
        # ✅ USAR MÉTODO ESTÁTICO CORRECTO
        atencion = Modelo_recepcionista.procesar_atencion_sin_cita_bd(datos_atencion)
        return atencion  # Ya retorna dict con "exito" y "mensaje"

    def obtener_citas_del_dia(self, fecha=None):
        """Retorna las citas del día"""
        # ✅ USAR MÉTODO ESTÁTICO CORRECTO DEL MODELO  
        return Modelo_recepcionista.obtener_citas_del_dia_bd(fecha)

    # === FUNCIONALIDADES ESPECÍFICAS DEL CENTRO MÉDICO ===
    
    def obtener_medicos_por_especialidad(self, especialidad_id):
        """Obtiene listado de médicos disponibles según su especialidad"""
        try:
            # ✅ USAR MÉTODO ESTÁTICO CORRECTO 
            medicos_objs = Modelo_medicos.obtener_medicos_por_especialidad(especialidad_id)
            if not medicos_objs:
                return []
            
            # ✅ CONVERTIR OBJETOS MÉDICO A DICCIONARIOS PARA LA VISTA
            medicos_dict = []
            for medico in medicos_objs:
                medicos_dict.append({
                    'id_medico': medico.id_medico,
                    'nombre': medico.nombre,
                    'apellido': medico.apellido,
                    'nombre_completo': medico.nombre_completo(),
                    'especialidad': medico.especialidad,
                    'horario_disponible': f"{medico.horario_inicio}-{medico.horario_fin}",
                    'disponible': medico.disponible,
                    'telefono': medico.telefono,
                    'email': medico.email
                })
            
            return medicos_dict
        except Exception as e:
            print(f"Error obteniendo médicos por especialidad: {e}")
            return []
    
    def consultar_costo_consulta(self, tipo_consulta_id, categoria_paciente="CAT002", id_aseguradora=None):
        """Consulta el costo de una consulta según su tipo"""
        return self.calculadora_costos.calcular_costo_consulta(
            tipo_consulta_id, categoria_paciente, id_aseguradora
        )
    
    def consultar_descuentos_convenios(self, id_aseguradora):
        """Consulta los descuentos aplicables a pacientes con convenios"""
        aseguradoras = self.cat_aseguradoras.obtener_todas()
        for aseg in aseguradoras:
            if aseg["id"] == id_aseguradora:
                return {
                    "nombre": aseg["nombre"],
                    "tipo": aseg["tipo"],
                    "descuento_general": aseg["descuento_general"],
                    "descuento_especializada": aseg["descuento_especializada"]
                }
        return None
    
    def calcular_costo_total_paciente(self, cedula_paciente, tipo_servicio_id, servicios_adicionales_ids=None):
        """Calcula el costo total de una consulta para un paciente específico"""
        paciente = Modelo_pacientes.obtener_paciente_por_cedula(cedula_paciente)
        if not paciente:
            return {"error": "Paciente no encontrado"}
        
        servicios_adicionales_ids = servicios_adicionales_ids or []
        
        resultado = self.calculadora_costos.calcular_total_con_servicios(
            tipo_servicio_id,
            paciente.categoria_paciente,
            servicios_adicionales_ids,
            None  # No hay id_aseguradora en la tabla pacientes
        )
        
        resultado["paciente"] = {
            "nombre": paciente.nombre_completo(),
            "categoria": paciente.categoria_paciente,
            "aseguradora": None  # No hay aseguradora en el modelo actual
        }
        
        return resultado
    
    def agendar_cita_medica(self, cedula_paciente, id_medico, fecha, hora, tipo_consulta_id):
        """Agenda una cita médica especificando el médico y la identificación del paciente"""
        # Verificar que el paciente existe
        paciente = Modelo_pacientes.obtener_paciente_por_cedula(cedula_paciente)
        if not paciente:
            return {"exito": False, "mensaje": "Paciente no encontrado"}
        
        # Verificar que el médico está disponible
        medico = Modelo_medicos.obtener_medico_por_id(id_medico)
        if not medico or not medico.disponible:
            return {"exito": False, "mensaje": "Médico no disponible"}
        
        # Calcular costo
        costo_info = self.consultar_costo_consulta(
            tipo_consulta_id, 
            paciente.categoria_paciente, 
            None  # No hay id_aseguradora en la tabla pacientes
        )
        
        # Crear la cita
        nueva_cita = Modelo_citas.crear_cita(
            id_paciente=cedula_paciente,
            id_medico=id_medico,
            fecha=fecha,
            hora=hora,
            tipo_consulta=tipo_consulta_id,
            costo=costo_info["precio_final"]
        )
        
        # Agregar al paciente
        cita_data = nueva_cita.to_dict()
        paciente.agregar_cita(cita_data)
        
        return {
            "exito": True, 
            "cita": nueva_cita.to_dict(),
            "costo_info": costo_info,
            "mensaje": "Cita agendada exitosamente"
        }
    
    def registrar_llegada_paciente_cita(self, cedula_paciente, id_cita=None):
        """Registra la llegada del paciente cuando asiste a su cita"""
        paciente = Modelo_pacientes.obtener_paciente_por_cedula(cedula_paciente)
        if not paciente:
            return {"exito": False, "mensaje": "Paciente no encontrado"}
        
        # Verificar cita si se proporciona ID
        if id_cita:
            cita_encontrada = None
            for cita in paciente.citas:
                if cita.get("id_cita") == id_cita:
                    cita_encontrada = cita
                    break
            
            if not cita_encontrada:
                return {"exito": False, "mensaje": "Cita no encontrada"}
            
            # Actualizar estado de la cita a "En curso"
            cita_encontrada["estado"] = "En curso"
            Modelo_citas.actualizar_estado_cita(id_cita, "En curso")
        
        # Registrar llegada en el modelo de recepcionista
        llegada = Modelo_recepcionista.registrar_llegada_paciente_bd(cedula_paciente)
        
        return {
            "exito": True,
            "llegada": llegada,
            "paciente": paciente.to_dict(),
            "mensaje": "Llegada registrada exitosamente"
        }
    
    def verificar_disponibilidad_sin_cita(self, tipo_urgencia="general"):
        """Verifica la disponibilidad de médicos para atención sin cita previa"""
        if tipo_urgencia == "urgencia":
            disponibilidad = Modelo_medicos.verificar_disponibilidad_urgencias()
        else:
            # Para consultas generales sin cita
            medicos_generales = Modelo_medicos.obtener_medicos_por_especialidad("ESP001")
            disponibilidad = {
                "total_disponibles": len(medicos_generales),
                "medicos": medicos_generales
            }
        
        return disponibilidad
    
    def asignar_turno_sin_cita(self, cedula_paciente, tipo_atencion="urgencia"):
        """Asigna un turno de atención para paciente sin cita previa"""
        # Verificar disponibilidad
        disponibilidad = self.verificar_disponibilidad_sin_cita(tipo_atencion)
        
        if disponibilidad["total_disponibles"] == 0:
            return {"exito": False, "mensaje": "No hay médicos disponibles"}
        
        # Asignar médico disponible
        medico_asignado = disponibilidad["medicos"][0]
        
        # Registrar atención
        datos_atencion = {
            "id_paciente": cedula_paciente,
            "tipo_atencion": tipo_atencion,
            "observaciones": "Atención sin cita previa"
        }
        
        atencion = Modelo_recepcionista.atender_paciente_sin_cita_bd(datos_atencion)
        
        return {
            "exito": True,
            "atencion": atencion,
            "medico_asignado": medico_asignado.to_dict(),
            "mensaje": f"Turno asignado with {medico_asignado.nombre_completo()}"
        }

    # === VALIDACIÓN DE PACIENTES ===
    
    def validar_existencia_paciente(self, cedula):
        """Valida si un paciente existe en la BD por su cédula"""
        try:
            if not cedula or not cedula.strip():
                return {"existe": False, "mensaje": "Ingrese una cédula", "paciente": None}
            
            cedula = cedula.strip()
            
            # Validación básica de formato de cédula
            if not cedula.isdigit() or len(cedula) < 6:
                return {"existe": False, "mensaje": "Formato de cédula inválido", "paciente": None}
            
            # Consultar en la BD
            paciente = Modelo_pacientes.obtener_paciente_por_cedula(cedula)
            
            if paciente:
                return {
                    "existe": True, 
                    "mensaje": f"Paciente encontrado: {paciente.nombre_completo()}", 
                    "paciente": {
                        "cedula": paciente.cedula,
                        "nombre": paciente.nombre,
                        "apellido": paciente.apellido,
                        "nombre_completo": paciente.nombre_completo(),
                        "telefono": paciente.telefono,
                        "email": paciente.email,
                        "categoria": paciente.categoria_paciente
                    }
                }
            else:
                return {"existe": False, "mensaje": "Paciente no encontrado en el sistema", "paciente": None}
                
        except Exception as e:
            print(f"Error validando paciente: {e}")
            return {"existe": False, "mensaje": "Error al consultar el sistema", "paciente": None}

    # === MÉTODOS DE CATÁLOGOS ===
    
    def obtener_especialidades_disponibles(self):
        """Retorna las especialidades disponibles desde el catálogo"""
        return self.cat_especialidades.obtener_todas()
    
    def consultar_costo_consulta(self, tipo_consulta_id, categoria_id, aseguradora_id):
        """Consulta el costo de una consulta usando la calculadora de costos"""
        try:
            # Usar la calculadora de costos para obtener el precio
            costo = self.calculadora_costos.calcular_costo_consulta(
                tipo_consulta_id, categoria_id, aseguradora_id
            )
            return costo
        except Exception as e:
            print(f"Error consultando costo: {e}")
            return None
    
    def obtener_catalogo_especialidades(self):
        """Retorna el catálogo de especialidades"""
        return self.cat_especialidades.obtener_todas()
    
    def obtener_catalogo_tipos_consulta(self):
        """Retorna el catálogo de tipos de consulta"""
        return self.cat_tipos_consulta.obtener_todos()
    
    def obtener_catalogo_aseguradoras(self):
        """Retorna el catálogo de aseguradoras"""
        return self.cat_aseguradoras.obtener_todas()
    
    def obtener_servicios_adicionales_disponibles(self):
        """Retorna el catálogo de servicios adicionales"""
        return self.cat_servicios.obtener_todos()
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        # Ya no hay ventanas Toplevel que cerrar, solo limpiar root
        # Usar after() para evitar parpadeo al crear login
        self.root.after(50, self._mostrar_login_sesion)
    
    def _mostrar_login_sesion(self):
        """Método auxiliar para mostrar el login al cerrar sesión"""
        if self.login_controlador:
            self.login_controlador.mostrar_login()
    
    def obtener_id_medico_por_nombre(self, nombre_completo):
        """Obtiene el ID de un médico a partir de su nombre completo"""
        try:
            # Usar el método estático del modelo de médicos
            medico_id = Modelo_medicos.obtener_id_medico_por_nombre(nombre_completo)
            return medico_id
        except Exception as e:
            print(f"Error obteniendo ID médico desde BD: {e}")
            return None
    
    def obtener_medicos_medicina_general(self):
        """Retorna la lista de médicos de Medicina General disponibles para atención sin cita"""
        try:
            print("🔍 DEBUG: Obteniendo médicos de Medicina General...")
            # ✅ USAR EL MÉTODO ESTÁTICO PARA OBTENER MÉDICOS POR ESPECIALIDAD
            # Usar ID numérico 1 para Medicina General (según TABLA_MEDICOS.txt)
            medicos_objs = Modelo_medicos.obtener_medicos_por_especialidad(1)  # 1 = Medicina General
            if not medicos_objs:
                print("❌ DEBUG: No se encontraron médicos de Medicina General")
                # Intentar con el nombre de la especialidad como alternativa
                medicos_objs = Modelo_medicos.obtener_medicos_por_especialidad('Medicina General')
                if not medicos_objs:
                    print("❌ DEBUG: Tampoco se encontraron con el nombre 'Medicina General'")
                    return []
            
            print(f"✅ DEBUG: Se encontraron {len(medicos_objs)} médicos de Medicina General")
            
            # ✅ CONVERTIR OBJETOS MÉDICO A DICCIONARIOS PARA LA VISTA
            medicos_dict = []
            for medico in medicos_objs:
                # Solo incluir médicos disponibles
                if medico.disponible:
                    medicos_dict.append({
                        'id_medico': medico.id_medico,
                        'nombre': medico.nombre,
                        'apellido': medico.apellido,
                        'nombre_completo': medico.nombre_completo(),
                        'especialidad': medico.especialidad,
                        'horario_disponible': f"{medico.horario_inicio}-{medico.horario_fin}",
                        'disponible': medico.disponible,
                        'telefono': medico.telefono,
                        'email': medico.email
                    })
                    print(f"📋 DEBUG: Médico disponible: {medico.nombre_completo()} - ID: {medico.id_medico}")
            
            print(f"✅ DEBUG: {len(medicos_dict)} médicos de Medicina General disponibles para la vista")
            return medicos_dict
        except Exception as e:
            print(f"❌ ERROR obteniendo médicos de Medicina General: {e}")
            import traceback
            traceback.print_exc()
            return []
