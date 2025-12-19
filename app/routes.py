from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignupForm, LoginForm
from app.middleware import patient_only, doctor_only
from models import get_db_connection
from app.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os
import time
from flask_mail import Message
from app import mail
import random
import string
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)
dashboard = Blueprint('dashboard', __name__)

# HARDCODED DOCTOR EMAILS - EXACTLY MATCHING WHAT USERS REGISTER WITH
DOCTOR_EMAILS = [
    'doctor1@drlabib.com',
    'doctor2@drlabib.com',
    'doctor3@drlabib.com',
    'doctor4@drlabib.com',
    'doctor5@drlabib.com'
]

def is_valid_phone(phone):
    pattern = re.compile("^05[0-9]{8}$")
    return pattern.match(phone) is not None

@auth.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'doctor':
            return redirect(url_for('dashboard.doctor'))
        else:
            return redirect(url_for('dashboard.select_doctor'))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        conn = get_db_connection()
        if conn is None:
            flash('Database error!', 'danger')
            return render_template('auth/login.html', form=form)

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, email, phone, password, role FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()

            if user_data is None:
                flash('Invalid email or password', 'danger')
                return render_template('auth/login.html', form=form)

            if check_password_hash(user_data[4], password):
                user = User(
                    id=user_data[0],
                    full_name=user_data[1],
                    email=user_data[2],
                    role=user_data[5]
                )
                login_user(user)
                flash('Logged in successfully!', 'success')

                if user.role == 'doctor':
                    return redirect(url_for('dashboard.doctor'))
                else:
                    return redirect(url_for('dashboard.select_doctor'))
            else:
                flash('Invalid email or password', 'danger')

        except Exception as e:
            flash('Login failed. Try again.', 'danger')
            print("Login Error:", e)
        finally:
            cursor.close()
            conn.close()

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        full_name = form.full_name.data
        phone = form.phone.data.strip()
        email = form.email.data.lower()
        password = form.password.data

        if not is_valid_phone(phone):
            flash('Please enter a valid Saudi mobile number (e.g., 0551234567)', 'danger')
            return render_template('auth/signup.html', form=form)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # CHECK IF EMAIL IS IN DOCTOR LIST (case-sensitive and exact match)
        role = 'doctor' if email in DOCTOR_EMAILS else 'patient'

        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed!', 'danger')
            return render_template('auth/signup.html', form=form)

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (full_name, email, phone, password, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, email, phone, hashed_password, role))
            conn.commit()
            flash('Account created successfully! Please login.', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('auth.login'))
        except Exception as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                if "email" in str(e):
                    flash('Email already registered!', 'danger')
                elif "phone" in str(e):
                    flash('Phone number already registered!', 'danger')
            else:
                flash('Registration failed. Try again.', 'danger')
            print(e)
            cursor.close()
        finally:
            conn.close()

    return render_template('auth/signup.html', form=form)

@auth.route('/otp-success')
def otp_success():
    return render_template('auth/otp_success.html')


# Add this BEFORE the complete_profile function

@auth.route('/upload-profile-pic', methods=['POST'])
@login_required
def upload_profile_pic():
    """Upload profile picture"""
    if 'profile_pic' not in request.files:
        return {"success": False, "error": "No file uploaded"}, 400
    
    file = request.files['profile_pic']
    
    if file.filename == '':
        return {"success": False, "error": "No file selected"}, 400
    
    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return {"success": False, "error": "Only PNG, JPG, JPEG, GIF allowed"}, 400
    
    # Validate file size (max 5MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > 5 * 1024 * 1024:
        return {"success": False, "error": "File too large (max 5MB)"}, 400
    
    try:
        # Create unique filename
        filename = f"profile_{current_user.id}_{int(time.time())}.{file.filename.rsplit('.', 1)[1].lower()}"
        upload_folder = os.path.join('app', 'static', 'uploads', 'profile_pics')
        
        # Create folder if doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Update database
        conn = get_db_connection()
        if not conn:
            return {"success": False, "error": "Database error"}, 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET profile_pic = %s WHERE id = %s
            """, (f"/static/uploads/profile_pics/{filename}", current_user.id))
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                "success": True,
                "profile_pic": f"/static/uploads/profile_pics/{filename}"
            }
        except Exception as e:
            print(f"Database error: {e}")
            return {"success": False, "error": "Failed to save profile picture"}, 500
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"Upload error: {e}")
        return {"success": False, "error": str(e)}, 500
    

    

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    conn = get_db_connection()
    if conn is None:
        flash('Database error', 'danger')
        return redirect(url_for('dashboard.patient' if current_user.role == 'patient' else 'dashboard.doctor'))

    try:
        cursor = conn.cursor()
        
        if request.method == 'POST':
            dob_str = f"{request.form.get('year')}-{request.form.get('month')}-{request.form.get('day')}"
            gender = request.form.get('gender')
            
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'danger')
                cursor.close()
                conn.close()
                return render_template('auth/complete_profile.html', user_data=None)

            if not gender:
                flash('Please select a gender', 'danger')
                cursor.close()
                conn.close()
                return render_template('auth/complete_profile.html', user_data=None)

            cursor.execute("""
                UPDATE users SET dob = %s, gender = %s WHERE id = %s
            """, (dob, gender, current_user.id))
            conn.commit()
            flash('Profile updated successfully!', 'success')
            cursor.close()
            conn.close()
            
            if current_user.role == 'doctor':
                return redirect(url_for('dashboard.doctor'))
            else:
                return redirect(url_for('dashboard.patient'))

        cursor.execute("SELECT dob, gender FROM users WHERE id = %s", (current_user.id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return render_template('auth/complete_profile.html', user_data=user_data)

    except Exception as e:
        print(f"Profile error: {e}")
        flash('An error occurred', 'danger')
        return redirect(url_for('dashboard.patient' if current_user.role == 'patient' else 'dashboard.doctor'))

# NEW: Select Doctor Page (after patient signup/login)
@dashboard.route('/select-doctor')
@login_required
@patient_only
def select_doctor():
    conn = get_db_connection()
    if not conn:
        flash('Database error', 'danger')
        return render_template('dashboard/error.html')
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, full_name, email FROM users WHERE role = 'doctor'")
        doctors = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('dashboard/select_doctor.html', doctors=doctors)
    except Exception as e:
        print(f"Error fetching doctors: {e}")
        flash('Could not load doctors', 'danger')
        return render_template('dashboard/error.html')

@dashboard.route('/patient/<int:doctor_id>')
@login_required
@patient_only
def patient(doctor_id):
    # Store selected doctor in session
    session['selected_doctor_id'] = doctor_id
    return render_template('dashboard/patient_dashboard.html')

@dashboard.route('/upload_video', methods=['POST'])
@login_required
@patient_only
def upload_video():
    if 'video' not in request.files:
        return {"success": False, "error": "No video uploaded"}, 400
    
    video = request.files['video']
    
    if video.filename == '':
        return {"success": False, "error": "No file selected"}, 400
    
    video.seek(0, os.SEEK_END)
    file_size = video.tell()
    video.seek(0)
    
    if file_size > 10 * 1024 * 1024:
        return {"success": False, "error": "File too large (max 10MB)"}, 400
    
    try:
        filename = f"patient_{current_user.id}_{int(time.time())}.webm"
        upload_folder = os.path.join('app', 'static', 'uploads', 'signs_videos')
        
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        video.save(filepath)
        
        from app.ml_model import model
        translated_text = model.translate_video(filepath)
        
        conn = get_db_connection()
        if not conn:
            return {"success": False, "error": "Database error"}, 500
        
        try:
            cursor = conn.cursor()
            
            # Get selected doctor from session or random
            doctor_id = session.get('selected_doctor_id')
            if not doctor_id:
                cursor.execute("SELECT id FROM users WHERE role = 'doctor' ORDER BY RAND() LIMIT 1")
                doctor = cursor.fetchone()
                doctor_id = doctor[0] if doctor else None
            
            if not doctor_id:
                cursor.execute("""
                    INSERT INTO users (full_name, email, phone, password, role)
                    VALUES ('Dr. Default', 'doctor@test.com', '0500000000', 'temp', 'doctor')
                """)
                conn.commit()
                doctor_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO conversations 
                (patient_id, doctor_id, patient_video_path, translated_text, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (current_user.id, doctor_id, f"/static/uploads/signs_videos/{filename}", translated_text, 'pending'))
            
            conn.commit()
            conversation_id = cursor.lastrowid
            
            return {
                "success": True, 
                "translation": translated_text,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            conn.rollback()
            print(f"Database error: {e}")
            return {"success": False, "error": "Failed to save conversation"}, 500
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"Upload error: {e}")
        return {"success": False, "error": str(e)}, 500

otp_storage = {}

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # DEBUG: Print incoming data
        print(f"\n=== FORGOT PASSWORD DEBUG ===")
        print(f"POST data keys: {request.form.keys()}")
        print(f"Session otp_sent (start): {session.get('otp_sent')}")
        print(f"Session otp_email (start): {session.get('otp_email')}")
        
        # STEP 1: Email submission (first time)
        if 'email' in request.form and not session.get('otp_sent'):
            email = request.form.get('email', '').strip().lower()
            print(f"DEBUG: New email submitted: {email}")
            
            if not email:
                flash('Please enter your email', 'danger')
                return render_template('auth/forgot_password.html')
            
            conn = get_db_connection()
            if not conn:
                flash('Database error. Please try again.', 'danger')
                return render_template('auth/forgot_password.html')
            
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, full_name FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if not user:
                    flash('Email not registered', 'danger')
                    return render_template('auth/forgot_password.html')
                
                otp = ''.join(random.choices(string.digits, k=6))
                print(f"DEBUG: OTP generated: {otp} for {email}")
                
                otp_storage[email] = {
                    'otp': otp,
                    'expires': datetime.now() + timedelta(minutes=10),
                    'user_id': user[0]
                }
                
                try:
                    msg = Message(
                        subject='Password Reset Code - Dr. Labib',
                        recipients=[email]
                    )
                    msg.body = f"""Hello {user[1]},

Your password reset code is: {otp}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
Dr. Labib Team
"""
                    mail.send(msg)
                    print(f"DEBUG: Email sent successfully to {email}")
                    
                    session['otp_email'] = email
                    session['otp_sent'] = True
                    print(f"DEBUG: Session updated - otp_email: {session.get('otp_email')}, otp_sent: {session.get('otp_sent')}")
                    flash('Verification code sent to your email!', 'success')
                    
                except Exception as e:
                    print(f"Email sending error: {e}")
                    flash('Failed to send email. Please check your internet connection.', 'danger')
                    return render_template('auth/forgot_password.html')
                
            except Exception as e:
                print(f"Database error: {e}")
                flash('An error occurred. Please try again.', 'danger')
                return render_template('auth/forgot_password.html')
        
        # STEP 2: OTP verification (after email sent)
        elif session.get('otp_sent'):
            print(f"DEBUG: OTP verification attempt")
            otp_input = ''.join([
                request.form.get(f'otp_{i}', '') for i in range(6)
            ]).strip()
            print(f"DEBUG: OTP input received: {otp_input}")
            
            if not otp_input or len(otp_input) != 6:
                flash('Please enter the complete 6-digit code', 'danger')
                return render_template('auth/forgot_password.html')
            
            email = session.get('otp_email')
            print(f"DEBUG: Checking OTP for email: {email}")
            stored_data = otp_storage.get(email)
            
            if not stored_data:
                flash('OTP expired. Please request a new code.', 'danger')
                session.pop('otp_sent', None)
                session.pop('otp_email', None)
                return redirect(url_for('auth.forgot_password'))
            
            if stored_data['otp'] == otp_input:
                if datetime.now() < stored_data['expires']:
                    print(f"DEBUG: OTP verified successfully")
                    session['otp_verified'] = True
                    session['reset_user_id'] = stored_data['user_id']
                    # Clear OTP data after verification
                    otp_storage.pop(email, None)
                    session.pop('otp_sent', None)
                    session.pop('otp_email', None)
                    return redirect(url_for('auth.reset_password'))
                else:
                    flash('OTP expired. Please request a new code.', 'danger')
                    otp_storage.pop(email, None)
                    session.pop('otp_sent', None)
                    session.pop('otp_email', None)
            else:
                print(f"DEBUG: OTP mismatch - Expected: {stored_data['otp']}, Got: {otp_input}")
                flash('Invalid code. Please try again.', 'danger')
        else:
            print(f"DEBUG: No email or otp_sent in form")
    
    return render_template('auth/forgot_password.html')


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if not session.get('otp_verified'):
        flash('Please verify your email first', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        new_password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not new_password or not confirm_password:
            flash('Please fill in all fields', 'danger')
            return render_template('auth/reset_password.html')
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/reset_password.html')
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return render_template('auth/reset_password.html')
        
        user_id = session.get('reset_user_id')
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        
        conn = get_db_connection()
        if not conn:
            flash('Database error. Please try again.', 'danger')
            return render_template('auth/reset_password.html')
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password = %s WHERE id = %s",
                (hashed_password, user_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            # Clear all session data
            session.pop('otp_verified', None)
            session.pop('reset_user_id', None)
            
            flash('Password reset successful! Please login with your new password.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            print(f"Password update error: {e}")
            flash('Failed to update password. Please try again.', 'danger')
            return render_template('auth/reset_password.html')
    
    return render_template('auth/reset_password.html')

@dashboard.route('/patient')
@login_required
@patient_only
def patient_dashboard():
    return render_template('dashboard/patient_dashboard.html')

@dashboard.route('/history')
@login_required
@patient_only
def history():
    conn = get_db_connection()
    if not conn:
        flash('Database error', 'danger')
        return render_template('dashboard/error.html')
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE patient_id = %s 
            ORDER BY timestamp DESC
        """, (current_user.id,))
        conversations = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('dashboard/history.html', conversations=conversations)
    except Exception as e:
        print(f"Error fetching history: {e}")
        flash('Could not load conversations', 'danger')
        return render_template('dashboard/error.html')

@dashboard.route('/conversation/<int:conv_id>', methods=['GET', 'POST'])
@login_required
def conversation(conv_id):
    conn = get_db_connection()
    if not conn:
        flash('Database error', 'danger')
        return redirect(url_for('dashboard.history' if current_user.role == 'patient' else 'dashboard.doctor'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if current_user.role == 'patient':
            cursor.execute("""
                SELECT c.* FROM conversations c
                WHERE c.id = %s AND c.patient_id = %s
            """, (conv_id, current_user.id))
        elif current_user.role == 'doctor':
            cursor.execute("""
                SELECT c.* FROM conversations c
                WHERE c.id = %s AND c.doctor_id = %s
            """, (conv_id, current_user.id))
        else:
            flash('Invalid role', 'danger')
            return redirect(url_for('auth.login'))
        
        conversation = cursor.fetchone()
        
        if not conversation:
            cursor.close()
            conn.close()
            flash('Conversation not found', 'danger')
            return redirect(url_for('dashboard.history' if current_user.role == 'patient' else 'dashboard.doctor'))
        
        if request.method == 'POST':
            message_text = request.form.get('message_text', '').strip()
            
            if not message_text:
                flash('Please enter a message', 'danger')
                cursor.close()
                conn.close()
                return render_template('dashboard/conversation.html', conv=conversation)
            
            try:
                if current_user.role == 'doctor':
                    cursor.execute("""
                        UPDATE conversations 
                        SET doctor_response_text = %s, status = 'responded'
                        WHERE id = %s
                    """, (message_text, conv_id))
                elif current_user.role == 'patient':
                    cursor.execute("""
                        UPDATE conversations 
                        SET patient_response_text = %s
                        WHERE id = %s
                    """, (message_text, conv_id))
                
                conn.commit()
                flash('Message sent successfully!', 'success')
                cursor.close()
                conn.close()
                return redirect(url_for('dashboard.conversation', conv_id=conv_id))
                
            except Exception as e:
                print(f"Message error: {e}")
                flash('Failed to send message', 'danger')
                cursor.close()
                conn.close()
                return render_template('dashboard/conversation.html', conv=conversation)
        
        cursor.close()
        conn.close()
        return render_template('dashboard/conversation.html', conv=conversation)
        
    except Exception as e:
        print(f"Error loading conversation: {e}")
        flash('Could not load conversation', 'danger')
        return redirect(url_for('dashboard.history' if current_user.role == 'patient' else 'dashboard.doctor'))

@dashboard.route('/doctor')
@login_required
@doctor_only
def doctor():
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard/error.html')
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT c.*, u.full_name as patient_name, u.email as patient_email
            FROM conversations c
            JOIN users u ON c.patient_id = u.id
            WHERE c.doctor_id = %s AND c.status = 'pending'
            ORDER BY c.timestamp DESC
        """, (current_user.id,))
        conversations = cursor.fetchall()
        
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                COUNT(CASE WHEN status = 'responded' THEN 1 END) as responded,
                COUNT(*) as total
            FROM conversations 
            WHERE doctor_id = %s AND DATE(timestamp) = CURDATE()
        """, (current_user.id,))
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('dashboard/doctor_dashboard.html', 
                             conversations=conversations, 
                             stats=stats)
    except Exception as e:
        print(f"Doctor dashboard error: {e}")
        return render_template('dashboard/error.html')