import streamlit as st
from modules.cartera import mostrar_modulo_cartera
from modules.jubilacion import mostrar_modulo_jubilacion
from modules.bonos import mostrar_modulo_bonos
from utils.exportar import generar_pdf_reporte

st.set_page_config(
    page_title="Calculadora Financiera",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    h1 {
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("💰 Calculadora Financiera")
    st.markdown("---")
    
    pagina = st.radio(
        "Selecciona un módulo:",
        ["🏠 Inicio", "📊 Cartera", "💰 Jubilación", "📈 Bonos", "📄 Exportar"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📚 Guía Rápida")
    st.write("""
    1. **Cartera**: Proyecta tu inversión
    2. **Jubilación**: Calcula tu pensión
    3. **Bonos**: Valora instrumentos
    4. **Exportar**: Descarga reporte
    """)
    
    st.markdown("---")
    st.caption("Desarrollado para Finanzas Corporativas")
    st.caption("© 2024 - Todos los derechos reservados")

if pagina == "🏠 Inicio":
    st.title("🏠 Bienvenido a tu Calculadora Financiera")
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 ¿Qué puedes hacer con esta aplicación?
    
    Esta herramienta te permite planificar tu futuro financiero de manera profesional y sencilla.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Módulo Cartera</h3>
            <p>Proyecta cómo crecerá tu inversión con aportes periódicos y interés compuesto</p>
            <ul>
                <li>Aportes iniciales y periódicos</li>
                <li>Gráficas de crecimiento</li>
                <li>Proyecciones a largo plazo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Módulo Jubilación</h3>
            <p>Calcula tu pensión mensual al jubilarte considerando impuestos</p>
            <ul>
                <li>Cálculo de impuestos</li>
                <li>Pensión mensual estimada</li>
                <li>Comparación de escenarios</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Módulo Bonos</h3>
            <p>Valora bonos y analiza sus flujos de caja descontados</p>
            <ul>
                <li>Valor presente de bonos</li>
                <li>Análisis de flujos</li>
                <li>Sensibilidad de tasas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Usa el menú lateral para comenzar con cualquier módulo")
    
    st.markdown("---")
    st.subheader("🚀 Ejemplo Rápido")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Escenario de ejemplo:**
        - Edad actual: 30 años
        - Inversión inicial: $5,000
        - Aporte mensual: $500
        - TEA esperada: 8%
        - Edad de jubilación: 65 años
        """)
    
    with col2:
        st.markdown("""
        **Resultado esperado:**
        - Plazo: 35 años
        - Total aportado: ~$215,000
        - Capital acumulado: ~$1,100,000
        - Pensión mensual: ~$8,500/mes
        """)
    
    st.success("💡 ¡Estos resultados son aproximados! Usa los módulos para cálculos exactos.")

elif pagina == "📊 Cartera":
    mostrar_modulo_cartera()

elif pagina == "💰 Jubilación":
    mostrar_modulo_jubilacion()

elif pagina == "📈 Bonos":
    mostrar_modulo_bonos()

elif pagina == "📄 Exportar":
    st.header("📄 Exportar Reporte")
    st.markdown("---")
    
    st.info("📋 Este módulo genera un reporte PDF con todos tus cálculos")
    
    tiene_datos = False
    datos_incluir = []
    
    if 'cartera_saldo_final' in st.session_state:
        st.success("✅ Datos de Cartera disponibles")
        datos_incluir.append("Cartera")
        tiene_datos = True
    else:
        st.warning("⚠️ No hay datos de Cartera")
    
    if 'jubilacion_data' in st.session_state:
        st.success("✅ Datos de Jubilación disponibles")
        datos_incluir.append("Jubilación")
        tiene_datos = True
    else:
        st.warning("⚠️ No hay datos de Jubilación")
    
    if 'bono_vp' in st.session_state:
        st.success("✅ Datos de Bonos disponibles")
        datos_incluir.append("Bonos")
        tiene_datos = True
    else:
        st.warning("⚠️ No hay datos de Bonos")
    
    st.markdown("---")
    
    if tiene_datos:
        st.write(f"**Secciones a incluir:** {', '.join(datos_incluir)}")
        
        if st.button("📥 Generar y Descargar PDF", type="primary", use_container_width=True):
            with st.spinner("Generando reporte..."):
                datos_cartera = None
                datos_jubilacion = None
                datos_bono = None
                
                if 'cartera_saldo_final' in st.session_state or 'cartera_grafico' in st.session_state:
                    datos_cartera = {
                        'monto_inicial': st.session_state['cartera_params']['monto_inicial'],
                        'aporte_periodico': st.session_state['cartera_params']['aporte_periodico'],
                        'tea': st.session_state['cartera_params']['tea'],
                        'anos': st.session_state['cartera_params']['anos'],
                        'saldo_final': st.session_state['cartera_saldo_final']
                    }
                    if 'cartera_grafico' in st.session_state:
                        datos_cartera['grafico'] = st.session_state['cartera_grafico']
                    if 'cartera_df' in st.session_state:
                        datos_cartera['df_detallado'] = st.session_state['cartera_df']
                
                if 'jubilacion_data' in st.session_state:
                    datos_jubilacion = st.session_state['jubilacion_data']
                    if 'jubilacion_grafico' in st.session_state:
                        datos_jubilacion['grafico'] = st.session_state['jubilacion_grafico']
                    if 'jubilacion_grafico_comparacion' in st.session_state:
                        datos_jubilacion['grafico_comparacion'] = st.session_state['jubilacion_grafico_comparacion']
                
                if 'bono_vp' in st.session_state:
                    datos_bono = {
                        'valor_nominal': st.session_state['bono_params']['valor_nominal'],
                        'tasa_cupon': st.session_state['bono_params']['tasa_cupon'],
                        'anos': st.session_state['bono_params']['anos'],
                        'vp_total': st.session_state['bono_vp']
                    }
                    if 'bono_grafico' in st.session_state:
                        datos_bono['grafico'] = st.session_state['bono_grafico']
                    if 'bono_df' in st.session_state:
                        datos_bono['df_flujos'] = st.session_state['bono_df']
                    if 'bono_grafico_sensibilidad' in st.session_state:
                        datos_bono['grafico_sensibilidad'] = st.session_state['bono_grafico_sensibilidad']
                        
                pdf_buffer = generar_pdf_reporte(datos_cartera, datos_jubilacion, datos_bono)
                
                st.download_button(
                    label="📄 Descargar Reporte PDF",
                    data=pdf_buffer,
                    file_name="reporte_financiero.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success("✅ Reporte generado exitosamente")
    else:
        st.error("❌ No hay datos para exportar. Por favor, completa al menos un módulo.")
        st.info("💡 Ve a los módulos de Cartera, Jubilación o Bonos para generar datos")