from vista.Menu_administrador import Menu_administrador_vista
from vista.Modificar_tarifas import Modificar_tarifas_vista
from vista.Beneficios import Beneficios_vista
from modelo.tipo_consulta import Modelo_tipos_consulta 
from modelo.catalogos import Catalogo_aseguradoras
import tkinter as tk

class Controlador_administrador:
    def __init__(self, root, usuario_actual=None, login_controlador=None):
        self.root = root
        self.usuario_actual = usuario_actual
        self.login_controlador = login_controlador
        
        # Inicializar modelos
        self.modelo_tipos_consulta = Modelo_tipos_consulta()
        self.catalogo_aseguradoras = Catalogo_aseguradoras()

    def mostrar(self):
        """Muestra la vista principal del menú de administrador"""
        self.vista = Menu_administrador_vista(self, self.root)

    def mostrar_modificar_tarifas(self):
        """Abre la ventana para modificar tarifas de tipos de consulta"""
        self.root.after(50, lambda: Modificar_tarifas_vista(self, self.root))

    def mostrar_beneficios(self):
        """Abre la ventana para gestionar beneficios de aseguradoras"""
        self.root.after(50, lambda: Beneficios_vista(self, self.root))

    # Métodos para tipos de consulta
    def obtener_tipos_consulta(self):
        """Retorna todos los tipos de consulta del sistema"""
        return self.modelo_tipos_consulta.obtener_todos_los_tipos_consulta()

    def obtener_tipos_consulta_activos(self):
        """Retorna solo los tipos de consulta activos"""
        return self.modelo_tipos_consulta.obtener_tipos_consulta_activos()

    def actualizar_precio_tipo_consulta(self, id_tipo_consulta, nuevo_precio):
        """Actualiza el precio base de un tipo de consulta"""
        return self.modelo_tipos_consulta.actualizar_precio_tipo_consulta(id_tipo_consulta, nuevo_precio)

    def agregar_tipo_consulta(self, nombre, descripcion, precio_base):
        """Agrega un nuevo tipo de consulta al sistema"""
        return self.modelo_tipos_consulta.agregar_tipo_consulta(nombre, descripcion, precio_base)

    def actualizar_tarifas(self, tarifas_actualizadas):
        """Actualiza las tarifas de tipos de consulta en el sistema"""
        try:
            # Debug: Verificar estructura de datos
            print(f"DEBUG - Estructura de tarifas_actualizadas: {tarifas_actualizadas}")
            
            # Validar que todas las tarifas tengan el formato correcto
            for i, tarifa in enumerate(tarifas_actualizadas):
                print(f"DEBUG - Tarifa {i}: {tarifa}, tipo: {type(tarifa)}")
                
                # Verificar si es un diccionario
                if isinstance(tarifa, dict):
                    # Extraer los datos necesarios del diccionario
                    id_tipo = tarifa.get('id_tipo_consulta')
                    nombre = tarifa.get('nombre')
                    precio = tarifa.get('precio_base')
                    
                    # Validar que los campos requeridos existan
                    if not id_tipo or not nombre or precio is None:
                        error_msg = f"Tarifa inválida - faltan campos requeridos: {tarifa}"
                        raise ValueError(error_msg)
                    
                else:
                    raise ValueError(f"Formato de tarifa inválido en posición {i}: {tarifa}")
                
                # Validar el precio
                if precio is None:
                    error_msg = f"Precio no puede ser None para {nombre}"
                    raise ValueError(error_msg)
                
                try:
                    # Limpiar el precio de posibles formatos
                    precio_limpio = str(precio).strip()
                    precio_limpio = precio_limpio.replace(',', '').replace(' ', '').replace('$', '')
                    
                    # Convertir a float
                    precio_numerico = float(precio_limpio)
                    
                    if precio_numerico < 0:
                        error_msg = f"El precio no puede ser negativo: {precio}"
                        raise ValueError(error_msg)
                    
                    if precio_numerico > 10000000:
                        error_msg = f"El precio es demasiado alto: {precio}"
                        raise ValueError(error_msg)
                    
                    print(f"DEBUG - Procesando tarifa: {nombre} - Precio: {precio_numerico}")
                        
                except (ValueError, TypeError) as e:
                    error_msg = f"Precio inválido para {nombre}: {precio}. Error: {str(e)}"
                    raise ValueError(error_msg)
            
            # Actualizar en la base de datos usando el modelo
            resultado = self.modelo_tipos_consulta.actualizar_multiples_precios(tarifas_actualizadas)
            
            print("DEBUG - Todas las tarifas validadas y actualizadas correctamente")
            return resultado
            
        except Exception as e:
            # Log del error
            import traceback
            traceback.print_exc()
            print(f"Error en actualizar_tarifas: {str(e)}")
            return False

    # Métodos para aseguradoras
    def obtener_aseguradoras(self):
        """Retorna todas las aseguradoras del sistema"""
        return self.catalogo_aseguradoras.obtener_todas()

    def obtener_aseguradoras_activas(self):
        """Retorna solo las aseguradoras activas"""
        return self.catalogo_aseguradoras.obtener_todas()  # Ya filtra por activas

    def actualizar_descuento_aseguradora(self, id_aseguradora, nuevo_descuento):
        """Actualiza el descuento de una aseguradora"""
        return self.catalogo_aseguradoras.actualizar_descuento(id_aseguradora, nuevo_descuento)

    def actualizar_beneficios(self, beneficios_actualizados):
        """Actualiza los beneficios/descuentos de aseguradoras en el sistema"""
        try:
            # Debug: Verificar estructura de datos
            print(f"DEBUG - Estructura de beneficios_actualizados: {beneficios_actualizados}")
            
            # Validar que todos los beneficios tengan el formato correcto
            for i, beneficio in enumerate(beneficios_actualizados):
                print(f"DEBUG - Beneficio {i}: {beneficio}, tipo: {type(beneficio)}")
                
                # Si es un diccionario (formato de aseguradora)
                if isinstance(beneficio, dict):
                    id_aseguradora = beneficio.get('id_aseguradora') or beneficio.get('id')
                    nombre = beneficio.get('nombre')
                    descuento = beneficio.get('descuento_general') or beneficio.get('descuento_porcentaje')
                    
                    if not id_aseguradora or not nombre or descuento is None:
                        raise ValueError(f"Beneficio inválido - faltan campos requeridos: {beneficio}")
                    
                    # Validar descuento
                    try:
                        descuento_numerico = float(descuento)
                        if descuento_numerico < 0 or descuento_numerico > 100:
                            raise ValueError(f"Descuento inválido para {nombre}: {descuento}")
                    except ValueError:
                        raise ValueError(f"Formato de descuento inválido para {nombre}: {descuento}")
                        
                else:
                    raise ValueError(f"Formato de beneficio inválido en posición {i}: {beneficio}")
            
            # Actualizar en la base de datos usando el catálogo
            resultado = self.catalogo_aseguradoras.actualizar_multiples_descuentos(beneficios_actualizados)
            
            print("DEBUG - Todos los beneficios validados y actualizados correctamente")
            return resultado
            
        except Exception as e:
            # Log del error
            import traceback
            traceback.print_exc()
            print(f"Error en actualizar_beneficios: {str(e)}")
            return False

    def desactivar_tipo_consulta(self, id_tipo_consulta):
        """Desactiva un tipo de consulta del sistema"""
        return self.modelo_tipos_consulta.desactivar_tipo_consulta(id_tipo_consulta)

    def activar_tipo_consulta(self, id_tipo_consulta):
        """Activa un tipo de consulta del sistema"""
        return self.modelo_tipos_consulta.activar_tipo_consulta(id_tipo_consulta)

    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        self.root.after(50, self._mostrar_login)
    
    def _mostrar_login(self):
        """Método auxiliar para mostrar el login"""
        if self.login_controlador:
            self.login_controlador.mostrar_login()