# 🇨🇱 Taller: Desarrollo Agéntico con Datos Públicos de Chile

Bienvenido/a 👋 En este taller vas a construir una aplicación que consume
**datos públicos del Estado de Chile**, usando **Kiro** como asistente y un
**servidor MCP** que conecta a Kiro con el [Portal de Datos Abiertos](https://datos.gob.cl).

> 💡 **No necesitas ser experto.** Sigue las secciones en orden y estarás
> construyendo tu app en unos minutos.

---

## 📑 Contenido

1. [🎯 Qué vas a lograr](#-qué-vas-a-lograr)
2. [🗺️ Cómo funciona](#️-cómo-funciona)
3. [✅ Requisitos](#-requisitos)
4. [🚀 Instalación y configuración](#-instalación-y-configuración)
5. [🧪 Probar que todo funciona](#-probar-que-todo-funciona)
6. [🧰 Herramientas disponibles](#-herramientas-disponibles)
7. [💡 Construye tu app](#-construye-tu-app)
8. [🆘 Solución de problemas](#-solución-de-problemas)

---

## 🎯 Qué vas a lograr

- 🔌 Conectar Kiro a un servidor MCP de datos chilenos.
- 🔎 Buscar y explorar datasets reales (transporte, educación, presupuesto...).
- 🛠️ Pedirle a Kiro que construya una app (por ejemplo en Streamlit) con esos datos.

---

## 🗺️ Cómo funciona

```
🧑‍💻 Tú  →  🤖 Kiro  →  🔌 Servidor MCP (este repo)  →  🌐 datos.gob.cl
```

- 🤖 **Kiro** entiende lo que pides y usa las herramientas del MCP.
- 🔌 **El servidor MCP** busca datasets y trae los datos.
- 🌐 **datos.gob.cl** es la fuente oficial de datos abiertos del Estado.

---

## ✅ Requisitos

| | Requisito | Cómo verificar |
|---|---|---|
| 1️⃣ | **Kiro** instalado | Ábrelo. Si abre, listo. |
| 2️⃣ | **Git** instalado | En terminal: `git --version` |
| 3️⃣ | **Internet** | Necesario para consultar datos.gob.cl |

> ℹ️ **No necesitas** instalar Python ni otras librerías a mano. El script de
> instalación se encarga de todo.

---

## 🚀 Instalación y configuración

Sigue estos pasos **en orden**.

### Paso 1️⃣ — Clonar el repositorio

📋 Copia y pega en tu terminal:

```bash
git clone <URL-DEL-REPO>
cd agentic-development-cl
```

> 🔗 Tu instructor/a te dará la `<URL-DEL-REPO>`.

### Paso 2️⃣ — Instalar dependencias

▶️ **macOS / Linux:**

```bash
./install.sh
```

▶️ **Windows:**

```bat
install.bat
```

⏳ Espera a que termine. Debe aparecer:

```
[ok] Instalación completa.
```

El script instala `uv`, crea el entorno del servidor, descarga las dependencias
y verifica que todo arranca. No tienes que hacer nada más aquí.

### Paso 3️⃣ — Abrir el proyecto en Kiro

📂 En Kiro: **File → Open Folder** y elige la carpeta `agentic-development-cl`
que acabas de clonar.

> ❗ **Importante:** abre esa carpeta exacta, no una carpeta superior. El servidor
> MCP viene preconfigurado en el repo (`.kiro/settings/mcp.json`) y Kiro lo
> detecta automáticamente al abrir esta carpeta como workspace.

### Paso 4️⃣ — Verificar la conexión

🔍 Abre el panel **MCP Servers** en la barra lateral de Kiro. Deberías ver:

- ✅ `servidor-chile-datos-publicos` en estado **conectado**
- 🛠️ Sus 4 herramientas listadas

> 🆘 ¿No aparece o está en error? Ve a [Solución de problemas](#-solución-de-problemas).

---

## 🧪 Probar que todo funciona

💬 Escríbele a Kiro:

```
Busca datasets de lugares de carga de tarjeta bip
y muéstrame las columnas del principal.
```

✨ Kiro usará las herramientas del MCP y te mostrará datos reales de datos.gob.cl.
Si ves columnas y filas de un dataset de puntos de carga bip!, ¡todo está
funcionando! 🎉

---

## 🧰 Herramientas disponibles

Estas son las herramientas que Kiro puede usar a través del MCP:

| 🛠️ Herramienta | ¿Para qué sirve? |
|---|---|
| 🔎 `search_datasets` | Buscar datasets por tema (con filtro de formato). |
| 📁 `list_dataset_resource` | Ver los archivos de un dataset y sus enlaces. |
| 👀 `preview_resource` | Espiar columnas y primeras filas de un archivo. |
| 📥 `get_resource_data` | Descargar un archivo completo y limpio. |

> 🧠 **La receta:** el MCP te da los datos → Kiro escribe el código → tú decides
> qué construir.

---

## 💡 Construye tu app

Ejemplos de peticiones que puedes hacerle a Kiro, usando datos de **transporte**:

- 🗺️ *"Crea una app Streamlit con un mapa de los puntos de carga de tarjeta bip! usando sus coordenadas."*
- 📊 *"Haz un gráfico con la cantidad de puntos de carga bip! por comuna."*
- 🔎 *"Agrega a la app un filtro para buscar puntos de carga bip! por comuna."*
- 📍 *"Muéstrame en una tabla los centros bip! de alto estándar y su dirección."*

> 💬 Empieza pidiéndole a Kiro que **busque** el dataset, luego que **explore** sus
> columnas, y finalmente que **construya** la app. Kiro encadena las herramientas
> del MCP por ti.

---

## 🆘 Solución de problemas

### ❌ El servidor MCP aparece en error o "no conectado"

- ✔️ Verifica que abriste la carpeta **raíz del repo** como workspace (Paso 3).
- ✔️ Confirma que `uv` está disponible: en terminal ejecuta `uv --version`.
  Si no lo reconoce, **cierra y reabre Kiro y la terminal** para refrescar el PATH.
- 🔄 Reconecta el servidor desde el panel **MCP Servers** (botón de recargar).

### ❌ Las herramientas no aparecen aunque el servidor esté conectado

- 🔄 Reconecta el servidor para que recargue la lista de herramientas.
- 📋 Revisa el panel de logs del MCP en Kiro: los mensajes del servidor aparecen
  ahí y te dirán si hubo algún error al cargar.

### ❌ Kiro usa `curl` o la terminal en vez del MCP

- El repo incluye una guía de comportamiento (`.kiro/steering/`) que le indica a
  Kiro preferir el MCP. Se carga sola al abrir el workspace.
- 💬 Sé específico: menciona **"datasets"** o **"datos.gob.cl"** en tu petición.
- Si insiste, pídele directamente: *"usa las herramientas del MCP
  servidor-chile-datos-publicos"*.

### 🔧 Verificar el servidor por fuera de Kiro

Desde la raíz del repo:

```bash
uv --directory mcp-server run python -c "import server, tools.chilean_data; print('OK')"
```

Si imprime `OK`, el servidor está sano y el problema está en la conexión con
Kiro, no en el código.

> 📖 ¿Necesitas más detalle de configuración? Revisa **[GUIA-KIRO.md](GUIA-KIRO.md)**.

---

## 📁 Estructura del repositorio

```
agentic-development-cl/
├── 📄 README.md            ← estás aquí
├── 📄 GUIA-KIRO.md         ← detalle de configuración del MCP
├── ⚙️ install.sh           ← instalación (macOS/Linux)
├── ⚙️ install.bat          ← instalación (Windows)
├── 📂 .kiro/               ← configuración del MCP (ya lista, no la toques)
└── 📂 mcp-server/          ← el servidor MCP
```

---

¡Éxito en el taller! 🇨🇱🚀
