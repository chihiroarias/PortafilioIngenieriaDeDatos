---
title: "UT3 - Práctica: Feature Engineering y Análisis rápido"
date: 2025-10-21
---

# UT3 - Práctica: Feature Engineering y Análisis rápido

## Contexto

Breve análisis de creación y evaluación de features sobre un dataset sintético de viviendas, aplicado como prueba a una muestra del Ames Housing.

## Objetivos

- Generar features útiles para predecir precio de viviendas.
- Evaluar distribución, outliers y calidad de las nuevas features.
- Medir importancia de features (Mutual Information, Random Forest).
- Validar el enfoque en una muestra real (Ames).

## Actividades (resumido)

- Crear dataset sintético (n=1000) con variables base: price, sqft, bedrooms, bathrooms, year_built, garage_spaces, lot_size, distance_to_city, school_rating, crime_rate.
- Construir features: ratios, temporales, transformaciones y scores compuestos.
- EDA: histogramas y detección de outliers (IQR).
- Evaluación: mutual_info_regression y RandomForestRegressor (n=100).
- Aplicación rápida de las transformaciones a muestra de Ames Housing.

## Datos

- Sintético: 1.000 filas, controles para valores positivos.
- Real: muestra de Ames Housing (5 registros) usada para ver consistencia de features.

## Features creadas (clave)

- Ratios: price_per_sqft, sqft_per_bedroom, bed_bath_ratio.
- Temporales: property_age, age_category, is_new_property.
- Transformaciones: log_price, sqrt_sqft, log_lot_size.
- Compuestas: luxury_score, location_score, efficiency_score.

## Análisis realizado (puntos)

- Distribuciones y skewness por feature.
- Outliers detectados con IQR (conteo y bounds).
- Top features por MI y por RandomForest (tablas y gráficas comparativas).
- Correlación con target en muestra Ames.

## Insights clave (3)

- price_per_sqft y sqft_per_bedroom son predictores fuertes.
- Log/sqrt ayudan a normalizar y mejorar relación con precio.
- Scores compuestos agregan señal útil cuando combinan variables relevantes.

## Limitaciones y buenas prácticas

- Evitar data‑leakage: aplicar transformaciones tras split.
- Documentar criterio de outliers (IQR) y evaluar efecto en modelos.
- Validar en datasets reales y ampliar muestras.

## Próximos pasos (prioritarios)

1. Ejecutar en el Ames Housing completo.
2. Selección automática (RFECV / Lasso).
3. Construir Pipeline reproducible (ColumnTransformer + Pipeline).
4. Añadir pruebas unitarias para transformaciones.
5. Evaluar modelos (LinearReg, RF, GB) con CV.

## Evidencias

- Ingresar al análisis [Open Practicos](../Practicos/Practico_8.ipynb)

