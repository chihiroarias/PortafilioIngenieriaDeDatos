# UT1 - Actividad 6 - Escalado de Datos y Comparación de Modelos

## Contexto

Análisis del impacto del escalado de datos en el rendimiento de algoritmos de machine learning usando el dataset Ames Housing, con enfoque en técnicas de preprocesamiento y prevención de data leakage.

## Objetivos

- Explorar y analizar escalas de variables en datos reales
- Implementar y comparar técnicas de escalado
- Evaluar impacto en algoritmos sensibles a la escala
- Crear pipelines reproducibles de preprocesamiento
- Comparar rendimiento de modelos con diferentes escalados

## Actividades

- 1. Setup y carga de datos - 15 min
- 2. Análisis exploratorio de escalas - 25 min
- 3. Identificación de variables problemáticas - 30 min
- 4. Implementación de técnicas de escalado - 25 min
- 5. Comparación de modelos - 35 min
- 6. Análisis de outliers post-escalado - 20 min
- 7. Pipeline reproducible - 15 min
- 8. Documentación - 25 min

## Desarrollo

### 1. Setup y Carga de Datos

Configuración del entorno con librerías necesarias y carga del dataset Ames Housing para análisis de escalas.

### 2. Análisis Exploratorio de Escalas

- Dataset: 2930 registros, 82 columnas
- Identificación de 37 columnas numéricas
- Análisis de estadísticas descriptivas y distribuciones

### 3. Identificación de Variables Problemáticas

**Columnas seleccionadas:** 'SalePrice', 'Lot Area', 'Gr Liv Area', 'Total Bsmt SF', '1st Flr SF', 'Year Built'

**Hallazgos principales:**

- **Columna más problemática:** 'Lot Area' (ratio máximo/mínimo: 215.35)
- **Outliers evidentes** en 'Gr Liv Area' y 'Lot Area'
- Escalas muy diferentes entre áreas, años y precios

### 4. Implementación de Técnicas de Escalado

- **StandardScaler:** Centrado y escalado basado en desviación estándar
- **MinMaxScaler:** Escalado a rango [0, 1]
- **RobustScaler:** Escalado robusto a outliers usando IQR
- **PowerTransformer:** Transformación para normalizar distribuciones sesgadas

### 5. Comparación de Modelos

**Resultados R²:**

- StandardScaler: 0.7684
- MinMaxScaler: 0.7684
- RobustScaler: 0.7685
- PowerTransformer: 0.7723
- Sin escalado: 0.7684

### 6. Análisis de Outliers Post-Escalado

**Detección en 'Gr Liv Area':**

- Original: 89 outliers (método IQR)
- Todos los scalers mantuvieron 89 outliers
- RobustScaler no modificó significativamente la detección

### 7. Pipeline Reproducible

Creación de pipeline con PowerTransformer para manejo óptimo de distribuciones sesgadas, logrando R² de 0.772 con validación cruzada.

### 8. Demostración Anti-Leakage

**Comparación de métodos:**

- Método con leakage: R² = 0.7721
- Método sin leakage: R² = 0.7684
- Pipeline: R² = 0.7723

**Impacto del leakage:** Inflación del 0.48% en R²

## Reflexión

Esta práctica demostró la importancia crítica del escalado de datos en machine learning. El PowerTransformer mostró mejor rendimiento en datos con distribuciones sesgadas típicas de precios inmobiliarios. La implementación de pipelines anti-leakage resultó esencial para evaluaciones honestas del modelo. La elección del escalador debe basarse en características específicas de los datos, siendo PowerTransformer especialmente útil para variables con alta skewness como las del dataset Ames Housing.
