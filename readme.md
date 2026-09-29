# 🚌 Bus Booking System (Flask + MySQL)

ប្រព័ន្ធកក់សំបុត្រឡានក្រុងតាមអនឡាញ (Bus Booking System) អភិវឌ្ឍន៍ឡើងដោយប្រើ **Flask (Python)**, **Jinja2 Templates**, និង **MySQL (phpMyAdmin)**[cite: 1, 3]។

---

## 📁 Project Structure & Description

```text
bus_booking/
│
├── app.py                     # File មេសម្រាប់ Run application និង Register Blueprints ទាំងអស់
├── connect.py                 # File សម្រាប់កូដតភ្ជាប់ទៅកាន់ MySQL Database
├── config.py                  # រក្សាទុក Config ផ្សេងៗ (Secret Key, DB credentials)
├── requirements.txt           # បញ្ជី Libraries ដែលត្រូវ install (Flask, mysql-connector-python, ...)[cite: 1]
│
├── routes/                    # ផ្ទុក Python modules សម្រាប់បែកចែក Logic តាម Blueprint
│   ├── __init__.py            # សញ្ញាប្រាប់ Python ឱ្យស្គាល់ folder នេះជា Package
│   ├── auth.py                # គ្រប់គ្រង Login / Logout / Register របស់ User និង Admin
│   ├── admin.py               # គ្រប់គ្រង Admin Dashboard[cite: 2]
│   ├── bus.py                 # គ្រប់គ្រងការបន្ថែម/កែប្រែ/លុប ព័ត៌មានឡានក្រុង (Buses)[cite: 2, 6]
│   ├── route.py               # គ្រប់គ្រងខ្សែផ្លូវរត់ From -> To (Routes)[cite: 4, 7]
│   ├── schedule.py            # គ្រប់គ្រងកាលវិភាគចេញដំណើរ និងតម្លៃសំបុត្រ (Schedules)[cite: 4, 8]
│   └── booking.py             # គ្រប់គ្រងដំណើរការកក់សំបុត្រ (Bookings)[cite: 5]
│
├── templates/                 # ផ្ទុក HTML Templates (Jinja2)
│   ├── layout/                # Base layouts សម្រាប់ extend
│   │   ├── base_user.html     # Layout មេសម្រាប់ User
│   │   └── base_admin.html    # Layout មេសម្រាប់ Admin
│   │
│   ├── auth/                  # ទំព័រពាក់ព័ន្ធនឹង Authentication
│   │   ├── login.html         # ទំព័រចូលប្រើប្រាស់
│   │   └── register.html      # ទំព័របង្កើត Account
│   │
│   ├── admin/                 # ទំព័រគ្រប់គ្រងសម្រាប់ Admin Panel[cite: 2]
│   │   ├── dashboard.html     # ទំព័រផ្ទាំងគ្រប់គ្រងសរុប (Dashboard)[cite: 2]
│   │   ├── buses.html         # គ្រប់គ្រងឡានក្រុង[cite: 2]
│   │   ├── routes.html        # គ្រប់គ្រងខ្សែផ្លូវរត់[cite: 2]
│   │   ├── schedules.html     # គ្រប់គ្រងកាលវិភាគ[cite: 2]
│   │   ├── bookings.html      # មើលបញ្ជីកក់សំបុត្រទាំងអស់[cite: 2]
│   │   ├── users.html         # គ្រប់គ្រងគណនីអ្នកប្រើប្រាស់[cite: 2]
│   │   ├── passengers.html    # បញ្ជីឈ្មោះអ្នកធ្វើដំណើរ[cite: 2]
│   │   └── report.html        # របាយការណ៍ប្រាក់ចំណូល និងការលក់[cite: 2]
│   │
│   └── user/                  # ទំព័រសម្រាប់អតិថិជន (User Interface)[cite: 4]
│       ├── index.html / search.html  # ទំព័រដើម និងទំព័រស្វែងរកជើងឡាន[cite: 4]
│       ├── my_bookings.html   # មើលប្រវត្តិ និងសំបុត្រដែលបានកក់[cite: 4]
│       └── profile.html       # គ្រប់គ្រងព័ត៌មានផ្ទាល់ខ្លួន[cite: 4]
│
└── static/                    # ផ្ទុក static assets
    ├── css/                   # ផ្ទុក File CSS (style.css, admin.css)
    ├── js/                    # ផ្ទុក File JavaScript (main.js)
    └── uploads/               # ផ្ទុករូបភាពដែល Upload (ឧ. រូបឡានក្រុង)[cite: 6]