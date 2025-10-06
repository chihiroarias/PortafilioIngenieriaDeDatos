---
title: "UT1 - Practica 4 - Dataset Ames Housing"
date: 2025-09-16
---

# UT1 - Actividad 4 - Dataset Ames Housing

## Contexto

Análisis avanzado de calidad de datos y técnicas de imputación en el dataset Ames Housing, aplicando métodos para el tratamiento de missing data y detección de outliers.

## Objetivos

- Explorar y limpiar el dataset Ames Housing
- Identificar y clasificar patrones de missing data (MCAR, MAR, MNAR)
- Implementar técnicas de detección de outliers
- Aplicar estrategias de imputación inteligente
- Crear pipelines reproducibles de limpieza de datos

## Actividades (con tiempos estimados)

- 1. Setup y carga de datos - 15 min
- 2. Análisis exploratorio inicial - 25 min
- 3. Detección de patrones de missing data - 30 min
- 4. Clasificación de tipos de missing data - 20 min
- 5. Detección y análisis de outliers - 25 min
- 6. Estrategias de imputación - 30 min
- 7. Pipeline reproducible - 15 min
- 8. Documentación - 30 min

## Desarrollo

### 1. Setup y Carga de Datos

Configuración del entorno con las librerías necesarias (pandas, numpy, matplotlib, seaborn, scikit-learn) y creación de missing data sintético para practicar diferentes escenarios.

### 2. Análisis Exploratorio Inicial

- Información general del dataset: 2930 registros, 82 columnas
- Identificación de tipos de datos y memoria utilizada
- Estadísticas descriptivas básicas

### 3. Detección de Patrones de Missing Data

- Análisis de columnas con valores faltantes
- Visualización de distribución de missing por fila y columna
- Identificación de patrones sistemáticos en los datos faltantes

### 4. Clasificación de Tipos de Missing Data

- **Year Built**: Patrón MCAR (Missing Completely at Random) - 8% aleatorio
- **Garage Area**: Patrón MAR (Missing at Random) - relacionado con Garage Type
- **SalePrice**: Patrón MNAR (Missing Not at Random) - relacionado con valores altos

### 5. Detección y Análisis de Outliers

- Aplicación de método IQR para distribuciones asimétricas
- Uso de Z-Score para distribuciones normales
- Comparación entre métodos de detección
- Visualización con boxplots y scatter plots

### 6. Estrategias de Imputación

- **Imputación simple**: media, mediana, moda
- **Imputación inteligente**: basada en relaciones entre variables
- **Anti-leakage**: split train/validation/test antes de imputar

### 7. Pipeline Reproducible

Creación de pipeline con ColumnTransformer para procesamiento separado de variables numéricas y categóricas.


## Reflexión

Esta práctica permitió profundizar en el análisis de calidad de datos, destacando la importancia de identificar correctamente los patrones de missing data para aplicar estrategias de imputación apropiadas. La implementación de técnicas anti-leakage y la creación de pipelines reproducibles son esenciales para mantener la integridad de los modelos predictivos. El análisis comparativo pre/post imputación demostró cómo las diferentes estrategias afectan las distribuciones y correlaciones, siendo crucial documentar estas decisiones en proyectos reales.
