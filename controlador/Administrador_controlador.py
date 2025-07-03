from vista.Menu_administrador import Menu_administrador_vista
from vista.Modificar_tarifas import Modificar_tarifas_vista
from vista.Beneficios import Beneficios_vista
from modelo.servicio import Modelo_servicios_adicionales
from modelo.paciente import Modelo_pacientes
from modelo.consulta import Modelo_consultas
import tkinter as tk

class Controlador_administrador:
    def __init__(self, root, usuario_actual=None, login_controlador=None):
        self.root = root
        self.usuario_actual = usuario_actual
        self.login_controlador = login_controlador
        
        # Inicializar modelos
        # Los servicios adicionales usan métodos estáticos, no necesitan instancia
        self.modelo_pacientes = Modelo_pacientes()
        self.modelo_consultas = Modelo_consultas()

    def mostrar(self):
        """Muestra la vista principal del menú de administrador"""
        self.vista = Menu_administrador_vista(self, self.root)

    def mostrar_modificar_tarifas(self):
        """Abre la ventana para modificar tarifas de servicios"""
        # Ya no necesitamos withdraw() porque no usamos Toplevel
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Modificar_tarifas_vista(self, self.root))

    def mostrar_beneficios(self):
        """Abre la ventana para gestionar beneficios"""
        # Ya no necesitamos withdraw() porque no usamos Toplevel
        # Usar after() para evitar parpadeo al crear nueva ventana
        self.root.after(50, lambda: Beneficios_vista(self, self.root))

    # Métodos para interactuar con los modelos
    def obtener_servicios(self):
        """Retorna todos los servicios del sistema"""
        return Modelo_servicios_adicionales.obtener_todos_los_servicios()

    def obtener_servicios_por_categoria(self, categoria):
        """Retorna servicios de una categoría específica"""
        return Modelo_servicios_adicionales.obtener_servicios_por_categoria(categoria)

    def actualizar_precio_servicio(self, id_servicio, nuevo_precio):
        """Actualiza el precio de un servicio"""
        # TODO: Implementar actualización de precio en BD
        print(f"⚠️ Funcionalidad pendiente: Actualizar precio de {id_servicio} a ${nuevo_precio}")
        return True

    def agregar_servicio(self, nombre, descripcion, precio, categoria):
        """Agrega un nuevo servicio al sistema"""
        # TODO: Implementar inserción de nuevo servicio en BD
        print(f"⚠️ Funcionalidad pendiente: Agregar servicio {nombre} - ${precio}")
        return None

    def actualizar_tarifas(self, tarifas_actualizadas):
        """Actualiza las tarifas de consulta en el sistema"""
        try:
            
            # En un sistema real, esto actualizaría la base de datos a través del modelo
            # Por ahora, simulamos la actualización exitosa
            
            # Validar que todas las tarifas tengan el formato correcto
            for i, (tipo, precio) in enumerate(tarifas_actualizadas):
                
                if not tipo or not precio:
                    error_msg = f"Tarifa inválida: {tipo} - {precio}"
                    raise ValueError(error_msg)
                
                try:
                    # Limpiar el precio de posibles formatos (comas, espacios, símbolos)
                    precio_limpio = str(precio).strip()
                    
                    # Remover comas, espacios y otros caracteres no numéricos excepto punto decimal
                    precio_limpio = precio_limpio.replace(',', '').replace(' ', '').replace('$', '')
                    
                    # Convertir a float
                    precio_numerico = float(precio_limpio)
                    
                    if precio_numerico < 0:
                        error_msg = f"El precio no puede ser negativo: {precio}"
                        raise ValueError(error_msg)
                    
                    # Validar que sea un precio razonable (por ejemplo, entre 0 y 1,000,000)
                    if precio_numerico > 1000000:
                        error_msg = f"El precio es demasiado alto: {precio}"
                        raise ValueError(error_msg)
                        
                except (ValueError, TypeError) as e:
                    error_msg = f"Precio inválido para {tipo}: {precio}. Error: {str(e)}"
                    raise ValueError(error_msg)
            
            # Aquí se actualizaría el modelo de tarifas
            # Por ejemplo: self.modelo_tarifas.actualizar_multiple(tarifas_actualizadas)
            
            # Simulamos una actualización exitosa
            return True
            
        except Exception as e:
            # Log del error (en un sistema real)
            import traceback
            traceback.print_exc()
            return False

    def actualizar_beneficios(self, beneficios_actualizados):
        """Actualiza los beneficios de entidades en el sistema"""
        try:
            # En un sistema real, esto actualizaría la base de datos a través del modelo
            # Por ahora, simulamos la actualización exitosa
            
            # Validar que todos los beneficios tengan el formato correcto
            for entidad, beneficio, descuento in beneficios_actualizados:
                if not entidad or not beneficio or not descuento:
                    raise ValueError(f"Beneficio inválido: {entidad} - {beneficio} - {descuento}")
                
                # Validar formato de descuento
                descuento_limpio = descuento.strip()
                if descuento_limpio.endswith('%'):
                    try:
                        porcentaje = float(descuento_limpio[:-1])
                        if porcentaje < 0 or porcentaje > 100:
                            raise ValueError(f"Porcentaje de descuento inválido para {entidad}: {descuento}")
                    except ValueError:
                        raise ValueError(f"Formato de porcentaje inválido para {entidad}: {descuento}")
                elif descuento_limpio.replace('.', '').isdigit():
                    try:
                        valor = float(descuento_limpio)
                        if valor < 0:
                            raise ValueError(f"Valor de descuento no puede ser negativo para {entidad}: {descuento}")
                    except ValueError:
                        raise ValueError(f"Valor de descuento inválido para {entidad}: {descuento}")
                else:
                    raise ValueError(f"Formato de descuento inválido para {entidad}: {descuento}")
            
            # Aquí se actualizaría el modelo de beneficios
            # Por ejemplo: self.modelo_beneficios.actualizar_multiple(beneficios_actualizados)
            
            # Simulamos una actualización exitosa
            return True
            
        except Exception as e:
            # Log del error (en un sistema real)
            print(f"Error al actualizar beneficios: {str(e)}")
            return False

    def desactivar_servicio(self, id_servicio):
        """Desactiva un servicio del sistema"""
        # TODO: Implementar desactivación en BD
        print(f"⚠️ Funcionalidad pendiente: Desactivar servicio {id_servicio}")
        return True

    def obtener_categorias_servicios(self):
        """Retorna todas las categorías de servicios"""
        return Modelo_servicios_adicionales.obtener_categorias_disponibles()

    def obtener_estadisticas_servicios(self):
        """Retorna estadísticas básicas de los servicios"""
        servicios = Modelo_servicios_adicionales.obtener_todos_los_servicios()
        activos = len(servicios)  # Todos los obtenidos están activos
        
        return {
            "total_servicios": len(servicios),
            "servicios_activos": activos,
            "servicios_inactivos": 0,  # No tenemos función para inactivos
            "categorias": len(Modelo_servicios_adicionales.obtener_categorias_disponibles())
        }

    def obtener_pacientes_con_deuda(self):
        """Retorna pacientes que tienen deuda pendiente"""
        pacientes = self.modelo_pacientes.obtener_todos_los_pacientes()
        return [p for p in pacientes if p.deuda > 0]

    def calcular_ingresos_totales(self):
        """Calcula los ingresos totales basados en las consultas"""
        consultas = self.modelo_consultas.obtener_todas_las_consultas()
        # En un sistema real, esto vendría de un modelo de facturación
        # Por ahora, simulamos con datos de ejemplo
        return sum(50.0 for c in consultas if c.estado == "Completada")

    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        # Ya no hay ventanas Toplevel que cerrar, solo limpiar root
        # Usar after() para evitar parpadeo al crear login
        self.root.after(50, self._mostrar_login)
    
    def _mostrar_login(self):
        """Método auxiliar para mostrar el login"""
        if self.login_controlador:
            self.login_controlador.mostrar_login()