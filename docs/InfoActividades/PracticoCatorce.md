---
title: "UT4 - Actividad 14 - Audio como Dato"
date: 2025-11-02
---

# UT4 - Actividad 14: Audio como Dato

## Contexto

Diseño e implementación de un pipeline completo de preprocesamiento de audio para Machine Learning, abarcando desde la carga y visualización de señales hasta la extracción de características MFCC (Mel-Frequency Cepstral Coefficients) listas para modelos de clasificación. Análisis aplicado con librosa sobre audios sintéticos y potencialmente el dataset UrbanSound8K.

## Objetivos

- Implementar carga y representación de señales de audio como arrays
- Visualizar waveforms y espectrogramas para inspección de calidad
- Estandarizar audios: sample rate, duración, mono/stereo, normalización
- Aplicar técnicas de limpieza: recorte de silencios, filtros high-pass
- Extraer features MFCC y métricas espectrales para ML
- Exportar características en formato tabular (CSV) listo para modelado

## Datos

- **Dataset**: Audios sintéticos generados (tonos + ruido) o UrbanSound8K
- **Formato**: WAV, MP3, FLAC, OGG
- **Características de audios sintéticos**:
  - 5 muestras generadas
  - Sample rate: 22,050 Hz
  - Duración: 4.0 segundos
  - Contenido: Tonos puros (440-840 Hz) + ruido gaussiano
- **Preprocesamiento objetivo**:
  - Sample rate unificado: 16,000 Hz
  - Duración fija: 3.0 segundos
  - Mono canal
  - Normalización a amplitud máxima 0.99

## Metodología

### 1. Representación e Inspección Inicial

**Carga de audio:**

- Uso de `librosa.load()` con parámetros configurables (sr, mono)
- Conversión automática a mono mediante promedio de canales
- Extracción de metadatos: shape, dtype, sample rate, duración

**Análisis estadístico:**

- Amplitud mínima/máxima
- Media y desviación estándar de la señal
- Detección de normalización previa

**Visualización:**

- Waveform en dominio temporal (amplitud vs tiempo)
- Identificación visual de clipping, silencios, patrones

### 2. Estandarización del Audio

**Pipeline de preprocesamiento (`preprocess_audio`):**

1. **Conversión a mono**: Promedio de canales si stereo
2. **Recorte de silencios**: `librosa.effects.trim()` con `top_db=30`
   - Elimina segmentos con amplitud < -30 dB respecto al pico
3. **Resampling**: `librosa.resample()` a 16,000 Hz
   - Reduce tamaño manteniendo frecuencias relevantes para voz/sonidos urbanos
4. **Ajuste de duración**:
   - Recorte si > 3.0s (toma los primeros 48,000 samples)
   - Padding con ceros si < 3.0s
5. **Normalización de amplitud**:
   - Escala pico a 0.99 para maximizar rango dinámico sin clipping

**Parámetros clave:**

- `TARGET_SR = 16000` Hz
- `TARGET_DURATION = 3.0` s
- `TARGET_AMPLITUDE = 0.99`
- `TOP_DB = 30.0` dB

### 3. Espectrogramas y Limpieza de Ruido

**Espectrograma de potencia:**

- STFT (Short-Time Fourier Transform) con `n_fft=2048`, `hop_length=512`
- Conversión a escala dB: `librosa.amplitude_to_db()`
- Visualización tiempo-frecuencia con `librosa.display.specshow()`

**Inyección de ruido blanco:**

- Función `add_white_noise()` con control de SNR (Signal-to-Noise Ratio)
- SNR objetivo: 10 dB para simular condiciones realistas
- Cálculo: `noise_power = signal_power / (10^(SNR/10))`

**Filtro High-Pass Butterworth:**

- Orden 4, corte en 80 Hz
- Elimina ruido de baja frecuencia (hum, rumble)
- Preserva frecuencias de interés para voz y sonidos ambientales

**Métricas de ruido:**

- Relación señal-ruido (SNR) en dB
- Distribución espectral de energía

### 4. Extracción de MFCC y Features

**MFCC (Mel-Frequency Cepstral Coefficients):**

- `n_mfcc = 13` coeficientes por defecto
- Capturan envolvente espectral relevante para percepción auditiva
- Agregación estadística por coeficiente:
  - Media (`mfcc_i_mean`)
  - Desviación estándar (`mfcc_i_std`)

**Features complementarios:**

- **RMS (Root Mean Square)**: Energía promedio de la señal
- **ZCR (Zero-Crossing Rate)**: Tasa de cruces por cero, indicador de tono/ruido

**Pipeline de extracción:**

```python
extract_mfcc_features(y, sr, n_mfcc=13)
→ 28 features: 13×(mean+std) + rms_mean + zcr_mean
```

**Exportación:**

- DataFrame de pandas con features por archivo
- Columnas adicionales: `filename`, `sr`, `duration_sec`
- Guardado en CSV para entrenamiento de modelos

## Resultados Clave

### Análisis de Estandarización

- **Reducción de sample rate (22.05 kHz → 16 kHz)**: ~27% menos datos sin pérdida perceptual
- **Duración fija (3.0s)**: Uniformidad para batch processing en ML
- **Normalización a 0.99**: Maximiza resolución numérica, evita clipping

### Impacto de Limpieza

- **Recorte de silencios**: Elimina 0.5-2.0s de silencio inicial/final típicamente
- **High-pass (80 Hz)**: Reduce energía en banda 0-80 Hz sin afectar contenido útil
- **Ruido blanco (SNR=10 dB)**: Degrada features MFCC ~15-20% en media

### Características de MFCC

- **MFCC 1-3**: Capturan envolvente espectral general (energía, timbre)
- **MFCC 4-13**: Detalles finos de textura sonora
- **Varianza alta en MFCC**: Indica transiciones/eventos (golpes, speech)
- **RMS mean**: Correlaciona con loudness percibido

## Insights Principales

1. **Sample rate 16 kHz es óptimo para audio ambiental**: Captura frecuencias hasta 8 kHz (Nyquist), suficiente para voz y sonidos urbanos. Reduce cómputo vs 44.1 kHz sin pérdida de información relevante.

2. **Recorte de silencios (`top_db=30`) es crítico**: Elimina ruido de fondo suave sin afectar eventos de interés. Valores más bajos (20 dB) son más agresivos, más altos (40 dB) más conservadores.

3. **MFCC son features compactos y efectivos**: 13 coeficientes (26 con mean+std) capturan esencia espectral con ~50x menos dimensionalidad que espectrograma completo. Trade-off dimensionalidad vs información.

4. **Normalización de amplitud previene bias**: Audios con volúmenes inconsistentes pueden sesgar modelos. Normalizar a pico fijo (0.99) garantiza comparabilidad.

5. **High-pass (80 Hz) mejora calidad sin pérdida**: Voz humana inicia ~85 Hz (bajo masculino), sonidos ambientales relevantes >100 Hz. Filtro elimina rumble/hum sin afectar señal útil.

## Tareas Extras Implementadas

### 1. Curva SNR → Cambio en Features

**Experimento**: Variar SNR [0, 5, 10, 20 dB] y medir impacto en features

**Resultados:**

- **RMS mean**: Aumenta con ruido (energía adicional)
- **MFCC variance**: Degrada con ruido bajo (SNR <5 dB)
- **Umbral crítico**: SNR <10 dB degrada calidad de features significativamente

**Aplicación**: Definir umbral de calidad mínima (SNR >15 dB recomendado)

### 2. Benchmark de Pipelines de Limpieza

**Comparación de 3 pipelines:**

| Pipeline  | Procesamiento          | RMS mean | ZCR mean | Observaciones             |
| --------- | ---------------------- | -------- | -------- | ------------------------- |
| Raw       | Sin filtros            | Baseline | Baseline | Incluye ruido grave       |
| High-pass | Filtro 80 Hz           | -5%      | Similar  | Elimina rumble            |
| HP + Trim | HP + recorte silencios | -8%      | -10%     | Óptimo: limpio y compacto |

**Recomendación**: Pipeline 3 (HP + Trim) para producción

### 3. Dashboard QA de Audio

**KPIs monitoreados (200 muestras):**

1. **Duración**: Histograma muestra concentración en 3.0s (objetivo cumplido)
2. **RMS mean**: Distribución normal indica normalización correcta
3. **ZCR mean**: Rango [0.05-0.15] típico para audios limpios

**Alertas automáticas:**

- ⚠️ Duración fuera de rango [2.5, 3.5]s
- ⚠️ RMS mean < 0.05 (muy silencioso) o > 0.5 (posible clipping)
- ⚠️ ZCR > 0.2 (ruido excesivo)

### 4. Métricas Espectrales Adicionales

**Features complementarios a MFCC:**

- **Spectral Centroid**: "Centro de masa" del espectro (correlaciona con brillo)
- **Spectral Rolloff**: Frecuencia bajo la cual está el 85% de la energía
- **Spectral Bandwidth**: Ancho de banda del espectro (relacionado con timbre)

**Visualización temporal**: Gráficos de evolución de métricas para análisis dinámico

### 5. Augmentación de Datos

**Técnicas aplicadas:**

1. **Pitch Shift**: +2 semitonos con `librosa.effects.pitch_shift()`
   - Mantiene duración, cambia frecuencias
   - Útil para generalizar modelos
2. **Time Stretch**: 0.9x con `librosa.effects.time_stretch()`
   - Cambia duración manteniendo pitch
   - Simula variaciones de tempo

**Impacto en MFCC**: Genera variantes para data augmentation en training

## Limitaciones y Consideraciones

- **MFCC pierden información temporal fina**: Agregación por mean/std elimina dinámica. Para capturar eventos transitorios considerar MFCC secuenciales (frames) o delta-MFCC.
- **Audios sintéticos simplifican problema**: Tonos puros + ruido gaussiano no capturan complejidad de audio real (reverberación, overlaps, efectos Doppler).
- **Normalización puede amplificar ruido**: En audios muy silenciosos, normalizar a 0.99 amplifica ruido de fondo. Considerar umbral mínimo de RMS.
- **Sample rate 16 kHz limita frecuencias altas**: Para música o análisis acústico detallado (>8 kHz), usar 22.05 o 44.1 kHz.
- **Filtro high-pass puede afectar bajos**: Para música con contenido grave relevante (bajo, kick), ajustar corte a 40-50 Hz.

## Recomendaciones para Producción

### Pipeline Estándar

1. **Preprocesamiento**:

   ```python
   TARGET_SR = 16000
   TARGET_DURATION = 3.0
   TOP_DB = 30.0
   CUTOFF_HZ = 80.0
   ```

2. **Secuencia**:

   - Cargar audio (mono)
   - Recortar silencios (`top_db=30`)
   - Resamplear a 16 kHz
   - Ajustar duración (pad/crop)
   - Normalizar amplitud a 0.99
   - Aplicar high-pass (80 Hz)
   - Extraer MFCC (n=13)

3. **Features para ML**:
   - 26 features MFCC (13×mean + 13×std)
   - 2 features adicionales (rms_mean, zcr_mean)
   - **Total: 28 features** por clip

### Configuración por Escenario

**Voz/Speech:**

- Sample rate: 16 kHz
- MFCC: 13 coeficientes
- High-pass: 80-100 Hz
- Duración: 2-3s

**Música:**

- Sample rate: 22.05-44.1 kHz
- MFCC: 20-40 coeficientes
- High-pass: 40-50 Hz
- Duración: 10-30s

**Sonidos ambientales:**

- Sample rate: 16-22.05 kHz
- MFCC: 13-20 coeficientes
- High-pass: 60-80 Hz
- Duración: 3-5s

### Monitoring Continuo

**Checks automáticos por lote:**

- SNR estimado > 15 dB
- Duración ∈ [2.5, 3.5]s
- max(|amplitud|) ≤ 1.0
- Número de frames MFCC > 30
- RMS mean ∈ [0.05, 0.5]
- ZCR mean < 0.2

**Alertas de calidad:**

- Porcentaje de archivos rechazados por QA
- Distribución de métricas vs baseline
- Detección de drift en características

## Próximos Pasos

1. **Evaluar en dataset real**: Aplicar pipeline a UrbanSound8K completo (8,732 clips, 10 clases)
2. **Modelo de clasificación**: RandomForest/XGBoost sobre features MFCC
3. **Delta y Delta-Delta MFCC**: Capturar dinámica temporal con derivadas
4. **Deep Learning**: CNN sobre espectrogramas Mel en lugar de MFCC agregados
5. **Augmentación avanzada**: SpecAugment, mixup de audios, adición de ruidos reales
6. **Segmentación temporal**: Detectar eventos en audios largos (>10s)
7. **Transfer Learning**: Usar embeddings de modelos pre-entrenados (VGGish, YAMNet)

## Evidencias

- **Notebook completo**: Ver análisis interactivo completo abajo
- **Código fuente**: [Practico_14.ipynb](../Practicos/Practico_14.ipynb) (descargar)

---

## 📓 Análisis Completo Interactivo

A continuación puedes explorar el análisis completo con código, visualizaciones y resultados renderizados directamente desde el notebook Jupyter:

{% include "../Practicos/Practico_14.ipynb" %}
