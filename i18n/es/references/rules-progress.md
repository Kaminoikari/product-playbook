# 🔁 Persistencia de Progreso y Recuperación de Interrupciones

> Se carga cuando el usuario dice "pausar," "guardar," o cuando el skill verifica progreso al inicio.

## Formato del Archivo de Progreso

Después de completar cada paso, crear o actualizar `.product-playbook-progress.md` en el directorio del proyecto:

```
# Guardado de Progreso de Product Playbook

- Modo: [Modo Rápido / Modo Completo / ...]
- Tipo de producto: [B2C / B2B / ...]
- Descripción del producto: [Descripción del producto del usuario]
- Progreso actual: S[X] / S[Y]
- Última actualización: [timestamp]

## Pasos Completados

### S1: [Nombre del paso] ✅
[Output central de este paso — retener suficiente detalle para no necesitar rehacerlo al recuperar]

### S2: [Nombre del paso] ✅
[Igual que arriba]

## Pasos Pendientes
- S3: [Nombre del paso]
- S4: [Nombre del paso]
- ...
```

### Ejemplo de Modo Extensión de Funcionalidad
```markdown
Modo: Extensión de Funcionalidad
Paso: S2/S4
S1: Problema + contexto del sistema existente ✅
S2: Tres soluciones paralelas + recomendación de IA ▶️
S3: Evaluación de riesgos ⬜
S4: Alcance de ejecución ⬜
```

## Reglas de Activación

1. **Auto-guardado**: Después de completar cada paso y ser confirmado por el usuario, actualizar inmediatamente el archivo de progreso
2. **Verificar al inicio**: Cuando el skill se activa, primero verificar si `.product-playbook-progress.md` existe. Si existe, mostrar:
```
Progreso no terminado de planificación de producto detectado ([nombre del modo], S[X]/S[Y]):
  1️⃣ Continuar — Retomar desde S[X]
  2️⃣ Empezar de nuevo — Limpiar progreso anterior y comenzar desde cero
(Ingresa 1 o 2)
```
3. **Comando de pausa**: Cuando el usuario dice "pausar," "hacer otra cosa primero," o "guardar," confirmar que el archivo de progreso ha sido actualizado y responder: "Progreso guardado en .product-playbook-progress.md (S[X]/S[Y]). Será detectado automáticamente la próxima vez que inicies el skill en este proyecto."
4. **Limpieza al completar**: Después de que todo el flujo esté completo y los documentos finales producidos, preguntar al usuario si desea eliminar el archivo de progreso
6. **Recordatorio de control de versiones**: Cuando `.product-playbook-progress.md` se crea por primera vez, recordar al usuario: "⚠️ Recomendamos agregar `.product-playbook-progress.md` a `.gitignore` — este archivo puede contener información sensible de estrategia de producto."
5. **Guardado de interrupción**: Cuando se detecta un prompt no relacionado durante el flujo (ver reglas de manejo de interrupciones en SKILL.md), guardar progreso incluso si el paso actual no está completo. Usar 🔶 (en progreso) en lugar de ✅ para el paso actual en el formato de guardado, y preservar el contenido parcialmente producido:
```
### S[X]: [Nombre del paso] 🔶 (en progreso, parcialmente completado)
[Contenido parcialmente producido]
⚠️ Este paso no está completo — retomar desde aquí al recuperar
```
