# Rendimiento medido — 4 de octubre de 2026

La última revisión del dashboard obtiene 96 puntos en escritorio y CLS 0,0056.
Consulta la [comparación posterior](#revisión-posterior-estabilidad-del-dashboard)
para sus muestras y validación; la primera comparación se conserva a continuación.

Comparación del commit `ef2d4a4` con los cambios de esta revisión. Cada cifra es
la mediana de tres ejecuciones consecutivas por página y perfil; se realizaron
18 auditorías antes y 18 después, sin ejecutar pruebas de navegador en paralelo.

## Condiciones

- Lighthouse 13.5.0, Node.js 24.21.0, Chromium 153.0.8010.12 y Linux.
- Servidor Python local sin compresión ni cabeceras de caché, igual en ambas rondas.
- Móvil: configuración predeterminada de Lighthouse; escritorio: `--preset=desktop`.
- Perfiles nuevos y caché limpiada por Lighthouse; sin cambiar las condiciones de red/CPU.
- En este entorno se usaron las opciones de Chromium `--headless --no-sandbox --disable-dev-shm-usage`.
  El script normalmente solo necesita `--headless`.

Son resultados de laboratorio de tres páginas representativas. No representan
tiempos medidos en un alojamiento público ni garantizan la puntuación de las 67 páginas.
Las muestras individuales, el navegador y la configuración están en
[performance-samples.json](performance-samples.json). Las instrucciones para
repetir la auditoría están en el [README](../README.md#medición-de-rendimiento).

## Resultados

Puntuación sobre 100; CLS mide el desplazamiento visual acumulado. Los bytes
incluyen los recursos transferidos durante la auditoría, sin compresión.

| Página / perfil | Puntuación antes → después | CLS antes → después | Transferencia KiB antes → después |
| --- | ---: | ---: | ---: |
| Dashboard / móvil | 52 → 72 | 0.342 → 0.001 | 1034.7 → 950.5 |
| Dashboard / escritorio | 94 → 91 | 0.029 → 0.122 | 1043.3 → 959.1 |
| Página vacía / móvil | 49 → 70 | 0.473 → 0.007 | 791.5 → 699.4 |
| Página vacía / escritorio | 78 → 96 | 0.416 → 0.085 | 783.5 → 699.2 |
| DataTables / móvil | 48 → 68 | 0.345 → 0.017 | 1978.4 → 1886.3 |
| DataTables / escritorio | 95 → 96 | 0.018 → 0.018 | 1970.4 → 1886.2 |


FCP es la primera aparición de contenido; LCP, la del elemento visible más
grande; TBT, el tiempo total durante el que las tareas largas bloquean el hilo principal.

| Página / perfil | FCP segundos antes → después | LCP segundos antes → después | TBT ms antes → después |
| --- | ---: | ---: | ---: |
| Dashboard / móvil | 4.05 → 4.35 | 6.01 → 4.80 | 25.5 → 40.0 |
| Dashboard / escritorio | 0.97 → 0.92 | 1.42 → 1.33 | 0.0 → 0.0 |
| Página vacía / móvil | 4.50 → 4.20 | 5.25 → 5.25 | 0.0 → 0.0 |
| Página vacía / escritorio | 0.89 → 0.84 | 1.08 → 1.04 | 0.0 → 0.0 |
| DataTables / móvil | 4.95 → 4.50 | 5.70 → 5.25 | 118.9 → 157.0 |
| DataTables / escritorio | 0.96 → 0.93 | 1.36 → 1.05 | 3.5 → 7.5 |


## Cambios aplicados

- El menú móvil ya está cerrado y su botón ocupa su espacio antes de inicializar JavaScript.
- Las alturas iniciales de `html`, `body` y `.wrapper` coinciden con las del layout nativo,
  evitando que la página vacía cambie la posición del pie al cargar los scripts.
- 62 páginas cargan la declaración de la fuente de iconos y sus alias, ahorrando
  86 593 bytes de CSS por página. El calendario y los cuatro catálogos conservan
  el inventario completo, necesario para los iconos creados dinámicamente.
- El actualizador genera la hoja ligera desde la fuente descargada, conserva
  el aviso de licencia y restaura la hoja completa cuando la página necesita `bi-*`.
- Las comprobaciones de páginas excluyen dependencias de herramientas y reportes generados.

## Límites y trabajo pendiente de la primera revisión

Cinco de los seis casos mejoran su puntuación mediana. El dashboard de escritorio
baja de 94 a 91: su CLS después varía entre 0,029 y 0,140 en las tres muestras.
La revisión posterior del dashboard, al final de este documento, corrige esa inestabilidad.
Las trazas siguen mostrando cambios al cargar fuentes e inicializar gráficos.
El FCP del dashboard móvil y el TBT de DataTables móvil también aumentan en esta
ronda; no todos los indicadores mejoraron. Conviene repetir las mediciones después
de reservar mejor el espacio inicial de los gráficos y revisar las métricas de fuentes.

Bootstrap y Chart.js siguen siendo los recursos principales de estas páginas.
No se purgaron sus estilos según una única carga: eso podría romper controles
abiertos después o ejemplos de otras páginas. Para un despliegue real, configurar
compresión y caché HTTP es otro paso, dependiente del alojamiento elegido.

## Validación

- 32 pruebas unitarias aprobadas, incluida la conservación de iconos dinámicos y
  la exclusión de páginas internas de `node_modules`.
- 67 páginas comprobadas en Chromium, con recursos, accesibilidad e interacciones.
- Navegación y pie de la página vacía comprobados con scripts bloqueados y después
  de inicializarlos en móvil y escritorio (tolerancia de 3 px).
- 40 capturas visuales aprobadas, con 0 % de píxeles cambiados y sin modificar referencias.
- Instalación reproducible de las herramientas con `npm ci` verificada.

## Revisión posterior: estabilidad del dashboard

Se comparó una copia obtenida con `git archive 874c5a3` con el dashboard corregido.
Se repitieron tres auditorías móviles y tres de escritorio por versión, con el mismo
Lighthouse, Chromium, servidor y configuración descritos arriba. Las muestras están en
[dashboard-performance-samples.json](dashboard-performance-samples.json).

| Perfil | Puntuación antes → después | CLS antes → después | FCP segundos antes → después | LCP segundos antes → después | TBT ms antes → después |
| --- | ---: | ---: | ---: | ---: | ---: |
| Móvil | 70 → 70 | 0.0019 → 0.0003 | 4.50 → 4.35 | 4.96 → 5.25 | 44.0 → 55.5 |
| Escritorio | 95 → 96 | 0.0288 → 0.0056 | 0.93 → 0.89 | 1.33 → 1.31 | 0.0 → 0.0 |

El código anterior, que había obtenido 91 en escritorio, dio 95 al repetirlo; esto
ilustra la variación entre rondas. La revisión llega a 96 y reduce el CLS: las tres
muestras finales coinciden en 0,0056 en escritorio y 0,0003 en móvil. En móvil el
LCP y TBT aumentaron en esta ronda y la puntuación se mantuvo; el cambio resuelve
la estabilidad inicial, sin mejorar todos los tiempos de carga.

La causa comprobada fue la inserción de descripciones y tablas accesibles después
de crear los gráficos. Esos paneles ahora están presentes desde el HTML inicial y
el plugin los reutiliza, conserva el foco y rellena sus tablas desde los datos reales.
Las fuentes locales de Poppins 300 y 400 se precargan para adelantar su descarga.
Se aplican las recomendaciones de Google para [contenido insertado y CLS](https://web.dev/articles/optimize-cls)
y [carga de fuentes](https://web.dev/learn/performance/optimize-web-fonts).

El HTML inicial añade 2 881 bytes transferidos por carga. No se añaden bibliotecas,
y las dos fuentes precargadas son las mismas que ya utilizaba el dashboard.

Validación de esta revisión:

- 32 pruebas unitarias y comprobación de recursos de las 67 páginas aprobadas.
- Pruebas completas de navegador, gráficos, tablas accesibles y actualizaciones aprobadas.
- Nueva prueba con fuentes retrasadas 600 ms e inicialización de gráficos bloqueada:
  los paneles mantienen su posición relativa, se reutilizan y conservan el foco del teclado.
- El CLS de esa prueba queda por debajo de 0,05 en escritorio y móvil.
- Las 40 capturas visuales coinciden con las referencias: 0 % de píxeles cambiados.
