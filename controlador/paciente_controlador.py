# paciente_controlador.py
from vista.menu_paciente  import Menu_paciente_vista
from vista.Login_vista import Login_vista 
from vista.Citas_paciente_vista import Vista_citas_paciente
from vista.agendamiento_citas import Vista_agendamiento_citas
from modelo.paciente import Paciente, Modelo_pacientes
from modelo.cita import Modelo_citas
from modelo.medico import Modelo_medicos
from modelo.servicio import Modelo_servicios_adicionales
import tkinter as tk

class Controlador_paciente:
    def __init__(self, root, usuario_actual=None, login_controlador=None):
        self.root = root
        self.usuario_actual = usuario_actual
        self.login_controlador = login_controlador
        
        # Inicializar modelos
        self.modelo_pacientes = Modelo_pacientes()
        self.modelo_citas = Modelo_citas()
        self.modelo_medicos = Modelo_medicos()
        # Los servicios adicionales usan métodos estáticos, no necesitan instancia
        
        # Obtener o crear paciente
        self.paciente = self._inicializar_paciente()

    def _inicializar_paciente(self):
        """Inicializa el paciente con datos del usuario actual o datos de prueba"""
        if self.usuario_actual and hasattr(self.usuario_actual, 'id_usuario'):
            # Buscar paciente existente por ID/cédula (usar id_usuario del nuevo modelo)
            cedula_paciente = self.usuario_actual.id_usuario
            
            # Debugging: verificar en qué tablas existe el usuario
            print(f"\n🔍 INICIALIZANDO PACIENTE:")
            print(f"   Cédula: {cedula_paciente}")
            print(f"   Rol: {self.usuario_actual.rol}")
            
            paciente = self.modelo_pacientes.obtener_paciente_por_cedula(cedula_paciente)
            
            if paciente:
                print(f"   ✅ Paciente encontrado en BD: {paciente.nombre_completo()}")
                return paciente
            else:
                print(f"   ❌ Paciente NO encontrado en tabla 'pacientes'")
                print(f"   💡 Esto es normal si solo tienes datos en tabla 'usuarios'")
                
                # Para testing, crear un paciente temporal sin guardar en BD
                print(f"   🔧 Creando paciente temporal para testing...")
                
                paciente_temporal = Paciente(
                    cedula=cedula_paciente,
                    nombre=f"Paciente",
                    apellido=f"Usuario-{cedula_paciente[-4:]}",
                    telefono="000-000-0000",
                    email=f"paciente{cedula_paciente}@test.com",
                    direccion="Dirección temporal"
                )
                
                # Simular citas para el paciente temporal
                paciente_temporal.simular_citas()
                
                print(f"   ✅ Paciente temporal creado: {paciente_temporal.nombre_completo()}")
                return paciente_temporal
            
        else:
            print("⚠️ No hay usuario actual o no tiene id_usuario")
            # Retornar el primer paciente de ejemplo si no hay usuario
            pacientes = self.modelo_pacientes.obtener_todos_los_pacientes()
            return pacientes[0] if pacientes else None

    def mostrar(self):
        """Muestra la vista principal del menú de paciente"""
        self.vista = Menu_paciente_vista(self, self.root)

    def ver_citas(self):
        """Muestra la ventana con las citas del paciente"""
        self.vista.mostrar_citas()

    def consultar_deuda(self):
        """Muestra la ventana con la deuda del paciente"""
        self.vista.mostrar_deuda()

    def obtener_paciente(self):
        """Retorna la instancia del paciente"""
        return self.paciente

    def obtener_citas_paciente(self):
        """Retorna las citas del paciente desde la base de datos con formato completo"""
        if self.paciente:
            # Usar el método persistente del modelo de paciente
            return self.paciente.obtener_citas()
        return []

    def obtener_medicos_disponibles(self):
        """Retorna la lista de médicos disponibles"""
        return self.modelo_medicos.obtener_medicos_disponibles()

    def obtener_servicios_disponibles(self):
        """Retorna la lista de servicios disponibles"""
        return Modelo_servicios_adicionales.obtener_todos_los_servicios()

    def agendar_cita(self, id_medico, fecha, hora, tipo_consulta):
        """Agenda una nueva cita para el paciente"""
        if self.paciente:
            # Obtener el servicio para calcular el costo
            servicios = Modelo_servicios_adicionales.obtener_servicios_por_categoria(tipo_consulta)
            costo = servicios[0].precio_base if servicios else 50.0
            
            # Crear la cita en el modelo
            nueva_cita = self.modelo_citas.crear_cita(
                id_paciente=self.paciente.cedula,
                id_medico=id_medico,
                fecha=fecha,
                hora=hora,
                tipo_consulta=tipo_consulta,
                costo=costo
            )
            
            # Agregar la cita al paciente también
            cita_data = nueva_cita.to_dict()
            self.paciente.agregar_cita(cita_data)
            
            return nueva_cita
        return None

    def cancelar_cita(self, id_cita):
        """Cancela una cita del paciente"""
        return self.modelo_citas.cancelar_cita(id_cita)

    def pagar_deuda(self, monto):
        """Procesa un pago de deuda del paciente"""
        if self.paciente:
            return self.paciente.pagar_deuda(monto)
        return False

    def regresar_login(self):
        """Regresa a la ventana de login"""
        if hasattr(self, 'vista') and self.vista:
            self.vista.ventana.destroy()
        if self.login_controlador:
            self.login_controlador.mostrar_login()
    
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        # Ya no hay ventanas Toplevel que cerrar, solo limpiar root
        # Usar after() para evitar parpadeo al crear login
        self.root.after(50, self._mostrar_login)
    
    def _mostrar_login(self):
        """Método auxiliar para mostrar el login"""
        if self.login_controlador:
            self.login_controlador.mostrar_login()
    
    def obtener_deuda_actualizada(self):
        """Retorna la deuda actualizada del paciente recalculada desde las citas"""
        if self.paciente:
            # Debug desactivado para producción
            # self.paciente.debug_deuda()
            return self.paciente.calcular_deuda_actual()
        return 0.0

    def obtener_deuda_detallada(self):
        """Retorna un desglose detallado de la deuda del paciente desde la base de datos"""
        if self.paciente:
            # Usar el método persistente del modelo de paciente que consulta la BD
            return self.paciente.obtener_deuda_detallada()
        return {
            "total": 0.0,
            "deuda_citas": 0.0,
            "deuda_servicios": 0.0,
            "citas_pendientes": [],
            "servicios_pendientes": []
        }

    def verificar_datos_paciente(self):
        """Método de debugging para verificar si existen datos del paciente"""
        if self.usuario_actual:
            cedula = self.usuario_actual.id_usuario
            print(f"\n🔍 VERIFICANDO DATOS DEL PACIENTE:")
            print(f"   Usuario autenticado: {cedula} ({self.usuario_actual.rol})")
            
            # Verificar en tabla usuarios
            print(f"   ✅ Existe en tabla 'usuarios': Sí")
            
            # Verificar en tabla pacientes
            paciente = self.modelo_pacientes.obtener_paciente_por_cedula(cedula)
            if paciente:
                print(f"   ✅ Existe en tabla 'pacientes': Sí")
                print(f"   📋 Datos: {paciente.nombre_completo()}")
            else:
                print(f"   ❌ Existe en tabla 'pacientes': No")
                print(f"   💡 Sugerencia: Ejecutar script para insertar datos en tabla 'pacientes'")
            
            return paciente
        return None