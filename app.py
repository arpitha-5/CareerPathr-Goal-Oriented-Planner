from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime
import os
from models import User

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------------- USER MODEL ----------------

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(user_data) if user_data else None

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!')
            return redirect(url_for('register'))
        
        # Check if user already exists
        if mongo.db.users.find_one({'email': email}):
            flash('Email already exists!')
            return redirect(url_for('register'))
        
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        # Create user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({
            'username': username, 
            'email': email, 
            'password': hashed_password
        })
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Please fill in all fields!')
            return redirect(url_for('login'))
        
        user_data = mongo.db.users.find_one({'email': email})
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash('Welcome back!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!')
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Get all goals for the current user
    goals = list(mongo.db.goals.find({'user_id': current_user.id}))
    
    # Categorize goals
    completed_goals = [goal for goal in goals if goal.get('status') == 'completed']
    in_progress_goals = [goal for goal in goals if goal.get('status') == 'in_progress']
    overdue_goals = [goal for goal in goals if goal.get('status') == 'overdue']
    
    # Get recent activities (placeholder for now)
    recent_activities = []
    
    return render_template('dashboard.html', 
                         goals=goals,
                         completed_goals=completed_goals,
                         in_progress_goals=in_progress_goals,
                         overdue_goals=overdue_goals,
                         recent_activities=recent_activities)

# Add Goal
@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form.get('category', 'General')
        priority = request.form.get('priority', 'medium')
        deadline = request.form.get('deadline')
        progress = int(request.form.get('progress', 0))
        milestones = request.form.get('milestones', '')
        resources = request.form.get('resources', '')
        
        # Create goal document
        goal_data = {
            'title': title,
            'description': description,
            'category': category,
            'priority': priority,
            'status': 'in_progress',
            'progress': progress,
            'milestones': milestones.split('\n') if milestones else [],
            'resources': resources,
            'user_id': current_user.id,
            'created_at': datetime.now(),
            'last_updated': datetime.now()
        }
        
        # Add deadline if provided
        if deadline:
            goal_data['deadline'] = datetime.strptime(deadline, '%Y-%m-%d')
        
        mongo.db.goals.insert_one(goal_data)
        flash('Goal created successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_goal.html')

# Edit Goal
@app.route('/edit_goal/<goal_id>', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = mongo.db.goals.find_one({'_id': ObjectId(goal_id), 'user_id': current_user.id})
    if not goal:
        flash('Goal not found!')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        update_data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'category': request.form.get('category', 'General'),
            'priority': request.form.get('priority', 'medium'),
            'progress': int(request.form.get('progress', 0)),
            'milestones': request.form.get('milestones', '').split('\n') if request.form.get('milestones') else [],
            'resources': request.form.get('resources', ''),
            'last_updated': datetime.now()
        }
        
        deadline = request.form.get('deadline')
        if deadline:
            update_data['deadline'] = datetime.strptime(deadline, '%Y-%m-%d')
        
        mongo.db.goals.update_one(
            {'_id': ObjectId(goal_id)}, 
            {'$set': update_data}
        )
        flash('Goal updated successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_goal.html', goal=goal)

# Delete Goal
@app.route('/delete_goal/<goal_id>')
@login_required
def delete_goal(goal_id):
    goal = mongo.db.goals.find_one({'_id': ObjectId(goal_id), 'user_id': current_user.id})
    if goal:
        mongo.db.goals.delete_one({'_id': ObjectId(goal_id)})
        flash('Goal deleted successfully!')
    else:
        flash('Goal not found!')
    return redirect(url_for('dashboard'))

# Update Goal Progress
@app.route('/update_progress/<goal_id>', methods=['POST'])
@login_required
def update_progress(goal_id):
    progress = int(request.form.get('progress', 0))
    mongo.db.goals.update_one(
        {'_id': ObjectId(goal_id), 'user_id': current_user.id},
        {'$set': {'progress': progress, 'last_updated': datetime.now()}}
    )
    flash('Progress updated successfully!')
    return redirect(url_for('dashboard'))

# Profile
@app.route('/profile')
@login_required
def profile():
    # Get user's goals and statistics
    goals = list(mongo.db.goals.find({'user_id': current_user.id}))
    
    # Calculate statistics
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.get('progress', 0) == 100])
    in_progress_goals = len([g for g in goals if g.get('progress', 0) > 0 and g.get('progress', 0) < 100])
    not_started_goals = len([g for g in goals if g.get('progress', 0) == 0])
    
    # Calculate average progress
    avg_progress = sum(g.get('progress', 0) for g in goals) / len(goals) if goals else 0
    
    # Get recent goals
    recent_goals = sorted(goals, key=lambda x: x.get('created_at', datetime.now()), reverse=True)[:5]
    
    # Get category breakdown
    categories = {}
    for goal in goals:
        cat = goal.get('category', 'General')
        categories[cat] = categories.get(cat, 0) + 1
    
    # Get priority breakdown
    priorities = {'High': 0, 'Medium': 0, 'Low': 0}
    for goal in goals:
        priority = goal.get('priority', 'Medium')
        if priority in priorities:
            priorities[priority] += 1
    
    stats = {
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'in_progress_goals': in_progress_goals,
        'not_started_goals': not_started_goals,
        'avg_progress': round(avg_progress, 1),
        'categories': categories,
        'priorities': priorities,
        'recent_goals': recent_goals
    }
    
    return render_template('profile.html', user=current_user, stats=stats)

# Update Profile
@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    
    # Check if username or email already exists (excluding current user)
    existing_user = mongo.db.users.find_one({
        '$and': [
            {'_id': {'$ne': ObjectId(current_user.id)}},
            {'$or': [{'username': username}, {'email': email}]}
        ]
    })

    if existing_user:
        flash('Username or email already exists!')
        return redirect(url_for('profile'))
    
    # Get additional profile data from form
    name = request.form.get('name')
    bio = request.form.get('bio')
    current_role = request.form.get('current_role')
    company = request.form.get('company')
    linkedin = request.form.get('linkedin')

    # Prepare update data
    update_fields = {'last_updated': datetime.now()}
    if username: update_fields['username'] = username
    if email: update_fields['email'] = email
    if name: update_fields['name'] = name
    if bio: update_fields['bio'] = bio
    if current_role: update_fields['current_role'] = current_role
    if company: update_fields['company'] = company
    if linkedin: update_fields['linkedin'] = linkedin

    # Update user data
    mongo.db.users.update_one(
        {'_id': ObjectId(current_user.id)},
        {'$set': update_fields}
    )
    
    # Update the current_user object in session (important for displaying updated info immediately)
    updated_user_data = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
    if updated_user_data:
        # Assuming current_user is a proxy, re-login or manually update its attributes
        # A simpler way is to just reload the user into the session if Flask-Login allows
        # For now, manually updating attributes for demonstration
        current_user._user = User(updated_user_data) # This might not work directly depending on Flask-Login setup
        # A more robust solution might involve: login_user(User(updated_user_data)) but this would re-hash the session

    flash('Profile updated successfully!')
    return redirect(url_for('profile'))

# Change Password
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not old_password or not new_password or not confirm_new_password:
            flash('Please fill in all fields!')
            return redirect(url_for('change_password'))

        user_data = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
        if not bcrypt.check_password_hash(user_data['password'], old_password):
            flash('Incorrect old password!')
            return redirect(url_for('change_password'))

        if new_password != confirm_new_password:
            flash('New passwords do not match!')
            return redirect(url_for('change_password'))

        if len(new_password) < 6:
            flash('New password must be at least 6 characters long!')
            return redirect(url_for('change_password'))

        hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        mongo.db.users.update_one(
            {'_id': ObjectId(current_user.id)},
            {'$set': {'password': hashed_new_password, 'last_updated': datetime.now()}}
        )
        flash('Password updated successfully!')
        return redirect(url_for('profile'))

    return render_template('change_password.html')

# Export Data
@app.route('/export_data')
@login_required
def export_data():
    flash('Data export functionality is not yet implemented.')
    return redirect(url_for('profile'))

# Delete Account
@app.route('/delete_account')
@login_required
def delete_account():
    flash('Account deletion functionality is not yet implemented.')
    return redirect(url_for('profile'))

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
