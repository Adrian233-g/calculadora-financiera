# 💰 Calculadora Financiera - Finanzas Corporativas

Aplicación web interactiva para proyección de inversiones, cálculo de jubilación y valoración de bonos.

## 🚀 Instalación

### Opción 1: Ejecución Directa (Python)

```bash
# Clonar o descargar el proyecto
cd calculadora_financiera

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

### Opción 2: Ejecutable Windows (.exe)

1. Descargar `CalculadoraFinanciera.exe`
2. Doble clic para ejecutar
3. Se abrirá automáticamente en el navegador

## 📦 Estructura del Proyecto

```
calculadora_financiera/
├── app.py                  # Aplicación principal
├── requirements.txt        # Dependencias
├── modules/               # Módulos funcionales
│   ├── cartera.py         # Crecimiento de cartera
│   ├── jubilacion.py      # Proyección de jubilación
│   └── bonos.py           # Valoración de bonos
├── utils/                 # Utilidades
│   ├── calculos.py        # Cálculos financieros
│   ├── validaciones.py    # Validaciones
│   └── exportar.py        # Exportación PDF
└── docs/                  # Documentación
    └── Manual_Usuario.pdf
```

## 🎯 Módulos

### 📊 Módulo A: Crecimiento de Cartera
- Cálculo de crecimiento con interés compuesto
- Aportes periódicos (mensual, trimestral, semestral, anual)
- Gráficas de evolución
- Proyección a largo plazo

### 💰 Módulo B: Proyección de Jubilación
- Cálculo de pensión mensual
- Consideración de impuestos (5% local, 29.5% extranjera)
- Opción de cobro total o pensión mensual
- Comparación de escenarios

### 📈 Módulo C: Valoración de Bonos
- Cálculo de valor presente
- Análisis de flujos de caja
- Múltiples frecuencias de pago
- Análisis de sensibilidad

## 🛠️ Tecnologías

- **Python 3.9+**
- **Streamlit**: Framework web
- **Pandas**: Manipulación de datos
- **Plotly**: Gráficas interactivas
- **ReportLab**: Generación de PDFs

## 👥 Equipo de Desarrollo

- **TAKESHY**: Integración y coordinación
- **ADRIAN**: Módulo de Cartera
- **ROBLES**: Módulo de Jubilación
- **SAMIRA**: Módulo de Bonos
- **BUSTOS**: Utilidades y exportación

## 📝 Uso Rápido

1. Ejecutar la aplicación
2. Seleccionar un módulo en el menú lateral
3. Ingresar los datos requeridos
4. Hacer clic en "Calcular"
5. Ver resultados y gráficas
6. Exportar a PDF si es necesario

## 🔧 Generar Ejecutable

Para crear el archivo .exe:

```bash
pyinstaller --onefile --windowed --add-data "modules;modules" --add-data "utils;utils" --icon=assets/logo.ico app.py
```

## 📖 Manual de Usuario

Ver `docs/Manual_Usuario.pdf` para instrucciones detalladas.

## 🐛 Solución de Problemas

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Puerto en uso
```bash
streamlit run app.py --server.port 8502
```

### Problemas con PDF
```bash
pip install --upgrade reportlab
```

## 📧 Soporte

Para dudas o problemas, contactar al equipo de desarrollo.

## 🌐 Deployment

### Opción 1: Streamlit Community Cloud (Recomendado - GRATIS)

La forma más fácil de deployar tu aplicación:

#### Paso 1: Subir a GitHub
```bash
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit - Calculadora Financiera"

# Crear rama principal
git branch -M main

# Conectar con GitHub (crear repositorio primero en github.com)
git remote add origin https://github.com/tu-usuario/calculadora-financiera.git

# Subir código
git push -u origin main
```

#### Paso 2: Deploy en Streamlit Cloud
1. Accede a: https://streamlit.io/cloud
2. Inicia sesión con tu cuenta de GitHub
3. Click en **"New app"**
4. Configura:
   - **Repository**: tu-usuario/calculadora-financiera
   - **Branch**: main
   - **Main file path**: app.py
5. Click en **"Deploy!"**
6. ¡Listo! Tu app estará disponible en: `https://tu-app.streamlit.app`

**Ventajas:**
- ✅ Completamente gratis
- ✅ Deploy automático con cada push a GitHub
- ✅ SSL/HTTPS incluido
- ✅ No requiere configuración de servidor

---

### Opción 2: Heroku

Para mayor control y recursos:

```bash
# Crear archivo Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Crear archivo setup.sh
cat > setup.sh << EOF
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = \$PORT
enableCORS = false
" > ~/.streamlit/config.toml
EOF

# Deploy a Heroku
heroku login
heroku create nombre-app
git push heroku main
```

---

### Opción 3: Docker

Para deployment en cualquier servidor:

```dockerfile
# Crear Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
# Build y run
docker build -t calculadora-financiera .
docker run -p 8501:8501 calculadora-financiera
```

---

### Opción 4: Railway / Render

Similares a Heroku, con plan gratuito:
- **Railway**: https://railway.app
- **Render**: https://render.com

Simplemente conecta tu repositorio de GitHub y selecciona:
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

---

### 📝 Consideraciones Importantes

1. **Variables de Entorno**: Si usas claves API, créalas en los secrets de Streamlit Cloud
2. **requirements.txt**: Asegúrate de que esté actualizado
3. **Puerto**: Streamlit Cloud usa el puerto automáticamente
4. **Memoria**: La app consume ~200MB en ejecución normal

### 🔒 Configuración de Secrets (Streamlit Cloud)

Si necesitas variables privadas:
1. En tu app deployada, ve a Settings → Secrets
2. Agrega en formato TOML:
```toml
[general]
api_key = "tu_clave_secreta"
```

## 📄 Licencia

Proyecto académico - Finanzas Corporativas 2024