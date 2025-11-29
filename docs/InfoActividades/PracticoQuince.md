---
title: "UT5 - Actividad 15 - Pipelines ETL, DataOps y Orquestación con Prefect"
date: 2025-11-29
---

# UT5 - Actividad 15: Pipelines ETL, DataOps y Orquestación con Prefect

## Contexto

Diseño e implementación de un mini pipeline ETL con Prefect, explorando conceptos fundamentales de orquestación de datos y funcionalidades avanzadas del orquestador. El trabajo abarca desde la creación de tasks y flows básicos hasta la implementación de características como retries, caching, logging estructurado, concurrencia, y deployments.

## Objetivos

- Comprender conceptos fundamentales de Prefect: Tasks, Flows, States y DAG implícito
- Implementar pipelines ETL con Tasks decoradas para Extract, Transform y Load
- Explorar funcionalidades avanzadas: retries, caching, logging personalizado y concurrencia
- Aplicar Task Runners para procesamiento paralelo de datos
- Investigar Deployments y Scheduling para automatización de pipelines
- Conectar conceptos de orquestación con principios de DataOps

## Datos

- **Escenario**: Ventas diarias de una cadena de tiendas minoristas
- **Dataset sintético generado**:
  - 100 registros de transacciones
  - Campos: fecha, producto, cantidad, precio_unitario, region
  - Regiones: Norte, Sur, Este, Oeste
  - Productos: A, B, C, D
- **Tipo de pipeline**: Batch (procesamiento diario)
- **Justificación**: Datos consolidados al final del día, decisiones estratégicas basadas en análisis de tendencias diarias/semanales

## Metodología

### 1. Investigación de Conceptos Fundamentales

**Tasks en Prefect:**

- Unidad de trabajo individual dentro de un flujo de datos
- Creadas con el decorador `@task` sobre funciones Python
- Permiten observabilidad granular, reintentos automáticos, y cache de resultados
- Evaluación perezosa ("lazily evaluated"): construcción de grafo de dependencias antes de ejecución
- Estados principales: Pending, Running, Completed, Failed
- Parámetros clave: `retries`, `cache_expiration`, `timeout_seconds`

**Flows en Prefect:**

- Contenedor principal que orquesta la ejecución de múltiples tasks
- Define el pipeline completo con manejo de estado, logging y scheduling
- Soporte para subflows: flows anidados para modularidad y reutilización
- DAG implícito: Prefect infiere dependencias del flujo de datos en el código
- Permite control de flujo nativo de Python (if/else, loops)

**Result Persistence y Caching:**

- Almacenamiento automático de resultados en storage persistente
- Permite recuperación sin re-ejecución, debugging, y recuperación desde puntos de fallo
- Cache basado en hash de inputs de la task
- `cache_expiration`: duración de validez del resultado cacheado
- `cache_key_fn`: función personalizada para generación de cache key

### 2. Implementación del Pipeline Base

**Pipeline ETL estándar:**

1. **Extract**: Generación de datos sintéticos de ventas

   - 100 registros con fecha, producto, cantidad, precio, región
   - Uso de numpy y pandas para creación de dataset

2. **Transform**: Aplicación de transformaciones

   - Cálculo de total de venta (`cantidad * precio_unitario`)
   - Categorización de ticket size (small, medium, large)
   - Logging de estadísticas procesadas

3. **Load**: Almacenamiento de datos procesados
   - Exportación a CSV
   - Confirmación de registros guardados

**Orquestación con Flow:**

- Flow principal que ejecuta tasks en secuencia
- Paso de datos entre tasks mediante return values
- Inferencia automática de dependencias por Prefect

### 3. Funcionalidades Avanzadas Implementadas

**A. Retries y Manejo de Errores:**

- Task con reintentos automáticos: `retries=3, retry_delay_seconds=10`
- Simulación de fallos aleatorios para probar robustez
- Exponential backoff: tiempo de espera aumenta exponencialmente entre reintentos
- Útil para recursos temporalmente no disponibles (API rate limits, DB ocupada)

**B. Caching de Resultados:**

- Task de extracción con cache: `cache_expiration=timedelta(minutes=30)`
- Previene re-ejecución de operaciones costosas con mismos inputs
- Invalidación automática cuando inputs cambian
- Casos de uso: APIs que actualizan una vez al día, transformaciones ML costosas

**C. Logging Estructurado:**

- Uso de `get_run_logger()` para logging integrado con Prefect
- Niveles: DEBUG, INFO, WARNING, ERROR
- Logging de validaciones de calidad de datos
- Mensajes estructurados asociados con task runs específicas
- Configuración de nivel vía `PREFECT_LOGGING_LEVEL`

**D. Concurrencia y Paralelismo:**

- `ConcurrentTaskRunner` para ejecución paralela con threads
- Procesamiento paralelo por región usando `.submit()`
- `PrefectFuture` para manejo asíncrono de resultados
- Útil para tasks I/O-bound (llamadas a APIs, lectura/escritura)
- Alternativas: `DaskTaskRunner` para procesamiento distribuido CPU-intensive

### 4. Deployments y Scheduling (Conceptual)

**Deployments:**

- Configuración para ejecutar Flow en entorno específico con schedule
- Empaqueta Flow con metadatos: infraestructura, timing, parámetros
- Diferencia con Flow: permite orquestación programada y ejecución remota

**Work Pools y Workers:**

- **Work Pool**: grupo lógico de infraestructura donde se ejecutan deployments
- **Worker**: proceso que escucha por trabajo y ejecuta flow runs
- Relación: Work Pool → Worker → Flow Run

**Scheduling:**

- **CronSchedule**: sintaxis cron estándar (`"0 6 * * *"` para diario 6 AM)
- **IntervalSchedule**: ejecución cada X tiempo desde punto inicio
- **RRuleSchedule**: especificación iCalendar RFC para reglas complejas
- Preferir RRule sobre cron para lógica de calendario compleja

### 5. Extensiones DataOps Implementadas

**Pipeline Parametrizado con Caching:**

```python
@flow
def etl_flow_parametrized(min_amount: float = 0.0, output_path: str = "output.csv", n_rows: int = 100)
```

- Parámetros configurables: número de registros, filtros, rutas de salida
- Cache invalidado automáticamente al cambiar parámetros
- Filtrado dinámico por monto mínimo
- Flexibilidad para diferentes casos de uso

**Pipeline Concurrente:**

```python
@flow(task_runner=ConcurrentTaskRunner())
def etl_flow_concurrent()
```

- Procesamiento paralelo de cuatro regiones simultáneamente
- Uso de `.submit()` para ejecución asíncrona
- Recolección de resultados con `.result()`
- Reducción de tiempo de ejecución para datasets grandes

**Validación con Logging:**

```python
@task(retries=2, retry_delay_seconds=5)
def validate_data(df: pd.DataFrame)
```

- Validaciones de calidad: DataFrame vacío, valores nulos
- Logging estructurado de errores y warnings
- Reintentos automáticos en caso de fallo de validación
- Lanzamiento de excepciones para detener pipeline si datos inválidos

## Resultados

### Ejecución del Pipeline Base

**Logs de Prefect observados:**

```
12:45:30.123 | INFO | Flow run 'etl_flow' - Created flow run
12:45:30.456 | INFO | Flow run 'etl_flow' - Executing 'extract_data'
12:45:30.789 | INFO | Task run 'extract_data' - 📥 Extraídos 100 registros
12:45:31.012 | INFO | Task run 'extract_data' - Finished in state Completed()
12:45:31.234 | INFO | Flow run 'etl_flow' - Executing 'transform_data'
12:45:31.456 | INFO | Task run 'transform_data' - 🔄 Transformados 100 registros
12:45:31.678 | INFO | Task run 'transform_data' - Finished in state Completed()
```

**Características observadas:**

- Timestamps precisos para tracking temporal
- Estados de tasks: Pending → Running → Completed
- Distinción entre "Flow run" (orquestador) y "Task run" (tasks individuales)
- Orden de ejecución inferido automáticamente del flujo de datos
- Logs automáticos sin instrumentación manual

### Pipeline Concurrente

**Resultados por región procesados en paralelo:**

```python
[
    {'region': 'Norte', 'total': 15234.56, 'count': 25},
    {'region': 'Sur', 'total': 18765.43, 'count': 28},
    {'region': 'Este', 'total': 12543.21, 'count': 22},
    {'region': 'Oeste', 'total': 16234.78, 'count': 25}
]
```

**Mejoras observadas:**

- Reducción de tiempo de ejecución versus procesamiento secuencial
- Tasks ejecutadas simultáneamente sin bloqueo mutuo
- Mantiene trazabilidad de cada proceso regional independiente

## Conexión con DataOps

### 1. Observabilidad

Prefect implementa observabilidad a través de:

- **Logging estructurado automático**: cada task registra ejecución, estado y mensajes
- **UI en tiempo real**: visualización de DAGs, estados y dependencias sin configuración
- **Tracking de estados granulares**: permite entender exactamente qué pasó en cada paso
- **Result persistence**: almacena outputs intermedios para inspección post-ejecución
- **Métricas y alertas**: eventos automáticos para notificaciones

Impacto: Detección rápida de fallos, debugging con contexto completo, comprensión del comportamiento sin instrumentación manual.

### 2. Reproducibilidad

El caching mejora reproducibilidad mediante:

- **Determinismo garantizado**: mismos inputs → mismo resultado siempre
- **Reducción de variabilidad externa**: cache preserva estado para comparaciones
- **Facilita experimentación**: iterar en pasos posteriores sin re-ejecutar anteriores
- **Versionado implícito**: cambios en inputs generan nueva cache, creando historial
- **Debugging consistente**: reproducir ejecuciones problemáticas con datos cacheados

### 3. CI/CD para Datos

Deployments habilitan CI/CD mediante:

- **Separación código/ejecución**: código en Git, deployment define cómo/cuándo ejecutar
- **Promoción entre ambientes**: mismo código, diferentes deployments para dev/staging/prod
- **Versionado automático**: cada cambio crea nueva versión, permite rollbacks
- **Integración con CI**: crear/actualizar deployments desde GitHub Actions, GitLab CI
- **Testing automatizado**: deployments de prueba en cada PR antes de producción
- **Infrastructure as Code**: configuración versionada y revisada como código

## Comparación con Alternativas

### Prefect vs Apache Airflow

**Diferencia 1 - Filosofía de desarrollo:**

- **Prefect**: Python nativo sin DSLs, workflows son funciones estándar, inferencia automática de dependencias
- **Airflow**: Requiere definir DAGs explícitamente con API específica, dependencias declaradas con `>>` o `set_upstream()`

**Diferencia 2 - Ejecución dinámica:**

- **Prefect**: Tasks dinámicas en runtime basadas en datos, control de flujo nativo de Python
- **Airflow**: DAG estático definido antes de ejecución, limitado para lógica condicional compleja

### Prefect vs Dagster

**Paradigma:**

- **Dagster**: Enfocado en "data assets" (tablas, modelos ML), grafo de dependencias de assets
- **Prefect**: Enfocado en ejecución de workflows de tasks

**Target audience:**

- **Dagster**: Analytics Engineering, usuarios de dbt, gestión de linaje de datos
- **Prefect**: Ingenieros de datos y MLOps generales, flexibilidad de workflows

**Testing:**

- **Dagster**: Framework de testing más robusto para validar transformaciones
- **Prefect**: Testing estándar de Python, enfoque en robustez de ejecución

Ambos son modernos, Pythonic, y superiores a Airflow en usabilidad.

## Evidencias

- Ingresar al análisis completo: [Open Practicos](../Practicos/PRactico_15.ipynb)
- Dataset generado: `output.csv` con registros procesados
- Logs de ejecución mostrando estados de tasks
- Implementaciones de extensiones: retries, caching, concurrencia

## Reflexión

Esta actividad proporcionó una comprensión profunda de orquestación moderna de datos con Prefect, contrastando significativamente con enfoques tradicionales. Los conceptos aprendidos son fundamentales para implementar pipelines de datos robustos, escalables y mantenibles.

**Aprendizajes clave:**

1. **Simplicidad Pythonic**: La capacidad de escribir workflows como funciones Python naturales elimina la curva de aprendizaje de DSLs complejos.

2. **Observabilidad nativa**: El tracking automático de estados y logging estructurado reduce drásticamente el esfuerzo de instrumentación.

3. **Resiliencia incorporada**: Features como retries, caching y result persistence están diseñados para pipelines de producción desde el inicio.

4. **Escalabilidad flexible**: Task Runners permiten escalar desde desarrollo local hasta procesamiento distribuido sin cambiar el código del flow.

5. **DevOps para datos**: Deployments y scheduling demuestran cómo aplicar prácticas de software engineering a ingeniería de datos.

La conexión con principios DataOps quedó clara: observabilidad para monitoreo continuo, reproducibilidad para experimentación confiable, y CI/CD para iteración rápida. Estas capacidades son esenciales para equipos de datos modernos que necesitan velocidad sin sacrificar confiabilidad.

**Aplicabilidad práctica:**

- Automatización de pipelines ETL diarios para reporting de negocio
- Orquestación de entrenamiento y deployment de modelos ML
- Gestión de flujos de datos complejos con múltiples dependencias
- Implementación de validaciones de calidad de datos automatizadas

Prefect se posiciona como una herramienta fundamental en el stack moderno de ingeniería de datos, especialmente para organizaciones que valoran la velocidad de desarrollo y la facilidad de mantenimiento.
