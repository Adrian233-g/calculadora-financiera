import streamlit as st

def validar_monto(monto, nombre="Monto"):
    """Valida que el monto sea no negativo"""
    if monto < 0:
        st.error(f"❌ {nombre} no puede ser negativo")
        return False
    return True

def validar_tea(tea):
    """Valida que la TEA esté en el rango permitido"""
    if tea < 0 or tea > 50:
        st.error("❌ La TEA debe estar entre 0% y 50%")
        return False
    return True

def validar_edad(edad_actual, edad_jubilacion):
    """Valida que las edades sean coherentes"""
    if edad_actual < 18:
        st.error("❌ La edad actual debe ser al menos 18 años")
        return False
    if edad_jubilacion <= edad_actual:
        st.error("❌ La edad de jubilación debe ser mayor a la edad actual")
        return False
    if edad_jubilacion > 100:
        st.error("❌ La edad de jubilación debe ser menor a 100 años")
        return False
    return True

def validar_anos(anos, nombre="Plazo"):
    """Valida que los años sean positivos"""
    if anos <= 0:
        st.error(f"❌ {nombre} debe ser mayor a 0")
        return False
    if anos > 80:
        st.error(f"❌ {nombre} no puede exceder 80 años")
        return False
    return True

def validar_campos_completos(**campos):
    """Verifica que todos los campos requeridos estén llenos"""
    faltantes = [nombre for nombre, valor in campos.items() if valor is None or valor == ""]
    if faltantes:
        st.warning(f"⚠️ Por favor completa los siguientes campos: {', '.join(faltantes)}")
        return False
    return True