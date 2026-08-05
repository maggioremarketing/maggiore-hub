# Herramientas IEP V2

- `iepv2-data/` — datos fuente de los experimentos (JSON). `data-jfm1.json` usa el esquema v1 (tablas planas, se transforma al vuelo); `data2-*.json` usan el esquema narrativo v2 (headline, charts con insight, learnings, recommendations).
- `iepv2-block2.html` — plantilla del bloque IEP V2 (CSS + JS) con el marcador `/*__IEPV2_DATA__*/[]`.
- `build-iepv2.py` — ensambla los datos, transforma v1→v2 e inyecta el bloque en `combe/index.html`. Ajustar las rutas del scratchpad a este directorio si se corre desde el repo.

Flujo para actualizar resultados: editar/añadir JSON en `iepv2-data/` → correr el build → commit + push (deploy automático).
Futuro: los JSON v2 se generarán desde la API de Meta (vía Windsor.ai) en lugar de extraerse de decks.
