---
title: "UT3 - Actividad: PCA y Feature Selection (Ames Housing)"
date: 2025-11-02
---

# UT3 - Actividad 10: PCA y Feature Selection (Resumen)

## Contexto

Análisis comparativo de técnicas de reducción dimensional (PCA) y selección de features (Filter, Wrapper, Embedded) sobre Ames Housing. Enfoque en trade‑off dimensionalidad/performance y validación cross‑validation.

## Objetivos

- Aplicar PCA para reducción dimensional y analizar varianza explicada.
- Evaluar métodos Filter (F-test, Mutual Information).
- Implementar métodos Wrapper (Forward Selection, Backward Elimination, RFE).
- Comparar métodos Embedded (Lasso, Ridge, Random Forest).
- Determinar mejor estrategia según métricas (RMSE, R²) y eficiencia.

## Datos

- Dataset: Ames Housing (1,460 casas).
- Preprocesamiento: imputación (median/most_frequent), label encoding categóricas.
- Target: SalePrice (regresión).
- Features: ~80 variables (numéricas y categóricas codificadas).

## Métodos evaluados (breve)

### PCA (Análisis de Componentes Principales)

- StandardScaler + PCA con n_components variando.
- Análisis de varianza explicada (scree plot).
- Selección por umbral (80%, 90%, 95% varianza).
- Feature reconstruction con loadings.

### Filter Methods

- F-test (SelectKBest con f_regression).
- Mutual Information (SelectKBest con mutual_info_regression).
- Top-k features (k=20 default, evaluado también k=30, 40).

### Wrapper Methods

- Forward Selection (greedy, añade features iterativamente).
- Backward Elimination (greedy, elimina features iterativamente).
- RFE (Recursive Feature Elimination con RandomForest).

### Embedded Methods

- Lasso (L1 regularization, coef ≠ 0).
- Ridge (L2 regularization, penalización coef).
- Random Forest (feature*importances* threshold).

## Métricas reportadas

- RMSE (Root Mean Squared Error) y R² por método.
- Cross-validation 5-fold para validación robusta.
- Reducción dimensional (% features vs original).
- Tiempo de ejecución (wrapper methods más costosos).

## Resultados clave (top 3 métodos)

1. **Mutual Information (Filter)**: Mejor RMSE (~$29k), 39 features, rápido.
2. **Forward Selection (Wrapper)**: RMSE similar (~$29k), 19 features, más costoso.
3. **Random Forest Embedded**: RMSE competitivo, balance features/performance.

## Insights principales (3)

1. Filter methods (MI) = mejor balance velocidad/performance para datasets grandes.
2. Wrapper methods (Forward/RFE) = óptimos cuando se busca mínimo de features manteniendo accuracy.
3. PCA útil para visualización y datasets con multicolinealidad severa, pero puede perder interpretabilidad.

## Trade-offs identificados

- **Velocidad vs Precisión**: Filter rápidos, Wrapper lentos pero más precisos.
- **Interpretabilidad vs Dimensionalidad**: PCA reduce bien pero pierde sentido de features originales.
- **Overfitting vs Underfitting**: Wrapper con riesgo de overfitting si no hay CV; Filter más robustos.

## Recomendación para producción

- Usar **Mutual Information (Filter)** como baseline rápido.
- Si tiempo permite: **RFE** para selección óptima con CV.
- Considerar **Lasso/Ridge** para datasets con multicolinealidad o necesidad de regularización.
- Pipeline: StandardScaler → SelectKBest(MI) → RandomForest/GradientBoosting.

## Próximos pasos (prioritarios)

1. Probar combinación híbrida: Filter (MI) pre-selección + RFE refinamiento.
2. Evaluar en otros datasets (cross-domain validation).
3. Automatizar selección de k óptimo con GridSearchCV.
4. Implementar pipeline completo con versionado de features.
5. Monitorear drift de importancia de features en producción.

## Evidencias

- Descargar el análisis: [Open Practicos](../Practicos/Practico_10.ipynb)
