# Niche Horizontal — Bootstrap 5

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
git clone https://github.com/claudioborja/Niche-Horizontal-Bootstrap5.git
cd Niche-Horizontal-Bootstrap5
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
| Formularios | 6 | [Editor Summernote](forms/form-summernote.html) |
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
| jQuery | 4.0.0 | Plugins existentes y comportamiento de la plantilla |
| jQuery Migrate | 4.0.2 | Compatibilidad temporal de Summernote, Peity y CubePortfolio |
| jQuery UI | 1.14.2 | Componentes utilizados por las páginas de ejemplo |
| Chart.js | 4.5.1 | Gráficos en dashboards y página de demostración |
| DataTables | 3.1.3 | Tablas con integración Bootstrap 5 |
| FullCalendar | 7.1.0 | Calendarios y arrastre de eventos |
| Summernote | 0.9.1 | Editor de texto con integración Bootstrap 5 |
| jQuery Validation | 1.22.1 | Validación del formulario por pasos |
| SheetJS | 0.20.3 | Exportación de tablas a XLSX, XLS, CSV y TXT |
| FilePond | 4.32.12 | Selección de archivos y adjuntos con vistas previas |
| Tabulator | 6.6.1 | Tablas editables, filtros y paginación local |
| Bootstrap Icons | 1.13.1 | Iconos generales y catálogos con búsqueda |
| Ion.RangeSlider | 2.5.0 | Siete ejemplos de selección de rangos |

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

jQuery se actualizó a 4.0.0. Summernote, Peity y CubePortfolio todavía utilizan
APIs retiradas: sus cinco páginas cargan jQuery Migrate 4.0.2 inmediatamente
después de jQuery. El resto utiliza jQuery 4 directamente. Este puente se podrá
retirar cuando esos plugins sean compatibles sin él.

FullCalendar 7.1.0 carga el bundle global, el plugin de Bootstrap 5 y sus dos
hojas de estilo locales. El inicializador utiliza `FullCalendar.Interaction.Draggable`
y los campos de evento `color` y `allDay`. Los sliders utilizan inputs
etiquetados y el tema integrado `modern` de Ion.RangeSlider 2.5.0.

Se retiraron Dropify, Dropzone, jsGrid y las cinco fuentes generales anteriores,
así como las copias sustituidas de jQuery, FullCalendar e Ion.RangeSlider.
Los SVG de marcas conservan su atribución y licencia en
[assets/img/brands/LICENSE.txt](assets/img/brands/LICENSE.txt). El historial de
Git permite recuperar los archivos retirados.

Las dependencias principales se sirven desde `assets/plugins/`. Algunas páginas
cargan recursos externos, como Google Fonts y Google Maps, que requieren conexión.
Para usar Google Maps en tu aplicación, configura tu propia clave en
[maps/map-google.html](maps/map-google.html).

## Estructura del proyecto

```text
Niche-Horizontal-Bootstrap5/
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
descarga desde su CDN. Summernote y Bootstrap Icons incluyen las fuentes necesarias para sus iconos.
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
tablas, editor e iconos. Incluye vistas móviles de los componentes actualizados.
Playwright es una herramienta opcional de pruebas; la plantilla continúa
funcionando sin Node.js ni un proceso de compilación.

```bash
python3 -m venv .venv
.venv/bin/pip install playwright==1.63.0
.venv/bin/python -m playwright install chromium
.venv/bin/python tools/check_browser.py
```

El comprobador inicia y cierra su propio servidor local. Bloquea los servicios
externos para no depender de Google Fonts ni de una clave de Google Maps;
la conexión real con Google Maps se debe comprobar con una clave válida.

Después de actualizar o personalizar la plantilla, inicia el servidor local y
revisa la consola y la pestaña de red del navegador.

| Componente | Comprobación |
| --- | --- |
| Dashboards | Navegación, dropdowns y distribución en escritorio y móvil |
| Chart.js | Los seis tipos de gráfico aparecen y se adaptan al tamaño de la ventana |
| DataTables | Búsqueda, ordenación, paginación y selección del tamaño de página donde estén habilitadas |
| Exportación | Descarga y apertura de XLSX, XLS, CSV y TXT; incluye filas filtradas de otras páginas |
| Calendario | Crear eventos externos, arrastrarlos al calendario y usar «remove after drop» |
| Summernote | Escribir, dar formato, insertar una imagen y cambiar a vista de código |
| Formulario por pasos | Campos obligatorios, mensajes de error y avance entre pasos |
| Bootstrap 5 | Cerrar alertas; cambiar pestañas; abrir dropdowns y el acordeón del FAQ; usar indicadores de carrusel y tooltips/popovers |
| Controles nativos | Cambiar interruptores; comprobar los estados deshabilitados, de solo lectura y la limpieza del grupo de radios |
| FilePond | Arrastrar archivos, previsualizar imágenes, comprobar el límite de 2 MB, los inputs deshabilitados y los adjuntos múltiples |
| Tabulator | Editar celdas, filtrar, paginar, confirmar el borrado y ordenar desde el selector externo |
| Iconos | Iconos del menú, estados dinámicos del correo, logotipos y búsqueda en los catálogos |
| Correo | Seleccionar y deseleccionar mensajes, también en otras páginas de la tabla, y cambiar sus estrellas |

La exportación utiliza el texto de las celdas y conserva el orden y el filtro
aplicados en DataTables. No reproduce imágenes ni estilos visuales de la tabla.
Los cambios en calendarios y formularios necesitan un backend para persistirse.

## Personalización

- Edita [assets/css/style.css](assets/css/style.css) para ajustar los estilos de la plantilla.
- Usa [assets/js/niche.js](assets/js/niche.js) para el comportamiento general.
- Ajusta [assets/js/bootstrap-components.js](assets/js/bootstrap-components.js) para inicializar tooltips y popovers nativos.
- Modifica [assets/plugins/functions/calendar-init.js](assets/plugins/functions/calendar-init.js) para los eventos de demostración.
- Ajusta [assets/plugins/chartjs/chart-int.js](assets/plugins/chartjs/chart-int.js) para los seis gráficos de Chart.js.
- Modifica [assets/js/chart-examples.js](assets/js/chart-examples.js) para las galerías de líneas, áreas y gráficos animados, y los dashboards alternativos.
- Usa [assets/js/mailbox.js](assets/js/mailbox.js) para la selección de mensajes y estrellas.
- Ajusta [assets/css/switches.css](assets/css/switches.css) y [assets/js/switches.js](assets/js/switches.js) para los controles nativos.
- Ajusta [assets/js/file-uploads.js](assets/js/file-uploads.js) para FilePond y [assets/js/editable-tables.js](assets/js/editable-tables.js) para Tabulator.
- Modifica [tools/component_migrations.py](tools/component_migrations.py) para las migraciones de páginas y la compatibilidad de iconos.
- Edita [assets/js/table-export.js](assets/js/table-export.js) para cambiar los botones y formatos de exportación.

Conserva las rutas relativas al mover páginas entre carpetas. Los datos de ejemplo
pueden sustituirse por respuestas de tu API en los inicializadores correspondientes.

## JavaScript de la plantilla

La lógica de aplicación está en archivos externos. Las páginas con la plantilla
cargan estos scripts en orden, después de jQuery:

1. `assets/js/niche.js`: registro compartido de plugins y callbacks de carga.
2. `assets/js/niche/layout.js`: cálculo de alturas y scroll opcional de la barra lateral.
3. `assets/js/niche/navigation.js`: menú horizontal, navegación lateral y árboles.
4. `assets/js/niche/widgets.js`: cajas colapsables, listas de tareas y paneles de chat.

Los componentes conservan sus APIs jQuery, opciones `data-*` y eventos de la
plantilla. El menú se inicializa desde el módulo de navegación cuando el DOM y
su plugin están disponibles; no necesita un bloque repetido en cada página.

Los scripts específicos se cargan después de sus bibliotecas:

| Archivo | Responsabilidad |
| --- | --- |
| `assets/js/dashboard-charts.js` | Tres gráficos del dashboard principal |
| `assets/js/knob-examples.js` | Ejemplos de indicadores circulares |
| `assets/js/data-tables.js` | Inicialización compartida de las tablas de ejemplo |
| `assets/js/text-editor.js` | Summernote, redacción de correo y acciones de edición/guardado |
| `assets/js/form-wizard.js` | Validación y navegación del formulario por pasos |

Para añadir acciones a botones, utiliza atributos `data-*` y listeners en su
archivo de componente. Evita scripts inline y atributos `onclick` en los HTML.
Las pruebas comprueban esa estructura, el orden de carga y las interacciones del
menú móvil, widgets, gráficos y formulario por pasos.

## Historial de cambios

### Organización del JavaScript — octubre de 2026

- División del núcleo minificado en registro de plugins, layout, navegación y widgets legibles.
- Centralización de 61 inicializaciones repetidas del menú horizontal.
- Extracción de scripts inline de gráficos, tablas, Summernote y formularios por pasos.
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

Abre un [issue](https://github.com/claudioborja/Niche-Horizontal-Bootstrap5/issues)
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
