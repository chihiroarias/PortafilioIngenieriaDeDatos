---
title: "UT3 - Actividad: Temporal Feature Engineering (Online Retail)"
date: 2025-11-02
---

# UT3 - Actividad 11: Temporal Feature Engineering

## Contexto

Análisis práctico de feature engineering temporal sobre dataset Online Retail (e-commerce UK, 2010-2011). Enfoque en lag features, rolling windows, RFM analysis y prevención de data leakage con TimeSeriesSplit.

## Objetivos

- Crear lag features y rolling aggregations con pandas (groupby + shift).
- Implementar RFM analysis (Recency, Frequency, Monetary) por cliente.
- Generar calendar features (día semana, mes, holidays) y encoding cíclico (sin/cos).
- Validar temporalmente con TimeSeriesSplit para prevenir leakage.
- Predecir repeat purchase (clasificación binaria) con Random Forest.

## Datos

- Dataset: Online Retail (Kaggle, ~540k transacciones).
- Período: 2010-2011, e-commerce UK.
- Limpieza: eliminar cancelaciones (InvoiceNo con 'C'), cantidades/precios ≤0, CustomerID nulos.
- Target: `will_purchase_again` (binario, compra en próximos 30 días).
- Nivel de análisis: order-level (1 orden = 1 fila, aggregated desde items).

## Features creadas (resumen)

### Lag Features (shift)

- `orders_last_7d`, `orders_last_30d`: órdenes previas por cliente.
- `revenue_last_7d`, `revenue_last_30d`: ingresos acumulados previos.
- `avg_order_value_last_30d`: valor promedio de órdenes pasadas.
- `days_since_last_order`: recencia desde última compra.

### Rolling Windows

- `orders_rolling_7d`, `orders_rolling_30d`: ventanas móviles de órdenes.
- `revenue_rolling_30d`: ingresos en ventana de 30 días.
- Nota: `closed='left'` para evitar incluir observación actual (leakage).

### RFM Analysis

- **Recency**: días desde última compra.
- **Frequency**: número de órdenes históricas.
- **Monetary**: valor total gastado histórico.
- Percentiles y categorización (High/Medium/Low).

### Calendar Features

- `day_of_week`, `month`, `quarter`, `is_weekend`.
- `is_month_start`, `is_month_end`, `is_quarter_end`.
- Encoding cíclico: `hour_sin`, `hour_cos`, `day_sin`, `day_cos` (continuidad temporal).

### External Variables (simuladas)

- `gdp_growth`, `unemployment_rate`, `consumer_confidence` (datos mensuales).
- Merge con forward fill (nunca backward = leakage).

## Pipeline de validación

- **TimeSeriesSplit** (3-5 folds): garantiza train siempre anterior a validation.
- Train/validation split respeta orden cronológico.
- Verificación: `train_dates.max() < val_dates.min()` en cada fold.

## Métricas reportadas

- **Base Model** (sin temporal features): AUC-ROC baseline.
- **Full Model** (con temporal features): AUC-ROC mejorado.
- Improvement: % de mejora sobre baseline.
- Feature importance: top features por categoría (lag, RFM, calendar, external).

## Resultados clave

- Temporal features mejoran significativamente el AUC (~10-20% improvement típico).
- **Top features**: `days_since_last_order`, `orders_last_30d`, `rfm_recency`.
- Lag y rolling features capturan patrones de comportamiento recurrente.
- RFM sigue siendo altamente predictivo en e-commerce.

## Insights principales (3)

1. **Lag features** = capturan historial reciente de comportamiento (últimos 7/30 días críticos).
2. **TimeSeriesSplit** = esencial para evitar data leakage en problemas temporales.
3. **RFM analysis** = simple pero poderoso, siempre relevante en contextos de clientes recurrentes.

## Prevención de data leakage (crítico)

- **shift(1)**: desplazar aggregations 1 período hacia atrás.
- **closed='left'**: rolling windows excluyen observación actual.
- **forward fill only**: nunca backward fill (usa información futura).
- **TimeSeriesSplit**: validación temporal estricta.
- **No target encoding sin CV**: evitar calcular promedios con el target actual.

## Recomendación para producción

- Pipeline: Limpieza → Lag/Rolling features → RFM → Calendar → TimeSeriesSplit → RandomForest/XGBoost.
- Monitorear drift temporal: distribuciones de features cambian con el tiempo.
- Re-entrenar periódicamente: modelos temporales degradan performance sin actualización.
- Guardar ventanas históricas: necesarias para generar lags en nuevas predicciones.

## Próximos pasos (prioritarios)

1. Probar XGBoost/LightGBM (mejor manejo de features temporales).
2. Explorar LSTM/GRU para secuencias largas de comportamiento.
3. Feature interaction: productos de features temporales (e.g., recency × frequency).
4. Segmentación de clientes: aplicar estrategias diferentes por segmento RFM.
5. Automatizar feature engineering temporal con tsfresh o featuretools.

## Evidencias

- Descargar el análisis: [Practico_11.ipynb](../Practicos/Practico_11.ipynb)
