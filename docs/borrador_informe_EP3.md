# Borrador de informe técnico — EVA3

**Proyecto:** Observabilidad del agente de IA  
**Asignatura:** Ingeniería de Soluciones con IA  
**Integrantes:** [Completar]  
**Fecha:** [Completar]

> Borrador de trabajo separado de la EVA2. El agente existente se toma como sistema bajo observación; sus archivos originales no se modifican. Los resultados, gráficos y recomendaciones deben completarse después de instrumentar y ejecutar las mediciones. La conclusión, las justificaciones técnicas y las reflexiones individuales deben ser redactadas por el equipo, según la pauta.

## 1. Objetivo

Esta evaluación busca observar el comportamiento del agente de IA mediante métricas, registros de ejecución y un dashboard. El análisis considerará la corrección de sus respuestas, la consistencia de resultados, la latencia, los errores y, cuando esté disponible, el consumo de recursos.

## 2. Sistema observado

El sistema bajo observación es un agente conversacional desarrollado previamente. Recibe solicitudes mediante una API, utiliza Gemini como modelo de lenguaje y LangGraph para coordinar la respuesta y las herramientas. Entre sus operaciones se encuentran la consulta de resúmenes mensuales, la gestión de borradores internos y la búsqueda o almacenamiento de notas asociadas a una empresa. Mantiene conversaciones y notas en almacenamiento persistente.

En el estado inicial revisado para esta evaluación, existe registro de errores de la API, pero todavía no hay un conjunto integrado de métricas de desempeño ni un dashboard que resuma las ejecuciones. Esta línea base se deberá confirmar al iniciar las pruebas de EVA3.

## 3. Plan de observabilidad

Se propone ejecutar un conjunto controlado de consultas con resultados esperados y registrar, para cada ejecución, un identificador técnico, hora, tipo de operación, herramienta utilizada, duración, resultado de éxito o error y consumo de tokens cuando el proveedor lo entregue. Los registros no deben incluir claves, texto privado de las conversaciones ni contenido de notas.

### Métricas propuestas

| Métrica | Cálculo o criterio | Resultado |
|---|---|---|
| Precisión de consultas | Casos con resultado correcto / total de casos evaluados | [Completar con mediciones] |
| Consistencia | Repeticiones equivalentes que mantienen el resultado esperado / total de repeticiones | [Completar con mediciones] |
| Latencia | Tiempo entre recepción de solicitud y respuesta; reportar mediana y percentil 95 | [Completar con mediciones] |
| Frecuencia de errores | Ejecuciones fallidas / ejecuciones totales, agrupadas por tipo | [Completar con mediciones] |
| Uso de recursos | Tokens de entrada/salida informados por el modelo; CPU/memoria si se instrumentan | [Completar con mediciones] |

La precisión debe evaluarse con consultas que tengan resultados de referencia. La consistencia debe medir si las respuestas conservan los datos y conclusiones esperados; no requiere que la redacción sea idéntica.

## 4. Diseño de pruebas y trazabilidad

El equipo definirá un conjunto de casos que cubra consultas mensuales válidas, períodos inválidos o ausentes, uso de herramientas, recuperación de notas y aislamiento entre empresas. Para cada caso se documentarán la entrada de prueba, el resultado esperado y el resultado observado.

Los eventos se relacionarán mediante un identificador de ejecución. La traza registrará las etapas principales —recepción, llamada al modelo, uso de herramienta y respuesta— junto con su duración y estado. Si ocurre un error, se registrará su categoría sin guardar contenido sensible.

**Casos ejecutados:** [Completar tabla con caso, resultado esperado, resultado observado, duración y estado].

## 5. Dashboard

El dashboard presentará al menos:

- Porcentaje de consultas correctas.
- Latencia mediana y percentil 95.
- Cantidad y frecuencia de errores por categoría.
- Comparación de resultados entre tipos de consulta o escenarios.
- Consumo de tokens o recursos, si esos datos están disponibles.

**Herramienta elegida:** [Completar].  
**Capturas y gráficos:** [Agregar evidencias del dashboard].

## 6. Hallazgos observados

Esta sección se completará después de ejecutar las pruebas y revisar el dashboard. Cada hallazgo deberá indicar la métrica observada, el escenario, el tamaño de la muestra y la evidencia que lo respalda.

1. [Hallazgo sustentado por datos]
2. [Hallazgo sustentado por datos]
3. [Hallazgo sustentado por datos]

## 7. Recomendaciones

Las recomendaciones se definirán a partir de los hallazgos medidos. Para cada una, el equipo describirá el problema observado, la evidencia, el cambio propuesto y el efecto que espera verificar en una nueva medición.

| Hallazgo y evidencia | Recomendación del equipo | Métrica para verificar el cambio |
|---|---|---|
| [Completar] | [Completar por el equipo] | [Completar] |

## 8. Privacidad y uso responsable

La instrumentación deberá registrar solo los datos necesarios para analizar el funcionamiento. Se excluirán claves de acceso, contenido de notas y texto completo de conversaciones. Las capturas del dashboard deberán ocultar identificadores o datos que permitan reconocer a personas o empresas. El acceso, la retención y la eliminación de los registros deberán definirse para la demostración.

**Medidas implementadas y evidencia:** [Completar luego de la instrumentación].

## 9. Conclusiones y reflexiones

[Redactar por el equipo. La pauta solicita que las conclusiones y reflexiones individuales sean elaboradas sin apoyo de IA.]

## Referencias

[Agregar referencias utilizadas en formato APA, incluidas la documentación técnica consultada y la declaración de uso de IA requerida por la pauta.]
