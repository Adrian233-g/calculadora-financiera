import numpy as np
import pandas as pd

def tasa_equivalente(tea, periodos_anuales):
    """Convierte TEA a tasa periódica equivalente"""
    return (1 + tea/100) ** (1/periodos_anuales) - 1

def calcular_crecimiento_cartera(monto_inicial, aporte_periodico, tea, periodos_totales, periodos_anuales):
    """Calcula el crecimiento de la cartera periodo por periodo"""
    tasa_periodica = tasa_equivalente(tea, periodos_anuales)
    
    datos = []
    saldo = monto_inicial
    total_aportes = monto_inicial
    
    for periodo in range(1, periodos_totales + 1):
        interes = saldo * tasa_periodica
        saldo = saldo + interes + aporte_periodico
        total_aportes += aporte_periodico
        
        datos.append({
            'Periodo': periodo,
            'Aporte': aporte_periodico,
            'Interés': round(interes, 2),
            'Saldo': round(saldo, 2),
            'Total Aportes': round(total_aportes, 2)
        })
    
    return pd.DataFrame(datos), saldo, total_aportes

def calcular_pension_mensual(capital, tea, anos_retiro):
    """Calcula la pensión mensual que se puede retirar"""
    tasa_mensual = tasa_equivalente(tea, 12)
    meses = anos_retiro * 12
    
    if tasa_mensual == 0:
        pension = capital / meses
    else:
        pension = capital * tasa_mensual / (1 - (1 + tasa_mensual) ** (-meses))
    
    return pension

def calcular_impuesto(ganancia, tipo_impuesto):
    """Calcula el impuesto sobre la ganancia"""
    tasas = {'local': 0.05, 'extranjera': 0.295}
    return ganancia * tasas.get(tipo_impuesto, 0)

def calcular_valor_bono(valor_nominal, tasa_cupon, frecuencia_pago, anos, tea_mercado):
    """Calcula el valor presente de un bono"""
    periodos_anuales = {'Mensual': 12, 'Bimestral': 6, 'Trimestral': 4, 
                        'Cuatrimestral': 3, 'Semestral': 2, 'Anual': 1}
    
    n_periodos = periodos_anuales[frecuencia_pago]
    periodos_totales = anos * n_periodos
    
    tasa_cupon_periodica = tasa_equivalente(tasa_cupon, n_periodos)
    tasa_descuento_periodica = tasa_equivalente(tea_mercado, n_periodos)
    
    cupon = valor_nominal * tasa_cupon_periodica
    
    flujos = []
    vp_total = 0
    
    for periodo in range(1, periodos_totales + 1):
        flujo = cupon
        if periodo == periodos_totales:
            flujo += valor_nominal
        
        vp_flujo = flujo / ((1 + tasa_descuento_periodica) ** periodo)
        vp_total += vp_flujo
        
        flujos.append({
            'Periodo': periodo,
            'Flujo': round(flujo, 2),
            'VP Flujo': round(vp_flujo, 2)
        })
    
    return pd.DataFrame(flujos), vp_total