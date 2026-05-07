# Handoff de Desarrollo — TASKS.md + TICKETS.md

## 📄 Plantilla TASKS.md

Principios fundamentales para desglose de funcionalidades:
- Comienza desde los imprescindibles del MVP (funcionalidades P0)
- Cada Tarea mapea a una User Story
- Las Fases tienen dependencias claras: Fase N+1 depende de outputs de Fase N
- Cada Tarea incluye criterios de aceptación que Claude Code puede auto-verificar

```markdown
# [Nombre del Producto] — Lista de Tareas de Desarrollo

## Fase 0: Inicialización del Proyecto
> Meta: Establecer un esqueleto de proyecto en blanco ejecutable

- [ ] **T0.1** Inicializar proyecto (`scripts/setup.sh` o manual)
  - Aceptación:
    - [ ] `npm run dev` / `python manage.py runserver` o comando equivalente inicia exitosamente
    - [ ] `.gitignore` creado, incluye `.env`, `.env.local`, `node_modules/`, `.product-playbook-progress.md`, `.product-dev-active`, y otros archivos sensibles
    - [ ] `.env.example` creado (solo nombres de claves, sin valores reales)
- [ ] **T0.2** Configurar linter + formatter
  - Aceptación: lint pasa sin errores
- [ ] **T0.3** Configurar base de datos + ejecutar migración inicial
  - Aceptación: Base de datos es conectable, tablas base están creadas
- [ ] **T0.4** Configurar estructura de rutas base
  - Aceptación: Todas las rutas principales de páginas son accesibles (retornar páginas en blanco está bien)

## Fase 1: Flujo Central (Ruta del Aha Moment)
> Meta: Permitir que los usuarios completen la ruta más corta desde la entrada hasta el Aha Moment
> Corresponde a User Stories: [US-001, US-002, ...]

- [ ] **T1.1** [Nombre de funcionalidad]
  - User Story: Como [Persona], quiero [acción], para poder [valor]
  - Criterios de Aceptación:
    - [ ] [Condición específica comprobable 1]
    - [ ] [Condición específica comprobable 2]
  - Notas Técnicas: [APIs requeridas / servicios de terceros / lógica especial]

- [ ] **T1.2** [Nombre de funcionalidad]
  - User Story: ...
  - Criterios de Aceptación: ...

> **Checkpoint de Finalización Fase 1**: El usuario puede completar [acción del Aha Moment]. Si no, no proceder a Fase 2.

## Fase 2: Completar el MVP
> Meta: Llenar todas las funcionalidades P0 restantes no cubiertas en Fase 1
> Corresponde a User Stories: [US-003, US-004, ...]

- [ ] **T2.1** [Nombre de funcionalidad]
  - ...

> **Checkpoint de Finalización Fase 2**: Todos los criterios de aceptación de User Stories P0 pasan.

## Fase 3: Calidad y Experiencia
> Meta: Manejo de errores, casos límite, estados de carga, seguridad básica

- [ ] **T3.1** Manejo global de errores
- [ ] **T3.2** Validación de formularios + casos límite
- [ ] **T3.3** Estados de carga + estados vacíos
- [ ] **T3.4** Verificación de seguridad (verificar cada ítem según `references/08-security-checklist.md`)
  - Aceptación:
    - [ ] Ítems relacionados con OWASP Top 10 atendidos (validación de input, autenticación, protección XSS, protección CSRF)
    - [ ] Cabeceras de seguridad configuradas (CSP, X-Frame-Options, HSTS, etc.)
    - [ ] Política CORS configurada (sin wildcard *)
    - [ ] Endpoints API sensibles tienen rate limiting
    - [ ] Respuestas de error API no filtran información interna
- [ ] **T3.5** Diseño responsive (si es Web)

## Fase 4: Despliegue
> Meta: Hacer la app accesible para usuarios externos

- [ ] **T4.1** Gestión de variables de entorno
- [ ] **T4.2** Configuración de despliegue
- [ ] **T4.3** Monitoreo básico + logging
```

---

## 📄 Plantilla TICKETS.md

TICKETS.md toma el desglose de funcionalidades de TASKS.md y produce contenido estructurado que puede usarse directamente para crear tickets en herramientas de gestión de proyectos. Cada ticket contiene toda la información que un PM necesita.

> **Meta de diseño**: Los PMs pueden copiar el contenido de cada ticket directamente a Jira / Asana / Linear u otras herramientas para crear tickets. Versiones futuras soportarán creación automática de tickets vía API.

```markdown
# [Nombre del Producto] — Lista de Tickets

> Generado: [timestamp]
> Corresponde a versión de TASKS.md: [versión/timestamp]
> Total: [N] tickets

---

## Resumen de Tickets

| # Ticket | Título | Fase | Prioridad | Horas Estimadas | Dependencias |
|----------|--------|------|----------|----------------|-------------|
| TKT-001 | [Título] | Fase 0 | P0 | [X]h | — |
| TKT-002 | [Título] | Fase 1 | P0 | [X]h | TKT-001 |
| ... | | | | | |

---

## TKT-001: [Título]

**Fase**: Fase 0 — Inicialización del Proyecto
**Tarea Correspondiente**: T0.1
**Prioridad**: P0
**Horas Estimadas**: [X] horas
**Dependencias**: Ninguna
**Asignado a**: [Rol/equipo, p.ej., Ingeniero Backend]

### Descripción

[1-3 párrafos describiendo lo que este ticket logra, incluyendo contexto de negocio y metas técnicas]

### User Story

Como [Persona], quiero [acción], para poder [valor]

### Criterios de Aceptación

- [ ] [Condición específica comprobable 1]
- [ ] [Condición específica comprobable 2]
- [ ] [Condición específica comprobable 3]

### Notas Técnicas

- [Consideraciones de implementación]
- [APIs requeridas / servicios de terceros]
- [Rutas de archivos o módulos relacionados]

### Etiquetas Sugeridas

`[Fase 0]` `[backend]` `[setup]`

---

## TKT-002: [Título]

[Mismo formato, expandido para cada ticket]
```

### Reglas de Ticketing

1. **Mapeo ticket-a-tarea**: Cada Tarea en TASKS.md mapea a un ticket (TKT-001 ↔ T0.1); Tareas demasiado grandes pueden dividirse en múltiples tickets
2. **Herencia de prioridad**: Fases 0-1 por defecto P0, Fase 2 por defecto P1, Fases 3-4 por defecto P2 — ajustable según puntuaciones RICE
3. **Dependencias**: Marcar explícitamente dependencias ticket-a-ticket para prevenir que los ingenieros salten pasos
4. **Horas estimadas**: Basado en el principio de granularidad de Tareas (1-4 horas), proporcionar estimaciones razonables
5. **Etiquetas sugeridas**: Incluir Fase, dominio técnico (frontend / backend / base de datos / infraestructura), módulo de funcionalidad

### Integración con Herramientas de Gestión de Proyectos (Reservado)

> Lo siguiente es un diseño de interfaz reservado para ticketing automático futuro. La versión actual solo produce TICKETS.md para creación manual de tickets por el PM.

El formato estructurado de TICKETS.md reserva los siguientes campos para importación futura por API:

| Campo | Mapeo Jira | Mapeo Asana | Mapeo Linear |
|-------|-----------|------------|-------------|
| # Ticket | Issue Key | Task ID | Issue ID |
| Título | Summary | Task Name | Title |
| Descripción | Description | Description | Description |
| Prioridad | Priority | Custom Field | Priority |
| Horas Estimadas | Story Points / Time Estimate | Custom Field | Estimate |
| Dependencias | Linked Issues | Dependencies | Relations |
| Etiquetas | Labels + Components | Tags | Labels |
| Fase | Epic | Section | Project |
| Asignado a | Assignee | Assignee | Assignee |
| Criterios de Aceptación | Acceptance Criteria (Description) | Subtasks | Sub-issues |

---

## Lógica de Desglose de Funcionalidades

Reglas para convertir funcionalidades MVP en Tareas:

### Principios de División de Fases

```
Fase 0: Esqueleto del proyecto (requerido para todos los modos)
  → Inicialización, linter, BD, rutas base

Fase 1: Ruta más corta al Aha Moment (más importante)
  → Funcionalidades mínimas necesarias desde la entrada del usuario hasta el Aha Moment
  → Solo incluye funcionalidades P0 en esta ruta

Fase 2: Completar el MVP
  → Llenar funcionalidades P0 restantes no cubiertas en Fase 1
  → Flujos secundarios, páginas de soporte

Fase 3: Calidad y Experiencia
  → Manejo de errores, casos límite, estados de carga/vacíos
  → Seguridad básica, diseño responsive

Fase 4: Despliegue
  → Variables de entorno, configuración de despliegue, monitoreo
```

### Principio de Granularidad de Tareas

- Cada Tarea debería completarse en **1-4 horas**
- Demasiado grande → Dividir en sub-Tareas (T1.1a, T1.1b)
- Demasiado pequeña → Fusionar con una Tarea relacionada
- Cada Tarea debe tener al menos un criterio de aceptación comprobable

### Mapeo User Story → Tarea

```
Una sola User Story puede mapear a 1-3 Tareas:
  US-001: Como nuevo usuario, quiero registrar una cuenta, para poder comenzar a usar el producto
    → T1.1: UI de página de registro
    → T1.2: API de registro + validación de datos
    → T1.3: Flujo de verificación de email (si es necesario para MVP)
```
