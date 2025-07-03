from vista.menu_director import Menu_director_vista
from modelo.usuario import Modelo_usuarios
from vista.Citas_paciente_vista import Vista_citas_paciente
from vista.Consolidado_vista import Vista_consolidado
from vista.Estadisticas_vista import Vista_estadisticas
from vista.Informe_vista import Vista_informe_servicios
from modelo.paciente import Modelo_pacientes
from modelo.medico import Modelo_medicos
from modelo.cita import Modelo_citas
from modelo.consulta import Modelo_consultas
from modelo.servicio import Modelo_servicios_adicionales
from datetime import datetime, timedelta
import tkinter as tk

class Controlador_director:
    def __init__(self, root, usuario_actual=None, login_controlador=None):
        self.root = root
        self.usuario_actual = usuario_actual
        self.login_controlador = login_controlador
        
        # Inicializar modelos
        self.modelo_usuarios = Modelo_usuarios()
        self.modelo_pacientes = Modelo_pacientes()
        self.modelo_medicos = Modelo_medicos()
        self.modelo_citas = Modelo_citas()
        self.modelo_consultas = Modelo_consultas()
        # Los servicios adicionales usan métodos estáticos, no necesitan instancia

    def mostrar(self):
        """Muestra la vista principal del menú de director"""
        self.vista = Menu_director_vista(self, self.root)

    # Mostrar vistas específicas
    def mostrar_informe_servicios(self):
        """Muestra el informe de servicios"""
        # Ya no necesitamos withdraw() porque no usamos Toplevel
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Vista_informe_servicios(self, self.root))

    def mostrar_citas_pacientes(self):
        """Muestra las citas de pacientes"""
        # Ya no necesitamos withdraw() porque no usamos Toplevel
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Vista_citas_paciente(self, self.root))

    def mostrar_consolidado_mensual(self):
        """Muestra el consolidado mensual"""
        # Ya no necesitamos withdraw() porque no usamos Toplevel
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Vista_consolidado(self, self.root))

    def mostrar_estadisticas(self):
        """Muestra las estadísticas del sistema"""
        # Ya no necesitamos withdraw() porque no usamos Toplevel
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Vista_estadisticas(self, self.root))

    # Métodos para generar informes y estadísticas
    def obtener_informe_servicios(self, fecha_inicio=None, fecha_fin=None):
        """Genera informe detallado de servicios"""
        servicios = Modelo_servicios_adicionales.obtener_todos_los_servicios()
        consultas = self.modelo_consultas.obtener_todas_las_consultas()
        
        # Filtrar por fechas si se proporcionan
        if fecha_inicio and fecha_fin:
            consultas = [c for c in consultas 
                        if fecha_inicio <= c.fecha_consulta.date() <= fecha_fin]
        
        informe = {
            "total_servicios": len(servicios),
            "servicios_activos": len(Modelo_servicios_adicionales.obtener_todos_los_servicios()),
            "consultas_periodo": len(consultas),
            "servicios_por_categoria": {},
            "ingresos_estimados": 0.0
        }
        
        # Agrupar servicios por categoría
        for servicio in servicios:
            categoria = servicio.categoria
            if categoria not in informe["servicios_por_categoria"]:
                informe["servicios_por_categoria"][categoria] = {
                    "cantidad": 0,
                    "precio_promedio": 0.0,
                    "servicios": []
                }
            
            informe["servicios_por_categoria"][categoria]["cantidad"] += 1
            informe["servicios_por_categoria"][categoria]["servicios"].append(servicio.to_dict())
        
        # Calcular precios promedio
        for categoria in informe["servicios_por_categoria"]:
            servicios_cat = informe["servicios_por_categoria"][categoria]["servicios"]
            if servicios_cat:
                promedio = sum(s["precio"] for s in servicios_cat) / len(servicios_cat)
                informe["servicios_por_categoria"][categoria]["precio_promedio"] = promedio
        
        return informe

    def obtener_consolidado_mensual(self, año=None, mes=None):
        """Genera consolidado mensual del sistema"""
        if not año:
            año = datetime.now().year
        if not mes:
            mes = datetime.now().month
            
        # Obtener datos del mes
        citas = self.modelo_citas.obtener_todas_las_citas()
        consultas = self.modelo_consultas.obtener_todas_las_consultas()
        pacientes = self.modelo_pacientes.obtener_todos_los_pacientes()
        
        # Filtrar por mes/año
        citas_mes = []
        consultas_mes = []
        
        for cita in citas:
            if hasattr(cita, 'fecha') and isinstance(cita.fecha, datetime):
                if cita.fecha.year == año and cita.fecha.month == mes:
                    citas_mes.append(cita)
        
        for consulta in consultas:
            if consulta.fecha_consulta.year == año and consulta.fecha_consulta.month == mes:
                consultas_mes.append(consulta)
        
        consolidado = {
            "periodo": f"{mes:02d}/{año}",
            "total_citas": len(citas_mes),
            "total_consultas": len(consultas_mes),
            "total_pacientes": len(pacientes),
            "citas_completadas": len([c for c in citas_mes if c.estado == "Confirmada"]),
            "consultas_completadas": len([c for c in consultas_mes if c.estado == "Completada"]),
            "pacientes_activos": len(self.modelo_pacientes.obtener_pacientes_activos()),
            "medicos_disponibles": len(self.modelo_medicos.obtener_medicos_disponibles()),
            "ingresos_estimados": len(consultas_mes) * 75.0,  # Promedio estimado
            "deuda_pendiente": sum(p.deuda for p in pacientes)
        }
        
        return consolidado

    def obtener_estadisticas_generales(self):
        """Retorna estadísticas generales del sistema"""
        return {
            "pacientes": {
                "total": len(self.modelo_pacientes.obtener_todos_los_pacientes()),
                "activos": len(self.modelo_pacientes.obtener_pacientes_activos()),
                "con_deuda": len([p for p in self.modelo_pacientes.obtener_todos_los_pacientes() if p.deuda > 0])
            },
            "medicos": {
                "total": len(self.modelo_medicos.obtener_todos_los_medicos()),
                "disponibles": len(self.modelo_medicos.obtener_medicos_disponibles()),
                "especialidades": len(self.modelo_medicos.obtener_especialidades())
            },
            "citas": {
                "total": len(self.modelo_citas.obtener_todas_las_citas()),
                "hoy": len(self.modelo_citas.obtener_citas_por_fecha(datetime.now().date()))
            },
            "consultas": self.modelo_consultas.obtener_estadisticas_consultas(),
            "servicios": {
                "total": len(Modelo_servicios_adicionales.obtener_todos_los_servicios()),
                "activos": len(Modelo_servicios_adicionales.obtener_todos_los_servicios()),
                "categorias": len(Modelo_servicios_adicionales.obtener_categorias_disponibles())
            }
        }

    def obtener_citas_pacientes(self, filtro_fecha=None):
        """Retorna las citas de pacientes con filtros opcionales"""
        citas = self.modelo_citas.obtener_todas_las_citas()
        
        if filtro_fecha:
            citas = [c for c in citas if c.fecha == filtro_fecha]
        
        # Enriquecer con información del paciente y médico
        citas_detalladas = []
        for cita in citas:
            paciente = self.modelo_pacientes.obtener_paciente_por_cedula(cita.id_paciente)
            medico = self.modelo_medicos.obtener_medico_por_id(cita.id_medico)
            
            cita_detalle = cita.to_dict()
            cita_detalle["paciente_nombre"] = paciente.nombre_completo() if paciente else "Desconocido"
            cita_detalle["medico_nombre"] = medico.nombre_completo() if medico else "Desconocido"
            cita_detalle["especialidad"] = medico.especialidad if medico else "N/A"
            
            citas_detalladas.append(cita_detalle)
        
        return citas_detalladas
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        # Ya no hay ventanas Toplevel que cerrar, solo limpiar root
        # Usar after() para evitar parpadeo al crear login
        self.root.after(50, self._mostrar_login)
    
    def _mostrar_login(self):
        """Método auxiliar para mostrar el login"""
        if self.login_controlador:
            self.login_controlador.mostrar_login()