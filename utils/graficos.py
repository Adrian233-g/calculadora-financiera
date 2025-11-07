"""
Utilidades para exportar gráficos de Plotly a imágenes.
Preserva el estilo y apariencia exacta de los gráficos web.
"""
import io
import streamlit as st

def exportar_grafico_a_imagen(fig):
    """
    Exporta un gráfico de Plotly a bytes de imagen PNG, preservando el estilo exacto.
    
    Args:
        fig: Figura de plotly.graph_objects
        
    Returns:
        bytes: Imagen en formato PNG con el estilo exacto de Plotly, o None si falla
    """
    try:
        import plotly.io as pio
        
        # Configurar el renderizador para máxima fidelidad visual
        # Usar tamaño grande para alta resolución en el PDF
        img_bytes = pio.to_image(
            fig, 
            format="png",
            width=1400,      # Ancho alto para buena resolución
            height=700,      # Altura proporcionada
            scale=2,         # Escala 2x para mayor calidad (equivalente a retina)
            engine="kaleido" # Motor de renderizado nativo de Plotly
        )
        return img_bytes
        
    except Exception as e:
        # Si falla kaleido, intentar con write_image (método alternativo)
        try:
            img_bytes = io.BytesIO()
            fig.write_image(
                img_bytes, 
                format="png",
                width=1400,
                height=700,
                scale=2
            )
            img_bytes.seek(0)
            return img_bytes.getvalue()
            
        except Exception as e2:
            # Último intento: sin especificar engine (usa el disponible)
            try:
                import plotly.io as pio
                img_bytes = pio.to_image(
                    fig,
                    format="png",
                    width=1400,
                    height=700,
                    scale=2
                )
                return img_bytes
                
            except Exception as e3:
                # Si todo falla, mostrar advertencia informativa
                if 'grafico_warning_shown' not in st.session_state:
                    st.error(
                        "❌ **Error al generar imágenes para el PDF**\n\n"
                        "Las gráficas no estarán disponibles en el reporte PDF.\n\n"
                        "**Solución**: Esto ocurre porque faltan dependencias del sistema. "
                        "Si estás en Streamlit Cloud, contacta al administrador para que agregue "
                        "el archivo `packages.txt` con las dependencias necesarias.\n\n"
                        f"**Detalles técnicos**: {str(e3)}"
                    )
                    st.session_state['grafico_warning_shown'] = True
                return None
