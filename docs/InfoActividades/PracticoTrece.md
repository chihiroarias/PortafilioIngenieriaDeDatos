---
title: "UT4 - Actividad 13 - Preprocesamiento de Imágenes"
date: 2025-11-02
---

# UT4 - Actividad 13: Preprocesamiento de Imágenes

## Contexto

Implementación práctica de un pipeline completo de preprocesamiento de imágenes, abarcando espacios de color, mejora de contraste, técnicas de suavizado y detección de features locales. Análisis aplicado sobre dataset de imágenes clásicas utilizando OpenCV y scikit-image.

## Objetivos

- Implementar representación y manipulación de imágenes como matrices
- Explorar conversiones entre espacios de color (RGB, HSV, LAB)
- Aplicar técnicas de mejora de contraste (global vs adaptativo CLAHE)
- Comparar métodos de suavizado preservando bordes (Gaussian vs Bilateral)
- Detectar y describir features locales con ORB/SIFT
- Evaluar impacto del preprocesamiento en calidad de features

## Datos

- **Dataset**: Imágenes clásicas de scikit-image
- **Imágenes incluidas**: camera, astronaut, coffee, coins, checkerboard, rocket, page
- **Formato**: PNG, 8-bit (rango 0-255)
- **Dimensiones**: Variables según imagen
- **Canales**: Grayscale y RGB

## Metodología

### 1. Representación e Inspección Inicial

- Lectura de imágenes con OpenCV (formato BGR)
- Conversión a RGB y escala de grises
- Análisis de propiedades: dimensiones, dtype, rango dinámico
- Generación de histogramas por canal para diagnóstico

### 2. Espacios de Color y Contraste

**Conversiones aplicadas:**

- RGB → HSV (Hue, Saturation, Value)
- RGB → LAB (Lightness, A, B)

**Técnicas de mejora de contraste:**

- **Ecualización global**: `cv2.equalizeHist()` en escala de grises
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: Aplicado sobre canal L\* de LAB
  - Parámetros: `clipLimit=2.0`, `tileGridSize=(8,8)`
  - Ventaja: Mejora contraste local sin saturar regiones homogéneas

**Métrica de contraste**: Desviación estándar de intensidades

### 3. Suavizado y Preservación de Bordes

**Filtros evaluados:**

- **Gaussian Blur**: `ksize=(5,5)`, `sigmaX=0` - Suavizado uniforme
- **Bilateral Filter**: `d=9`, `sigmaColor=75`, `sigmaSpace=75` - Preserva bordes

**Detección de bordes**: Canny Edge Detector con umbrales (100, 200)

**Métricas:**

- Varianza de gradientes: mide "rugosidad" de la imagen
- Edge ratio: proporción de píxeles clasificados como bordes

### 4. Detección de Features Locales

**Detector utilizado**: ORB (Oriented FAST and Rotated BRIEF)

- Parámetros: `nfeatures=1000`, `scaleFactor=1.2`, `nlevels=8`
- Descriptores binarios (256 bits)

**Variantes comparadas:**

- Original (grayscale)
- Gaussian blur
- CLAHE en canal L\*

**Evaluación de repetibilidad:**

- Matching entre variantes con BFMatcher (NORM_HAMMING, crossCheck=True)
- Métrica: `matches_ratio = matches / min(kp1, kp2)`

## Resultados Clave

### Análisis de Contraste

- **Rango dinámico típico**: 0-255 (8-bit completo)
- **CLAHE vs Global**: CLAHE preserva mejor detalles en regiones con iluminación variable
- **STD aumenta** tras ecualización: indicador de mayor contraste

### Suavizado y Bordes

- **Bilateral filter**: Mejor preservación de bordes (mayor varianza de gradientes)
- **Gaussian blur**: Reduce ruido pero difumina estructuras finas
- **Edge ratio**: Bilateral mantiene más bordes relevantes con menos ruido

### Features Locales

- **CLAHE aumenta densidad de keypoints**: Mayor contraste local → más puntos detectables
- **Repetibilidad alta con CLAHE**: Descriptores más distintivos y consistentes
- **Trade-off nfeatures vs tiempo**: Más features = mayor precisión pero más costo computacional

## Insights Principales

1. **Canal L\* (LAB) es ideal para ajustes de contraste**: Separa luminancia de cromaticidad, evitando distorsión de colores al aplicar CLAHE.

2. **Bilateral filter es superior para feature detection**: Preserva bordes críticos mientras elimina ruido, resultando en keypoints más robustos.

3. **Preprocesamiento impacta directamente en feature quality**: CLAHE en L\* incrementó keypoints detectados ~20-30% y mejoró repetibilidad en matching.

4. **Checks automáticos de calidad son esenciales**:
   - `num_keypoints < 100`: alerta de baja calidad de imagen
   - `edges_ratio ∉ [0.02, 0.15]`: posible ruido excesivo o falta de detalle
   - `contrast_std < 20`: imagen de bajo contraste requiere preprocesamiento

## Tareas Extras Implementadas

### 1. Curva Sensibilidad-Ruido

- **Barrido de parámetros CLAHE**: clipLimit [1.5-4.0] × tileSize [4-16]
- **Resultado**: clipLimit=2.5 con tileSize=8 ofrece mejor balance
- **Trade-off visualizado**: Más clipLimit → más keypoints pero más ruido (edge ratio aumenta)

### 2. Benchmark SIFT vs ORB

**Comparación de descriptores:**

| Métrica           | ORB (binario) | SIFT (flotante)        |
| ----------------- | ------------- | ---------------------- |
| Tiempo            | ~0.05s        | ~0.15s                 |
| Keypoints         | ~800-1000     | ~900-1100              |
| Matches válidos   | ~450-600      | ~500-700               |
| Tamaño descriptor | 256 bits      | 128 floats (512 bytes) |

**Conclusión**: ORB es **3x más rápido** que SIFT con calidad comparable para matching básico. SIFT ofrece ~10% más matches pero con mayor costo.

### 3. Dashboard QA - KPIs por Lote

**Métricas monitoreadas:**

- Conteo de features (threshold: >100)
- Contraste STD (threshold: >20)
- Porcentaje de bordes (rango: 2-15%)
- Repetibilidad (ratio de matches)

**Sistema de alertas**:

- ⚠️ LOW_FEATURES: imagen degradada o baja textura
- ⚠️ EDGES_OUT_OF_RANGE: ruido excesivo o falta de estructura
- ⚠️ LOW_CONTRAST: requiere ecualización

## Limitaciones y Consideraciones

- **CLAHE puede amplificar ruido**: Requiere suavizado previo en imágenes muy ruidosas
- **Parámetros dataset-específicos**: clipLimit y tileSize deben ajustarse según contenido
- **ORB no es invariante a escala extrema**: Para cambios de escala >3x considerar SIFT
- **Bilateral filter es costoso**: Para pipelines en tiempo real evaluar aproximaciones rápidas

## Recomendaciones para Producción

1. **Pipeline estándar**:

   - Conversión a LAB
   - CLAHE en L\* (clipLimit=2.0-2.5, tileSize=8)
   - Bilateral filter (d=9, sigmaColor=75, sigmaSpace=75)
   - Detección con ORB (nfeatures=1000-1500)

2. **Configuración según escenario**:

   - **Baja iluminación**: Aumentar clipLimit a 3.0-3.5
   - **Alta resolución**: Incrementar tileSize a 12-16
   - **Tiempo real**: Usar ORB con nfeatures=500, considerar GPU

3. **Monitoring continuo**:
   - Registrar KPIs por imagen (num_features, contrast_std, edges_ratio)
   - Alertas automáticas para imágenes fuera de rangos esperados
   - Baseline de referencia por tipo de escena

## Próximos Pasos

1. Evaluar descriptores deep learning (SuperPoint, D2-Net) para mayor robustez
2. Implementar pipeline con tracking temporal para video
3. Automatizar selección de parámetros con GridSearch sobre métricas de matching
4. Integrar con sistema de QA para detección de anomalías en lote
5. Probar en datasets específicos de dominio (médico, satelital, industrial)

## Evidencias

- **Notebook completo**: Ver análisis interactivo completo abajo
- **Código fuente**: [Practico_13.ipynb](../Practicos/Practico_13.ipynb) (VISUALIZAR)
