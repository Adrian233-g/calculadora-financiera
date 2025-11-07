"""
Utilidades para exportar gráficos de Plotly a imágenes.
Maneja la compatibilidad con Streamlit Cloud donde Kaleido puede no funcionar.
"""
import io
import streamlit as st

def exportar_grafico_a_imagen(fig):
    """
    Exporta un gráfico de Plotly a bytes de imagen PNG.
    
    Args:
        fig: Figura de plotly.graph_objects
        
    Returns:
        bytes: Imagen en formato PNG, o None si falla la exportación
    """
    try:
        # Intenta usar Kaleido (funciona localmente)
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format="png")
        img_bytes.seek(0)
        return img_bytes.getvalue()
    except Exception as e:
        # Si falla (como en Streamlit Cloud), intenta con plotly.io directamente
        try:
            import plotly.io as pio
            img_bytes = pio.to_image(fig, format="png")
            return img_bytes
        except Exception as e2:
            # Si también falla, muestra advertencia y devuelve None
            st.warning(
                "⚠️ No se pudo generar la imagen del gráfico para el PDF. "
                "El gráfico se mostrará en pantalla pero no estará disponible en el reporte PDF. "
                "Esto es normal en algunos entornos de despliegue."
            )
            return None
