# 🛡️ Forensic Blockchain Simulator v4.0

Una plataforma interactiva avanzada diseñada para la educación en ciberseguridad y los fundamentos de la tecnología Blockchain. Este simulador permite a los usuarios explorar la inmutabilidad de los datos, los mecanismos de consenso (Proof of Work) y los vectores de ataque forense a través de una interfaz de usuario premium.

![Blockchain Preview](https://img.shields.io/badge/Blockchain-SHA--256-blue?style=for-the-badge&logo=blockchain-dot-com)
![Python Version](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web--Server-orange?style=for-the-badge&logo=flask)

---

## 🚀 Características Principales

### 💎 Arquitectura Atómica
El núcleo del simulador ha sido refactorizado bajo principios de **Alta Cohesión y Bajo Acoplamiento**:
- **Consensus Engine**: Implementación robusta de Proof of Work.
- **Atomic Models**: Transacciones y Bloques desacoplados para escalabilidad.
- **Audit System**: Registro forense dual (Consola y archivo `.log`).

### 🔬 Laboratorio de Ciberseguridad (Hacking Lab)
- **Inyección de Datos**: Simula ataques de corrupción modificando bloques históricos.
- **Validación en Tiempo Real**: Escaneo forense automático que detecta rupturas de integridad.
- **Visualización de "Cadena Rota"**: Animaciones de glitch y auras rojas que indican pérdida de confianza en el ledger.

### 🎨 Experiencia de Usuario "Hacker-Style"
- **Zero Native Alerts**: Interacciones fluidas gestionadas por **SweetAlert2**.
- **Educational Tooltips**: Explicaciones técnicas dinámicas integradas con **Tippy.js**.
- **Matrix Mining Animation**: Animación de lluvia hexadecimal durante el proceso de minería.
- **Integridad Visual**: Conectores de pulso SVG que cambian su estado según la salud del sistema.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3, Flask, Hashlib, Logging.
- **Frontend**: HTML5 Semántico, CSS Grid/Flexbox moderno, Vanilla JS.
- **Librerías UI**: SweetAlert2 (Notificaciones), Tippy.js (Tooltips), Suit UI / Outfit Fonts.

---

## 📋 Guía de Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/joseberna/poc-blockchain-v1.git
cd poc-blockchain-v1
```

### 2. Configurar el entorno (Opcional)
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors
```

### 3. Iniciar el Nodo Forense
```bash
python3 app.py
```

### 4. Explorar el Laboratorio
Accede a `http://127.0.0.1:5000` en tu navegador.

---

## ☁️ Despliegue en Render

Este repositorio está optimizado para despliegues rápidos en **Render** mediante el archivo `render.yaml` incluido:

1.  **Repo Connect**: Conecta este repositorio en Render.
2.  **Auto Config**: Render detectará automáticamente el archivo `render.yaml`.
3.  **Start Command**: `gunicorn app:app` (Gestionado por Render Infrastructure).

---

## 🧬 Objetivos del Ejercicio
Este proyecto fue diseñado para demostrar los 3 pilares de Blockchain:
1. **Descentralización y Confianza**: A través del registro inmutable.
2. **Criptografía**: Uso de SHA-256 para la identidad de cada bloque.
3. **Mecanismo de Consenso**: Demo de la dificultad computacional para prevenir ataques de spam o re-escritura.

---

## 🤝 Créditos
Desarrollado con ❤️ por **Jose Berna** con arquitectura dirigida por **Antigravity AI**.
