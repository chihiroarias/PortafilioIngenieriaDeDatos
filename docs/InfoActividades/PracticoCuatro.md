---
title: "UT1 - Practica 3 - Dataset Netflix"
date: 2025-09-09
---

# UT1 - Actividad 3 - Dataset Netflix

## Contexto

Exploración del dataset de taxis, el mismo viene de diversas fuentes con distintas informaciones, una trae las zonas y otra el calendario con fechas importantes.
La idea normalizar los datos y relizar las combinaciones que nos permitan facilitar las rutas en momentos complejos por fechas de eventos.

## Objetivos

- Aprender a integrar datos de múltiples fuentes
- Dominar los diferentes tipos de joins con pandas
- Realizar análisis agregados con groupby
- Crear reportes consolidados de datos integrados

## Actividades (con tiempos estimados)

- 1. Investigar dataset y cargar los datos de las distintas fuentes - 10 min
- 2. Limpieza y normalización de datos - 20 min
- 3. Joins de los datos - 30 min
- 4. Análisis por Borough - 20 min
- 4. Análisis por Borough y Día Especial - 15 min
- 5. Aplicación de técnicas para datasets grandes - 30 min

## Desarrollo

- 1. Investigación del dataset:
     El dataset es de Netflix, contiene información detallada sobre el catálogo de contenido de la plataforma.

- 2.  Limpieza de datos:
      La limpieza mostró una gran parcela de datos faltantes, ante eso se realizó un análisis de los datos faltantes. Posteriormente se descartaron incongruencias o datos con anomalías.

- 3.  Análisis de los datos:
      Primeramente se realizaron diversos análisis del contenido:
      - Por categrías
      - Temporal
      - Geográfico
      - Por género

- 4. Visualizaciones:
     Se realizaron las visualizaciones con el fin de contestar las siguientes preguntas:

     ¿Qué tipo de visualización es más efectiva para mostrar distribuciones temporales? 💡 PISTA: Compara line plot vs area plot vs bar plot

     ¿Por qué usamos diferentes tipos de gráficos para diferentes datos? 💡 PISTA: 🔗 Guía de tipos de gráficos

     ¿Qué insights de negocio obtuviste que Netflix podría usar? 💡 PISTA: Piensa en estrategias de contenido, mercados objetivo, tipos de producción

     ¿Cuál fue la visualización más reveladora y por qué? 💡 PISTA: ¿Qué patrón no esperabas ver?

     ¿Cómo mejorarías este análisis con más datos? 💡 PISTA: Datos de audiencia, ratings de IMDb, presupuestos, etc.

     Dentro de las visualizaciones vemos:

     Datos faltantes: Muestra columnas con valores nulos, clave para la limpieza de datos.

     Análisis temporal: Ilustra la evolución del catálogo de Netflix a lo largo del tiempo.

     Análisis geográfico: Presenta la distribución del contenido por países de origen.

- 5. Documentación: Registro dentro de el portafolio y responder las preguntas en base a la infromación analizadad.

## Evidencias

![Análisis por Borough](../assets/practico3/analisisPorBoroughE3.png)
![Técnicas del dataset](../assets/practico3/tecnicasDatasetE3.png)
![Matriz de correlación](../assets/practico3/matrizCorrelacionesE3.png)

- Ingresar al análisis [Abrir Practicos](../../Practicos/practico4.ipynb)

## Reflexión

La integración de múltiples fuentes (Parquet, CSV, JSON) mediante joins fue el núcleo del proyecto. Dominar las agregaciones con groupby transformó los datos en métricas clave, mientras que el gran volumen exigió optimizar el rendimiento con técnicas y formatos eficientes.
