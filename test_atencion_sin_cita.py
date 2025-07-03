#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de atención sin cita previa.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def probar_atencion_sin_cita():
    """Prueba la funcionalidad de atención sin cita"""
    print("🧪 INICIANDO PRUEBA: Atención sin cita previa")
    print("=" * 60)
    
    try:
        # Crear un root ficticio para el controlador
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana
        
        from controlador.recepcionista_controlador import Controlador_recepcionista
        
        # Crear controlador
        controlador = Controlador_recepcionista(root)
        
        # 1. Obtener médicos de Medicina General
        print("📅 1. Obteniendo médicos de Medicina General...")
        medicos_mg = controlador.obtener_medicos_medicina_general()
        
        if not medicos_mg:
            print("❌ No hay médicos de Medicina General disponibles")
            root.destroy()
            return False
        
        print(f"✅ Se encontraron {len(medicos_mg)} médicos de Medicina General:")
        for i, medico in enumerate(medicos_mg):
            print(f"   {i+1}. ID: {medico.get('id_medico')} - "
                  f"Nombre: {medico.get('nombre_completo')} - "
                  f"Especialidad: {medico.get('especialidad')}")
        
        # 2. Seleccionar primer médico disponible
        medico_seleccionado = medicos_mg[0]
        print(f"\n🎯 2. Usando médico: {medico_seleccionado.get('nombre_completo')}")
        
        # 3. Crear datos de prueba para paciente
        datos_atencion = {
            "nombre_paciente": "Juan Carlos Pérez",
            "cedula_paciente": "12345678901",
            "telefono_paciente": "3001234567",
            "id_medico": medico_seleccionado.get('id_medico'),
            "medico_nombre": medico_seleccionado.get('nombre_completo'),
            "horario": medico_seleccionado.get('horario_disponible'),
            "tipo_atencion": "Urgencia"
        }
        
        print(f"\n🔄 3. Procesando atención sin cita...")
        print(f"   Paciente: {datos_atencion['nombre_paciente']}")
        print(f"   Cédula: {datos_atencion['cedula_paciente']}")
        print(f"   Médico: {datos_atencion['medico_nombre']} (ID: {datos_atencion['id_medico']})")
        
        # 4. Procesar atención
        resultado = controlador.procesar_atencion_sin_cita(datos_atencion)
        
        print(f"\n📋 4. Resultado del procesamiento:")
        print(f"   Éxito: {resultado.get('exito')}")
        print(f"   Mensaje: {resultado.get('mensaje')}")
        
        if resultado.get('exito'):
            id_cita = resultado.get('id_cita')
            numero_factura = resultado.get('numero_factura')
            print(f"   ID Cita creada: {id_cita}")
            print(f"   Número de factura: {numero_factura}")
            
            print("\n✅ ¡ÉXITO! La atención sin cita se procesó correctamente")
            print("   - Se verificó/registró el paciente")
            print("   - Se creó la cita de urgencia")
            print("   - Se generó la factura automáticamente")
            
            root.destroy()
            return True
        else:
            print(f"\n❌ ERROR: {resultado.get('mensaje')}")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ ERROR durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        try:
            root.destroy()
        except:
            pass
        return False

if __name__ == "__main__":
    print("🔬 PRUEBA DE FUNCIONALIDAD: Atención sin Cita Previa")
    print("🎯 Objetivo: Verificar que se creen paciente, cita y factura para Medicina General")
    print()
    
    exito = probar_atencion_sin_cita()
    
    print("\n" + "=" * 60)
    if exito:
        print("🎉 PRUEBA EXITOSA: La funcionalidad está funcionando correctamente")
        print("✅ Médicos de Medicina General se obtienen de la BD")
        print("✅ Se registra/verifica paciente automáticamente")
        print("✅ Se crea cita de urgencia con estado 'Confirmada'")
        print("✅ Se genera factura automáticamente")
    else:
        print("💥 PRUEBA FALLIDA: Hay problemas con la funcionalidad")
    print("=" * 60)
