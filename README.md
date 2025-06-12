# 📈 FocusFlow API – Habit Tracker with Django REST Framework

**FocusFlow** is a minimalistic habit tracking API that lets users log daily habits and monitor their progress over time.  
Built with 💡 Django REST Framework and secured with 🔐 Token Authentication.

---

## 🚀 Features

- 🔐 Token-based user authentication (`/login/`)
- ✅ User can:
  - Create and manage daily **habits**
  - Log **habit entries** per date
  - See only their own data
- 🔎 Filter and search support for habits
- 🔧 Swagger & ReDoc auto-generated docs
- 🔁 Ready to connect with mobile or frontend app

---

## 📦 Tech Stack

- Python 3.11+
- Django 4.x
- Django REST Framework
- DRF Authtoken
- drf-yasg (Swagger)

---

## 📂 API Endpoints

| Method   | Endpoint        | Description           |
| -------- | --------------- | --------------------- |
| POST     | `/login/`       | Login and get token   |
| GET      | `/me/`          | Get current user      |
| GET/POST | `/habits/`      | List or create habits |
| GET/POST | `/habit-entry/` | Log habit progress    |
| GET      | `/swagger/`     | Swagger UI            |
| GET      | `/redoc/`       | ReDoc documentation   |

---

## ⚙️ Setup & Run

```bash
git clone https://github.com/yourusername/focusflow-api.git
cd focusflow-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📌 Create a superuser:

```bash
python manage.py createsuperuser
```

## 🔐 Authentication

- Register via `/register/`
- Login via `/login/` with `username` and `password`
- Copy the returned token and use it as:

```makefile
Authorization: Token your_token_here
```

-Use Swagger UI → click Authorize → paste token as:
`Token abc123...`

## 📌 Example Request: Create Habit

```http
POST /habits/
Authorization: Token your_token_here

{
  "name": "Read 30 mins",
  "goal_per_day": 1
}
```

## ✨ Roadmap

- [x] User registration
- [x] Token login
- [x] Habit & entry CRUD
- [x] User filtering
- [x] Swagger docs
- [ ] Progress analytics endpoint
- [ ] Dockerfile
- [ ] Unit tests

## 🤝 Contributions

Pull requests and stars welcome! ⭐

## 📜 License

MIT License
