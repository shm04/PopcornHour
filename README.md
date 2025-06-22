
# 🎬 PopcornHour

Plataforma web sencilla para mostrar un catálogo de películas, con autenticación y autorización por roles (usuario/admin), desarrollada con **Flask** y **SQLAlchemy**.

---

## ⚙️ Tecnologías

- **Backend**: Flask + Flask-SQLAlchemy
- **Frontend**: HTML + CSS (Jinja2 templates)
- **Autenticación**: Flask-Login
- **Base de datos**: SQLite (modo local)

---

## 🧪 Funcionalidades

- Registro e inicio de sesión
- Roles diferenciados: `admin` y `user`
- Catálogo de películas dinámico
- CRUD completo de películas (solo admin)
- Control de acceso a rutas
- Diseño simple y responsive

---

## 🔧 Instalación

1. Clona el repo

```bash
git clone https://github.com/tuusuario/popcornhour.git
cd popcornhour
```

2. Activa un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala dependencias

```bash
pip install -r requirements.txt
```

4. Crea la base de datos

```python
from app import db
db.create_all()
```

5. Corre la app

```bash
python app.py
```

Visita: `http://localhost:5000`

---

## 👥 Roles

- **Admin**: puede agregar, editar, eliminar películas
- **Usuario**: solo puede ver el catálogo

---

## 📁 Estructura

```
popcornhour/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
│
├── templates/
│   └── *.html
├── static/
│   └── css/
│       └── styles.css
│
└── documentation/
    ├── db/
    │   └── erd.png
    └── flows/
        └── *.png
```

---

## 🧠 Autor

Desarrollado por **Sebastian Hernandez**  
🔗 GitHub: [github.com/shm04](https://github.com/shm04)

---
