CareerPathr – Goal Oriented Planner 🚀
CareerPathr is an innovative, goal-oriented planner built with Python (Flask) and MongoDB. It helps users plan, track, and achieve their goals with a structured, user-friendly interface. The project is designed for students, professionals, and anyone looking to manage their personal or academic goals efficiently.

🔹 Features
User Authentication: Register, login, and secure session management with Flask-Login and bcrypt.

Dashboard: Comprehensive view of all goals, categorized into 'Completed', 'In Progress', and 'Overdue', with goal statistics and recent activities.

Profile Management: Detailed profile page displaying personal information, career aspirations, goal statistics, and recent achievements. Users can update their username, email, full name, bio, current role, company, and LinkedIn profile.

Account Actions: Options to change password, export user data, and delete the account.

Improved Goal Management: Functionality to add, edit, and delete goals, including progress updates.

Enhanced Navigation: Modern and responsive navigation bar with clear links to different sections.

Flash Messaging: Stylish and animated flash messages for user feedback.

Modern UI/UX: Revamped user interface with glassmorphism effects, gradients, and subtle animations for a premium feel.

Favicon & Branding: Professional logo included for branding.

📁 Folder Structure
csharp
Copy code
careerpath/
│
├── app.py              # Main Flask application
├── models.py           # MongoDB models
├── .env                # Environment variables (MongoDB URI, secret key)
├── requirements.txt    # Python dependencies
├── static/
│   ├── style.css       # CSS styling
│   └── career.png      # Logo & favicon
└── templates/          # HTML templates
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── add_goal.html
    ├── edit_goal.html
    ├── profile.html
    └── change_password.html
🛠 Technology Stack
Backend: Python, Flask, Flask-PyMongo, Flask-Login, Flask-Bcrypt

Database: MongoDB Atlas (cloud-based)

Frontend: HTML, CSS, Jinja2 templates

Environment: .env for sensitive keys

Deployment Ready: Can be deployed on Render, Railway, or PythonAnywhere

User Model: Defined in models.py, includes fields for username, email, and additional profile details like full name, bio, current role, company, and LinkedIn profile.

⚡ Installation & Setup
Clone the repository:

bash
Copy code
git clone <your-repo-url>
cd careerpathr
Create virtual environment & activate:

bash
Copy code
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
venv\Scripts\activate
Setup .env file in the root:

env
Copy code
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/careerpathr
Run the Flask app:

bash
Copy code
flask run
Open in browser:
Visit http://127.0.0.1:5000/

📝 Usage
Register a new account.

Login to access your dashboard.

Add goals with a title and description.

View all goals and track progress from the dashboard.

Visit your profile to see account info and total goals.

Update your personal and career details on the profile page.

Manage your goals by adding, editing, or deleting them.

Change your account password securely.

Explore your goal statistics and recent achievements on the profile page.

🌐 Future Enhancements
AI-powered goal suggestions using OpenAI API.

Notifications and reminders.

Implement actual data export (PDF/CSV) and account deletion functionality.

Transform into a React + Flask full-stack web app.

📌 Screenshots

(You can add actual screenshots here later)

📄 License
MIT License – free to use, modify, and distribute.