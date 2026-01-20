from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, User, Message
from app.utils import sanitize_input, validate_email, validate_message
from sqlalchemy.exc import IntegrityError

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Display all messages with users."""
    page = request.args.get('page', 1, type=int)
    messages = db.paginate(
        db.select(Message).join(User).order_by(Message.created_at.desc()),
        page=page,
        per_page=10
    )
    return render_template('index.html', messages=messages)

@main_bp.route('/add-message', methods=['GET', 'POST'])
def add_message():
    """Add a new message."""
    if request.method == 'POST':
        name = sanitize_input(request.form.get('name', '').strip())
        email = sanitize_input(request.form.get('email', '').strip())
        message_text = sanitize_input(request.form.get('message', '').strip())
        
        # Validation
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Jméno musí mít alespoň 2 znaky.')
        
        if not validate_email(email):
            errors.append('Zadejte platný email.')
        
        if not message_text or len(message_text) < 5:
            errors.append('Zpráva musí mít alespoň 5 znaků.')
        
        if len(message_text) > 1000:
            errors.append('Zpráva nesmí přesáhnout 1000 znaků.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('main.add_message'))
        
        try:
            # Find or create user
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(name=name, email=email)
                db.session.add(user)
                db.session.flush()
            else:
                # Update name if different
                if user.name != name:
                    user.name = name
            
            # Create message
            new_message = Message(user_id=user.id, message=message_text)
            db.session.add(new_message)
            db.session.commit()
            
            flash('Vaše zpráva byla úspěšně přidána!', 'success')
            return redirect(url_for('main.index'))
            
        except IntegrityError:
            db.session.rollback()
            flash('Chyba při přidání zprávy. Zkuste to prosím znovu.', 'danger')
            return redirect(url_for('main.add_message'))
        except Exception as e:
            db.session.rollback()
            flash(f'Chyba: {str(e)}', 'danger')
            return redirect(url_for('main.add_message'))
    
    return render_template('add_message.html')

@main_bp.route('/delete-message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    """Delete a message."""
    message = db.get_or_404(Message, message_id)
    
    try:
        db.session.delete(message)
        db.session.commit()
        flash('Příspěvek byl úspěšně smazán.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Chyba při mazání: {str(e)}', 'danger')
    
    # Redirect to index
    return redirect(url_for('main.index'))

@main_bp.route('/user/<int:user_id>')
def user_messages(user_id):
    """Display all messages from a specific user."""
    user = db.get_or_404(User, user_id)
    page = request.args.get('page', 1, type=int)
    messages = db.paginate(
        db.select(Message).where(Message.user_id == user_id).order_by(Message.created_at.desc()),
        page=page,
        per_page=10
    )
    return render_template('user_messages.html', user=user, messages=messages)
