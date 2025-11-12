# Portfolio Template

Este repositorio es un **template** para documentar el **portafolio** del curso usando **MkDocs + Material** con despliegue automático a GitHub Pages.

## Cómo usar

1. Escribe únicamente en `docs/`.
2. Crea entradas en `docs/portfolio/` siguiendo `plantilla.md`.
3. Mantén el **frontmatter** en cada `.md`:
   ```yaml
   ---
   title: "Título de la página"
   date: YYYY-MM-DD
   ---
   ```
4. Usa nombres de archivo con orden: `01-titulo.md`, `02-otro.md`.
5. Enlaza recursos con rutas relativas.

## Ejecutar localmente

```bash
pip install -r requirements.txt
mkdocs serve
```

## Notebooks con contenido interactivo

Los notebooks con mapas interactivos (Folium), widgets o visualizaciones JavaScript requieren ser "trusteados" para renderizar correctamente:

### Opción 1: Trust individual (en VS Code)

1. Abre el notebook
2. Clic en "File → Trust Notebook" o el mensaje que aparece arriba
3. Ejecuta todas las celdas (Ctrl+Shift+P → "Execute All Cells")
4. Guarda el archivo (Ctrl+S)

### Opción 2: Trust todos los notebooks (terminal)

```bash
python trust_notebooks.py
```

Luego ejecuta cada notebook manualmente para generar los outputs.

## Despliegue

Cada `push` a `main` ejecuta el build con `--strict` y publica en GitHub Pages.
