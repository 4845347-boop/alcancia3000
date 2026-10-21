Alcancía 3000
Tus finanzas, tu ritmo

Aplicación web educativa para ayudar a estudiantes salvadoreños a registrar sus ingresos y gastos, administrar metas de ahorro, revisar estadísticas y motivarse con retos, rachas y logros. Los importes se presentan en dólares estadounidenses (USD).
Objetivo
Promover hábitos de ahorro y organización financiera mediante una herramienta sencilla que puede utilizarse desde un navegador de computadora, incluso sin una conexión a Internet una vez disponible el archivo.
Funcionalidades incluidas
- Inicio: muestra saldo, ingresos, gastos, resumen del mes y movimientos recientes.
- Movimientos: registra, consulta, edita y elimina ingresos y gastos; permite filtrar por tipo y categoría.
- Categorías: crea categorías para ingresos y gastos y permite reorganizar los movimientos al eliminar una categoría en uso.
- Metas de ahorro: crea metas, registra abonos, calcula el porcentaje de avance y muestra el monto faltante.
- Estadísticas: presenta ingresos y gastos por mes, gráfico comparativo de seis meses y distribución de gastos por categoría.
- Retos, rachas y logros: permite crear retos y marcar el cumplimiento; registra rachas y desbloquea reconocimientos por condiciones programadas.
- Respaldo: exporta e importa datos mediante archivos JSON y permite restablecer la información.
Tecnologías utilizadas
Tecnología	Uso
HTML5	Estructura de las pantallas
CSS3	Estilos, animaciones y diseño adaptable
JavaScript	Lógica, validaciones, navegación y gráficos SVG
localStorage	Persistencia de los datos en el navegador


Importante: esta versión es un archivo HTML independiente. No utiliza SQLite, MySQL, un servidor backend ni una API de inteligencia artificial. El almacenamiento es local al navegador y no equivale a una base de datos relacional.
Requisitos
- Laptop o computadora con Windows, Linux o macOS.
- Navegador moderno como Google Chrome o Microsoft Edge.
- No requiere instalar Python, .NET, Android Studio, paquetes ni dependencias.
Cómo ejecutar
1. Descarga el repositorio o el archivo alcancia3000.html.
2. Abre la carpeta donde se encuentra el archivo.
3. Haz doble clic en alcancia3000.html para abrirlo en Chrome o Edge.
4. Utiliza el menú inferior para navegar por Inicio, Movimientos, Metas, Estadísticas y Retos.
No es necesario iniciar sesión: el alcance actual es de uso individual en un navegador.
Guía rápida de prueba
1. En Inicio, pulsa + Ingreso y registra un ingreso de $20.00 (por ejemplo, categoría Mesada).
2. Pulsa − Gasto y registra un gasto de $5.00 (por ejemplo, categoría Transporte).
3. Verifica que el saldo mostrado sea $15.00.
4. En Metas, crea una meta de $100.00 y registra un abono de $10.00.
5. Comprueba que la meta indique un avance del 10 %.
6. Visita Estadísticas para observar el resumen y los gráficos.
7. En Ajustes y respaldo (ícono de engranaje), exporta un archivo JSON.
Estos son casos de prueba sugeridos; sus resultados deben comprobarse realmente en el navegador antes de anotarlos como aprobados.
Almacenamiento y respaldos
Los datos se almacenan en localStorage, bajo la clave alcancia3000.v1. El modelo incluye colecciones de categorías, movimientos, metas, retos, rachas y logros, además de configuración.
- El guardado es local al navegador y al perfil. Si se borran los datos del sitio/navegador, podrían perderse los registros.
- Para exportar: abre el botón de Ajustes y respaldo → Exportar respaldo.
- Para restaurar: Ajustes y respaldo → Importar respaldo, selecciona el JSON exportado y confirma. La importación reemplaza los datos actuales.
- No se sincronizan datos automáticamente entre computadoras.
- Para conservar evidencia, realiza respaldos antes de borrar datos o cambiar de equipo.
Estructura del repositorio
Alcancia3000/
├── alcancia3000.html             # Programa web completo
├── README.md                     # Instrucciones del proyecto
└── documentacion/               # Documentos de entrega (si se agregan)
    ├── 01_Manual_de_Usuario.html
    ├── 02_Manual_Tecnico.html
    ├── 03_Diagrama_Entidad_Relacion_Logico.svg
    └── 04_Tabla_de_Requerimientos.csv
Arquitectura resumida
El HTML concentra la presentación, lógica de negocio y persistencia en un solo archivo. JavaScript administra el objeto de datos y lo serializa como JSON en localStorage. El diagrama entidad-relación entregado es un modelo lógico, no un esquema de tablas SQL implementadas.
Seguridad, límites y mejoras pendientes
- No hay autenticación ni roles de usuario.
- No existe base de datos SQL ni sincronización en la nube.
- Los datos almacenados localmente no están cifrados por la aplicación.
- Las funciones no emplean inteligencia artificial generativa.
- La información es educativa y no constituye asesoría financiera profesional.
- Como mejoras futuras se pueden evaluar una base de datos relacional, perfiles de usuario y mecanismos adicionales de respaldo.
Documentación y entrega académica
El repositorio puede acompañarse de manual de usuario, manual técnico, diagrama lógico, tabla de requerimientos, capturas de pruebas y video de demostración de 90 segundos. Incluye solo resultados y capturas verificadas realmente al probar el programa.

Proyecto: Alcancía 3000 · Desarrollo de Software · INDEL · Octubre de 2026.
