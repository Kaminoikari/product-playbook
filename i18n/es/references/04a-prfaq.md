# Fase 3: Desarrollo — PR-FAQ (Working Backwards)

## 3.1 Método Working Backwards de Amazon (PR-FAQ)

Comienza escribiendo el comunicado de prensa del producto — te obliga a trabajar hacia atrás desde el resultado para el cliente:

```
## [Nombre del Producto] Comunicado de Prensa

**Titular**: [¿Qué puede lograr el usuario? Una oración.]
**Subtitular**: [¿Qué problema resuelve, y para quién?]

**Párrafo Inicial (Aha Moment)**:
[Describe el momento en que el usuario experimenta el valor central del producto — el momento "¡Wow!"]

**Descripción del Punto de Dolor**:
[¿Qué problema enfrentan los usuarios hoy? ¿Por qué las soluciones actuales no son suficientes?]

**Descripción de la Solución**:
[¿Cómo resuelve nuestro producto este problema? (Describe la experiencia — no listes funcionalidades)]

**Cita del Cliente**:
"[Una cita de un usuario objetivo que represente una reacción emocional genuina]"

**FAQ (Las Preguntas Más Difíciles)**:
P: [La pregunta más difícil de responder]
R: [Una respuesta honesta]
```

> Si no puedes escribir un comunicado de prensa que emocione a la gente, la dirección del producto puede estar equivocada — regresa y redefine el problema.

### 📝 Lista de Verificación de Calidad PR-FAQ

Claude debe marcar cada ítem ✅ o ❌ después de producir el PR-FAQ; ítems ❌ deben incluir cómo mejorar:
- [ ] ¿El titular está escrito desde la perspectiva del usuario? ("Los usuarios ahora pueden hacer X" vs. "Lanzamos la funcionalidad Y")
- [ ] ¿Un lector puede entender "por qué esto importa" en 10 segundos de leer el primer párrafo?
- [ ] ¿La descripción del punto de dolor proviene de un escenario real de usuario?
- [ ] ¿La primera oración de la sección de solución comienza con la experiencia/escenario del usuario (no un verbo de funcionalidad)?
- [ ] ¿La cita del cliente suena como algo que diría una persona real?
- [ ] ¿La FAQ incluye una comparación directa contra herramientas existentes?

**Reglas de Ejecución (Hard Gate):**
- Debe identificar al menos 1 "tensión interna" o "área que vale la pena iterar" — no puede marcar todo ✅ y darlo por terminado
- Si todos los ítems pasan, adicionalmente declarar "¿Cuál es la suposición más frágil en este PR-FAQ?"
- El estándar de calidad del PR-FAQ de Amazon viene de encontrar problemas, no de confirmar que no los hay
- ❌ Problemas comunes: el titular suena como un anuncio de producto en lugar de noticia, la sección de solución se convierte en una lista de funcionalidades, las FAQs son todas preguntas fáciles

---

### ✍️ Reglas de Escritura de la Sección de Solución (Cuerpo)

**La primera oración de la sección de solución NO DEBE comenzar con una descripción de funcionalidad.**

❌ Ejemplos prohibidos:
- "MealPrep te permite ingresar un menú con un clic y auto-calcula ingredientes"
- "El sistema genera automáticamente una lista de compras basada en el menú"
- "Haz clic en el botón 'Generar Lista' para completar tu planificación de preparación"

✅ Ejemplos correctos:
- "Ahora, el Chef López solo necesita 10 minutos el viernes por la tarde para confirmar cada detalle de la preparación del fin de semana"
- "La Gerente García ya no tiene que revisar tres hojas de Excel para saber si hay suficiente inventario"

**Fórmula**: Comienza con la experiencia del usuario / escenario específico → luego di "Esto es posible gracias a [mecanismo del producto]" para introducir la funcionalidad.

**Auto-verificación (obligatorio antes de enviar)**: lee en voz alta la primera oración de tu propio párrafo de Solución. Si el sujeto es el nombre del producto o "el sistema" / "la app" / "los usuarios pueden", **reescríbela**. El sujeto debe ser un actor específico (persona nombrada, rol, o pronombre que se refiere a un usuario) haciendo algo o experimentando un momento.

---

### 📍 Requisitos del Párrafo Inicial (Lead)

El párrafo inicial (Aha Moment) debe contener LOS TRES:

1. Un **actor nombrado o específico por rol** ("Alex", "Chef López", "el gerente de cocina de un bistró de 30 asientos") — nunca "los usuarios" de forma genérica.
2. Un **tiempo / lugar / detonante concreto** ("el viernes por la tarde", "después del ajetreo del almuerzo", "antes del fin de semana").
3. **Al menos 2 números específicos** — cantidades, duraciones, montos en dólares, porcentajes. "En 30 segundos", "para 3 escenarios de prestamistas", "$2,400/mes", "ventana de preparación de 20 minutos". Los números vagos ("unos minutos", "varias opciones") FAIL este requisito.

Un lead que tiene el actor + escenario pero sin números concretos se lee como texto publicitario — el comunicado de prensa se supone que debe hacer visible un resultado específico, no aspiracional.

---

### ❓ Estándar de Preguntas Incisivas en FAQ

**Al menos 1 FAQ debe ser: "¿Por qué no seguir usando [herramienta existente]?"**

Requisitos de formato de respuesta:
1. **Primero, reconoce las fortalezas de la herramienta existente** (no la descartes)
2. **Luego explica la brecha** (no una brecha de funcionalidades, sino una brecha fundamental de escenario)

❌ Patrón de respuesta prohibido: "Las herramientas existentes carecen de funcionalidades — la nuestra es más poderosa"
✅ Patrón de respuesta correcto:
> "Excel absolutamente puede rastrear números, y los chefs ya saben cómo usarlo. El problema es que cada fin de semana los cálculos necesitan rehacerse — re-ingresar, re-convertir — y la hora que toma no es porque alguien sea malo con las hojas de cálculo, es porque el problema realmente es así de complejo. MealPrep no te ahorra habilidades de Excel — te ahorra la carga mental de empezar desde cero cada vez."

---

### 🧪 Requisitos del FAQ Interno

Por separado del FAQ Externo (de cara al cliente), produce una sección de **FAQ Interno** con al menos:

**P: ¿Cuál es la suposición más riesgosa en este PR-FAQ? Si es falsa, ¿qué mata al producto?**
R: Nombra UNA suposición específica (no una lista). Ejemplos de respuestas bien formadas:
- "Asumimos que los gerentes de cocina confiarán en las órdenes de compra autogeneradas sin verificación manual. Si no lo hacen (porque errores de inventario pasados les costaron dinero), revisarán cada línea dos veces y nuestra propuesta de valor de 'ahorra 1 hora' colapsa a 'ahorra 5 minutos'."
- "Asumimos que las fotos de las publicaciones contienen suficiente resolución para extraer los metros cuadrados de forma confiable. Si el OCR basado en imágenes falla en más del 20% de las publicaciones, la experiencia central de 'captura y listo' se rompe."

**P: ¿Cuál es el experimento más pequeño que invalidaría esta suposición?**
R: Una prueba concreta previa al lanzamiento — entrevistar a N usuarios, hacer un smoke-test de una landing page con un objetivo de conversión X, correr un piloto interno de 2 semanas, etc. **Genérico como "rastrearemos el engagement" o "observaremos la retención" FAILS este requisito** — esos miden el éxito después del lanzamiento, no la invalidación antes del compromiso.

El FAQ Interno no es para clientes. Existe para que el equipo se obligue a nombrar qué podría matar al producto ANTES de construirlo.

---

**Ejemplo (producto ficticio — App de Calculadora de Hipotecas):**

```
## MortgageSnap Ayuda a Compradores Primerizos a Entender Lo Que Pueden Pagar en 3 Minutos

**Subtitular**: Sin visitas al banco, sin esperar cotizaciones de tasas — calcula tus pagos mensuales con tu pareja, incluso a medianoche

**Párrafo Inicial (Aha Moment)**:
Después de navegar por Zillow a altas horas de la noche, Alex ve una casa que le encanta pero no tiene
idea si realmente puede pagarla. Abre MortgageSnap, captura la pantalla de la publicación, y la app
extrae automáticamente el precio y los metros cuadrados. En 30 segundos, muestra pagos mensuales
para tres escenarios de préstamo. Comparte los resultados con su esposa, y por primera vez, están
viendo los mismos números juntos.

**Descripción del Punto de Dolor**:
Los compradores de vivienda primerizos que comparan opciones de hipoteca tienen que ingresar términos
manualmente en múltiples sitios web de bancos y esperar respuestas. Cuando quieres hacer cálculos
a altas horas de la noche, no hay herramienta conveniente — así que la gente termina armando una
hoja de Excel o simplemente se rinde.

**Descripción de la Solución**:
Ahora, Alex dedica 3 minutos en vez de 3 noches para saber qué es realmente accesible. Captura una
publicación en su teléfono, ve los pagos mensuales para tres escenarios de prestamistas aparecer en
30 segundos, y comparte una sola pantalla con su esposa — de modo que la conversación pasa de "creo
que podemos pagarlo" a "aquí están los tres números que deberíamos discutir." Esto funciona porque
MortgageSnap extrae automáticamente el precio y los metros cuadrados de la imagen de la publicación,
y luego obtiene ofertas de tasas en vivo de prestamistas asociados.

**Cita del Cliente**:
"Finalmente no tengo que esperar a que el banco me devuelva la llamada a medianoche. Tres minutos y puedo
decirle a mi esposa exactamente cuánto pagaríamos cada mes."

**FAQ**:
P: Ya hay montones de calculadoras de hipoteca — ¿qué tiene de diferente?
R: Las calculadoras existentes requieren que ingreses tasas de interés, plazos de préstamo y otros
parámetros, pero la mayoría de los compradores primerizos ni siquiera conocen esos números.
La diferencia de MortgageSnap es que obtiene automáticamente ofertas reales de varios prestamistas —
todo lo que necesitas proporcionar es el precio y tu enganche.
```