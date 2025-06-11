from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import certifi

app = Flask(__name__)
app.secret_key = '22aa07cb23266e5f6dc58fdda6ef4c694b503a994e6812cd94d3ca8484787ae'

bcrypt = Bcrypt(app)

# MongoDB connection
client = MongoClient("mongodb+srv://Nachiket:Nachi1234@cluster0.knecg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=certifi.where())
db = client["Safar"]
users_collection = db["users"]

# Routes
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("pages/about.html")


@app.route('/destinations')
def destinations():
    return render_template('destinations.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        users_collection.insert_one({
            'fullname': fullname,
            'email': email,
            'phone': phone,
            'password': hashed_password
        })

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({'email': email})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['email'] = email
            return redirect(url_for('destinationstwo'))  # Login successful

        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')    

# @app.route('/profile', methods=['GET'])
# def profile():
#     if 'email' not in session:
#         return redirect(url_for('login'))

#     # Fetch user from the users_collection using session email
#     user = users_collection.find_one({'email': session['email']})
    
#     if not user:
#         return redirect(url_for('login'))  # Optional: handle case if user not found

#     return render_template('profile.html', user=user)


@app.route('/destinationstwo')
def destinationstwo():
    if 'email' not in session:
        return redirect(url_for('destinations'))
    return render_template('destinationstwo.html')

@app.route('/profile')
def profile():
    if 'email' not in session:
        flash('You must be logged in to view your profile.')
        return redirect(url_for('login'))

    user = users_collection.find_one({'email': session['email']})
    if not user:
        flash('User not found.')
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))



@app.route('/tajmahal_ar')
def tajmahal_ar():
        return render_template('pages/TajMahalAr.html')

@app.route('/tajmahal_vr')
def tajmahal_vr():
        return render_template('pages/TajMahalVr.html')

@app.route('/tajmahal_vrlaunch')
def tajmahal_vrlaunch():
        return render_template('pages/TajMahalLaunch.html')

@app.route('/download_tajmahal')
def download_apk():
    return send_from_directory('static/Apps', 'TajMahal.apk', as_attachment=True)



@app.route('/angkor_ar')
def angkor_ar():
        return render_template('pages/AngkorAr.html')

@app.route('/angkor_vr')
def angkor_vr():
        return render_template('pages/AngkorVr.html')

@app.route('/angkor_vrlaunch')
def angkor_vrlaunch():
        return render_template('pages/AngkorLaunch.html')

@app.route('/download_angkor')
def download_angkor():
    return send_from_directory('static/Apps', 'Angkor.apk', as_attachment=True)



@app.route('/colosseum_ar')
def chapel_ar():
        return render_template('pages/ColosseumAr.html')

@app.route('/colosseum_vr')
def chapel_vr():
        return render_template('pages/ColosseumVr.html')

@app.route('/colosseum_vrlaunch')
def chapel_vrlaunch():
        return render_template('pages/ColosseumLaunch.html')

@app.route('/download_colosseum')
def download_colosseum():
    return send_from_directory('static/Apps', 'Colosseum.apk', as_attachment=True)



@app.route('/ellora_ar')
def ellora_ar():
        return render_template('pages/ElloraAr.html')

@app.route('/ellora_vr')
def ellora_vr():
        return render_template('pages/ElloraVr.html')

@app.route('/ellora_vrlaunch')
def ellora_vrlaunch():
        return render_template('pages/ElloraLaunch.html')

@app.route('/download_ellora')
def download_ellora():
    return send_from_directory('static/Apps', 'Ellora.apk', as_attachment=True)



@app.route('/liberty_ar')
def liberty_ar():
        return render_template('pages/LibertyAr.html')

@app.route('/liberty_vr')
def liberty_vr():
        return render_template('pages/LibertyVr.html')

@app.route('/liberty_vrlaunch')
def liberty_vrlaunch():
        return render_template('pages/LibertyLaunch.html')

@app.route('/download_liberty')
def download_liberty():
    return send_from_directory('static/Apps', 'Liberty Island.apk', as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)
