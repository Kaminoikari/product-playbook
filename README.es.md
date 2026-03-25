[English](README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Español](README.es.md) | [한국어](README.ko.md)

# 🎯 The Product Playbook

**Skill de IA de planificación de producto de clase mundial — de la idea al desarrollo, un framework para gobernarlos a todos**

[![npm version](https://img.shields.io/npm/v/product-playbook.svg)](https://www.npmjs.com/package/product-playbook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://code.claude.com)
[![Claude.ai](https://img.shields.io/badge/Claude.ai-Custom%20Skill-blue)](https://claude.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![i18n](https://img.shields.io/badge/i18n-6%20languages-green)](README.md)

> Integra los frameworks de PM de mayor impacto de Lenny's Podcast (Teresa Torres, Shreyas Doshi, Gibson Biddle, April Dunford, Todd Jackson, Marty Cagan, Richard Rumelt, y otros) — convirtiendo a la IA en tu coach senior de product management.

---

## ✨ ¿Qué es esto?

The Product Playbook es un **Skill de Claude AI** que te guía sistemáticamente a través de la planificación de producto de principio a fin, desde cero hasta uno. No es solo un prompt — es un sistema completo de guía de frameworks interactivo que incluye:

- 🧭 **6 modos de ejecución** — desde validación rápida en 30 minutos hasta planes de producto completos (incluyendo una ruta rápida de expansión de funcionalidades)
- 📐 **22 frameworks de producto** — cubriendo toda la cadena Discovery → Define → Develop → Deliver
- 🔄 **Motor de propagación de cambios** — modifica cualquier paso y todos los outputs downstream se actualizan automáticamente
- 📎 **Integración inteligente de archivos** — sube datos, capturas de pantalla o documentos; la IA los integra automáticamente en el paso relevante
- 🔗 **Handoff de desarrollo** — genera CLAUDE.md + TASKS.md + TICKETS.md para un handoff fluido al desarrollo en Claude Code
- 📊 **Output multi-formato** — PDF (con marcadores), reportes HTML, documentos Word, presentaciones PowerPoint, paquetes de handoff de desarrollo
- 📄 **Importación inteligente de documentos** — análisis de PDF en tres capas (extracción de texto → Claude Vision → OCR como respaldo), soporte DOCX/PPTX

**Activa todo el flujo con una sola oración:**

```
Quiero construir un producto
```

---

## 🎬 Demo

<p align="center">
  <img src="assets/demo-build-es.gif" alt="Demo de The Product Playbook — Modo Build" width="800">
</p>

> La demo anterior muestra el **Modo Build**: describe tus requisitos → escanea el codebase → detecta el stack tecnológico → aplica frameworks para clarificación del problema, luego salta directamente al diseño de solución.

---

## 🚀 Inicio Rápido

### Opción 1: Skill Personalizado de Claude.ai

1. Descarga este repositorio como archivo zip
2. Ve a [Claude.ai](https://claude.ai) → Configuración → Skills Personalizados
3. Sube toda la carpeta `product-playbook/`
4. Di "Quiero construir un producto" en una conversación para activar el skill

### Opción 2: Skill de Claude Code (Recomendado)

> 💡 Para actualizar: simplemente vuelve a ejecutar el comando de instalación para sobrescribir con la última versión.

| Método | Ideal para | Requisitos |
|--------|-----------|------------|
| ① Copiar y Pegar | Principiantes | Solo abre Claude Code |
| ② Instalación en una línea | Desarrolladores | Terminal |
| ③ Instalación manual | Rutas personalizadas | Terminal + git |

#### ① Instalación Copiar y Pegar (Más fácil)

Después de abrir Claude Code, pega lo siguiente y Claude manejará la instalación automáticamente:

```
Por favor ejecuta los siguientes comandos para instalar (o actualizar) el skill product-playbook,
y dime el resultado cuando termines:

git clone https://github.com/kaminoikari/product-playbook.git /tmp/product-playbook
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r /tmp/product-playbook ~/.claude/skills/product-playbook
cp /tmp/product-playbook/commands/* ~/.claude/commands/
rm -rf /tmp/product-playbook
```

#### ② Instalación en una línea (Terminal)

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash

# npx (requiere Node.js)
npx product-playbook
```

Desinstalar:

```bash
curl -fsSL https://raw.githubusercontent.com/kaminoikari/product-playbook/main/install.sh | bash -s -- --uninstall
# o
npx product-playbook --uninstall
```

#### ③ Instalación Manual

```bash
git clone https://github.com/kaminoikari/product-playbook.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r product-playbook ~/.claude/skills/product-playbook
cp product-playbook/commands/* ~/.claude/commands/
```

Una vez instalado, activa en Claude Code:

```bash
# Comando principal del skill
> /product-playbook

# Comandos Slash (disponibles después de instalar)
> /product-quick Quiero construir una app de seguimiento de gastos
> /product-full una plataforma social para mascotas
> /product-revision rediseñar nuestro flujo de checkout de e-commerce

# O lenguaje natural
> Quiero planificar un producto
> Analiza mi producto usando JTBD
> Ayúdame a planificar un MVP
```

---

## 📦 Estructura de Archivos

```
product-playbook/
├── SKILL.md                          # Motor central: definiciones de modos, secuencias de pasos, sistema de comandos
├── LICENSE                           # Licencia MIT
├── README.md                         # README en inglés
├── README.zh-TW.md                   # README en chino tradicional
├── assets/
│   └── demo.gif                      # Animación demo del README
├── commands/                         # Comandos Slash del CLI de Claude Code (instalación opcional)
│   ├── product-quick.md              # /product-quick — Modo rápido
│   ├── product-full.md               # /product-full — Modo completo
│   ├── product-revision.md           # /product-revision — Modo revisión
│   ├── product-build.md              # /product-build — Modo build
│   ├── product-prd.md                # /product-prd — Generar PRD
│   ├── product-report.md             # /product-report — Generar reporte HTML
│   └── product-dev.md                # /product-dev — Generar paquete de handoff de desarrollo
└── references/
    ├── 00-opportunity-check.md       # Evaluación de oportunidad + Modelo DHM
    ├── 01-strategy.md                # Strategy Blocks + Rumelt + OKR
    ├── 02-discovery.md               # Persona + JTBD + OST + Journey Map
    ├── 03-define.md                  # Puntos de dolor + Posicionamiento + HMW + Evaluación de oportunidades
    ├── 04-develop.md                 # PR-FAQ + Pre-mortem + RICE + MVP + PRD
    ├── 05-deliver.md                 # North Star + PMF + GTM + Modelo de negocio + Spec de producto
    ├── 06-html-report.md             # Spec de output de reporte de planificación HTML
    ├── 07-dev-handoff.md             # Handoff de desarrollo: CLAUDE.md + TASKS.md + Arquitectura
    ├── 08-security-checklist.md      # OWASP Top 10 + CORS + CSP + Arquitectura de seguridad
    ├── rules-context.md              # Reglas de acumulación de contexto de producto cross-sesión
    ├── rules-document-tools.md       # Gestión de dependencias de herramientas de conversión de documentos
    ├── rules-import-document.md      # Análisis de PDF en tres capas + importación DOCX/PPTX
    ├── rules-export-document.md      # Exportación multi-formato (PDF/DOCX/PPTX)
    ├── rules-*.md                    # Reglas de pasos por modo + reglas de progreso/cambio/integración de archivos
    └── templates/
        ├── prd-style.css             # CSS profesional de grado impresión para exportación PDF
        └── report-style.css          # CSS de optimización de impresión para reporte HTML → PDF
```

---

## 🧭 Seis Modos de Ejecución

| Modo | Pasos | Duración | Ideal para |
|------|-------|----------|-----------|
| 🚀 **Modo Rápido** | 3 pasos | ~30 min | Validación rápida de ideas, preparación de pitch |
| 📦 **Modo Completo** | 20 pasos | Varias horas | Planificación de nuevo producto, grandes renovaciones |
| 🔄 **Modo Revisión** | 12 pasos | 1-2 horas | Iteración sobre productos existentes |
| ✏️ **Modo Personalizado** | 4-16 pasos | Variable | Llenar vacíos específicos |
| ⚡ **Modo Build** | 7 pasos | ~1 hora | El problema es conocido, ir directo a soluciones |
| 🔧 **Expansión de Funcionalidades** | 4 pasos | ~30 min | Agregar una sola funcionalidad a un producto existente |

---

## 📐 Frameworks Incluidos

### Entendiendo Usuarios
| Framework | Creador | Propósito |
|-----------|---------|----------|
| JTBD (Jobs to Be Done) | Clayton Christensen | Descubrir el trabajo real que los usuarios intentan realizar |
| Persona | — | Arquetipos de usuario impulsados por tarea/motivación |
| User Journey Map | — | Mapeo de experiencia de usuario de principio a fin |
| Descubrimiento Continuo | Teresa Torres | Hábito semanal de hablar con usuarios |
| OST (Opportunity Solution Tree) | Teresa Torres | Conectar sistemáticamente oportunidades con soluciones |

### Definiendo el Problema
| Framework | Creador | Propósito |
|-----------|---------|----------|
| Posicionamiento | April Dunford | Contexto competitivo y diferenciación |
| HMW (How Might We) | — | Transformar puntos de dolor en desafíos de diseño |

### Diseño de Solución
| Framework | Creador | Propósito |
|-----------|---------|----------|
| Working Backwards / PR-FAQ | Amazon | Comenzar desde el resultado del cliente y trabajar hacia atrás |
| Pre-mortem | Shreyas Doshi | Predecir y prevenir el fracaso antes de que suceda |
| Modelo GEM | Gibson Biddle | Priorización Growth / Engagement / Monetization |
| Puntuación RICE | Intercom | Priorización cuantitativa de funcionalidades |
| Definición de MVP | — | Alcance mínimo viable del producto |

### Estrategia
| Framework | Creador | Propósito |
|-----------|---------|----------|
| Strategy Blocks | Chandra Janakiraman | Jerarquía Misión → Visión → Estrategia |
| Kernel de Buena Estrategia | Richard Rumelt | Diagnóstico → Política guía → Acción coherente |
| Modelo DHM | Gibson Biddle | Delight / Hard to copy / Margin-enhancing |
| Empowered Teams | Marty Cagan | Equipos empoderados vs. feature teams |

### Medición y Entrega
| Framework | Creador | Propósito |
|-----------|---------|----------|
| North Star Metric | Sean Ellis / Amplitude | Métrica única que representa el valor central para el usuario |
| Framework de Cuatro Niveles de PMF | Todd Jackson | Evaluar product-market fit |
| Sean Ellis Score | Sean Ellis | Cuantificar entusiasmo de PMF |
| Estrategia GTM | — | Lanzamiento go-to-market y adquisición |
| Modelo de Negocio y Precios | — | Selección de modelo de ingresos y precios basados en valor |

---

## 🔑 Funcionalidades Clave

### 📎 Integración Inteligente de Archivos

Sube archivos complementarios en cualquier paso — la IA los identifica e integra automáticamente:

| Subida | Auto-integrado en |
|--------|-------------------|
| Capturas de pantalla de competidores | Análisis de posicionamiento |
| Transcripciones de entrevistas | Persona + JTBD |
| CSV de datos de usuario | Evaluación de oportunidades + evaluación PMF |
| PDF de reporte de mercado | Evaluación de oportunidades + Estrategia |
| PRD existente | Modo revisión + MVP |

### 🔄 Motor de Propagación de Cambios

Modifica cualquier paso upstream y los outputs downstream se actualizan automáticamente:

```
Modificar JTBD → auto-actualiza HMW, Posicionamiento, PR-FAQ, North Star, Resumen de Spec de Producto
Modificar MVP  → auto-actualiza User Stories, DB Schema, Resumen de Spec de Producto
```

### 🔗 Handoff de Desarrollo

Genera un paquete completo de handoff de desarrollo e inicia desarrollo en Claude Code con un solo comando:

```
📦 Paquete de Handoff de Desarrollo
├── CLAUDE.md          → Memoria de proyecto de Claude Code
├── TASKS.md           → Desglose de funcionalidades + entrega por fases
├── TICKETS.md         → Lista de tickets (lista para Jira/Asana/Linear)
├── docs/
│   ├── PRD.md         → PRD completo
│   ├── ARCHITECTURE.md → DB Schema + API + estructura de directorios
│   └── PRODUCT-SPEC.md → Resumen de spec de producto
└── scripts/
    └── setup.sh       → Script de inicialización en un solo comando
```

```bash
# Inicia desarrollo en Claude Code con un solo comando
> Por favor lee CLAUDE.md y TASKS.md, comienza ejecutando la Fase 0
```

### 📄 Importación y Exportación de Documentos

**Importa** cualquier documento existente al flujo de planificación — sin copiar y pegar manualmente:

```
PDF (digital)       → extracción de texto pymupdf (instantáneo, gratuito)
PDF (vectorial/escaneo) → análisis semántico Claude Vision (mejor calidad)
PDF (respaldo)      → Tesseract OCR (funciona offline)
DOCX / PPTX         → conversión Pandoc
```

**Exporta** outputs de planificación a formatos profesionales:

```
/export pdf   → renderizado Playwright + marcadores pikepdf (CJK perfecto)
/export docx  → Pandoc + plantilla de referencia
/export pptx  → generación de diapositivas Pandoc
/export html  → reporte HTML interactivo (existente)
```

> **¿Por qué PDF via Playwright?** WeasyPrint produce texto CJK ilegible. Playwright (Chromium) renderiza perfectamente — verificado en producción con documentos en chino tradicional.

### 🔥 Planifica Directamente sobre Sistemas Existentes (Funcionalidad Estrella del Modo Build)

Lanza el **Modo Build** dentro de un directorio de proyecto existente — Claude Code lee tu codebase mientras hace planificación de producto, fusionando efectivamente **planificación de producto** y **evaluación de factibilidad técnica** en un solo flujo:

```
Tu Proyecto Existente                 Product Playbook
┌─────────────────┐                ┌─────────────────────┐
│ src/             │  ← auto-scan → │ Riesgos Pre-mortem   │
│ db/schema.sql    │  ← auto-scan → │ Alcance MVP          │
│ api/routes/      │  ← auto-scan → │ Priorización RICE    │
│ package.json     │  ← auto-scan → │ Desglose User Story  │
│ CLAUDE.md        │  ← auto-scan → │ Handoff dev (delta)  │
└─────────────────┘                └─────────────────────┘
```

**Ejemplo de uso:**

```bash
# 1. Navega a tu proyecto existente
cd /ruta/a/tu-proyecto-existente

# 2. Lanza Claude Code
claude

# 3. Usa el Modo Build y describe la funcionalidad que quieres agregar
> /product-build Quiero agregar notificaciones en tiempo real a mi sistema existente
```

Claude Code automáticamente:
- Escanea tu estructura de directorios, stack tecnológico y esquema BD
- Ejecuta Pre-mortem basado en tu **arquitectura real** (no riesgos hipotéticos)
- Genera MVP y User Stories que se conectan directamente a módulos existentes
- Produce un paquete de handoff de desarrollo como un **plan incremental**, no una construcción desde cero

> 💡 **¿Por qué es esto poderoso?** La planificación de producto tradicional y la evaluación técnica son procesos separados — los PMs escriben specs, se las lanzan a los ingenieros, y los ingenieros dicen "esto no se puede hacer." El Modo Build fundamenta el proceso de planificación en restricciones reales del sistema, eliminando el ir y venir.

### 🔒 Seguridad Integrada

Los paquetes de handoff de desarrollo automáticamente incluyen arquitectura de seguridad — sin parches como ocurrencia tardía:

- **Lista de verificación OWASP Top 10** — validación de input, autenticación/autorización, protección XSS/CSRF
- **Sección de arquitectura de seguridad** — políticas CORS, cabeceras CSP, rate limiting, middleware de seguridad API
- **Plantilla .gitignore** — auto-excluye `.env`, credenciales, archivos de progreso
- **Escenarios de seguridad Pre-mortem** — filtraciones de datos, tomas de cuenta, abuso de API como consideraciones obligatorias

### 📦 Acumulación de Contexto de Producto Cross-Sesión

Los outputs de planificación se guardan automáticamente en `.product-context.md` y se cargan en la siguiente sesión:

```
1ra sesión (Modo Completo) → guarda Identidad + Estrategia Central + Arquitectura
2da sesión (Expansión de Funcionalidades) → auto-carga stack tecnológico y módulos, omitiendo recopilación redundante
3ra sesión (Modo Revisión) → lleva adelante decisiones históricas y puntos de dolor conocidos, enfocándose en deltas
```

### 🏢 Adaptación Automática B2B / B2C

Una vez confirmado el tipo de producto, los frameworks se auto-adaptan:

| Aspecto | B2C | B2B |
|---------|-----|-----|
| Persona | Segmentación por motivación individual | Persona dual Comprador + Usuario |
| PMF | DAU / Retención / Sean Ellis | Clientes que pagan / NRR / NPS |
| North Star | Conteo de completación de acción central | ARR / Net Revenue Retention |
| Aha Moment | Dentro del primer uso | Onboarding / Time-to-Value |

---

## 📊 Resultados del Benchmark de Calidad

Comparando la calidad de respuesta entre "con guía del Skill" y "sin guía del Skill" usando calificación automática por IA, cuantificamos el impacto real del Skill.

### Cuatro Iteraciones Comparadas

| Iteración | Ítems de Prueba | Tasa de Aprobación con Skill | Tasa de Aprobación sin Skill | Delta |
|-----------|:--------------:|:---------------------------:|:----------------------------:|:-----:|
| Iteración 1 (Línea base) | 6 | 100% | 57.4% | +42.6% |
| Iteración 2 | 6 | 100% | 63.3% | +36.7% |
| Iteración 3 | 6 | 94.1% | 38.2% | +55.9% |
| **Iteración 4 (Última)** | **9** | **100%** | **31%** | **+69% ✅** |

### Resultados Detallados Iteración 4 (9 pruebas x 49 expectativas)

| Ítem de Prueba | Con Skill | Sin Skill | Delta |
|---------------|:--------:|:---------:|:-----:|
| Selección de Modo (3 pasos progresivos) | 100% | 0% | +100% |
| Análisis JTBD Modo Rápido | 100% | 43% | +57% |
| Profundidad JTBD (nivel org B2B) | 100% | 57% | +43% |
| Escritura PR-FAQ | 100% | 33% | +67% |
| Modo Revisión | 100% | 67% | +33% |
| Hard Gate de Autoevaluación de Calidad | 100% | 0% | +100% |
| **Modo Expansión de Funcionalidades (Nuevo)** | **100%** | **17%** | **+83%** |
| **Integración de Seguridad (Nuevo)** | **100%** | **25%** | **+75%** |
| **Context Bootstrap (Nuevo)** | **100%** | **0%** | **+100%** |

### Hallazgos Clave

- **Hard Gate de Autoevaluación de Calidad** (+100%): Si la IA critica proactivamente su propio output con estándares estrictos, señala brechas y exige mejoras después de completar un entregable — 0% de tasa de aprobación sin el Skill
- **Context Bootstrap** (+100%): Si la IA recopila información foundacional del producto antes de comenzar a planificar, en lugar de saltar directamente a implementación técnica — completamente omitido sin el Skill
- **Modo Expansión de Funcionalidades** (+83%): Si la IA reconoce escenarios de "agregar una funcionalidad a un producto existente" y activa un flujo simplificado de 4 pasos en lugar de los 7-12 pasos completos — sin el Skill, salta directamente a soluciones técnicas
- **Integración de Seguridad** (+75%): Si el handoff de desarrollo incluye arquitectura de seguridad, plantillas .gitignore y medidas de seguridad específicas de plataforma — sin el Skill, la seguridad se reduce a una tabla resumen

> Ver [`evals/`](./evals/) para metodología detallada y datos.

---

## 💬 Comandos Disponibles

### ⌨️ Comandos Slash del CLI de Claude Code

El comando principal disponible después de instalar el Skill:

| Comando | Descripción |
|---------|-------------|
| `/product-playbook` | Lanzar el flujo guiado completo de planificación de producto |

Para atajos más granulares, instala los comandos slash pre-construidos de la carpeta `commands/`:

```bash
# Instalar todos los comandos slash
cp -r product-playbook/commands/* ~/.claude/commands/
```

| Comando | Descripción |
|---------|-------------|
| `/product-quick <descripción>` | Modo Rápido — recorre JTBD → PR-FAQ → North Star en menos de 30 min |
| `/product-full <descripción>` | Modo Completo — plan de producto completo de 20 pasos |
| `/product-revision <descripción>` | Modo Revisión — iterar y optimizar un producto existente |
| `/product-build <descripción>` | Modo Build — omitir Discovery, ir directo a soluciones |
| `/product-prd` | Generar paquete de entrega de ingeniería PRD |
| `/product-report` | Generar reporte de planificación HTML |
| `/product-dev` | Generar paquete de handoff de desarrollo (CLAUDE.md + TASKS.md + TICKETS.md) |

### 💬 Comandos de Lenguaje Natural en Conversación

#### Control de Flujo
- `Cambiar a [framework]` — cambiar frameworks inmediatamente
- `Omitir este paso` — omitir el paso actual
- `Volver a [nombre del paso]` — regresar a cualquier paso para modificarlo
- `Simplificar esto` / `Expandir esto` — ajustar profundidad

#### Comandos de Output
- `Generar reporte` — reporte de planificación HTML
- `Generar PRD` — entrega de ingeniería (incluye diagramas de flujo + DB Schema + wireframes)
- `Generar presentación` — presentación PowerPoint
- `Iniciar desarrollo` — paquete de handoff de desarrollo (CLAUDE.md + TASKS.md)
- `/export pdf` — exportar como PDF con tipografía profesional, portada, índice y marcadores
- `/export docx` — exportar como documento Word
- `/export pptx` — exportar como diapositivas PowerPoint
- `/parse [file]` — analizar un PDF/DOCX/PPTX en Markdown para uso en planificación

#### Comandos de Análisis
- `Ejecutar evaluación de completitud` — evaluar cobertura de planificación
- `Identificar suposiciones` — listar suposiciones no validadas
- `Ejecutar un Pre-mortem` — análisis pre-mortem
- `¿En qué nivel de PMF está este producto?` — evaluación de PMF
- `Encontrar el cuello de botella` — análisis de obstáculos del Aha Moment

---

## 🤝 Contribuyendo

¡Las contribuciones son bienvenidas! Aquí hay algunas áreas donde la ayuda es especialmente apreciada:

- 🌍 **Soporte multi-idioma** — traducir frameworks a otros idiomas
- 📐 **Nuevos frameworks** — agregar más frameworks de product management
- 📝 **Ejemplos** — agregar más ejemplos trabajados a cada framework
- 🐛 **Reportes de bugs** — problemas de lógica o brechas encontradas durante el uso
- 💡 **Mejoras de UX** — sugerencias para flujo de interacción y diseño de comandos

### Cómo Contribuir

1. Haz un fork de este repo
2. Crea tu rama de funcionalidad (`git checkout -b feature/framework-increible`)
3. Haz commit de tus cambios (`git commit -m 'feat: agregar framework increíble'`)
4. Haz push a la rama (`git push origin feature/framework-increible`)
5. Abre un Pull Request

### Guías de Contribución

- El contenido de frameworks en archivos de referencia debe citar fuentes
- Nuevos frameworks deben incluir actualizaciones al índice de frameworks y secuencias de pasos de SKILL.md
- Las listas de autoevaluación de calidad usan formato ✅ / ❌
- Soporte multi-idioma: mantener versiones en todos los idiomas soportados

---

## 📚 Fuentes de Frameworks y Lecturas Adicionales

Los frameworks en este proyecto están sintetizados del trabajo público de estos líderes de pensamiento:

| Líder de Pensamiento | Contribución Central | Lectura Recomendada |
|---------------------|---------------------|---------------------|
| Teresa Torres | Descubrimiento Continuo, OST | *Continuous Discovery Habits* |
| Shreyas Doshi | LNO, Pre-mortem, Tres Niveles de Trabajo de Producto | Lenny's Podcast Ep.3 |
| Gibson Biddle | Modelo DHM, GEM | Lenny's Podcast |
| April Dunford | Framework de Posicionamiento | *Obviously Awesome* |
| Todd Jackson | PMF de Cuatro Niveles, Cuatro P's | Lenny's Podcast |
| Richard Rumelt | Buena Estrategia / Mala Estrategia | *Good Strategy Bad Strategy* |
| Marty Cagan | Empowered Teams | *Inspired*, *Empowered* |
| Clayton Christensen | Jobs to Be Done | *Competing Against Luck* |
| Amazon | Working Backwards / PR-FAQ | *Working Backwards* |
| Sean Ellis | Sean Ellis Score, Growth | *Hacking Growth* |
| Lenny Rachitsky | Shape / Ship / Synchronize | Lenny's Newsletter + Podcast |

---

## 📄 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE) — libre de usar, modificar y distribuir sin restricciones.

---

## ⭐ Historial de Estrellas

Si este proyecto te ayuda, ¡dale una ⭐ para que más personas puedan encontrarlo!

---

<p align="center">
  <strong>Construido con ❤️ para Product Managers que quieren construir cosas que importan.</strong>
</p>

---

Copyright (c) 2026 Charles Chen.
