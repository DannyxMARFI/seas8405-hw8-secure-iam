# 🔐 Keycloak Realm Setup Notes

This folder contains the configuration for the Keycloak identity provider used to secure the Flask microservice in this project.

---

## 📁 Contents

- `realm-export.json`: Exported configuration of the `demo-realm` realm, including:
  - A confidential client named `flask-client`
  - A test user `testuser`
  - OIDC settings suitable for development

---

## 🧭 Manual Configuration Instructions

If you prefer setting up Keycloak manually through the web interface, follow these steps:

### 1. Start Keycloak

Visit: [http://localhost:8080](http://localhost:8080)  
Login with:
- **Username**: `admin`
- **Password**: `admin`

---

### 2. Create Realm

- Click the dropdown (top left) → **Create Realm**
- **Name**: `demo-realm`
