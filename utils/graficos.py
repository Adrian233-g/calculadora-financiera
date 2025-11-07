"""
Utilidades para exportar gráficos de Plotly a imágenes.
Funciona tanto localmente como en Streamlit Cloud sin requerir Chrome/Kaleido.
"""
import io
import streamlit as st

def exportar_grafico_a_imagen(fig):
    """
    Exporta un gráfico de Plotly a bytes de imagen PNG.
    Primero intenta con Kaleido (si está disponible), luego usa matplotlib
    con los colores/estilo exactos de Plotly.
    
    Args:
        fig: Figura de plotly.graph_objects
        
    Returns:
        bytes: Imagen en formato PNG, o None si falla
    """
    # Intento 1: Usar Kaleido si está disponible (desarrollo local)
    try:
        import plotly.io as pio
        img_bytes = pio.to_image(
            fig, 
            format="png",
            width=1400,
            height=700,
            scale=2,
            engine="kaleido"
        )
        return img_bytes
    except:
        pass
    
    # Intento 2: Matplotlib con paleta de colores de Plotly (fallback robusto)
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend sin display
        
        # Paleta de colores de Plotly (plotly_white theme)
        PLOTLY_COLORS = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', 
                         '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
        
        # Crear figura con fondo blanco (como plotly_white)
        fig_mpl, ax = plt.subplots(figsize=(14, 7), facecolor='white')
        ax.set_facecolor('white')
        
        # Extraer y graficar cada trace con el estilo de Plotly
        for idx, trace in enumerate(fig.data):
            color = PLOTLY_COLORS[idx % len(PLOTLY_COLORS)]
            
            if hasattr(trace, 'x') and hasattr(trace, 'y'):
                # Determinar el tipo de gráfico
                trace_type = trace.type if hasattr(trace, 'type') else 'scatter'
                
                if trace_type == 'scatter':
                    mode = trace.mode if hasattr(trace, 'mode') else 'lines'
                    
                    if 'lines' in mode:
                        # Líneas con grosor de Plotly
                        linewidth = trace.line.width if hasattr(trace, 'line') and hasattr(trace.line, 'width') else 2
                        line_color = trace.line.color if hasattr(trace, 'line') and hasattr(trace.line, 'color') else color
                        
                        ax.plot(trace.x, trace.y, 
                               label=trace.name if hasattr(trace, 'name') and trace.name else '',
                               color=line_color if isinstance(line_color, str) else color,
                               linewidth=linewidth,
                               alpha=0.9)
                    
                    if 'markers' in mode:
                        ax.scatter(trace.x, trace.y,
                                 label=trace.name if hasattr(trace, 'name') and trace.name else '',
                                 color=color,
                                 s=50,
                                 alpha=0.8)
                
                elif trace_type == 'bar':
                    # Gráfico de barras
                    marker_color = trace.marker.color if hasattr(trace, 'marker') and hasattr(trace.marker, 'color') else color
                    ax.bar(trace.x, trace.y,
                          label=trace.name if hasattr(trace, 'name') and trace.name else '',
                          color=marker_color if isinstance(marker_color, str) else color,
                          alpha=0.85)
        
        # Aplicar títulos y etiquetas con el estilo de Plotly
        if hasattr(fig.layout, 'title') and fig.layout.title:
            title_text = fig.layout.title.text if hasattr(fig.layout.title, 'text') else str(fig.layout.title)
            ax.set_title(title_text, fontsize=16, fontweight='normal', pad=20)
        
        if hasattr(fig.layout, 'xaxis') and fig.layout.xaxis and hasattr(fig.layout.xaxis, 'title'):
            xlabel = fig.layout.xaxis.title.text if hasattr(fig.layout.xaxis.title, 'text') else str(fig.layout.xaxis.title)
            ax.set_xlabel(xlabel, fontsize=12)
        
        if hasattr(fig.layout, 'yaxis') and fig.layout.yaxis and hasattr(fig.layout.yaxis, 'title'):
            ylabel = fig.layout.yaxis.title.text if hasattr(fig.layout.yaxis.title, 'text') else str(fig.layout.yaxis.title)
            ax.set_ylabel(ylabel, fontsize=12)
        
        # Estilo de cuadrícula como Plotly (gris claro)
        ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='#E5E5E5')
        ax.set_axisbelow(True)
        
        # Leyenda si hay múltiples traces
        if len(fig.data) > 1:
            ax.legend(frameon=True, fancybox=False, edgecolor='#E5E5E5', 
                     fontsize=10, loc='best')
        
        # Estilo de los ejes (líneas grises claras)
        for spine in ax.spines.values():
            spine.set_edgecolor('#D3D3D3')
            spine.set_linewidth(1)
        
        # Guardar como PNG de alta calidad
        plt.tight_layout()
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig_mpl)
        
        img_bytes.seek(0)
        return img_bytes.getvalue()
        
    except Exception as e:
        # Si todo falla, mostrar error solo una vez
        if 'grafico_warning_shown' not in st.session_state:
            st.warning(
                "⚠️ No se pudieron generar las imágenes de los gráficos para el PDF. "
                "Los gráficos se mostrarán en pantalla pero podrían no estar en el reporte PDF."
            )
            st.session_state['grafico_warning_shown'] = True
        return None
