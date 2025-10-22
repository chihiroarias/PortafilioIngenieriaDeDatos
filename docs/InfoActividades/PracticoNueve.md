---
title: "UT3 - Actividad: Encoding Categórico y Pipelines (Adult Income)"
date: 2025-10-21
---

# UT3 - Actividad 9: Encoding Categórico y Pipelines (Resumen)

## Contexto

Análisis práctico sobre técnicas de codificación para variables categóricas (Adult Income). Enfoque en cardinalidad, prevención de data‑leakage y balance rendimiento/dimensionalidad.

## Objetivos

- Evaluar Label, One‑Hot (baja cardinalidad) y Target Encoding (alta cardinalidad).
- Construir pipeline con branching (ColumnTransformer).
- Medir accuracy, AUC y F1; analizar trade‑offs y explicabilidad.

## Datos

- Dataset: Adult Income (UCI).
- Limpieza: strip categorías, drop NA.
- Target: income >50K → target binario.
- Cardinalidad destacada: native-country (alta).

## Experimentos (breve)

- Label Encoding (todas las categóricas) → RandomForest.
- One‑Hot Encoding (solo baja cardinalidad) → RandomForest.
- Target Encoding (alta cardinalidad, CV para evitar leakage) → RandomForest.
- Branched Pipeline: One‑Hot (baja) + Target (alta) + StandardScaler (num) → RandomForest.

## Métricas reportadas (por experimento)

- Métricas: Accuracy, AUC-ROC, F1, training_time, n_features.
- Observación general: Branched Pipeline suele dar mejor trade‑off (accuracy alto, dimensionalidad controlada).
- Nota: Target Encoding requiere CV/smoothing para evitar overfitting.

## Explicabilidad

- Se extrajeron feature names post‑preprocessor y se analizaron importancias del RandomForest.
- Análisis por tipo de feature (numérica, one‑hot, target‑encoded) para evaluar aporte relativo.

## Insights clave (3)

1. One‑Hot = buena para baja cardinalidad; explota información pero escala mal.
2. Target Encoding = eficiente en alta cardinalidad pero exige CV y smoothing.
3. Pipeline branched combina ventajas: mantiene información sin explosionar dimensión.

## Problemas críticos y mitigaciones

- Riesgo de data‑leakage con target encoding → Mitigar con CV o leave‑one‑out / smoothing.
- Categorías no vistas → manejar con handle_unknown / values por defecto.
- Explosión dimensional → usar target/binary/embedding según caso.

## Recomendación para producción (resumida)

- Usar Branched Pipeline (ColumnTransformer): One‑Hot para ≤10 categorías, Target/Binary/Embeddings para alta cardinalidad.
- Guardar encoders (versionar), monitorizar drift de categorías y reentrenar periódicamente.

## Próximos pasos (prioritarios)

1. Ejecutar experimentos con cross‑validation completo y reporte reproducible.
2. Tunear smoothing en TargetEncoder y comparar con Binary/Embedding.
3. Implementar tests unitarios para transformaciones y E2E para pipeline.
4. Evaluar embeddings para categorías con cardinalidad muy alta.

## evidencia

- Descargar el análisis: [Open Practicos](../Practicos/Practico_9.ipynb)
