# Alcancía 3000 — Prototipo funcional en Python

Aplicación de escritorio educativa para estudiantes salvadoreños. Conserva el concepto del manual original: registrar ingresos y gastos en USD, ahorrar mediante metas, visualizar estadísticas, desbloquear logros y funcionar sin Internet.

> **Alcance:** prototipo de escritorio Python/Tkinter, no APK ni app móvil .NET MAUI. Las funciones indicadas a continuación fueron programadas, pero las pruebas incluidas no sustituyen las pruebas manuales en la computadora de entrega.

## Cómo ejecutar (Windows)

1. Instala **Python 3.10 o superior** desde python.org; durante la instalación marca **Add Python to PATH**.
2. Extrae la carpeta ZIP completa.
3. Haz doble clic en **INICIAR.bat**. También puedes abrir la terminal dentro de la carpeta y ejecutar `python app.py`.
4. Se abre una ventana con el menú lateral. No requiere XAMPP, MySQL, ni acceso a Internet.
5. Tus datos se guardan en `C:\Users\TU_USUARIO\.alcancia3000\alcancia.db` (no dentro de la carpeta ZIP).

Para ejecutar las pruebas automáticas: `python -m unittest discover -s tests -v`.

## Estructura física del código

```text
Alcancia3000_Python/
├── app.py                # Ventanas y componentes de la interfaz Tkinter
├── logic.py              # Validaciones, cálculos, metas, logros, exportación
├── database.py           # Tablas y consultas en SQLite
├── tests/
│   └── test_logic.py     # Casos de prueba automatizados
├── requirements.txt      # No se necesitan paquetes extra
├── INICIAR.bat           # Iniciar en Windows
└── README.md             # Documentación y manual de uso
```

## Diseño lógico (arquitectura)

```text
ESTUDIANTE
   ↓ clic en botones / completa formularios
app.py — Interfaz (Inicio, Movimientos, Metas, Estadísticas, Logros)
   ↓ pide operaciones, NO hace consultas SQL directamente
logic.py — Reglas de negocio / validaciones
   ↓ pide guardar o leer información
 database.py — SQLite local
   ↓
alcancia.db — categories, movements, goals, contributions
```

**Relaciones de datos:** `categories (1) ── (N) movements`; `goals (1) ── (N) contributions`.

Los valores monetarios se guardan como **centavos enteros**, para evitar errores con decimales. `movements.kind` admite `ingreso` o `gasto`. Un movimiento corresponde a una categoría del mismo tipo.

## 70 % o más del funcionamiento previsto

| Requisito del manual | Implementación |
|---|---|
| RF-01 Registrar ingresos | ✅ |
| RF-02 Registrar gastos | ✅ |
| RF-03 Listar, editar y eliminar movimientos | ✅ |
| RF-04 Categorizar gastos | ✅ categorías predefinidas y gráfico por categoría |
| RF-05 Calcular ingresos, gastos y saldo | ✅ |
| RF-06 Crear y gestionar metas | ✅ crear, aportar, eliminar |
| RF-07 Gráficas mensuales | ✅ barras de gastos por categoría |
| RF-08 Logros | ✅ 5 distintivos calculados automáticamente |
| RF-09 Rachas | ✅ días consecutivos con registros |
| RF-10 Retos | 🟡 un reto semanal de constancia; no editor de retos |
| RF-11 Persistencia local | ✅ SQLite |
| RF-12 Trabajo sin Internet | ✅ |
| RF-13 Formularios validados | ✅ fechas, montos, categorías y disponibilidad |
| RF-14 Progreso de ahorro | ✅ barra y porcentaje |

**Alcance pendiente:** aplicación móvil Android, configurador de categorías, retos configurables, respaldos automáticos, perfiles y autenticación. Se considera un **prototipo funcional**, no un producto móvil terminado.

## Lógica financiera importante

- **Saldo** = ingresos − gastos.
- **Disponible** = ingresos − gastos − dinero reservado en metas.
- **Aportar a una meta** reserva dinero disponible y no lo registra como gasto. Así se evita contar el mismo dinero dos veces.
- No se puede registrar un gasto o aportar a una meta si no alcanza el saldo disponible.
- Al eliminar una meta, sus aportes se liberan; al eliminar un ingreso, se valida que el dinero reservado y los gastos no queden sin respaldo.
- **Progreso** = ahorrado / objetivo × 100.
- **Racha** = días seguidos con al menos un movimiento; cuenta desde hoy, o desde ayer si todavía no registraste nada hoy.
- Las insignias se calculan en tiempo real desde los datos, así evitan duplicados.

## Manual breve de usuario

**Primer uso:** abre la aplicación; comienza registrando un ingreso en **Inicio > Registrar ingreso**, por ejemplo Mesada, $20.00, fecha de hoy y descripción “Dinero semanal”.

**Agregar gasto:** selecciona **Movimientos > Gasto**; completa monto, descripción, fecha y categoría. El sistema resta el importe del disponible.

**Editar o eliminar:** entra a **Movimientos**, haz clic sobre una fila y utiliza **Editar selección** o **Eliminar selección**.

**Ahorrar:** entra a **Metas > Nueva meta**, indica nombre y objetivo (por ejemplo, “Audífonos”, $30.00). Después haz clic en **Aportar**. Un aporte se reserva del dinero disponible.

**Analizar tus hábitos:** abre **Estadísticas**, introduce un mes `AAAA-MM` y pulsa **Consultar**. Verás el total de ingresos y gastos, más las barras por categoría.

**Gamificación:** entra a **Logros** para comprobar tus insignias y tu racha. La pantalla propone un reto de registrar movimientos durante tres días seguidos.

**Exportar:** en **Movimientos**, selecciona **Exportar CSV** para guardar un archivo compatible con Excel.

## Ejemplo para explicar en exposición

1. Registro un ingreso de $20.00 → disponible $20.00.
2. Registro un gasto de transporte de $3.00 → disponible $17.00.
3. Creo una meta de $10.00 y reservo $5.00 → saldo $17.00, reservado $5.00, disponible $12.00.
4. Abro estadísticas → transporte aparece como gasto; el ahorro reservado **no** aparece como gasto.
5. Cierro la aplicación y vuelvo a abrirla → los datos permanecen en SQLite.

## Diferencial innovador

La app distingue entre **saldo total** y **dinero verdaderamente disponible**, usa metas de ahorro como sobres virtuales, propone una racha motivadora y funciona offline: un enfoque sencillo para estudiantes que desean controlar su mesada sin depender de bancos o Internet.
