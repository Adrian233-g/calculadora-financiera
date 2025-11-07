import streamlit as st
import plotly.graph_objects as go
from utils.calculos import calcular_valor_bono
from utils.validaciones import validar_monto, validar_tea, validar_anos
import io
import base64


def mostrar_modulo_bonos():
    st.header("📈 Módulo C: Proyeccion de Bonos")
    st.markdown("---")
    
    with st.expander("ℹ️ Ayuda - ¿Cómo usar esta calculadora?"):
        st.write("""
        Este módulo calcula el valor presente de un bono considerando:
        - **Valor nominal**: Valor facial del bono.
        - **Tasa cupón**: Interés que paga el bono.
        - **Perioricidad*: Con qué periodo se paga los cupones.
        - **TEA mercado**: Tasa de retorno que exiges.
        
        El valor presente te dice cuánto deberías pagar hoy por ese bono.
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Datos del Bono")
        
        valor_nominal = st.number_input(
            "Valor Nominal (USD)",
            min_value=0.0,
            value=1000.0,
            step=100.0,
            help="Valor facial o principal del bono"
        )
        
        tasa_cupon = st.number_input(
            "Tasa Cupón (% TEA)",
            min_value=0.0,
            max_value=50.0,
            value=8.0,
            step=0.5,
            help="Tasa de interés anual que paga el bono"
        )
        
        frecuencia_pago = st.selectbox(
            "Frecuencia de Pago",
            ["Mensual", "Bimestral", "Trimestral", "Cuatrimestral", "Semestral", "Anual"],
            index=5,
            help="Con qué frecuencia el bono paga cupones"
        )
    
    with col2:
        st.subheader("⚙️ Condiciones del Mercado")
        
        anos = st.number_input(
            "Plazo (años)",
            min_value=1,
            max_value=50,
            value=10,
            help="Años hasta el vencimiento del bono"
        )
        
        tea_mercado = st.number_input(
            "TEA Mercado - Tasa de Retorno Esperada (%)",
            min_value=0.0,
            max_value=50.0,
            value=10.0,
            step=0.5,
            help="Tasa de retorno que exiges por invertir en este bono"
        )
        
        st.info("""
        💡 **Interpretación:**
        - Si VP > Valor Nominal: el bono está sobrevaluado
        - Si VP < Valor Nominal: el bono está subvaluado
        - Si VP = Valor Nominal: el bono está a la par
        """)
    
    st.markdown("---")
    
    if st.button("🔍 Calcular Valor del Bono", type="primary", use_container_width=True):
        if not all([validar_monto(valor_nominal, "Valor nominal"),
                   validar_tea(tasa_cupon),
                   validar_tea(tea_mercado),
                   validar_anos(anos, "Plazo")]):
            return
        
        df_flujos, vp_total = calcular_valor_bono(
            valor_nominal, tasa_cupon, frecuencia_pago, anos, tea_mercado
        )
        
        st.session_state['bono_df'] = df_flujos
        st.session_state['bono_vp'] = vp_total
        st.session_state['bono_params'] = {
            'valor_nominal': valor_nominal,
            'tasa_cupon': tasa_cupon,
            'frecuencia_pago': frecuencia_pago,
            'anos': anos,
            'tea_mercado': tea_mercado
        }
        
        st.success("✅ Valoración completada exitosamente")
    
    if 'bono_vp' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Resultados de Valoración")
        
        params = st.session_state['bono_params']
        vp = st.session_state['bono_vp']
        
        diferencia = vp - params['valor_nominal']
        porcentaje = (diferencia / params['valor_nominal']) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Valor Nominal", f"${params['valor_nominal']:,.2f}")
        col2.metric("Valor Presente", f"${vp:,.2f}", delta=f"{porcentaje:+.2f}%")
        col3.metric("Diferencia", f"${diferencia:,.2f}")
        
        if vp > params['valor_nominal']:
            st.success("✅ El bono está **sobrevaluado** (vale más que su valor nominal)")
            st.write("💡 La tasa cupón es mayor que la tasa de mercado")
        elif vp < params['valor_nominal']:
            st.warning("⚠️ El bono está **subvaluado** (vale menos que su valor nominal)")
            st.write("💡 La tasa cupón es menor que la tasa de mercado")
        else:
            st.info("📌 El bono está **a la par** (vale igual que su valor nominal)")
        
        st.markdown("---")
        st.subheader("📊 Flujos de Caja del Bono")
        
        df = st.session_state['bono_df']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['Periodo'],
            y=df['Flujo'],
            name='Flujo de Caja',
            marker_color='lightblue',
            text=df['Flujo'].apply(lambda x: f"${x:,.0f}"),
            textposition='outside'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Periodo'],
            y=df['VP Flujo'],
            name='VP de Flujo',
            mode='lines+markers',
            line=dict(color='red', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Flujos de Caja y Valor Presente',
            xaxis_title='Periodo',
            yaxis_title='Monto (USD)',
            template='plotly_white',
            hovermode='x unified'
        )

        
        
        st.plotly_chart(fig, use_container_width=True)
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format="png")
        img_bytes.seek(0)
        st.session_state['bono_grafico'] = img_bytes.getvalue()
        
        with st.expander("📋 Ver Tabla Detallada de Flujos"):
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"**Valor Presente Total: ${vp:,.2f}**")
        
        with st.expander("📈 Análisis de Sensibilidad"):
            st.subheader("Valor del Bono según TEA de Mercado")
            
            tasas = [i for i in range(0, 21)]
            valores = []
            
            for tasa in tasas:
                _, vp_temp = calcular_valor_bono(
                    params['valor_nominal'],
                    params['tasa_cupon'],
                    params['frecuencia_pago'],
                    params['anos'],
                    tasa
                )
                valores.append(vp_temp)
            
            fig_sens = go.Figure()
            
            fig_sens.add_trace(go.Scatter(
                x=tasas,
                y=valores,
                mode='lines+markers',
                line=dict(color='green', width=3),
                marker=dict(size=8)
            ))
            
            fig_sens.add_hline(
                y=params['valor_nominal'],
                line_dash="dash",
                line_color="red",
                annotation_text=f"Valor Nominal: ${params['valor_nominal']:,.0f}"
            )
            
            fig_sens.update_layout(
                title='Valor del Bono vs TEA de Mercado',
                xaxis_title='TEA de Mercado (%)',
                yaxis_title='Valor Presente (USD)',
                template='plotly_white'
            )
            
            st.plotly_chart(fig_sens, use_container_width=True)
            
            # Guardar gráfica de sensibilidad para PDF
            img_bytes_sens = io.BytesIO()
            fig_sens.write_image(img_bytes_sens, format="png")
            img_bytes_sens.seek(0)
            st.session_state['bono_grafico_sensibilidad'] = img_bytes_sens.getvalue()
            
            st.info("💡 A mayor tasa de mercado, menor es el valor presente del bono")
    