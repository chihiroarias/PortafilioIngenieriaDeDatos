---
title: "UT2 - Actividad 7 - Detectar y Corregir Sesgo con Fairlearn"
date: 2025-09-16
---

# UT2 - Actividad 7 - Detectar y Corregir Sesgo con Fairlearn

## Contexto

Análisis de sesgo en datasets históricos utilizando técnicas de machine learning ético, aplicando detección y corrección de sesgos en Boston Housing y Titanic con la librería Fairlearn.

## Objetivos

- Detectar sesgo histórico en datasets reales (Boston Housing + Titanic)
- Analizar impacto del sesgo en predicciones de modelos
- Comparar estrategias: detección vs corrección
- Evaluar cuándo detectar vs cuándo corregir automáticamente
- Desarrollar criterios éticos para deployment responsable

## Actividades

### Parte I - Boston Housing: Detectar Sesgo Racial Histórico

**Hallazgos principales:**

- Variable 'B' codifica proporción de población afroamericana
- Correlación con precios: 0.333
- **Brecha de precios detectada:** $4.54k (23.8%)
- Baja proporción afroamericana: $23.35k vs Alta proporción: $18.81k

**Decisión ética:** USAR SOLO PARA EDUCACIÓN - NO PARA PRODUCCIÓN

### Parte II - Titanic: Detectar + Corregir Sesgo Sistemático

**Sesgos identificados:**

- **Género:** Brecha de supervivencia 55.3%
- **Clase:** Brecha entre 1ra y 3ra clase: 35.4%

**Resultados modelos:**

- Baseline: Accuracy = 0.794, Demographic Parity Diff: 0.357
- Modelo Fair: Accuracy = 0.782, Demographic Parity Diff: 0.038

**Trade-off análisis:**

- Performance loss: 1.5%
- Fairness gain: 0.319
- **Recomendación:** ✅ Usar modelo FAIR - excelente trade-off

## Evidencias

- Ingresar al análisis [Open Practicos](../Practicos/Practico7.ipynb)

## Reflexión

Esta práctica demostró la importancia crítica de detectar y corregir sesgos en modelos de machine learning. En Boston Housing, la variable racial históricamente sesgada debe usarse solo con fines educativos, nunca en producción. En Titanic, Fairlearn demostró ser efectivo para reducir significativamente el sesgo de género con mínima pérdida de precisión. La elección entre detección y corrección depende del contexto: detección para análisis histórico, corrección para modelos en producción que afectan a personas reales.
