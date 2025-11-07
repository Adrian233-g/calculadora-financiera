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
    replicando EXACTAMENTE el estilo de Plotly incluyendo fills, líneas punteadas, etc.
    
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
    
    # Intento 2: Matplotlib con estilo EXACTO de Plotly (fallback robusto)
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
        
        # Variables para controlar el orden de relleno
        fill_between_data = []
        
        # Extraer y graficar cada trace con el estilo EXACTO de Plotly
        for idx, trace in enumerate(fig.data):
            color = PLOTLY_COLORS[idx % len(PLOTLY_COLORS)]
            
            if hasattr(trace, 'x') and hasattr(trace, 'y'):
                # Determinar el tipo de gráfico
                trace_type = trace.type if hasattr(trace, 'type') else 'scatter'
                
                if trace_type == 'scatter':
                    mode = trace.mode if hasattr(trace, 'mode') else 'lines'
                    
                    # Obtener el color de la línea
                    line_color = color
                    if hasattr(trace, 'line') and hasattr(trace.line, 'color'):
                        line_color = trace.line.color
                    
                    # Obtener ancho de línea
                    linewidth = 2
                    if hasattr(trace, 'line') and hasattr(trace.line, 'width'):
                        linewidth = trace.line.width
                    
                    # Obtener estilo de línea (sólida o punteada)
                    linestyle = '-'
                    if hasattr(trace, 'line') and hasattr(trace.line, 'dash'):
                        if trace.line.dash == 'dash':
                            linestyle = '--'
                        elif trace.line.dash == 'dot':
                            linestyle = ':'
                        elif trace.line.dash == 'dashdot':
                            linestyle = '-.'
                    
                    # Graficar la línea
                    if 'lines' in mode or mode == 'lines':
                        line, = ax.plot(trace.x, trace.y, 
                               label=trace.name if hasattr(trace, 'name') and trace.name else '',
                               color=line_color if isinstance(line_color, str) else color,
                               linewidth=linewidth,
                               linestyle=linestyle,
                               alpha=1.0,
                               zorder=3)
                        
                        # Detectar si hay fill (relleno debajo de la línea)
                        if hasattr(trace, 'fill') and trace.fill:
                            fill_type = trace.fill
                            fillcolor = line_color
                            
                            # Obtener color de relleno si está especificado
                            if hasattr(trace, 'fillcolor') and trace.fillcolor:
                                fillcolor = trace.fillcolor
                            
                            # Aplicar transparencia al relleno
                            if isinstance(fillcolor, str) and fillcolor.startswith('rgba'):
                                # Extraer valores RGBA
                                import re
                                rgba_match = re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)', fillcolor)
                                if rgba_match:
                                    r, g, b, a = rgba_match.groups()
                                    fillcolor = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
                                    fill_alpha = float(a)
                                else:
                                    fill_alpha = 0.3
                            else:
                                fill_alpha = 0.3
                            
                            # Almacenar datos de relleno para aplicar después
                            if fill_type == 'tonexty':
                                # Rellenar hasta la línea anterior
                                fill_between_data.append({
                                    'x': trace.x,
                                    'y': trace.y,
                                    'color': fillcolor if isinstance(fillcolor, str) else line_color,
                                    'alpha': fill_alpha,
                                    'previous_idx': idx - 1
                                })
                            elif fill_type == 'tozeroy':
                                # Rellenar hasta cero
                                ax.fill_between(trace.x, 0, trace.y, 
                                              color=fillcolor if isinstance(fillcolor, str) else line_color,
                                              alpha=fill_alpha,
                                              zorder=1)
                    
                    if 'markers' in mode:
                        ax.scatter(trace.x, trace.y,
                                 label=trace.name if hasattr(trace, 'name') and trace.name else '',
                                 color=color,
                                 s=50,
                                 alpha=0.8,
                                 zorder=4)
                
                elif trace_type == 'bar':
                    # Gráfico de barras
                    marker_color = trace.marker.color if hasattr(trace, 'marker') and hasattr(trace.marker, 'color') else color
                    ax.bar(trace.x, trace.y,
                          label=trace.name if hasattr(trace, 'name') and trace.name else '',
                          color=marker_color if isinstance(marker_color, str) else color,
                          alpha=0.85,
                          zorder=3)
        
        # Aplicar rellenos entre líneas (tonexty)
        if fill_between_data and len(fig.data) > 1:
            for fill_data in fill_between_data:
                prev_idx = fill_data['previous_idx']
                if prev_idx >= 0 and prev_idx < len(fig.data):
                    prev_trace = fig.data[prev_idx]
                    if hasattr(prev_trace, 'y'):
                        ax.fill_between(fill_data['x'], 
                                      prev_trace.y, 
                                      fill_data['y'],
                                      color=fill_data['color'],
                                      alpha=fill_data['alpha'],
                                      zorder=2)
        
        # Aplicar títulos y etiquetas con el estilo de Plotly
        if hasattr(fig.layout, 'title') and fig.layout.title:
            title_text = fig.layout.title.text if hasattr(fig.layout.title, 'text') else str(fig.layout.title)
            ax.set_title(title_text, fontsize=16, fontweight='normal', pad=20, color='#2C3E50')
        
        if hasattr(fig.layout, 'xaxis') and fig.layout.xaxis and hasattr(fig.layout.xaxis, 'title'):
            xlabel = fig.layout.xaxis.title.text if hasattr(fig.layout.xaxis.title, 'text') else str(fig.layout.xaxis.title)
            ax.set_xlabel(xlabel, fontsize=12, color='#2C3E50')
        
        if hasattr(fig.layout, 'yaxis') and fig.layout.yaxis and hasattr(fig.layout.yaxis, 'title'):
            ylabel = fig.layout.yaxis.title.text if hasattr(fig.layout.yaxis.title, 'text') else str(fig.layout.yaxis.title)
            ax.set_ylabel(ylabel, fontsize=12, color='#2C3E50')
        
        # Estilo de cuadrícula como Plotly (gris muy claro)
        ax.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#E1E5EB', zorder=0)
        ax.set_axisbelow(True)
        
        # Leyenda si hay múltiples traces
        if len(fig.data) > 1:
            legend = ax.legend(frameon=True, fancybox=False, edgecolor='#E5E5E5', 
                     fontsize=11, loc='best', framealpha=0.95)
            legend.get_frame().set_facecolor('white')
        
        # Estilo de los ejes (líneas grises claras como Plotly)
        for spine in ax.spines.values():
            spine.set_edgecolor('#D6D6D6')
            spine.set_linewidth(0.8)
        
        # Color de los ticks
        ax.tick_params(colors='#2C3E50', which='both')
        
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
                f"⚠️ No se pudieron generar las imágenes de los gráficos para el PDF. "
                f"Los gráficos se mostrarán en pantalla pero podrían no estar en el reporte PDF. Error: {str(e)}"
            )
            st.session_state['grafico_warning_shown'] = True
        return None
