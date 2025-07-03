# modelo/consulta.py
from datetime import datetime
import random

class Consulta:
    def __init__(self, id_consulta, id_cita, id_paciente, id_medico, 
                 fecha_consulta=None, diagnostico="", tratamiento="", 
                 observaciones="", estado="Pendiente"):
        self.id_consulta = id_consulta
        self.id_cita = id_cita
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.fecha_consulta = fecha_consulta or datetime.now()
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.estado = estado  # Pendiente, En proceso, Completada
        self.medicamentos_recetados = []
        self.examenes_solicitados = []

    def agregar_medicamento(self, nombre_medicamento, dosis, frecuencia, duracion):
        """Agrega un medicamento recetado"""
        medicamento = {
            "nombre": nombre_medicamento,
            "dosis": dosis,
            "frecuencia": frecuencia,
            "duracion": duracion
        }
        self.medicamentos_recetados.append(medicamento)

    def agregar_examen(self, tipo_examen, descripcion=""):
        """Agrega un examen solicitado"""
        examen = {
            "tipo": tipo_examen,
            "descripcion": descripcion,
            "fecha_solicitud": datetime.now(),
            "estado": "Solicitado"
        }
        self.examenes_solicitados.append(examen)

    def to_dict(self):
        """Convierte la consulta a diccionario"""
        return {
            "id_consulta": self.id_consulta,
            "id_cita": self.id_cita,
            "id_paciente": self.id_paciente,
            "id_medico": self.id_medico,
            "fecha_consulta": self.fecha_consulta.strftime("%Y-%m-%d %H:%M") if isinstance(self.fecha_consulta, datetime) else self.fecha_consulta,
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "observaciones": self.observaciones,
            "estado": self.estado,
            "medicamentos": self.medicamentos_recetados,
            "examenes": self.examenes_solicitados
        }

class Modelo_consultas:
    def __init__(self):
        self.consultas = []
        self.contador_id = 1
        self._generar_consultas_ejemplo()

    def _generar_consultas_ejemplo(self):
        """Genera consultas de ejemplo"""
        diagnosticos = [
            "Hipertensión arterial", "Diabetes tipo 2", "Gastritis", 
            "Migraña", "Gripe común", "Bronquitis", "Dermatitis",
            "Ansiedad", "Lumbalgia", "Faringitis"
        ]
        
        tratamientos = [
            "Medicación y dieta baja en sodio",
            "Control glucémico y ejercicio",
            "Medicación antiácida y dieta",
            "Analgésicos y descanso",
            "Antivirales y reposo",
            "Antibióticos y expectorantes",
            "Cremas tópicas y antihistamínicos",
            "Terapia psicológica y relajación",
            "Fisioterapia y antiinflamatorios",
            "Antibióticos y gárgaras"
        ]

        for i in range(15):
            consulta = Consulta(
                id_consulta=self.contador_id,
                id_cita=f"CITA{random.randint(1, 50)}",
                id_paciente=f"PAC{random.randint(100, 999)}",
                id_medico=f"MED{random.randint(1, 10)}",
                fecha_consulta=datetime.now(),
                diagnostico=random.choice(diagnosticos),
                tratamiento=random.choice(tratamientos),
                observaciones=f"Observaciones para consulta {self.contador_id}",
                estado=random.choice(["Completada", "En proceso", "Pendiente"])
            )
            
            # Agregar algunos medicamentos y exámenes aleatorios
            if random.choice([True, False]):
                consulta.agregar_medicamento("Ibuprofeno", "400mg", "Cada 8 horas", "5 días")
            
            if random.choice([True, False]):
                consulta.agregar_examen("Análisis de sangre", "Hemograma completo")
            
            self.consultas.append(consulta)
            self.contador_id += 1

    def crear_consulta(self, id_cita, id_paciente, id_medico, diagnostico="", 
                      tratamiento="", observaciones=""):
        """Crea una nueva consulta"""
        nueva_consulta = Consulta(
            id_consulta=self.contador_id,
            id_cita=id_cita,
            id_paciente=id_paciente,
            id_medico=id_medico,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            observaciones=observaciones
        )
        
        self.consultas.append(nueva_consulta)
        self.contador_id += 1
        return nueva_consulta

    def obtener_todas_las_consultas(self):
        """Retorna todas las consultas"""
        return self.consultas

    def obtener_consulta_por_id(self, id_consulta):
        """Busca una consulta por su ID"""
        for consulta in self.consultas:
            if consulta.id_consulta == id_consulta:
                return consulta
        return None

    def obtener_consultas_por_paciente(self, id_paciente):
        """Retorna las consultas de un paciente específico"""
        return [consulta for consulta in self.consultas if consulta.id_paciente == id_paciente]

    def obtener_consultas_por_medico(self, id_medico):
        """Retorna las consultas de un médico específico"""
        return [consulta for consulta in self.consultas if consulta.id_medico == id_medico]

    def obtener_consultas_por_fecha(self, fecha):
        """Retorna las consultas de una fecha específica"""
        consultas_fecha = []
        for consulta in self.consultas:
            if isinstance(consulta.fecha_consulta, datetime):
                if consulta.fecha_consulta.date() == fecha:
                    consultas_fecha.append(consulta)
        return consultas_fecha

    def actualizar_estado_consulta(self, id_consulta, nuevo_estado):
        """Actualiza el estado de una consulta"""
        consulta = self.obtener_consulta_por_id(id_consulta)
        if consulta:
            consulta.estado = nuevo_estado
            return True
        return False

    def completar_consulta(self, id_consulta, diagnostico, tratamiento, observaciones=""):
        """Completa una consulta con diagnóstico y tratamiento"""
        consulta = self.obtener_consulta_por_id(id_consulta)
        if consulta:
            consulta.diagnostico = diagnostico
            consulta.tratamiento = tratamiento
            consulta.observaciones = observaciones
            consulta.estado = "Completada"
            return True
        return False

    def obtener_estadisticas_consultas(self):
        """Retorna estadísticas básicas de las consultas"""
        total = len(self.consultas)
        completadas = len([c for c in self.consultas if c.estado == "Completada"])
        pendientes = len([c for c in self.consultas if c.estado == "Pendiente"])
        en_proceso = len([c for c in self.consultas if c.estado == "En proceso"])
        
        return {
            "total_consultas": total,
            "completadas": completadas,
            "pendientes": pendientes,
            "en_proceso": en_proceso,
            "porcentaje_completadas": (completadas / total * 100) if total > 0 else 0
        }
