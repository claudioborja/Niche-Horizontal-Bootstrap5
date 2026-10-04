# Horizonte Admin

[![Pruebas de la plantilla](https://github.com/claudioborja/horizonte-admin/actions/workflows/tests.yml/badge.svg)](https://github.com/claudioborja/horizonte-admin/actions/workflows/tests.yml)

Plantilla de administración con navegación horizontal, construida con HTML, CSS
y JavaScript. Incluye **67 páginas de ejemplo**, cuatro dashboards y componentes
para tablas, gráficos, calendarios, formularios y editores de texto.

Este repositorio mantiene y moderniza una plantilla original de terceros. Las
pantallas utilizan datos de demostración: para gestionar usuarios, enviar correo,
guardar archivos o persistir eventos, debes conectarlas a tu propia aplicación.

## Inicio rápido

Necesitas un navegador moderno y Python 3 para servir los archivos localmente.
No hay un paso de compilación ni dependencias que instalar con npm.

Si todavía no tienes el repositorio:

```bash
git clone https://github.com/claudioborja/horizonte-admin.git
cd horizonte-admin
```

Desde la raíz del proyecto:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Abre [http://localhost:8000](http://localhost:8000) y navega por el menú.
Para detener el servidor, pulsa `Ctrl+C` en la terminal.

El servidor de Python permite explorar la plantilla. Los formularios de
login y registro envían un `POST` a `index.html`; este servidor no procesa esos
envíos. Conecta los formularios a un backend para implementar la autenticación.

## Páginas incluidas

| Sección | Páginas | Ejemplo |
| --- | ---: | --- |
| Dashboards | 4 | [Dashboard principal](index.html) |
| Aplicaciones | 8 | [Calendario](apps/apps-calendar.html) |
| Gráficos | 5 | [Chart.js](charts/chart-chart-js.html) |
| Formularios | 6 | [Editor de texto](forms/form-summernote.html) |
| Iconos | 6 | [Bootstrap Icons](icons/icon-fontawesome.html) |
| Mapas | 2 | [Mapa vectorial](maps/map-vector.html) |
| Páginas generales y autenticación | 14 | [Login](pages/pages-login.html) |
| Tablas | 4 | [DataTables y exportación](tables/table-data-table.html) |
| Componentes de interfaz | 16 | [Botones](ui/ui-buttons.html) |
| Widgets | 2 | [Widgets de datos](widgets/widget-data.html) |
| **Total** | **67** | |

Los dashboards alternativos están en [index2.html](index2.html),
[index3.html](index3.html) e [index4.html](index4.html).

## Dependencias principales

Versiones incluidas y referenciadas por las páginas después de la actualización:

| Dependencia | Versión | Uso |
| --- | --- | --- |
| Bootstrap | 5.3.8 | Layout, estilos y componentes de interfaz |
| Popper | 2.11.8 | Posicionamiento de dropdowns, tooltips y popovers |
| jQuery | 4.0.0 | Plugins e inicializadores pendientes de migración |
| Chart.js | 4.5.1 | Gráficos en dashboards y página de demostración |
| DataTables | 3.1.3 | Tablas con integración Bootstrap 5 |
| FullCalendar | 7.1.0 | Calendarios y arrastre de eventos |
| Jodit | 4.17.1 | Editor de texto independiente de jQuery, con tablas, imágenes y HTML |
| jQuery Validation | 1.22.1 | Validación del formulario por pasos |
| SheetJS | 0.20.3 | Exportación de tablas a XLSX, XLS, CSV y TXT |
| FilePond | 4.32.12 | Selección de archivos y adjuntos con vistas previas |
| Tabulator | 6.6.1 | Tablas editables, filtros y paginación local |
| Bootstrap Icons | 1.13.1 | Iconos generales y catálogos con búsqueda |
| Ion.RangeSlider | 2.5.0 | Siete ejemplos de selección de rangos |
| Poppins (Fontsource) | 5.3.0 | Tipografía local en WOFF2, pesos 300–700 |

Los ejemplos que utilizaban Morris.js, Raphaël y Chartist ahora usan Chart.js.
Los interruptores, checkboxes y radios utilizan controles nativos con estilos de
Bootstrap 5. El calendario utiliza `Date` y ya no carga Moment.

FilePond 4.32.12 sustituye Dropify y Dropzone; Tabulator 6.6.1 sustituye jsGrid;
Bootstrap Icons 1.13.1 unifica los iconos generales.

FilePond incluye Image Preview 4.6.12 y File Validate Size 2.2.8. Las cargas son
locales: conectar `server` a una API permite guardar los archivos. Las tablas
conservan sus datos originales, filtros, edición, borrado y paginación; los
cambios se pierden al recargar. Los catálogos de iconos mantienen sus rutas y
pasan a mostrar Bootstrap Icons con búsqueda. Los logotipos que no incluye la
nueva fuente se conservan como SVG de Font Awesome (SIL OFL 1.1). Las banderas
y los iconos meteorológicos conservan sus bibliotecas especializadas.

jQuery 4.0.0 funciona sin jQuery Migrate. Jodit 4.17.1 sustituye Summernote;
Chart.js sustituye Peity en los minigráficos; una galería con CSS Grid y un
`<dialog>` nativo sustituye CubePortfolio. Se retiraron los cuatro plugins
antiguos y sus inicializadores. Las rutas `form-summernote.html` y
`chart-peity.html` se conservan para mantener los enlaces existentes.

Jodit permite formato de texto, listas, enlaces, tablas, imágenes, vídeo,
vista HTML, deshacer/rehacer y pantalla completa. Su editor de código usa un
textarea local, sin descargar herramientas adicionales. Las imágenes se insertan
como datos Base64; para guardar documentos o enviar correo necesitas tu backend.
Edit/Save conserva el contenido de demostración hasta recargar la página.

La galería conserva sus 12 imágenes, categorías y contadores. La vista ampliada
recorre las imágenes del filtro seleccionado, con botones Previous/Next y flechas
del teclado; se cierra con Close, Escape o pulsando fuera del diálogo.
Los 18 minigráficos y los tres del tercer dashboard conservan sus valores, colores
y proporciones; Chart.js los redimensiona al cambiar el tamaño disponible.

FullCalendar 7.1.0 carga el bundle global, el plugin de Bootstrap 5 y sus dos
hojas de estilo locales. El inicializador utiliza `FullCalendar.Interaction.Draggable`
y los campos de evento `color` y `allDay`. Los sliders utilizan inputs
etiquetados y el tema integrado `modern` de Ion.RangeSlider 2.5.0.

Se retiraron Dropify, Dropzone, jsGrid y las cinco fuentes generales anteriores,
así como las copias sustituidas de jQuery, FullCalendar e Ion.RangeSlider.
Los SVG de marcas conservan su atribución y licencia en
[assets/img/brands/LICENSE.txt](assets/img/brands/LICENSE.txt). El historial de
Git permite recuperar los archivos retirados.

Las dependencias principales y Poppins se sirven desde `assets/plugins/`.
La tipografía no necesita conexión con Google Fonts. Google Maps utiliza un
servicio externo que requiere conexión.
Para usar Google Maps en tu aplicación, configura tu propia clave en
[maps/map-google.html](maps/map-google.html).

## Estructura del proyecto

```text
horizonte-admin/
├── index.html                   # Dashboard principal
├── index2.html                  # Dashboards alternativos
├── index3.html
├── index4.html
├── apps/                        # Calendario, contactos y pantallas de correo
├── charts/                      # Ejemplos de gráficos
├── forms/                       # Formularios, validación y editor
├── icons/                       # Catálogos de iconos
├── maps/                        # Google Maps y mapas vectoriales
├── pages/                       # Autenticación, perfil, factura y otras páginas
├── tables/                      # Tablas y exportación
├── ui/                          # Componentes de interfaz
├── widgets/                     # Widgets de ejemplo
├── assets/
│   ├── css/                     # Estilos de la plantilla y fuentes
│   ├── img/                     # Imágenes
│   ├── js/
│   │   ├── niche.js             # Comportamiento general
│   │   ├── chart-examples.js    # Galerías y dashboards con Chart.js
│   │   ├── mailbox.js           # Selección de mensajes y estrellas
│   │   ├── switches.js          # Estados de los controles nativos
│   │   └── table-export.js      # Exportación con SheetJS
│   └── plugins/                 # Bibliotecas y sus inicializadores
├── tools/
│   └── update_dependencies.py   # Instalación de versiones fijadas
└── README.md
```

## Actualizar las dependencias

Desde la raíz del repositorio, con Python 3 y acceso a Internet:

```bash
python3 tools/update_dependencies.py
```

El script instala las versiones fijadas en `UPDATES`; no busca automáticamente
la última versión de cada biblioteca. Reutiliza archivos que cumplen sus
comprobaciones de contenido y descarga los pendientes.

Antes de modificar el proyecto, prepara todas las descargas, adapta las rutas e
inicializaciones y comprueba las referencias locales de JavaScript y CSS de las
67 páginas. Si una descarga o validación falla, no aplica la migración. Si falla
una escritura, intenta restaurar los archivos que ya había modificado.

Para los paquetes npm utiliza jsDelivr, con UNPKG como alternativa. SheetJS se
descarga desde su CDN. Bootstrap Icons incluye las fuentes necesarias para sus iconos; Jodit utiliza iconos SVG integrados.
El actualizador no elimina carpetas automáticamente; jQuery UI se actualiza
en su ubicación existente. Después de nuevas migraciones, comprueba las
referencias antes de retirar recursos adicionales.

Las comprobaciones de contenido detectan respuestas inesperadas; no sustituyen
las pruebas de funcionamiento en el navegador.

Para comprobar las migraciones sin descargar bibliotecas ni modificar los
recursos instalados:

```bash
python3 tools/test_component_migrations.py
```

Para revisar las referencias locales de scripts, estilos, imágenes, favicon
y recursos de CSS, sin acceso a Internet:

```bash
python3 tools/check_assets.py
```

Estas pruebas verifican rutas, opciones conservadas, catálogos de iconos y que
un fallo de descarga no modifique las páginas. La instalación completa se
simula en una carpeta temporal.

Si falla la ejecución:

- **Error de DNS:** comprueba la conexión de la terminal y vuelve a ejecutar.
- **HTTP 403:** el script intenta UNPKG para los paquetes npm disponibles desde jsDelivr.
- **Contenido inesperado:** revisa la URL, el tamaño y el marcador indicados en el error.
- **Ruta local inexistente:** corrige el archivo o su referencia antes de repetir la migración.

## Comprobar los componentes

La prueba automatizada abre las 67 páginas en Chromium, comprueba errores de
JavaScript y recursos locales, y prueba los calendarios, sliders, archivos,
tablas, editor, galería, minigráficos e iconos. Incluye vistas móviles de los componentes actualizados y nueve reglas de
accesibilidad con axe-core 4.13.0 (herramienta de pruebas local, licencia MPL-2.0), incluido contraste de texto.
Playwright es una herramienta opcional de pruebas; la plantilla continúa
funcionando sin Node.js ni un proceso de compilación.

```bash
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements-test.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tools/check_browser.py
```

El comprobador inicia y cierra su propio servidor local. Bloquea los servicios
externos para no depender de una clave de Google Maps y comprueba que Poppins
carga desde el repositorio. La conexión real con Google Maps se debe comprobar
con una clave válida.

### Comparación visual

`tools/check_visual.py` compara 40 capturas de escritorio (1440 px) y móvil
(390 px). Incluye dashboards, tabla accesible de gráficos, calendario,
validación, wizard con errores, DataTables, galería, acceso y aviso de demo.
También cubre navegación y cuenta abiertas, galería filtrada y su diálogo,
pestañas horizontales y verticales activas, tablas filtradas y sin resultados,
panel de correo colapsado, popover abierto y FAQ expandida.

Cada estado se activa con los controles reales y se verifica antes de capturar.
Los diálogos y menús superpuestos se capturan dentro de la ventana, para revisar
su posición; los demás casos guardan la página completa.

```bash
.venv/bin/python -m unittest discover -s tools -p 'test_*.py'
.venv/bin/python tools/check_visual.py
```

Las referencias están en `tools/visual-baselines`. La prueba usa Chromium y
Playwright fijados, Linux, fuentes locales, fecha fija, zona UTC y movimiento
reducido. Espera a las fuentes e imágenes antes de capturar. Si cambian las
dimensiones o más del 0,1 % de los píxeles (diferencia de canal mayor de 12),
falla y deja la captura actual, la referencia, las diferencias resaltadas y
`report.json` en `tools/visual-results`.

Después de un cambio visual intencional, revisa las imágenes y actualiza las
referencias explícitamente; la ejecución normal y CI nunca las reemplazan:

```bash
.venv/bin/python tools/check_visual.py --update
.venv/bin/python tools/check_visual.py
```

Revisa y versiona las imágenes actualizadas junto con el cambio que las explica.
Si actualizas Playwright/Chromium, también revisa las referencias en el nuevo
entorno. Pillow es solo una dependencia de pruebas, no de la plantilla.

### Medición de rendimiento

La auditoría opcional usa [Lighthouse](https://github.com/GoogleChrome/lighthouse)
13.5.0. Requiere Node.js 22.19 o posterior y Chrome/Chromium; estas herramientas
no son necesarias para usar la plantilla. Instala las versiones fijadas y ejecuta:

```bash
npm ci --prefix tools/lighthouse
python3 tools/check_performance.py
```

Si Chrome no está en una ubicación habitual, define `CHROME_PATH` con la ruta
de su ejecutable. El script inicia y cierra un servidor local, mide dashboard,
página vacía y DataTables en móvil y escritorio, y realiza tres ejecuciones
consecutivas por caso. Guarda los informes JSON completos y `summary.json` con
las medianas de puntuación, FCP, LCP, TBT, CLS y bytes transferidos en
`tools/performance-results` (excluido de Git). Se pueden elegir otras páginas:

```bash
python3 tools/check_performance.py --pages index.html apps/apps-calendar.html --runs 3
```

La configuración móvil utiliza la simulación predeterminada de Lighthouse;
escritorio utiliza `--preset=desktop`. Las mediciones locales sirven para comparar
cambios con el mismo equipo, navegador y configuración. El servidor Python no
aplica compresión ni caché HTTP; los tiempos de un alojamiento real pueden variar.
No se eliminan estilos de Bootstrap solo porque una página no los use: también
deben funcionar las otras páginas y los controles que se abren al interactuar.

Consulta los resultados y condiciones de la comparación en
[docs/performance.md](docs/performance.md).

Las páginas con iconos heredados cargan `bootstrap-icons-font.css` y
`icon-compat.css`; el calendario y los cuatro catálogos conservan `bootstrap-icons.min.css`.
Si añades iconos con clases `bi bi-*`, utiliza la hoja completa en esa página,
también cuando los crees desde JavaScript. Ambas hojas usan la misma fuente local.

### Pruebas automáticas en GitHub

[GitHub Actions](https://github.com/claudioborja/horizonte-admin/actions/workflows/tests.yml)
ejecuta las comprobaciones en cada push y pull request. También permite iniciarlas
desde el botón **Run workflow** de la pestaña Actions.

El workflow de [.github/workflows/tests.yml](.github/workflows/tests.yml) utiliza
Ubuntu 24.04 y Python 3.14 para comprobar los recursos locales, las migraciones,
la estructura del JavaScript y las 67 páginas en Chromium. Instala el navegador
y sus dependencias automáticamente, y prueba las interacciones en escritorio y
móvil, y compara las 40 capturas de referencia. Si falla, guarda las capturas
y diferencias como artefacto durante siete días. No necesita claves de Google
Maps ni un backend.

Las versiones de las herramientas están fijadas en
[tools/requirements-test.txt](tools/requirements-test.txt). Las acciones se fijan
por commit; las ejecuciones usan permisos de lectura y tienen un límite de
15 minutos. Un nuevo cambio en la misma rama cancela la ejecución anterior.

Los ejemplos de validación muestran mensajes visibles asociados al campo con
`aria-describedby`. El wizard valida cada paso, marca los campos inválidos y
lleva el foco al primer error al intentar avanzar. Sus datos son de demostración:
no se envían ni se guardan. La tabla exporta las filas filtradas en XLSX, XLS,
CSV y TXT.

Después de actualizar o personalizar la plantilla, inicia el servidor local y
revisa la consola y la pestaña de red del navegador.

| Componente | Comprobación |
| --- | --- |
| Dashboards | Navegación, dropdowns y distribución en escritorio y móvil |
| Chart.js | Los seis tipos de gráfico aparecen y se adaptan al tamaño de la ventana |
| DataTables | Búsqueda, ordenación, paginación y selección del tamaño de página donde estén habilitadas |
| Exportación | Descarga y apertura de XLSX, XLS, CSV y TXT; incluye filas filtradas de otras páginas |
| Calendario | Crear eventos externos, arrastrarlos al calendario y usar «remove after drop» |
| Jodit | Escribir, dar formato, insertar imágenes y tablas, cambiar a vista HTML y usar Edit/Save |
| Galería | Filtrar categorías, abrir imágenes, navegar con botones/flechas y cerrar con Escape |
| Minigráficos | Dibujar pies, anillos, barras y líneas, incluidas series negativas |
| Formulario por pasos | Campos obligatorios, correo válido, mensajes asociados al campo, foco en el primer error y avance entre pasos |
| Bootstrap 5 | Cerrar alertas; cambiar pestañas; abrir dropdowns y el acordeón del FAQ; usar indicadores de carrusel y tooltips/popovers |
| Controles nativos | Cambiar interruptores; comprobar los estados deshabilitados, de solo lectura y la limpieza del grupo de radios |
| FilePond | Arrastrar archivos, previsualizar imágenes, comprobar el límite de 2 MB, los inputs deshabilitados y los adjuntos múltiples |
| Tabulator | Editar celdas, filtrar, paginar, confirmar el borrado y ordenar desde el selector externo |
| Iconos | Iconos del menú, estados dinámicos del correo, logotipos y búsqueda en los catálogos |
| Correo | Seleccionar y deseleccionar mensajes, también en otras páginas de la tabla, y cambiar sus estrellas |

La exportación utiliza el texto de las celdas y conserva el orden y el filtro
aplicados en DataTables. No reproduce imágenes ni estilos visuales de la tabla.
Los cambios en calendarios y formularios necesitan un backend para persistirse.

## Accesibilidad, imágenes y tipografía

Las 67 páginas permiten ampliar la vista y ofrecen un enlace **Skip to content**.
El menú admite Tab, Enter/Space, ArrowDown y Escape; sus botones anuncian el estado
abierto/cerrado. Los botones con iconos tienen nombres accesibles, los formularios
asocian etiquetas y controles, y los IDs de formularios y pestañas son únicos.
Las imágenes decorativas usan `alt=""`; los iconos decorativos se ocultan al lector.
El foco del teclado tiene un indicador visible.

Las imágenes locales incluyen dimensiones para reservar espacio antes de cargar.
Los logos y las primeras imágenes de contenido cargan inmediatamente; 222 imágenes
posteriores usan `loading="lazy"`. Las 36 copias WebP conservan exactamente los
píxeles originales y reducen el total de esos archivos de 162.187 a 43.956 bytes
(**72,9 %**). Los archivos originales siguen disponibles para enlaces existentes y
componentes que todavía los utilizan. La galería abre las imágenes disponibles;
el comprobador de recursos también valida sus enlaces.

Para regenerar las copias sin pérdida (herramienta opcional):

```bash
.venv/bin/pip install -r tools/requirements-images.txt
.venv/bin/python tools/optimize_images.py
```

El script comprueba que los píxeles no cambien y solo genera WebP si ahorra al menos
un 10 %. Guarda tamaños y dimensiones en [tools/image_optimization.json](tools/image_optimization.json).
Al añadir imágenes nuevas, referencia la copia generada en el HTML y especifica
su texto alternativo, dimensiones y política de carga según su posición.

Poppins incluye cinco pesos (300, 400, 500, 600 y 700) y los subconjuntos Latin,
Latin Extended y Devanagari. El navegador descarga los que necesita, con
`font-display: swap`. Su licencia SIL OFL 1.1 está en
[assets/plugins/poppins-5.3.0/LICENSE](assets/plugins/poppins-5.3.0/LICENSE).
El actualizador instala los archivos WOFF2 y genera la hoja local `poppins.css`.

Las pruebas verifican contraste de texto, alternativas de imágenes, nombres de botones y enlaces,
etiquetas de campos, zoom y atributos ARIA, además del menú con teclado y las vistas
móviles. Estas comprobaciones cubren esos aspectos concretos; no constituyen una
auditoría completa de conformidad WCAG.

### Lectura y controles en móvil

`assets/css/accessibility.css` define tonos legibles para navegación, tarjetas,
alertas y componentes de ejemplo. Conserva Poppins y la familia de colores de la
plantilla. Las estrellas y etiquetas de selección del correo, los controles de
paneles y los selectores de color tienen áreas pulsables de al menos 44 × 44 px.

El buscador y el menú de cuenta comparten la cabecera móvil sin desbordarse.
La línea de tiempo se adapta al contenedor hasta un máximo de 800 px.
Los dos calendarios abren la vista diaria por debajo de 768 px; permiten cambiar
de vista manualmente y recuerdan la vista de escritorio al cruzar ese umbral.

Las pruebas de navegador comprueban contraste de texto en las 67 páginas,
la cabecera y la línea de tiempo a 320, 390, 768 y 1440 px, la selección desde
el borde de las etiquetas del correo y los cambios de vista de los calendarios.

## Personalización

- Edita [assets/css/theme.css](assets/css/theme.css) para los colores, tipografía,
  espaciados, bordes redondeados y sombras compartidos. Las 67 páginas lo cargan
  antes de las hojas de componentes; no requiere compilación.

Las variables conservan el aspecto por defecto y distinguen el color de marca
de los tonos utilizados para texto legible. Estos son los ajustes principales:

| Variable | Elementos que controla |
| --- | --- |
| `--niche-color-primary` | Cabecera, botones principales y pestañas de la plantilla |
| `--niche-color-primary-border` | Borde de los botones principales |
| `--niche-color-link`, `--niche-color-link-hover` | Enlaces y sus estados |
| `--niche-color-text`, `--niche-color-muted` | Texto general y secundario |
| `--niche-color-surface`, `--niche-color-page` | Superficies de componentes y fondo del contenido |
| `--niche-color-info`, `--niche-color-success`, `--niche-color-warning`, `--niche-color-danger` | Estados legibles en los componentes de la plantilla |
| `--niche-font-family`, `--niche-font-size-base` | Fuente compartida y tamaño base |
| `--niche-content-padding`, `--niche-card-padding` | Espacio interior del contenido y de las tarjetas estándar |
| `--niche-dashboard-card-padding` | Espacio interior de las tarjetas del primer dashboard |
| `--niche-button-padding-x`, `--niche-button-padding-y` | Espacio interior de los botones estándar |
| `--niche-radius-card`, `--niche-radius-dashboard-card`, `--niche-radius-button` | Forma de tarjetas y botones |
| `--niche-shadow-card`, `--niche-shadow-dashboard` | Sombras de las dos variantes de tarjetas |
| `--niche-space-1` a `--niche-space-8` | Escala compartida de espaciado, incluidos los huecos de la galería |
| `--niche-control-hit-size` | Área pulsable de los controles pequeños; valor por defecto: 44 px |

Puedes editar los valores en `theme.css` o cargar tu propia hoja **después de
`accessibility.css`**, con ajustes globales en `:root`. Por ejemplo:

```css
:root {
  --niche-color-primary: #233b6e;
  --niche-color-primary-border: var(--niche-color-primary);
  --niche-color-link: var(--niche-color-primary);
  --niche-card-padding: 24px;
  --niche-dashboard-card-padding: 24px;
  --niche-radius-card: 8px;
  --niche-radius-button: 8px;
}
```

Los estilos específicos y las variantes de demostración de los plugins mantienen
sus propias opciones. Los gráficos conservan las paletas de sus inicializadores.
Tras cambiar colores o tamaños, ejecuta las pruebas para revisar contraste y
adaptación móvil. `check_design_quality.py` comprueba que las variables modifican
los componentes reales en el navegador.

Los gráficos comparten la tipografía y el color de texto del tema mediante
`assets/js/chart-theme.js`. Cárgalo después de Chart.js y antes del inicializador
de la página. Las leyendas se generan desde los datos del gráfico.

`assets/js/chart-accessibility.js` se carga después de `chart-theme.js` y antes
de los inicializadores. Añade nombres y resúmenes asociados al canvas, y tablas
con encabezados de fila y columna bajo «View chart data». Se abren con Enter o
Espacio y permiten desplazamiento horizontal con teclado en móvil. Las tablas
usan los mismos datos del gráfico y se actualizan con `chart.update()`, incluida
la indicación de series ocultas; siguen mostrando todos los valores.

El dashboard principal incluye los tres paneles `.chart-data` en el HTML inicial,
con `data-chart-for` igual al ID del canvas. El plugin reutiliza sus descripciones,
controles y regiones de tabla para reservar el espacio antes de cargar los gráficos,
conservar el foco y sustituir «Loading chart data…» por los valores actuales.
Si cambias las series del dashboard, ajusta también su resumen inicial en el HTML;
el plugin lo actualiza desde los datos al inicializarse. Las páginas sin paneles
iniciales siguen usando la generación automática.
El dashboard precarga las variantes latinas de Poppins 300 y 400. Si sustituyes
la tipografía del tema, ajusta o retira esas dos precargas en su `<head>`.

Los minigráficos incluyen sus valores y proporciones en el nombre accesible.
Los indicadores Knob muestran el valor y su rango como texto actualizado al
cambiar el control. Sigue las recomendaciones de
[accesibilidad de Chart.js](https://www.chartjs.org/docs/latest/general/accessibility.html).

- Edita [assets/css/style.css](assets/css/style.css) para ajustar los estilos de la plantilla.
- Usa [assets/js/niche.js](assets/js/niche.js) para el comportamiento general.
- Ajusta [assets/js/bootstrap-components.js](assets/js/bootstrap-components.js) para inicializar tooltips y popovers nativos.
- Modifica [assets/plugins/functions/calendar-init.js](assets/plugins/functions/calendar-init.js) para los eventos de demostración.
- Ajusta [assets/plugins/chartjs/chart-int.js](assets/plugins/chartjs/chart-int.js) para los seis gráficos de Chart.js.
- Modifica [assets/js/chart-examples.js](assets/js/chart-examples.js) para las galerías de líneas, áreas y gráficos animados, y los dashboards alternativos.
- Usa [assets/js/mailbox.js](assets/js/mailbox.js) para la selección de mensajes y estrellas.
- Ajusta [assets/css/switches.css](assets/css/switches.css) y [assets/js/switches.js](assets/js/switches.js) para los controles nativos.
- Ajusta [assets/js/file-uploads.js](assets/js/file-uploads.js) para FilePond y [assets/js/editable-tables.js](assets/js/editable-tables.js) para Tabulator.
- Ajusta [assets/js/gallery.js](assets/js/gallery.js) y [assets/css/gallery.css](assets/css/gallery.css) para la galería.
- Ajusta [assets/js/mini-charts.js](assets/js/mini-charts.js) para los gráficos compactos.
- Modifica [tools/legacy_widget_migrations.py](tools/legacy_widget_migrations.py) para la migración del editor, los minigráficos y la galería.
- Modifica [tools/component_migrations.py](tools/component_migrations.py) para las migraciones de páginas y la compatibilidad de iconos.
- Edita [assets/js/table-export.js](assets/js/table-export.js) para cambiar los botones y formatos de exportación.

Conserva las rutas relativas al mover páginas entre carpetas. Los datos de ejemplo
pueden sustituirse por respuestas de tu API en los inicializadores correspondientes.

## Acciones de demostración

`assets/js/demo-actions.js` se carga al final de las 67 páginas. Los enlaces
«Home» apuntan al dashboard. Los enlaces sin destino y los botones de muestra
se identifican como demo y muestran un aviso accesible sin saltar al comienzo
de la página. Los controles reales de menús, pestañas, galerías, calendarios,
editores, tablas y exportación mantienen sus acciones.

Los formularios de acceso, registro y recuperación muestran una aclaración
visible y no envían datos ni crean cuentas. La búsqueda de cabecera tampoco
consulta un servicio. «Send» y «Draft» en el correo indican que no se envía ni
se guarda el mensaje. Son ejemplos para integrar después con tu aplicación.

Al implementar una función real, sustituye su enlace o manejador y evita marcar
el control con `data-demo-action`. Elimina `demo-actions.js` en tu aplicación,
o adapta su manejador global de formularios para que permita tus envíos reales.
El actualizador conserva estas aclaraciones mediante `tools/demo_migrations.py`.

## Carga de recursos por página

54 de las 67 páginas funcionan sin cargar jQuery ni su adaptador. Las otras
13 mantienen jQuery por sus plugins o inicializadores. jQuery UI permanece
almacenado para compatibilidad, pero ninguna página lo carga: no hay controles
que lo utilicen. Los estilos de DataTables, pestañas y wizard se cargan solo
cuando la página contiene el componente correspondiente.

`tools/page_dependencies.py` mantiene esta selección al ejecutar el actualizador.
Conserva jQuery ante scripts desconocidos para no romper nuevas integraciones.
Si agregas un plugin, declara sus dependencias en el HTML y comprueba su página.
El núcleo, Bootstrap, iconos y fuentes siguen compartidos; los archivos de
bibliotecas disponibles en `assets/plugins` no se eliminan.

## Ejemplos mínimos de componentes

Los siguientes fragmentos usan rutas desde la raíz del proyecto. Si tu página
está en una subcarpeta, antepone `../` a las rutas de `assets/`. Guarda el código
JavaScript en archivos externos y cárgalos después de sus bibliotecas.

### Estilos y núcleo compartidos

Incluye estos estilos en `<head>`, en este orden:

```html
<link rel="stylesheet" href="assets/plugins/bootstrap-5.3.8/css/bootstrap.min.css">
<link rel="stylesheet" href="assets/plugins/poppins-5.3.0/poppins.css">
<link rel="stylesheet" href="assets/css/theme.css">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/plugins/bootstrap-icons-1.13.1/font/bootstrap-icons.min.css">
<link rel="stylesheet" href="assets/css/icon-compat.css">
<link rel="stylesheet" href="assets/plugins/hmenu/ace-responsive-menu.css">
<link rel="stylesheet" href="assets/css/accessibility.css">
```

Incluye estos scripts antes de `</body>`. El núcleo funciona sin jQuery:

```html
<script src="assets/plugins/popper-2.11.8/popper.min.js"></script>
<script src="assets/plugins/bootstrap-5.3.8/js/bootstrap.min.js"></script>
<script src="assets/js/bootstrap-components.js"></script>
<script src="assets/js/niche.js"></script>
<script src="assets/js/niche/layout.js"></script>
<script src="assets/js/niche/navigation.js"></script>
<script src="assets/js/niche/widgets.js"></script>
```

Para personalizar colores, fuentes o espaciado, carga tu CSS después de los
estilos compartidos y modifica las variables de `theme.css`. Para copiar una
página completa con cabecera y pie, parte de [pages/pages-blank.html](pages/pages-blank.html).

### Menú con submenú

Coloca este bloque dentro de `.wrapper`. Usa rutas reales en los enlaces.
`navigation.js` configura apertura, teclado y comportamiento móvil:

```html
<nav aria-label="Main navigation">
  <div class="menu-toggle">
    <button id="menu-btn" type="button" aria-label="Toggle navigation"
            aria-controls="respMenu" aria-expanded="false">Menu</button>
  </div>
  <ul id="respMenu" class="ace-responsive-menu" data-menu-style="horizontal">
    <li><a href="index.html">Home</a></li>
    <li>
      <a href="#" role="button">Examples</a>
      <ul>
        <li><a href="tables/table-data-table.html">Tables</a></li>
        <li><a href="forms/form-elements.html">Forms</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

Conserva un único `respMenu` y `menu-btn` por página. Cambia etiquetas y destinos;
no hace falta añadir un inicializador jQuery.

### Panel colapsable

`widgets.js` conecta los botones mediante `data-widget`. Los botones con iconos
necesitan nombre accesible:

```html
<section class="box">
  <div class="box-header">
    <h3 class="box-title">Report</h3>
    <div class="box-tools">
      <button class="btn btn-box-tool" type="button" data-widget="collapse"
              aria-label="Collapse report">
        <i class="fa fa-minus" aria-hidden="true"></i>
      </button>
    </div>
  </div>
  <div class="box-body">Your content goes here.</div>
</section>
```

Puedes controlarlo desde un archivo externo con
`Niche.component(document.querySelector('.box'), 'boxWidget', 'collapse')`.
Para varios paneles, utiliza un selector específico para cada uno.

### Formulario con validación nativa

Este ejemplo comprueba un correo y muestra el resultado sin enviarlo. Para
formularios con varios pasos, consulta [forms/form-wizard.html](forms/form-wizard.html)
y su inicializador `assets/js/form-wizard.js`.

```html
<form id="contact-demo">
  <label for="contact-email" class="form-label">Email address</label>
  <input id="contact-email" name="email" type="email" class="form-control"
         required aria-describedby="contact-email-help">
  <p id="contact-email-help" class="form-text">Use an address such as name@example.com.</p>
  <button type="submit" class="btn btn-primary">Check email</button>
  <p id="contact-result" role="status"></p>
</form>
```

Guarda este código en `assets/js/contact-demo.js` y añade su `<script src>` al
final de la página. El navegador muestra el error y enfoca el campo inválido;
`role="status"` anuncia el resultado cuando el correo es válido:

```javascript
// assets/js/contact-demo.js
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contact-demo');
    const result = document.getElementById('contact-result');
    form.addEventListener('invalid', function () { result.textContent = ''; }, true);
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        result.textContent = 'Valid email. No information was sent.';
    });
});
```

### Tabla con búsqueda y paginación

Añade este CSS después de Bootstrap:

```html
<link rel="stylesheet" href="assets/plugins/datatables-3.1.3/css/dataTables.bootstrap5.min.css">
```

La tabla necesita encabezados y un ID propio:

```html
<div class="table-responsive">
  <table id="people" class="table table-striped">
    <caption>Example contacts</caption>
    <thead><tr><th scope="col">Name</th><th scope="col">Email</th></tr></thead>
    <tbody>
      <tr><td>Ada</td><td>ada@example.com</td></tr>
      <tr><td>Linus</td><td>linus@example.com</td></tr>
    </tbody>
  </table>
</div>
```

Carga estos scripts en orden, después del núcleo y antes de `</body>`. jQuery es
necesario para DataTables; incluye una sola copia por página:

```html
<script src="assets/plugins/jquery-4.0.0/jquery.min.js"></script>
<script src="assets/plugins/datatables-3.1.3/dataTables.min.js"></script>
<script src="assets/plugins/datatables-3.1.3/dataTables.bootstrap5.min.js"></script>
<script src="assets/js/people-table.js"></script>
```

Guarda este inicializador en `assets/js/people-table.js`:

```javascript
// assets/js/people-table.js
document.addEventListener('DOMContentLoaded', function () {
    new DataTable('#people', { pageLength: 10 });
});
```

Para exportación de filas filtradas, copia las dependencias y el inicializador
de [tables/table-data-table.html](tables/table-data-table.html). Para edición,
consulta [tables/table-jsgrid.html](tables/table-jsgrid.html), que usa Tabulator.
El adaptador `niche/jquery-bridge.js` solo es necesario si también quieres usar
las antiguas llamadas como `$('.box').boxWidget()`; colócalo después de los
módulos del núcleo y de jQuery.

### Gráfico con tabla accesible

El contenedor fija la altura del canvas; el resumen y la tabla se añaden fuera
de ese contenedor. Usa un ID diferente para cada gráfico:

```html
<section class="info-box">
  <h4>Weekly sales</h4>
  <div class="position-relative" style="height:300px">
    <canvas id="weekly-sales" role="img" aria-label="Weekly sales"></canvas>
  </div>
</section>
```

Carga los scripts en este orden:

```html
<script src="assets/plugins/chart-js-4.5.1/chart.umd.js"></script>
<script src="assets/js/chart-theme.js"></script>
<script src="assets/js/chart-accessibility.js"></script>
<script src="assets/js/weekly-sales.js"></script>
```

Guarda el inicializador en `assets/js/weekly-sales.js`. Sustituye etiquetas,
valores y nombre de la serie por los tuyos:

```javascript
// assets/js/weekly-sales.js
document.addEventListener('DOMContentLoaded', async function () {
    await document.fonts.load('12px ' + Chart.defaults.font.family);
    const sales = new Chart(document.getElementById('weekly-sales'), {
        type: 'bar',
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday'],
            datasets: [{ label: 'Sales', data: [12, 18, 15] }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } }
        }
    });
    // To refresh values later: change sales.data, then call sales.update().
});
```

El resumen y la tabla accesible se generan con esos datos y se actualizan al
llamar a `sales.update()`. No necesitan una segunda copia manual de los valores.

## JavaScript de la plantilla

La lógica de aplicación está en archivos externos. El núcleo funciona con
JavaScript nativo y carga estos cuatro scripts en orden:

1. `assets/js/niche.js`: registro de componentes, instancias y callbacks de carga.
2. `assets/js/niche/layout.js`: alturas y scroll nativo de la barra lateral.
3. `assets/js/niche/navigation.js`: menú horizontal, barras laterales y árboles.
4. `assets/js/niche/widgets.js`: cajas colapsables, tareas y paneles de chat.

El núcleo no requiere jQuery, Ace Responsive Menu ni SlimScroll. Conserva el HTML
y los atributos `data-*`, utiliza eventos DOM y animaciones del navegador que
respetan la preferencia de movimiento reducido. El menú se inicializa al estar
listo el DOM, con ratón, teclado y cambios entre escritorio y móvil. Las páginas
siguen siendo HTML independientes, sin compilación ni framework.

Para usar un componente desde JavaScript nativo:

```javascript
const box = document.querySelector('.box');
Niche.component(box, 'boxWidget', 'collapse');
Niche.component(box, 'boxWidget', 'expand');
const instance = Niche.getComponent(box, 'boxWidget');
box.addEventListener('collapsed.boxwidget', () => console.log('Panel collapsed'));
```

`Niche.component(element, name, options)` inicializa una sola instancia por
elemento y componente. También acepta un selector y un nombre de método como
tercer argumento. `Niche.defineComponent` permite registrar componentes nuevos.
Los callbacks nativos de tareas reciben el checkbox DOM como `this`.

Las páginas que requieren jQuery cargan después `assets/js/niche/jquery-bridge.js`, un
adaptador opcional para las llamadas jQuery `layout`, `pushMenu`, `tree`,
`controlSidebar`, `boxWidget`, `todoList` y `directChat`. Conserva las instancias
`data('lte.*')`, eventos y `noConflict`, y conecta las llamadas con el mismo
componente nativo. Se puede omitir al usar únicamente la API `Niche`.

jQuery se mantiene para los plugins e inicializadores de terceros que todavía
lo utilizan, por ejemplo DataTables, Ion.RangeSlider, Knob y el formulario por
pasos. Migrar el núcleo no elimina esa dependencia del conjunto de la plantilla.

Los scripts específicos se cargan después de sus bibliotecas:

| Archivo | Responsabilidad |
| --- | --- |
| `assets/js/dashboard-charts.js` | Tres gráficos del dashboard principal |
| `assets/js/knob-examples.js` | Ejemplos de indicadores circulares |
| `assets/js/data-tables.js` | Inicialización compartida de las tablas de ejemplo |
| `assets/js/text-editor.js` | Jodit, redacción de correo y acciones de edición/guardado |
| `assets/js/form-wizard.js` | Validación y navegación del formulario por pasos |

Para añadir acciones a botones, utiliza atributos `data-*` y listeners en su
archivo de componente. Evita scripts inline y atributos `onclick` en los HTML.
Las pruebas comprueban esa estructura, el orden de carga y las interacciones del
menú móvil, widgets, gráficos y formulario por pasos. Incluyen un contexto de
navegador que carga únicamente el núcleo, sin jQuery ni scripts de plugins, y
otro que verifica las páginas completas y el adaptador de compatibilidad.

## Historial de cambios

### Núcleo JavaScript nativo — octubre de 2026

- Registro, layout, menú, barras laterales, árboles y widgets sin dependencia de jQuery.
- Scroll y animaciones nativos con preferencia de movimiento reducido.
- Adaptador opcional para las llamadas jQuery anteriores, usando las mismas instancias.
- Retirada del JavaScript de Ace Responsive Menu y de SlimScroll.
- Pruebas del núcleo sin cargar jQuery, además de compatibilidad y revisión de las 67 páginas.


### Accesibilidad, imágenes y fuentes locales — octubre de 2026

- Zoom habilitado, enlace para saltar al contenido y foco visible en las 67 páginas.
- Menú con teclado y estados ARIA; etiquetas, controles con iconos e IDs corregidos.
- Dimensiones en las imágenes, carga diferida en 222 y 36 copias WebP sin pérdida.
- Poppins WOFF2 local con cinco pesos y licencia conservada.
- Comprobaciones de accesibilidad con axe-core y validación de enlaces de galería.


### Retirada de plugins antiguos — octubre de 2026

- Jodit 4.17.1 sustituye Summernote en el editor y la redacción de correo.
- Chart.js sustituye Peity en 18 ejemplos y tres minigráficos del dashboard.
- Galería nativa con CSS Grid, filtros, contadores y diálogo de imágenes.
- Retirada de CubePortfolio, Peity, Summernote y jQuery Migrate.
- Actualizador y pruebas adaptados para mantener la migración al repetirlo.

### Pruebas automáticas — octubre de 2026

- Workflow de GitHub Actions para push, pull request y ejecución manual.
- Comprobación de recursos, migraciones, estructura del JavaScript y navegador.
- Versiones de herramientas fijadas y caché de descargas Python.
- Insignia del estado de las pruebas y documentación para ejecutarlas localmente.

### Organización del JavaScript — octubre de 2026

- División del núcleo minificado en registro de plugins, layout, navegación y widgets legibles.
- Centralización de 61 inicializaciones repetidas del menú horizontal.
- Extracción de scripts inline de gráficos, tablas, editores y formularios por pasos.
- Acciones de edición/guardado mediante listeners y atributos `data-editor-action`.
- Inicialización de dropdowns compartida y protección contra registros duplicados.
- Pruebas de estructura y de comportamiento para los componentes reorganizados.

### Bibliotecas y migraciones completadas — octubre de 2026

- jQuery 4.0.0 y jQuery Migrate 4.0.2, limitado a las páginas con plugins antiguos.
- FullCalendar 7.1.0: estilos Bootstrap 5, API de arrastre y colores actualizados; eventos de día completo explícitos.
- Ion.RangeSlider 2.5.0: restauración de los siete controles mediante inputs etiquetados y su tema integrado.
- FilePond 4.32.12 y plugins de vista previa/validación sustituyen Dropify y Dropzone.
- Tabulator 6.6.1 sustituye jsGrid; Bootstrap Icons 1.13.1 sustituye cinco fuentes generales.
- Retirada de once carpetas sustituidas, conservando las marcas SVG y su licencia.
- Corrección de inicializadores de mapas y timeline, orden de carga del editor y fondos inexistentes.
- Pruebas de navegador reproducibles y comprobaciones de rutas y migraciones idempotentes.

### Limpieza de recursos — octubre de 2026

- Eliminación de 21 carpetas de plugins y siete inicializadores sin referencias activas.
- Retirada de cargas sobrantes de tooltip/popover en las páginas de carrusel y listas.
- Corrección de rutas de fuentes de Weather Icons y Dropify.
- Sustitución de fondos e imágenes de pago ausentes por colores e insignias de texto.
- Comprobador de recursos locales e exclusión de cachés Python en Git.
- Conservación de los componentes cuya migración todavía necesita descargar bibliotecas.

### Compatibilidad con Bootstrap 5 — octubre de 2026

- Sustitución de utilidades antiguas de floats, imágenes, columnas, texto y tamaños de controles.
- Botones, insignias, selects, archivos, checkboxes, radios y grupos de inputs con clases Bootstrap 5.
- Cierre de alertas con `btn-close` y `data-bs-dismiss`; acordeón nativo en el FAQ.
- Indicadores de carrusel como botones, relaciones entre pestañas y paneles, y estados de validación nativos.
- Tooltips y popovers nativos sustituyen los plugins anteriores; se conservan las direcciones, alineaciones y temas de los ejemplos.
- Inicialización compartida y ajustes del menú horizontal para Bootstrap 5.

### Simplificación de componentes — octubre de 2026

- Chart.js sustituye Morris.js, Raphaël y Chartist en las páginas y dashboards que los cargaban.
- Las galerías conservan sus datos de ejemplo, tooltips y gráficos animados; las animaciones respetan la preferencia de movimiento reducido.
- Bootstrap Switch e iCheck se sustituyen por controles nativos con estilos Bootstrap 5 y etiquetas asociadas.
- La selección de mensajes funciona con las filas filtradas de DataTables, incluidas las de otras páginas.
- El grupo de radios que admite quedar vacío dispone de un botón «Clear selection».
- El calendario deja de cargar Moment y el dashboard alternativo utiliza la copia local de jQuery.
- Se conservan las rutas `chart-morris.html`, `chart-chartist.html` y `ui-bootstrap-switch.html` para mantener los enlaces existentes.

### Actualización de dependencias — octubre de 2026

- Bootstrap 5.3.8, Chart.js 4.5.1 y jQuery UI 1.14.2.
- Migración a DataTables 3.1.3 con integración Bootstrap 5 de la misma versión.
- FullCalendar 6.1.21 y arrastre de eventos mediante `FullCalendar.Draggable`.
- Eliminación de referencias a un CSS de calendario que contenía un error de descarga.
- Summernote 0.9.1 y sus fuentes; jQuery Validation 1.22.1 servido localmente.
- SheetJS 0.20.3 sustituye TableExport y FileSaver en la página de tablas.
- El calendario utiliza `Date`; Moment se retiró en la simplificación posterior.
- Restauración de los seis gráficos de Chart.js y de la inicialización de Bootstrap Switch.
- Corrección de rutas inexistentes de Chart.js, Popper y Bootstrap Switch.
- Script de actualización con preparación de descargas y comprobación de rutas locales.

### Migración a Bootstrap 5 — agosto de 2025

- Modernización de las pantallas de login, registro y recuperación de contraseña.
- Ajustes de alineación, estilos y distribución responsive.
- Adaptación del sistema de columnas y de componentes de interfaz.

## Contribuciones

Abre un [issue](https://github.com/claudioborja/horizonte-admin/issues)
con la página afectada, los pasos para reproducir el problema y el navegador usado.
Para proponer cambios, envía un pull request y describe las comprobaciones realizadas.

## Origen y licencias

La plantilla procede de una versión original propietaria de terceros. Este
repositorio incorpora modificaciones de mantenimiento y modernización, pero no
incluye un archivo `LICENSE` general que establezca permisos para todo el proyecto.
Las bibliotecas incorporadas conservan sus avisos de licencia en sus archivos.
Revisa las condiciones aplicables a la plantilla, imágenes, fuentes y componentes
antes de reutilizarlos o redistribuirlos.

Mantenedor indicado por el proyecto: [@claudioborja](https://github.com/claudioborja).
