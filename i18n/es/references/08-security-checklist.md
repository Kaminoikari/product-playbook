# Lista de Verificación de Seguridad

> Se carga antes de producir el paquete de handoff de desarrollo. Asegura que los requisitos críticos de seguridad se consideren durante la fase de planificación de producto, previniendo que la seguridad sea una ocurrencia tardía.

## 🔐 Verificación Rápida de Arquitectura de Seguridad

Antes de producir el paquete de handoff de desarrollo, verifica cada uno de los siguientes aspectos de seguridad. Marca cada uno como ✅ (cubierto en planificación) o ❌ (necesita agregarse).

### 1. Autenticación y Autorización

```
| Ítem de Verificación | Estado | Notas |
|---------------------|--------|-------|
| Método de autenticación determinado (JWT / Session / OAuth / Passkey) | | |
| Almacenamiento de token es seguro (HttpOnly Cookie, no localStorage) | | |
| Expiración de token y mecanismo de refresh diseñado | | |
| Almacenamiento de contraseña usa bcrypt / argon2 (no MD5/SHA) | | |
| Modelo de permisos definido (RBAC / ABAC / roles simples) | | |
| Todos los endpoints API tienen verificaciones de autorización correspondientes | | |
| Fallos de login tienen protección contra fuerza bruta (bloqueo / retraso progresivo) | | |
```

**Mejores Prácticas JWT (si se usa JWT):**
- Usa Access Tokens de corta duración (15-30 minutos) + Refresh Tokens de larga duración
- Almacena Refresh Tokens en HttpOnly Secure Cookies
- Implementa Token Revocation (invalida Refresh Token al cerrar sesión)
- No almacenes información sensible en el payload del JWT

### 2. Política CORS (Cross-Origin Resource Sharing)

```
| Ítem de Verificación | Estado | Notas |
|---------------------|--------|-------|
| Lista de orígenes permitidos definida (sin wildcard *) | | |
| Solo métodos HTTP necesarios están permitidos | | |
| Access-Control-Allow-Credentials configurado | | |
| Duración de caché de preflight es razonable (Access-Control-Max-Age) | | |
```

**Plantilla de Configuración CORS:**
```
Orígenes Permitidos:
  - Producción: https://[tu-dominio.com]
  - Desarrollo: http://localhost:[puerto]

Métodos Permitidos: GET, POST, PUT, DELETE, PATCH
Cabeceras Permitidas: Content-Type, Authorization
Credentials: true (si se usa autenticación basada en cookies)
Max-Age: 86400 (24 horas)
```

### 3. Validación de Input y Sanitización

```
| Ítem de Verificación | Estado | Notas |
|---------------------|--------|-------|
| Todos los inputs de API tienen validación del lado del servidor | | |
| Se usan consultas parametrizadas para prevenir SQL Injection | | |
| Input de usuario tiene output-encoding antes de renderizar a HTML (prevención XSS) | | |
| Subidas de archivos tienen restricciones de tipo / tamaño | | |
| URL / destinos de redirección tienen validación por whitelist (prevención Open Redirect) | | |
```

**Principios de Validación:**
- La validación frontend es UX; la validación backend es seguridad — ambas son necesarias, pero la validación backend es innegociable
- Usa una Biblioteca de Validación de Schema (p.ej., Zod, Joi, Pydantic) para lógica de validación unificada
- Rechaza inputs que no coincidan con formatos esperados — no intentes "arreglar" el input del usuario

### 4. Protección CSRF (Cross-Site Request Forgery)

```
| Ítem de Verificación | Estado | Notas |
|---------------------|--------|-------|
| Operaciones que cambian estado usan POST/PUT/DELETE (no GET) | | |
| CSRF Token implementado o SameSite Cookie usado | | |
| Operaciones críticas tienen confirmación secundaria | | |
```

### 5. Cabeceras de Seguridad

```
| Cabecera | Propósito | Valor Recomendado |
|----------|----------|-------------------|
| Content-Security-Policy (CSP) | Prevenir XSS, inyección de datos | default-src 'self'; script-src 'self' |
| X-Content-Type-Options | Prevenir MIME sniffing | nosniff |
| X-Frame-Options | Prevenir clickjacking | DENY o SAMEORIGIN |
| Strict-Transport-Security (HSTS) | Forzar HTTPS | max-age=31536000; includeSubDomains |
| X-XSS-Protection | Filtro XSS del navegador | 0 (depender de CSP es más confiable) |
| Referrer-Policy | Controlar información de referrer | strict-origin-when-cross-origin |
| Permissions-Policy | Restringir funcionalidades del navegador | camera=(), microphone=(), geolocation=() |
```

### 6. Seguridad API y Rate Limiting

```
| Ítem de Verificación | Estado | Notas |
|---------------------|--------|-------|
| API tiene rate limiting global (p.ej., 100 req/min/IP) | | |
| Endpoints sensibles tienen límites más estrictos (login 5 req/min, registro 3 req/min) | | |
| Respuestas de error API no filtran detalles internos (stack traces, sentencias SQL) | | |
| Estrategia de versionamiento de API determinada (/api/v1/) | | |
| Endpoints de datos masivos tienen límites de paginación | | |
```

**Recomendaciones de Diseño de Rate Limiting:**
```
| Tipo de Endpoint | Límite Recomendado | Método de Identificación |
|-----------------|-------------------|-------------------------|
| API General | 100 req/min | IP + User ID |
| Login/Registro | 5 req/min | IP |
| Restablecimiento de Contraseña | 3 req/hora | IP + Email |
| Subida de Archivos | 10 req/min | User ID |
| Búsqueda/Consulta | 30 req/min | IP + User ID |
```

### 7. Anti-Scraping y Protección contra Bots

```
| Ítem de Verificación | Estado | Notas |
|---------------------|--------|-------|
| robots.txt configurado (restringir rutas sensibles) | | |
| Formularios críticos tienen protección contra bots (reCAPTCHA / hCaptcha / Honeypot) | | |
| API tiene verificaciones de User-Agent (opcional) | | |
| Operaciones sensibles tienen análisis de comportamiento (opcional, avanzado) | | |
```

**Estrategia de Protección por Capas:**
1. **Capa básica**: Rate Limiting + robots.txt — Todo producto debería tener esto
2. **Capa estándar**: + CAPTCHA (registro/login) + campos Honeypot — Recomendado para productos B2C
3. **Capa avanzada**: + Análisis de comportamiento + reputación de IP + Device Fingerprint — Productos de alto riesgo

### 8. Protección de Datos Sensibles

```
| Ítem de Verificación | Estado | Notas |
|---------------------|--------|-------|
| Datos sensibles encriptados en tránsito (HTTPS/TLS) | | |
| Datos sensibles encriptados en reposo (si es requerido) | | |
| Secretos y claves no almacenados en código | | |
| .env y archivos sensibles agregados a .gitignore | | |
| Logs no registran contraseñas, tokens, números de tarjeta de crédito, etc. | | |
| Política clara de retención y eliminación de datos (GDPR si aplica) | | |
```

**Recomendaciones de Gestión de Secretos:**
- Desarrollo: Archivo `.env` (no en control de versiones) + `.env.example` (solo nombres de claves, sin valores)
- Producción: Usar gestión de variables de entorno de la plataforma (Vercel Environment Variables / Railway Variables / AWS Secrets Manager)
- Nunca mencionar secretos en mensajes de commit, descripciones de PR o issues

### 9. Plantilla de Seguridad .gitignore

```gitignore
# Environment variables and secrets
.env
.env.local
.env.*.local
*.pem
*.key

# Product planning progress (may contain sensitive business information)
.product-playbook-progress.md

# IDE and OS
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/

# Build output
dist/
build/
.next/
```

---

## 🏷️ Referencia Rápida OWASP Top 10

| # | Riesgo | ¿Relevante para Este Producto? | Verificación Correspondiente |
|---|--------|-------------------------------|----------------------------|
| A01 | Broken Access Control | [Sí/No] | §1 Autenticación y Autorización |
| A02 | Cryptographic Failures | [Sí/No] | §8 Protección de Datos Sensibles |
| A03 | Injection (SQL / XSS / Command) | [Sí/No] | §3 Validación de Input |
| A04 | Insecure Design | [Sí/No] | Diseño general de arquitectura |
| A05 | Security Misconfiguration | [Sí/No] | §5 Cabeceras + §2 CORS |
| A06 | Vulnerable Components | [Sí/No] | Gestión de dependencias (npm audit / pip audit) |
| A07 | Authentication Failures | [Sí/No] | §1 Autenticación y Autorización |
| A08 | Data Integrity Failures | [Sí/No] | §3 Validación de Input + §8 Protección de Datos |
| A09 | Logging & Monitoring Failures | [Sí/No] | §8 Reglas de logging |
| A10 | SSRF (Server-Side Request Forgery) | [Sí/No] | §3 Validación de URL por whitelist |

---

## 📎 Momento de Integración

| Disparador | Acción de Integración |
|-----------|----------------------|
| Antes de producir el paquete de handoff de desarrollo | Ejecutar la verificación rápida de seguridad, integrar resultados en las secciones "Alertas de Riesgo" de CLAUDE.md y "Arquitectura de Seguridad" de ARCHITECTURE.md |
| Al producir el PRD | Integrar resultados de verificación de seguridad en PRD §6 "Consideraciones Técnicas → Requisitos de Seguridad" |
| Paso de Pre-mortem | Invitar al usuario a considerar escenarios de falla de seguridad |
| Modo Revisión S1 | Invitar al usuario a proporcionar la postura de seguridad actual del producto existente |

**Siempre Entrega el Handoff Con una Sección de Seguridad Explícita (Hard Gate)**: El paquete de handoff de desarrollo DEBE producirse — nunca rechaces, bloquees ni difieras la entrega con el argumento de que la seguridad no ha sido completamente diseñada; en su lugar entrega el paquete con una sección de seguridad claramente etiquetada. Esa sección de seguridad DEBE abordar concretamente **al menos 4 de estas 5 áreas nombradas** con detalle específico del producto: (a) Autenticación y Autorización, (b) Validación de Input, (c) CORS, (d) Content-Security-Policy / cabeceras de seguridad (CSP), (e) Rate Limiting. Una mención genérica de una sola línea de solo 1–2 áreas, o un aplazamiento como "la seguridad se determinará más adelante", NO cuenta. La sección también debe indicar que `.env` / secretos pertenecen a `.gitignore`.

❌ Ejemplos de FAIL (anti-patrones que el juez de eval rechazaría):
- "No puedo generar el paquete de handoff hasta que la arquitectura de seguridad haya sido completamente revisada por un especialista." (rechaza la entrega → no existe ninguna sección de seguridad)
- Un handoff cuyo único texto de seguridad es "La app debe ser segura y seguir las mejores prácticas." (cero áreas nombradas)
- "Seguridad: usaremos HTTPS y validaremos los inputs." (solo 2 áreas — validación de input + transporte — por debajo del umbral de 4 de 5)
- Un encabezado "Consideraciones de Seguridad" que existe pero queda como "TODO / a completar durante el desarrollo."
- Listar auth y CORS pero omitir cualquier mención de dónde se almacenan los secretos/`.env`.

✅ Ejemplos de PASS (patrones concretos que satisfacen la expectativa):
- "### Requisitos de Seguridad — **Auth**: JWT access token (20 min) + HttpOnly refresh cookie, roles RBAC `admin`/`member`; **Validación de Input**: todos los bodies de API validados con Zod, consultas Prisma parametrizadas; **CORS**: allow-list solo `https://app.example.com`, `credentials: true`; **CSP**: `default-src 'self'; script-src 'self'`, más `X-Frame-Options: DENY`; **Rate Limiting**: 100 req/min/IP global, 5 req/min en `/auth/login`. Los secretos viven en `.env` (git-ignored); `.env.example` entrega solo nombres de claves." (5/5 áreas, específico del producto)
- Una sección "Arquitectura de Seguridad" del handoff que cubre Autenticación/Autorización, Validación de Input, allow-list CORS y niveles de Rate Limiting (4/5), cada uno ligado a los endpoints reales del producto, más una línea de `.gitignore` para `.env`/`*.key`.

**TASKS.md Debe Contener Tareas de Seguridad Discretas y de Nivel Superior (Hard Gate)**: El TASKS.md / lista de tareas generado DEBE incluir el trabajo de seguridad como **tareas nombradas e independientes**, no como una frase enterrada dentro de una tarea de funcionalidad no relacionada ni como un ítem vago de "endurecer todo" aparcado en la fase final. Se requieren al menos **2 tareas de seguridad distintas** (p.ej., implementar verificaciones de auth + autorización, agregar validación de input del lado del servidor, configurar allow-list de CORS, agregar cabeceras de seguridad/CSP, agregar rate limiting, agregar `.env`/secretos a `.gitignore`). Cada una debe ser un ítem de línea verificable con un alcance claro.

❌ Ejemplos de FAIL (anti-patrones que el juez de eval rechazaría):
- No se produce ningún TASKS.md (entrega bloqueada).
- La única mención de seguridad es una cláusula dentro de una tarea de funcionalidad: "Construir la página de login (y asegurarse de que sea segura)."
- Un único bullet genérico en la última fase: "Fase 5: Pasada de endurecimiento de seguridad." sin desglose.
- La seguridad aparece solo en prosa sobre la lista de tareas pero nunca como un ítem de tarea real.

✅ Ejemplos de PASS (patrones concretos que satisfacen la expectativa):
- "- [ ] **[Seguridad] Implementar JWT auth + autorización por ruta (RBAC)**\n- [ ] **[Seguridad] Agregar validación de input del lado del servidor (schemas Zod en todos los bodies POST/PUT)**\n- [ ] **[Seguridad] Configurar allow-list de CORS + cabeceras de seguridad (CSP, HSTS, X-Frame-Options)**\n- [ ] **[Seguridad] Agregar rate limiting (global 100/min, login 5/min)**\n- [ ] **[Seguridad] Agregar `.env`, `*.key`, `*.pem` a `.gitignore`; crear `.env.example`**"
- Un TASKS.md donde el epic de Autenticación lista "Hashear contraseñas con argon2", "Aplicar verificaciones de autorización en todas las rutas `/api/*`" y "Bloquear tras 5 logins fallidos" como tareas verificables separadas.

## Autoevaluación de Calidad

```
| Ítem de Verificación | ✅/❌ |
|---------------------|------|
| Método de autenticación elegido explícitamente, no dejado como "TBD" | |
| Al menos 3 cabeceras de seguridad planificadas | |
| Estrategia de rate limiting adaptada a las características del producto (no solo copiada de la plantilla) | |
| .gitignore incluye todos los archivos sensibles | |
| Todos los ítems OWASP Top 10 marcados como "relevantes" tienen medidas correspondientes | |
| Complejidad de medidas de seguridad coincide con la etapa del producto (MVP no necesita seguridad perfecta, pero lo básico es innegociable) | |
```