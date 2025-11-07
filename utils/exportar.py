from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from datetime import datetime
import io
from reportlab.platypus import Image
from reportlab.pdfgen import canvas

class PDFConEncabezadoPiePagina(canvas.Canvas):
    """Clase personalizada para agregar encabezado y pie de página"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        page_count = len(self.pages)
        for page_num, page in enumerate(self.pages, start=1):
            self.__dict__.update(page)
            self.draw_page_elements(page_num, page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_elements(self, page_num, page_count):
        """Dibuja el encabezado y pie de página"""
        page_width, page_height = letter
        
        # Encabezado
        self.saveState()
        self.setFillColor(colors.HexColor('#2C3E50'))
        self.rect(0, page_height - 40, page_width, 40, fill=True, stroke=False)
        
        self.setFillColor(colors.white)
        self.setFont('Helvetica-Bold', 14)
        self.drawString(50, page_height - 27, "CALCULADORA FINANCIERA")
        
        self.setFont('Helvetica', 9)
        self.drawRightString(page_width - 50, page_height - 27, "Reporte de Análisis Financiero")
        
        # Línea decorativa debajo del encabezado
        self.setStrokeColor(colors.HexColor('#3498DB'))
        self.setLineWidth(2)
        self.line(50, page_height - 42, page_width - 50, page_height - 42)
        
        # Pie de página
        self.setStrokeColor(colors.HexColor('#BDC3C7'))
        self.setLineWidth(1)
        self.line(50, 40, page_width - 50, 40)
        
        self.setFillColor(colors.HexColor('#7F8C8D'))
        self.setFont('Helvetica', 9)
        fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.drawString(50, 25, f"Fecha de generación: {fecha_generacion}")
        
        self.setFont('Helvetica-Bold', 9)
        self.drawRightString(page_width - 50, 25, f"Página {page_num} de {page_count}")
        
        self.restoreState()

def generar_pdf_reporte(datos_cartera, datos_jubilacion, datos_bono=None):
    """Genera un PDF con el reporte completo en estilo profesional"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=80,  # Aumentado para el encabezado
        bottomMargin=70  # Aumentado para el pie de página
    )
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=10,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=12,
        spaceBefore=25,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#BDC3C7'),
        borderPadding=5
    )
    
    subsection_style = ParagraphStyle(
        'SubSection',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        leftIndent=20
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#7F8C8D'),
        alignment=1
    )
    
    elements.append(Paragraph("REPORTE FINANCIERO", title_style))
    elements.append(Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y')}", date_style))
    elements.append(Spacer(1, 0.4*inch))
    
        # ========== MÓDULO A: PROYECCIÓN DE CARTERA ==========
    if datos_cartera:
        # Título de sección
        elements.append(Paragraph("1. MÓDULO A: PROYECCIÓN DE CARTERA", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Tabla general - mantener unida
        info = [
            ['Descripción', 'Valor'],
            ['Monto Inicial', f"$ {datos_cartera['monto_inicial']:,.2f}"],
            ['Aporte Periódico', f"$ {datos_cartera['aporte_periodico']:,.2f}"],
            ['Tasa Efectiva Anual (TEA)', f"{datos_cartera['tea']:.2f}%"],
            ['Plazo', f"{datos_cartera['anos']} años"],
            ['Saldo Final Proyectado', f"$ {datos_cartera['saldo_final']:,.2f}"],
        ]
        
        t = Table(info, colWidths=[3.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#7F8C8D')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3*inch))
        
        # 1.1 Detalle de proyección - mantener tabla unida
        if 'df_detallado' in datos_cartera:
            detalle_elements = []
            detalle_elements.append(Paragraph("1.1. Detalle de Proyección", subsection_style))
            detalle_elements.append(Spacer(1, 0.1*inch))
            
            df = datos_cartera['df_detallado']
            df_data = [['Periodo', 'Aporte', 'Saldo', 'Total Aportes']]
            
            # Si hay más de 12 filas, mostrar primeras 5, puntos suspensivos, y últimas 5
            if len(df) > 12:
                for i in range(5):
                    row = df.iloc[i]
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Aporte']:,.2f}",
                        f"$ {row['Saldo']:,.2f}",
                        f"$ {row['Total Aportes']:,.2f}"
                    ])
                df_data.append(['...', '...', '...', '...'])
                for i in range(len(df)-5, len(df)):
                    row = df.iloc[i]
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Aporte']:,.2f}",
                        f"$ {row['Saldo']:,.2f}",
                        f"$ {row['Total Aportes']:,.2f}"
                    ])
            else:
                for _, row in df.iterrows():
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Aporte']:,.2f}",
                        f"$ {row['Saldo']:,.2f}",
                        f"$ {row['Total Aportes']:,.2f}"
                    ])
            
            t_detalle = Table(df_data, colWidths=[1.2*inch, 1.6*inch, 1.6*inch, 1.6*inch])
            t_detalle.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
                ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ]))
            detalle_elements.append(t_detalle)
            
            # Agrupar el subtítulo con la tabla
            elements.append(KeepTogether(detalle_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # 1.2 Gráfica de Crecimiento - mantener gráfica unida
        if 'grafico' in datos_cartera and datos_cartera['grafico'] is not None:
            grafico_elements = []
            grafico_elements.append(Paragraph("1.2. Gráfica de Crecimiento", subsection_style))
            grafico_elements.append(Spacer(1, 0.1*inch))
            img = io.BytesIO(datos_cartera['grafico'])
            grafico_elements.append(Image(img, width=5.5*inch, height=3*inch))
            
            # Agrupar el subtítulo con la gráfica
            elements.append(KeepTogether(grafico_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # Salto de página después de la sección de Cartera
        elements.append(PageBreak())
    if datos_cartera:
        elements.append(Paragraph("1. MÓDULO A: PROYECCIÓN DE CARTERA", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Tabla general
        info = [
            ['Descripción', 'Valor'],
            ['Monto Inicial', f"$ {datos_cartera['monto_inicial']:,.2f}"],
            ['Aporte Periódico', f"$ {datos_cartera['aporte_periodico']:,.2f}"],
            ['Tasa Efectiva Anual (TEA)', f"{datos_cartera['tea']:.2f}%"],
            ['Plazo', f"{datos_cartera['anos']} años"],
            ['Saldo Final Proyectado', f"$ {datos_cartera['saldo_final']:,.2f}"],
        ]
        
        t = Table(info, colWidths=[3.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#7F8C8D')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3*inch))
        
        # 1.1 Detalle de proyección - mantener tabla unida
        if 'df_detallado' in datos_cartera:
            detalle_elements = []
            detalle_elements.append(Paragraph("1.1. Detalle de Proyección", subsection_style))
            detalle_elements.append(Spacer(1, 0.1*inch))
            
            df = datos_cartera['df_detallado']
            df_data = [['Periodo', 'Aporte', 'Saldo', 'Total Aportes']]
            
            # Si hay más de 12 filas, mostrar primeras 5, puntos suspensivos, y últimas 5
            if len(df) > 12:
                for i in range(5):
                    row = df.iloc[i]
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Aporte']:,.2f}",
                        f"$ {row['Saldo']:,.2f}",
                        f"$ {row['Total Aportes']:,.2f}"
                    ])
                df_data.append(['...', '...', '...', '...'])
                for i in range(len(df)-5, len(df)):
                    row = df.iloc[i]
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Aporte']:,.2f}",
                        f"$ {row['Saldo']:,.2f}",
                        f"$ {row['Total Aportes']:,.2f}"
                    ])
            else:
                for _, row in df.iterrows():
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Aporte']:,.2f}",
                        f"$ {row['Saldo']:,.2f}",
                        f"$ {row['Total Aportes']:,.2f}"
                    ])
            
            t_detalle = Table(df_data, colWidths=[1.2*inch, 1.6*inch, 1.6*inch, 1.6*inch])
            t_detalle.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
                ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ]))
            detalle_elements.append(t_detalle)
            
            # Agrupar el subtítulo con la tabla
            elements.append(KeepTogether(detalle_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # 1.2 Gráfica de Crecimiento - mantener gráfica unida
        if 'grafico' in datos_cartera and datos_cartera['grafico'] is not None:
            grafico_elements = []
            grafico_elements.append(Paragraph("1.2. Gráfica de Crecimiento", subsection_style))
            grafico_elements.append(Spacer(1, 0.1*inch))
            img = io.BytesIO(datos_cartera['grafico'])
            grafico_elements.append(Image(img, width=5.5*inch, height=3*inch))
            
            # Agrupar el subtítulo con la gráfica
            elements.append(KeepTogether(grafico_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # Salto de página después de la sección de Cartera
        elements.append(PageBreak())
    
    # ========== MÓDULO B: PROYECCIÓN DE JUBILACIÓN ==========
    if datos_jubilacion:
        # Título de sección
        elements.append(Paragraph("2. MÓDULO B: PROYECCIÓN DE JUBILACIÓN", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Tabla general - mantener unida
        info = [
            ['Descripción', 'Valor'],
            ['Capital Acumulado (Bruto)', f"$ {datos_jubilacion['capital_bruto']:,.2f}"],
            ['Ganancia Generada', f"$ {datos_jubilacion['ganancia']:,.2f}"],
            ['Impuesto a la Renta', f"$ {datos_jubilacion['impuesto']:,.2f}"],
            ['Capital Neto Disponible', f"$ {datos_jubilacion['capital_neto']:,.2f}"],
            ['Pensión Mensual Estimada', f"$ {datos_jubilacion['pension_mensual']:,.2f}"],
        ]
        
        t = Table(info, colWidths=[3.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#7F8C8D')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3*inch))
        
        # 2.1 Gráfica de proyección de retiro mensual
        if 'grafico' in datos_jubilacion and datos_jubilacion['grafico'] is not None:
            grafico_elements = []
            grafico_elements.append(Paragraph("2.1. Gráfica de Proyección de Retiro Mensual", subsection_style))
            grafico_elements.append(Spacer(1, 0.1*inch))
            img = io.BytesIO(datos_jubilacion['grafico'])
            grafico_elements.append(Image(img, width=5.5*inch, height=3*inch))
            
            # Agrupar el subtítulo con la gráfica
            elements.append(KeepTogether(grafico_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # 2.2 Gráfica de comparación de edades de retiro
        if 'grafico_comparacion' in datos_jubilacion and datos_jubilacion['grafico_comparacion'] is not None:
            grafico_elements = []
            grafico_elements.append(Paragraph("2.2. Gráfica de Comparación de Edades de Retiro", subsection_style))
            grafico_elements.append(Spacer(1, 0.1*inch))
            img = io.BytesIO(datos_jubilacion['grafico_comparacion'])
            grafico_elements.append(Image(img, width=5.5*inch, height=3*inch))
            
            # Agrupar el subtítulo con la gráfica
            elements.append(KeepTogether(grafico_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # Salto de página después de la sección de Jubilación
        elements.append(PageBreak())
    
    # ========== MÓDULO C: VALORACIÓN DE BONO ==========
    if datos_bono:
        # Título de sección
        elements.append(Paragraph("3. MÓDULO C: VALORACIÓN DE BONO", section_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Tabla general - mantener unida
        info = [
            ['Descripción', 'Valor'],
            ['Valor Nominal', f"$ {datos_bono['valor_nominal']:,.2f}"],
            ['Tasa de Cupón', f"{datos_bono['tasa_cupon']:.2f}%"],
            ['Plazo del Bono', f"{datos_bono['anos']} años"],
            ['Valor Presente Total', f"$ {datos_bono['vp_total']:,.2f}"],
        ]
        
        t = Table(info, colWidths=[3.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#7F8C8D')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3*inch))
        
        # 3.1 Flujos de caja - mantener tabla unida
        if 'df_flujos' in datos_bono:
            flujos_elements = []
            flujos_elements.append(Paragraph("3.1. Flujos de Caja", subsection_style))
            flujos_elements.append(Spacer(1, 0.1*inch))
            
            df = datos_bono['df_flujos']
            df_data = [['Periodo', 'Flujo', 'VP Flujo']]
            
            # Si hay más de 12 filas, mostrar primeras 5, puntos suspensivos, y últimas 5
            if len(df) > 12:
                for i in range(5):
                    row = df.iloc[i]
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Flujo']:,.2f}",
                        f"$ {row['VP Flujo']:,.2f}"
                    ])
                df_data.append(['...', '...', '...'])
                for i in range(len(df)-5, len(df)):
                    row = df.iloc[i]
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Flujo']:,.2f}",
                        f"$ {row['VP Flujo']:,.2f}"
                    ])
            else:
                for _, row in df.iterrows():
                    df_data.append([
                        str(row['Periodo']),
                        f"$ {row['Flujo']:,.2f}",
                        f"$ {row['VP Flujo']:,.2f}"
                    ])
            
            t_detalle = Table(df_data, colWidths=[1.5*inch, 2.25*inch, 2.25*inch])
            t_detalle.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
                ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.HexColor('#7F8C8D')),
            ]))
            flujos_elements.append(t_detalle)
            
            # Agrupar el subtítulo con la tabla
            elements.append(KeepTogether(flujos_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # 3.2 Gráfica de valor presente por periodo
        if 'grafico' in datos_bono and datos_bono['grafico'] is not None:
            grafico_elements = []
            grafico_elements.append(Paragraph("3.2. Gráfica de Valor Presente por Periodo", subsection_style))
            grafico_elements.append(Spacer(1, 0.1*inch))
            img = io.BytesIO(datos_bono['grafico'])
            grafico_elements.append(Image(img, width=5.5*inch, height=3*inch))
            
            # Agrupar el subtítulo con la gráfica
            elements.append(KeepTogether(grafico_elements))
            elements.append(Spacer(1, 0.3*inch))
        
        # 3.3 Gráfica de Valor del Bono según TEA de Mercado
        if 'grafico_sensibilidad' in datos_bono and datos_bono['grafico_sensibilidad'] is not None:
            grafico_elements = []
            grafico_elements.append(Paragraph("3.3. Gráfica de Valor del Bono según TEA de Mercado", subsection_style))
            grafico_elements.append(Spacer(1, 0.1*inch))
            img = io.BytesIO(datos_bono['grafico_sensibilidad'])
            grafico_elements.append(Image(img, width=5.5*inch, height=3*inch))
            
            # Agrupar el subtítulo con la gráfica
            elements.append(KeepTogether(grafico_elements))
            elements.append(Spacer(1, 0.25*inch))
            elements.append(Spacer(1, 0.25*inch))
    
    # Construir el PDF con encabezado y pie de página personalizados
    doc.build(elements, canvasmaker=PDFConEncabezadoPiePagina)
    buffer.seek(0)
    return buffer