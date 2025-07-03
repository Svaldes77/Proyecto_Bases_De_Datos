from vista.menu_director import Menu_director_vista
from vista.Citas_paciente_vista import Vista_citas_paciente
from vista.Consolidado_vista import Vista_consolidado
from vista.Estadisticas_vista import Vista_estadisticas
from vista.Informe_vista import Vista_informe_servicios
from modelo.director import Director_modelo 
from datetime import datetime, timedelta
import tkinter as tk

class Controlador_director:
    def __init__(self, root, usuario_actual=None, login_controlador=None):
        self.root = root
        self.usuario_actual = usuario_actual
        self.login_controlador = login_controlador
        
        # Inicializar modelo del director
        self.director_modelo = Director_modelo()

    def mostrar(self):
        """Muestra la vista principal del menú de director"""
        self.vista = Menu_director_vista(self, self.root)

    # ==================== MOSTRAR VISTAS ESPECÍFICAS ====================
    
    def mostrar_informe_servicios(self):
        """Muestra el informe de servicios"""
        self.root.after(50, lambda: Vista_informe_servicios(self, self.root))

    def mostrar_citas_pacientes(self):
        """Muestra las citas de pacientes"""
        self.root.after(50, lambda: Vista_citas_paciente(self, self.root))

    def mostrar_consolidado_mensual(self):
        """Muestra el consolidado mensual"""
        self.root.after(50, lambda: Vista_consolidado(self, self.root))

    def mostrar_estadisticas(self):
        """Muestra las estadísticas del sistema"""
        self.root.after(50, lambda: Vista_estadisticas(self, self.root))

    # ==================== MÉTODOS PARA ESPECIALIDADES ====================
    
    def obtener_especialidades_con_medicos(self):
        """Obtiene todas las especialidades con la cantidad de médicos"""
        return self.director_modelo.obtener_especialidades_con_medicos()
    
    def obtener_todas_especialidades(self):
        """Obtiene todas las especialidades activas"""
        return self.director_modelo.obtener_todas_especialidades()
    
    def obtener_medicos_por_especialidad(self, id_especialidad):
        """Obtiene todos los médicos de una especialidad específica"""
        return self.director_modelo.obtener_medicos_por_especialidad(id_especialidad)
    
    # ==================== MÉTODOS PARA GRÁFICAS ====================
    
    def obtener_datos_grafico_especialidades(self):
        """Obtiene los datos para crear gráficas de especialidades"""
        return self.director_modelo.obtener_datos_grafico_especialidades()
    
    # ==================== MÉTODOS PARA ESTADÍSTICAS ====================
    
    def obtener_estadisticas_generales(self):
        """Retorna estadísticas generales del sistema"""
        return self.director_modelo.obtener_estadisticas_generales()
    
    # ==================== MÉTODOS PARA BÚSQUEDA DE CITAS ====================
    
    def buscar_citas_paciente(self, cedula_paciente):
        """
        Busca todas las citas de un paciente específico
        
        Args:
            cedula_paciente (str): Cédula del paciente
            
        Returns:
            tuple: (datos_paciente, lista_citas)
        """
        try:
            # Obtener datos del paciente
            datos_paciente = self.director_modelo.obtener_datos_paciente(cedula_paciente)
            
            if not datos_paciente:
                return None, []
            
            # Obtener citas del paciente
            citas = self.director_modelo.buscar_citas_por_paciente(cedula_paciente)
            
            return datos_paciente, citas
            
        except Exception as e:
            print(f"Error en controlador al buscar citas: {e}")
            return None, []
    
    def obtener_datos_paciente(self, cedula_paciente):
        """Obtiene los datos básicos de un paciente"""
        return self.director_modelo.obtener_datos_paciente(cedula_paciente)
    
    # ==================== MÉTODOS PARA INFORMES ====================
    
    def generar_informe_especialidades(self):
        """Genera un informe detallado de especialidades y médicos"""
        return self.director_modelo.generar_informe_especialidades()
    
    def generar_informe_medicos_por_especialidad(self, id_especialidad):
        """Genera un informe detallado de médicos en una especialidad"""
        return self.director_modelo.generar_informe_medicos_por_especialidad(id_especialidad)
    
    def obtener_informe_servicios(self, fecha_inicio=None, fecha_fin=None):
        """Genera informe detallado de servicios - Compatible con versión anterior"""
        # Mantener compatibilidad con la vista existente
        try:
            # Obtener especialidades como "servicios" para compatibilidad
            especialidades = self.director_modelo.obtener_especialidades_con_medicos()
            
            informe = {
                "total_servicios": len(especialidades),
                "servicios_activos": len([esp for esp in especialidades if esp['activo']]),
                "consultas_periodo": 0,  # Se puede implementar después
                "servicios_por_categoria": {},
                "ingresos_estimados": 0.0
            }
            
            # Agrupar especialidades por cantidad de médicos
            for especialidad in especialidades:
                categoria = f"{especialidad['cantidad_medicos']} médicos"
                if categoria not in informe["servicios_por_categoria"]:
                    informe["servicios_por_categoria"][categoria] = {
                        "cantidad": 0,
                        "precio_promedio": 0.0,
                        "servicios": []
                    }
                
                informe["servicios_por_categoria"][categoria]["cantidad"] += 1
                informe["servicios_por_categoria"][categoria]["servicios"].append({
                    "codigo": especialidad['codigo'],
                    "nombre": especialidad['nombre'],
                    "descripcion": especialidad['descripcion'],
                    "cantidad_medicos": especialidad['cantidad_medicos']
                })
            
            return informe
            
        except Exception as e:
            print(f"Error generando informe de servicios: {e}")
            return {
                "total_servicios": 0,
                "servicios_activos": 0,
                "consultas_periodo": 0,
                "servicios_por_categoria": {},
                "ingresos_estimados": 0.0
            }

    def obtener_consolidado_mensual(self, año=None, mes=None):
        """Genera consolidado mensual del sistema"""
        if not año:
            año = datetime.now().year
        if not mes:
            mes = datetime.now().month
            
        try:
            # Obtener estadísticas generales
            estadisticas = self.director_modelo.obtener_estadisticas_generales()
            especialidades = self.director_modelo.obtener_especialidades_con_medicos()
            
            consolidado = {
                "periodo": f"{mes:02d}/{año}",
                "total_citas": 0,  # Se puede implementar después con tabla de citas
                "total_consultas": 0,  # Se puede implementar después
                "total_pacientes": 0,  # Se puede implementar después
                "citas_completadas": 0,
                "consultas_completadas": 0,
                "pacientes_activos": 0,
                "medicos_disponibles": estadisticas.get('medicos_disponibles', 0),
                "total_especialidades": estadisticas.get('total_especialidades', 0),
                "total_medicos": estadisticas.get('total_medicos', 0),
                "especialidades_con_medicos": len([esp for esp in especialidades if esp['cantidad_medicos'] > 0]),
                "especialidades_sin_medicos": len([esp for esp in especialidades if esp['cantidad_medicos'] == 0]),
                "ingresos_estimados": 0.0,
                "deuda_pendiente": 0.0
            }
            
            return consolidado
            
        except Exception as e:
            print(f"Error generando consolidado mensual: {e}")
            return {
                "periodo": f"{mes:02d}/{año}",
                "total_citas": 0,
                "total_consultas": 0,
                "total_pacientes": 0,
                "citas_completadas": 0,
                "consultas_completadas": 0,
                "pacientes_activos": 0,
                "medicos_disponibles": 0,
                "ingresos_estimados": 0.0,
                "deuda_pendiente": 0.0
            }

    def obtener_citas_pacientes(self, filtro_fecha=None):
        """Retorna las citas de pacientes con filtros opcionales"""
        try:
            # Por ahora devolver lista vacía hasta implementar tabla de citas
            # Se puede implementar después agregando el método correspondiente al modelo
            return []
            
        except Exception as e:
            print(f"Error obteniendo citas de pacientes: {e}")
            return []
    
    def obtener_ingresos_servicios_por_fecha(self, anio, mes):
        """
        Obtiene los ingresos por servicios adicionales para un año y mes específicos
        """
        try:
            return self.director_modelo.obtener_ingresos_servicios_por_fecha(anio, mes)
        except Exception as e:
            print(f"Error en controlador al obtener ingresos por servicios: {e}")

            return []
        
    # ...existing code...

    # AGREGAR después del método obtener_datos_paciente (línea ~72):
    def obtener_servicios_adicionales_cita(self, id_cita):
        """
        Obtiene los servicios adicionales de una cita específica
        
        Args:
            id_cita (int): ID de la cita
            
        Returns:
            list: Lista de servicios adicionales
        """
        try:
            return self.director_modelo.obtener_servicios_adicionales_cita(id_cita)
        except Exception as e:
            print(f"Error al obtener servicios adicionales: {e}")
            return []

# ...existing code...
    # ==================== MÉTODOS DE NAVEGACIÓN ====================
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        self.root.after(50, self._mostrar_login)
    
    def _mostrar_login(self):
        """Método auxiliar para mostrar el login"""
        if self.login_controlador:
            self.login_controlador.mostrar_login()