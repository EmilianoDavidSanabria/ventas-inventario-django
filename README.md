# Sistema de Ventas e Inventario 📦📊

Proyecto web desarrollado con Django y Django REST Framework para la gestión de productos, ventas, estadísticas, exportación de datos, seguridad avanzada y rendimiento optimizado. Ideal para negocios que necesiten controlar su inventario y visualizar métricas.

---

## 🧩 Funcionalidades principales

- Registro y login de usuarios (con Django Auth)
- CRUD completo de productos y ventas
- Gráficos estáticos con Matplotlib y dinámicos con Plotly
- Filtros avanzados de ventas (por fechas, productos, rangos de precios, estado)
- Estadísticas mensuales y trimestrales
- Productos más vendidos con gráficos interactivos
- Exportación de ventas a Excel (`.xlsx`)
- Paginación y caché para mejorar el rendimiento
- Seguridad robusta (XSS, CSRF, HSTS, CSP, hashing de contraseñas)
- Autenticación con JWT (SimpleJWT)
- Control de tráfico con throttling de DRF
- tests: tests con `Django TestCase` cubriendo lógica de CRUD, cálculos de stock y validación de exportación Excel (`OpenPyXL`).
- Verificación de endpoints con `Django REST Framework` y autenticación `JWT`.
- Tests de integridad para renderizado de gráficos `Matplotlib` y `Plotly` (MIME types).
- Docker Entorno contenedorizado con `Dockerfile` y `docker-compose.yml` (App + PostgreSQL).

---

## 🛠️ Tecnologías usadas

- Python 3
- Django 4
- Django REST Framework
- Django Simple JWT
- Matplotlib
- Plotly
- Pandas
- OpenPyXL
- PostgreSQL
- Bootstrap

---

1. Cloná el repositorio:

```bash
git clone https://github.com/EmilianoDavidSanabria/nombre-del-repo.git
cd nombre-del-repo
