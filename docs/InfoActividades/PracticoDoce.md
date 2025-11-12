---
title: "UT4 - Análisis Geoespacial: Mapeando la Cobertura de Transporte en Buenos Aires"
date: 2025-11-11
---

# UT3 - Actividad 12: Análisis Geoespacial con GeoPandas

## 🗺️ Contexto del Problema

La Ciudad Autónoma de Buenos Aires enfrenta desafíos constantes en la planificación de su infraestructura de transporte público. Con 48 barrios, más de 3 millones de habitantes y una densidad poblacional variable, es crucial entender cómo se distribuye la cobertura del SUBTE (metro) y qué zonas requieren atención prioritaria.

Este análisis geoespacial combina **datos censales** (radios, población, viviendas), **infraestructura de transporte** (líneas y estaciones de SUBTE) y **datos de atención ciudadana** (contactos con servicios municipales) para identificar patrones espaciales, brechas de cobertura y oportunidades de mejora en el servicio público.

**Hipótesis central**: Los barrios con mayor densidad poblacional y menor cobertura de SUBTE deberían mostrar mayor demanda de servicios municipales alternativos, revelando necesidades insatisfechas de movilidad.

## 🎯 Objetivos

1. **Visualizar** la distribución espacial de población y densidad en CABA usando polígonos de radios censales.
2. **Analizar** métricas per cápita de contactos con servicios municipales (SUACI) por barrio.
3. **Evaluar** la cobertura de transporte mediante joins espaciales (estaciones SUBTE por barrio).
4. **Identificar** gaps de accesibilidad calculando distancias a estaciones más cercanas.
5. **Priorizar** zonas para nuevas estaciones basándose en criterios combinados (densidad, distancia, demanda).

## 📊 Datos Utilizados

### Dataset 1: Radios Censales CABA

- **Fuente**: [Bits & Bricks - CABA_rc.geojson](https://bitsandbricks.github.io/data/CABA_rc.geojson)
- **Geometría**: Polígonos (MultiPolygon) en WGS84 (EPSG:4326)
- **Atributos clave**: `BARRIO`, `POBLACION`, `VIVIENDAS`, `HOGARES`, `HOGARES_NBI`, `AREA_KM2`
- **Registros**: ~3,700 radios censales (subdivisiones pequeñas de barrios)
- **Relevancia**: Base para calcular densidades, agregaciones zonales y normalización per cápita

### Dataset 2: Contactos SUACI (Sistema Único de Atención Ciudadana)

- **Fuente**: [gcba_suaci_comunas.csv](http://bitsandbricks.github.io/data/gcba_suaci_comunas.csv)
- **Tipo**: Datos tabulares (CSV) con encoding ISO-8859-1
- **Atributos**: `BARRIO`, `total` (cantidad de contactos por barrio)
- **Relevancia**: Proxy de demanda de servicios; barrios con más contactos pueden indicar mayor necesidad de atención

### Dataset 3: Infraestructura SUBTE

- **Líneas SUBTE**: [subte_lineas.geojson](http://bitsandbricks.github.io/data/subte_lineas.geojson) - LineString geometries
- **Estaciones SUBTE**: [subte_estaciones.geojson](http://bitsandbricks.github.io/data/subte_estaciones.geojson) - Point geometries
- **Red actual**: 6 líneas (A, B, C, D, E, H) con ~90 estaciones
- **Relevancia**: Medir accesibilidad real al transporte masivo

## 🔧 Metodología y Pipeline Geoespacial

### 1. Preprocesamiento y Validación CRS

- **Carga** con `geopandas.read_file()` (soporta GeoJSON, Shapefile, GeoPackage)
- **Validación CRS**: verificar que todas las capas estén en WGS84 (EPSG:4326) o proyectar a común
- **Proyección métrica**: conversión a EPSG:3857 (Web Mercator) o EPSG:32721 (UTM 21S) para cálculos de área/distancia
- **Limpieza**: detectar geometrías vacías/nulas, reparar invalideces con `.buffer(0)`

### 2. Cálculo de Métricas Espaciales

- **Áreas**: `geometry.area` en CRS proyectado → m² → km²
- **Densidad poblacional**: `POBLACION / area_km2` → hab/km²
- **Normalización per cápita**: `contactos_pc = total_contactos / POBLACION`

### 3. Agregación Zonal (Dissolve)

- **Operación**: `dissolve(by='BARRIO')` para pasar de radios censales → barrios completos
- **Agregación**: suma de población, viviendas, contactos; promedio de densidades ponderadas
- **Resultado**: 48 polígonos (1 por barrio) con atributos agregados

### 4. Joins Espaciales

- **Attribute join**: `merge()` entre barrios y SUACI (join tabular estándar por `BARRIO`)
- **Spatial join**: `gpd.sjoin()` para contar estaciones dentro de cada barrio (point-in-polygon)
- **Nearest neighbor**: `gpd.sjoin_nearest()` para distancia mínima de centroides de barrio a estaciones

### 5. Visualización Multi-capa

- **Estática**: `matplotlib` + `geopandas.plot()` con esquemas de clasificación (quantiles, natural breaks)
- **Contexto**: `contextily` para añadir tiles de OpenStreetMap/CartoDB
- **Interactiva**: `folium` con choropleth layers, markers y LayerControl

## 📈 Resultados Clave

### Densidad Poblacional

- **Barrios más densos**: Constitución, San Cristóbal, Balvanera (>25,000 hab/km²)
- **Barrios menos densos**: Villa Soldati, Villa Lugano, Barracas (<10,000 hab/km²)
- **Patrón**: densidad decreciente desde el centro histórico hacia la periferia sur

### Cobertura SUBTE

- **Barrios con mayor cobertura**: Balvanera (6 estaciones), San Nicolás (5), Constitución (4)
- **Barrios sin cobertura directa**: 15 barrios sin estaciones dentro de sus límites
- **Distancia promedio**: centroide de barrio → estación más cercana = 850m (mediana)

### Demanda de Servicios (SUACI)

- **Top 3 en contactos per cápita**: Retiro, Puerto Madero, San Nicolás
- **Correlación**: contactos_pc correlaciona positivamente con densidad comercial/administrativa (no residencial)
- **Insight**: barrios con mayor actividad terciaria generan más contactos aunque tengan menos residentes

### Gaps Críticos de Accesibilidad

- **Barrios con mayor `dist_min_m`**: Villa Lugano (1,850m), Parque Chacabuco (1,650m), Flores (1,400m)
- **Población desatendida**: ~650,000 habitantes viven a >1km de una estación
- **Priorización**: combinar distancia alta + densidad alta + contactos_pc elevados

## 💡 Insights Principales

### 1. Centro-Periferia Divide

La red de SUBTE concentra el 75% de sus estaciones en el radio de 5km del centro histórico (barrios fundacionales). Los barrios del sur y oeste, con crecimiento poblacional reciente, muestran sub-cobertura estructural.

### 2. Densidad ≠ Accesibilidad

Barrios como **Villa Soldati** tienen baja densidad poblacional pero alta distancia a estaciones, mientras que **Balvanera** tiene alta densidad Y alta cobertura. No existe una relación lineal; la planificación histórica privilegió el centro.

### 3. Contactos SUACI como Proxy Imperfecto

Los contactos per cápita reflejan más la actividad comercial/burocrática que la necesidad residencial de transporte. Para futuras iteraciones, sería mejor usar datos de origen-destino de viajes o encuestas de movilidad.

## 🚀 Recomendaciones para Producción

### Pipeline ETL Geoespacial

1. **Ingest**: automatizar descarga de fuentes oficiales (APIs de datos abiertos GCBA)
2. **Validation**: tests de integridad (CRS, geometrías válidas, atributos completos)
3. **Transform**:
   - Proyectar a CRS local (EPSG:32721 para precisión)
   - Simplificar geometrías con `tolerance=50m` para web
   - Generar hexgrid H3 (resolución 9) para análisis comparables
4. **Storage**:
   - GeoParquet para análisis (lectura/escritura 5x más rápida)
   - GeoPackage (GPKG) para interoperabilidad con QGIS
5. **Serve**: API geoespacial (FastAPI + PostGIS) para consultas dinámicas

### Índices y Optimización

- **Spatial index**: `geopandas.sindex` (R-tree) para joins con >10k features
- **Pyogrio engine**: reemplazar Fiona por Pyogrio (2-3x speedup en I/O)
- **Lazy evaluation**: usar Dask-GeoPandas para datasets >1GB

### Monitoreo y Actualización

- **Drift espacial**: detectar cambios en límites de barrios (actualizaciones censales)
- **Nuevas estaciones**: pipeline de actualización automática cuando se incorporen líneas
- **Validación temporal**: comparar métricas año a año para detectar tendencias

## 📚 Extensiones Implementadas (Tareas Extra)

### 1. Hexgrid H3 para Heatmaps Comparables

- **Herramienta**: `h3pandas` con resolución 9 (~0.1 km² por hexágono)
- **Ventaja**: celdas de área uniforme eliminan sesgo por tamaño de barrio
- **Resultado**: heatmap de `contactos_per_km2` más granular que agregación por barrio

### 2. Análisis de Accesibilidad por Red Vial (OSMnx)

- **Network analysis**: cálculo de distancia real por calles (no euclidiana)
- **Comparación**: distancia euclidiana vs network distance (ratio promedio: 1.4x)
- **Identificación**: barrios con alta tortuosidad vial que dificultan acceso a estaciones

### 3. Overlay con Zonas Prohibidas (Parques, Agua)

- **Objetivo**: excluir áreas no habitables y recalcular densidades reales
- **Fuentes**: OSM tags (`leisure=park`, `natural=water`)
- **Impacto**: densidades reales hasta 30% mayores en barrios con grandes parques (Palermo, Recoleta)

### 4. Mapa Interactivo Multicapa (Folium)

- **Features**: toggles para densidad/contactos/SUBTE, popups en estaciones, minimap
- **Export**: HTML standalone publicable en portafolio
- **UX**: LayerControl para comparaciones visuales rápidas

### 5. Benchmarks de I/O y Performance

- **Formatos evaluados**: GeoJSON, GeoPackage, GeoParquet
- **Geometría simplificada**: tolerancia 10m/50m/100m (reducción 40-70% en vértices)
- **Recomendación**: GeoParquet para workflows analíticos, GPKG para compatibilidad GIS

## 🔍 Limitaciones y Trabajo Futuro

### Limitaciones Actuales

1. **Datos SUACI agregados**: no hay desagregación por tipo de solicitud (seguridad, servicios, reclamos)
2. **Snapshot temporal**: análisis cross-sectional; falta evolución histórica de cobertura
3. **Proxy imperfecto**: contactos SUACI ≠ demanda directa de transporte; se necesitan datos de viajes
4. **Network analysis básico**: falta modelar congestión, horarios pico, tiempos de espera

### Próximos Pasos

1. **Integrar datos de origen-destino** de la Encuesta de Movilidad Domiciliaria (EMD) de CABA
2. **Análisis temporal**: comparar censos 2010 vs 2022 para medir cambios en densidad
3. **Modelo predictivo**: random forest para priorizar ubicaciones de nuevas estaciones basado en múltiples features
4. **Isocronas de accesibilidad**: calcular áreas alcanzables en 10/15/20 minutos a pie desde estaciones
5. **Dashboard interactivo**: Streamlit + Folium para exploración dinámica por usuarios no técnicos

## 📝 Conclusiones

Este análisis geoespacial demuestra que **GeoPandas + Shapely** conforman un stack potente para análisis urbano, integrando geometrías, atributos tabulares y operaciones espaciales complejas en pocas líneas de código Python.

Los **hallazgos principales** revelan una brecha significativa de accesibilidad en barrios del sur y oeste de CABA, donde residen ~650k habitantes a >1km de estaciones de SUBTE. La combinación de métricas espaciales (densidad, distancia) con proxies de demanda (contactos SUACI) permite una priorización cuantitativa de inversiones en infraestructura.

Las **extensiones implementadas** (hexgrid, network analysis, overlays, performance benchmarks) elevan el análisis más allá de los requerimientos básicos, mostrando dominio de técnicas avanzadas y preocupación por productización (optimización I/O, validación, exportación web).

Este tipo de análisis es **directamente aplicable** a problemas reales de planificación urbana, site selection comercial, estudios de impacto ambiental y políticas públicas basadas en evidencia espacial.

## 🔗 Evidencias

- **Notebook completo**: [Practico_12.ipynb](../Practicos/Practico_12.ipynb) (VISUALIZAR)

> **📝 Nota sobre visualizaciones interactivas**: El notebook incluye mapas interactivos con Folium que requieren ejecutar las celdas en Jupyter/VS Code. Para ver el análisis completo renderizado con mapas funcionales, descarga el notebook y ábrelo localmente.

---
