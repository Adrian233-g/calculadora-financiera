"""
Utilidades para exportar gráficos de Plotly a imágenes.
Maneja la compatibilidad con Streamlit Cloud donde Kaleido puede no funcionar.
"""
import io
import streamlit as st

def exportar_grafico_a_imagen(fig):
    """
    Exporta un gráfico de Plotly a bytes de imagen PNG.
    Intenta múltiples métodos para máxima compatibilidad.
    
    Args:
        fig: Figura de plotly.graph_objects
        
    Returns:
        bytes: Imagen en formato PNG, o None si todos los métodos fallan
    """
    # Método 1: Intentar con plotly.io.to_image (usa kaleido internamente)
    try:
        import plotly.io as pio
        img_bytes = pio.to_image(fig, format="png", width=1100, height=600)
        return img_bytes
    except Exception as e1:
        # Método 2: Intentar con write_image a BytesIO
        try:
            img_bytes = io.BytesIO()
            fig.write_image(img_bytes, format="png", width=1100, height=600)
            img_bytes.seek(0)
            return img_bytes.getvalue()
        except Exception as e2:
            # Método 3: Usar matplotlib como alternativa robusta
            try:
                import matplotlib.pyplot as plt
                from PIL import Image
                import numpy as np
                
                # Convertir Plotly a imagen usando renderer estático
                img_bytes = io.BytesIO()
                
                # Crear una figura de matplotlib basada en los datos de plotly
                fig_mpl, ax = plt.subplots(figsize=(11, 6))
                
                # Extraer datos del gráfico de Plotly
                for trace in fig.data:
                    if hasattr(trace, 'x') and hasattr(trace, 'y'):
                        ax.plot(trace.x, trace.y, label=trace.name if trace.name else '')
                
                # Configurar el gráfico
                if fig.layout.title:
                    ax.set_title(str(fig.layout.title.text) if hasattr(fig.layout.title, 'text') else str(fig.layout.title))
                if fig.layout.xaxis and fig.layout.xaxis.title:
                    ax.set_xlabel(str(fig.layout.xaxis.title.text) if hasattr(fig.layout.xaxis.title, 'text') else str(fig.layout.xaxis.title))
                if fig.layout.yaxis and fig.layout.yaxis.title:
                    ax.set_ylabel(str(fig.layout.yaxis.title.text) if hasattr(fig.layout.yaxis.title, 'text') else str(fig.layout.yaxis.title))
                
                if len(fig.data) > 1:
                    ax.legend()
                ax.grid(True, alpha=0.3)
                
                # Guardar como PNG
                plt.tight_layout()
                plt.savefig(img_bytes, format='png', dpi=100, bbox_inches='tight')
                plt.close(fig_mpl)
                
                img_bytes.seek(0)
                return img_bytes.getvalue()
                
            except Exception as e3:
                # Si todo falla, mostrar advertencia UNA SOLA VEZ usando session_state
                if 'grafico_warning_shown' not in st.session_state:
                    st.warning(
                        "⚠️ No se pudieron generar las imágenes de los gráficos para el PDF. "
                        "Los gráficos se mostrarán en pantalla pero no estarán disponibles en el reporte PDF. "
                        "Esto puede ocurrir en algunos entornos de despliegue."
                    )
                    st.session_state['grafico_warning_shown'] = True
                return None
