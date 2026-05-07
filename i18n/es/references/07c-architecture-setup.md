# Handoff de Desarrollo — ARCHITECTURE.md + setup.sh

## 📄 Plantilla ARCHITECTURE.md

```markdown
# [Nombre del Producto] — Arquitectura Técnica

## Estructura de Directorios

[Generar la estructura de directorios correspondiente basada en el stack tecnológico]

## Diseño de Base de Datos

[Consolidar del DB Schema del PRD — convertir a SQL CREATE TABLE o definiciones de modelos ORM]

### Diagrama ER

[Mermaid erDiagram]

### Descripciones de Tablas Clave

| Tabla | Descripción | Campos Clave | Recomendaciones de Índices |
|-------|------------|-------------|--------------------------|
| | | | |

## Diseño de API

[Definir endpoints de API RESTful o schema GraphQL basado en User Stories y especificaciones de funcionalidades]

### Lista de Endpoints

| Método | Ruta | Descripción | Tarea Correspondiente |
|--------|------|------------|----------------------|
| GET | /api/v1/[recurso] | [Descripción] | T1.1 |
| POST | /api/v1/[recurso] | [Descripción] | T1.2 |

### Autenticación

[JWT / Session / OAuth, etc.]

## Servicios de Terceros

| Servicio | Propósito | Funcionalidad Correspondiente |
|----------|----------|-------------------------------|
| | | |

## Arquitectura de Seguridad

### Configuración CORS

| Configuración | Valor | Notas |
|--------------|-------|-------|
| Orígenes Permitidos | [Dominio de producción, localhost:puerto] | No usar wildcard * |
| Métodos Permitidos | GET, POST, PUT, DELETE | Basado en necesidades reales de API |
| Cabeceras Permitidas | Content-Type, Authorization | |
| Credentials | true/false | Depende del método de autenticación |

### Cabeceras de Seguridad

[Seleccionar cabeceras aplicables de references/08-security-checklist.md §5 basado en requisitos del producto]

### Estrategia de Rate Limiting

| Tipo de Endpoint | Límite | Método de Identificación |
|-----------------|-------|-------------------------|
| API General | [X] req/min | IP + User ID |
| Login/Registro | [X] req/min | IP |
| Subida de Archivos | [X] req/min | User ID |

### Manejo de Datos Sensibles

- Gestión de secretos: [.env + variables de entorno de plataforma / Secrets Manager]
- Reglas de logging: Nunca registrar contraseñas, tokens o datos personales
- Encriptación de datos: [TLS en tránsito / requisitos de encriptación en reposo]

> Lista completa de seguridad en `references/08-security-checklist.md`
```

---

## 📄 Plantilla .gitignore

```gitignore
# Variables de entorno y secretos
.env
.env.local
.env.*.local
*.pem
*.key

# Progreso de planificación de producto (puede contener información de negocio sensible)
.product-playbook-progress.md
# Marcador de handoff de desarrollo de Product-playbook (session-local; no commitear)
.product-dev-active

# IDE y OS
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# Dependencias
node_modules/
__pycache__/
*.pyc
venv/

# Output de build
dist/
build/
.next/
```

---

## 📄 Plantilla setup.sh

```bash
#!/bin/bash
# [Nombre del Producto] — Script de Inicialización del Proyecto
# Uso: chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 Inicializando [Nombre del Producto]..."

# ===== Verificar prerequisitos =====
command -v [node/python/etc] >/dev/null 2>&1 || { echo "❌ [runtime] es requerido"; exit 1; }

# ===== Instalar dependencias =====
echo "📦 Instalando dependencias..."
[npm install / pip install -r requirements.txt / etc]

# ===== Configuración del entorno =====
if [ ! -f .env ]; then
  echo "📝 Creando archivo .env..."
  cp .env.example .env
  echo "⚠️  Por favor edita .env y completa las variables de entorno requeridas"
fi

# ===== Inicialización de base de datos =====
echo "🗄️  Inicializando base de datos..."
[comandos de migración]

echo ""
echo "✅ ¡Inicialización completa!"
echo ""
echo "Siguientes pasos:"
echo "  1. Edita .env para completar las variables de entorno"
echo "  2. Inicia el servidor de desarrollo: [comando de inicio]"
echo "  3. Comienza a desarrollar: claude \"Lee CLAUDE.md y TASKS.md, luego comienza a ejecutar la Fase 1\""
```

---

## Texto de Guía al Usuario

### En Claude Chat / Cowork

Después de producir el paquete de handoff, muestra la siguiente guía:

```
📦 ¡El paquete de handoff de desarrollo está listo! Incluye los siguientes archivos:

  CLAUDE.md        → Memoria de proyecto de Claude Code (contexto de producto + especificaciones técnicas)
  TASKS.md         → Lista de tareas de desarrollo (4 Fases, [N] Tareas en total)
  TICKETS.md       → Lista de tickets ([N] tickets, listos para crear en Jira/Asana/Linear)
  docs/PRD.md      → PRD completo
  docs/ARCHITECTURE.md → Arquitectura técnica (esquema BD + API + estructura de directorios)
  docs/PRODUCT-SPEC.md → Resumen de Spec de Producto
  scripts/setup.sh → Script de inicialización en un solo comando

🔗 Cómo iniciar el desarrollo:

  1. Descarga y extrae a tu carpeta de proyecto
  2. Abre una terminal y navega a la carpeta del proyecto
  3. Lanza Claude Code:
     $ claude
  4. Dile a Claude Code que comience:
     > Lee CLAUDE.md y TASKS.md, luego comienza a ejecutar la Fase 0

💡 Consejos:
  - Claude Code lee automáticamente CLAUDE.md, así que ya conoce el contexto completo del producto
  - Después de completar cada Fase, preguntará si deseas proceder a la siguiente
  - Para ajustar el alcance de funcionalidades, simplemente edita TASKS.md directamente
  - La lista "Explícitamente No Hacer" en CLAUDE.md previene que Claude Code construya fuera del alcance
```

### Confirmación Final Pre-Output

```
Antes de producir el paquete de handoff de desarrollo, necesito confirmar algunas cosas:

1. Stack tecnológico: [Confirmado / Necesita confirmación]
2. Nombre del producto (para el nombre de la carpeta del proyecto): [Confirmado / Necesita confirmación]
3. ¿Alguna otra restricción o preferencia técnica?
   - p.ej., Debe usar un ORM específico, necesita soportar navegadores específicos, CI/CD existente, etc.
```
