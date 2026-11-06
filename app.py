from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL Database Configuration (Connected to your phpMyAdmin 'midproj' database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/midproj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='Eco Warrior')
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    co2 = db.Column(db.Float, default=0.0)
    water = db.Column(db.Integer, default=0)
    waste = db.Column(db.Float, default=0.0)

class Habit(db.Model):
    __tablename__ = 'habit'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(20), default='Daily')
    eco_points = db.Column(db.Integer, nullable=False)
    co2_saved = db.Column(db.Float, default=0.5)
    completed = db.Column(db.Boolean, default=False)
    streak = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/')
def index():
    user_data = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            habits = Habit.query.filter_by(user_id=user.id).all()
            user_data = {
                'name': user.name,
                'username': user.username,
                'points': user.points,
                'streak': user.streak,
                'co2': user.co2,
                'water': user.water,
                'waste': user.waste,
                'habits': [{
                    'id': str(h.id),
                    'name': h.title,
                    'category': h.category,
                    'frequency': h.frequency,
                    'points': h.eco_points,
                    'co2': h.co2_saved,
                    'completed': h.completed,
                    'streak': h.streak
                } for h in habits],
                'weeklyLogs': [
                    {'day': 'Mon', 'points': 35, 'co2': 2.5},
                    {'day': 'Tue', 'points': 50, 'co2': 4.1},
                    {'day': 'Wed', 'points': 20, 'co2': 1.8},
                    {'day': 'Thu', 'points': 60, 'co2': 4.5},
                    {'day': 'Fri', 'points': 40, 'co2': 3.2},
                    {'day': 'Sat', 'points': 40, 'co2': 2.3},
                    {'day': 'Sun', 'points': user.points, 'co2': user.co2}
                ]
            }
    return render_template('index.html', server_user=user_data)

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username'), password=data.get('password')).first()
    if user:
        session['user_id'] = user.id
        return jsonify({'success': True, 'name': user.name})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    existing = User.query.filter_by(username=data.get('username')).first()
    if existing:
        return jsonify({'success': False, 'message': 'Username already taken'}), 400
    
    new_user = User(
        name=data.get('name'),
        username=data.get('username'),
        password=data.get('password'),
        points=25,
        streak=1,
        co2=1.5,
        water=20,
        waste=1.0
    )
    db.session.add(new_user)
    db.session.commit()
    
    # Add a default starter habit
    default_habit = Habit(
        title='Reusable Water Bottle',
        category='water',
        eco_points=15,
        co2_saved=0.4,
        user_id=new_user.id
    )
    db.session.add(default_habit)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/habit/add', methods=['POST'])
def api_add_habit():
    if 'user_id' not in session:
        return jsonify({'success': False}), 401
    data = request.get_json()
    new_habit = Habit(
        title=data.get('name'),
        category=data.get('category'),
        frequency=data.get('frequency'),
        eco_points=int(data.get('points')),
        co2_saved=float(data.get('co2')),
        user_id=session['user_id']
    )
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/habit/toggle/<int:habit_id>', methods=['POST'])
def api_toggle_habit(habit_id):
    if 'user_id' not in session:
        return jsonify({'success': False}), 401
    habit = Habit.query.filter_by(id=habit_id, user_id=session['user_id']).first()
    user = User.query.get(session['user_id'])
    if habit and user:
        habit.completed = not habit.completed
        if habit.completed:
            habit.streak += 1
            user.points += habit.eco_points
            user.co2 += habit.co2_saved
            if habit.category == 'water': user.water += 15
            if habit.category == 'waste': user.waste += 0.8
        else:
            habit.streak = max(1, habit.streak - 1)
            user.points = max(0, user.points - habit.eco_points)
            user.co2 = max(0.0, user.co2 - habit.co2_saved)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/habit/delete/<int:habit_id>', methods=['POST'])
def api_delete_habit(habit_id):
    if 'user_id' not in session:
        return jsonify({'success': False}), 401
    habit = Habit.query.filter_by(id=habit_id, user_id=session['user_id']).first()
    if habit:
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user_id', None)
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)