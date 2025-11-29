# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database.models import init_db, create_lead, get_all_leads, update_lead, delete_lead, get_lead_by_id, test_connection
from config import config
import os

app = Flask(__name__)
app.config.from_object(config['default'])

# Inicializar la base de datos al iniciar la aplicación
print("🚀 Iniciando aplicación LeadTracker...")
print(f"📊 Usando: {config['default'].DB_ENGINE.upper()}")
if init_db():
    print("✅ Base de datos inicializada correctamente")
else:
    print("❌ Error inicializando base de datos")

@app.route('/')
def index():
    """Página principal con formulario de registro"""
    servicios = [
        "Consultoría Tecnológica",
        "Desarrollo de Software",
        "Marketing Digital",
        "Análisis de Datos",
        "Transformación Digital",
        "Soporte Técnico"
    ]
    return render_template('index.html', servicios=servicios)

@app.route('/leads')
def leads():
    """Página para ver todos los leads"""
    all_leads = get_all_leads()
    return render_template('leads.html', leads=all_leads)

@app.route('/add_lead', methods=['POST'])
def add_lead():
    """Endpoint para agregar nuevo lead"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()
        interes = request.form.get('interes', '').strip()
        
        # Validaciones básicas
        if not nombre or not correo or not interes:
            flash('Por favor complete todos los campos obligatorios', 'error')
            return redirect(url_for('index'))
        
        if create_lead(nombre, correo, telefono, interes):
            flash('Lead registrado exitosamente!', 'success')
        else:
            flash('Error al registrar el lead. El correo puede estar duplicado.', 'error')
        
        return redirect(url_for('index'))

@app.route('/api/leads', methods=['GET'])
def api_leads():
    """API endpoint para obtener leads en formato JSON"""
    all_leads = get_all_leads()
    return jsonify(all_leads)

@app.route('/edit_lead/<int:lead_id>', methods=['GET', 'POST'])
def edit_lead(lead_id):
    """Editar lead existente"""
    lead = get_lead_by_id(lead_id)
    if not lead:
        flash('Lead no encontrado', 'error')
        return redirect(url_for('leads'))
    
    servicios = [
        "Consultoría Tecnológica",
        "Desarrollo de Software",
        "Marketing Digital",
        "Análisis de Datos",
        "Transformación Digital",
        "Soporte Técnico"
    ]
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()
        interes = request.form.get('interes', '').strip()
        
        if not nombre or not correo or not interes:
            flash('Por favor complete todos los campos obligatorios', 'error')
            return render_template('edit_lead.html', lead=lead, servicios=servicios)
        
        if update_lead(lead_id, nombre, correo, telefono, interes):
            flash('Lead actualizado exitosamente!', 'success')
            return redirect(url_for('leads'))
        else:
            flash('Error al actualizar el lead.', 'error')
    
    return render_template('edit_lead.html', lead=lead, servicios=servicios)

@app.route('/delete_lead/<int:lead_id>')
def delete_lead_route(lead_id):
    """Eliminar lead"""
    if delete_lead(lead_id):
        flash('Lead eliminado exitosamente!', 'success')
    else:
        flash('Error al eliminar el lead.', 'error')
    
    return redirect(url_for('leads'))

@app.route('/health')
def health_check():
    """Endpoint para verificar el estado de la aplicación y base de datos"""
    db_status = "✅ Conectado" if test_connection() else "❌ Error"
    return {
        "status": "OK",
        "database": db_status,
        "service": "LeadTracker API"
    }

if __name__ == '__main__':
    print(f"🌐 Servidor iniciado en http://0.0.0.0:5000")
    print(f"📊 Conectado a RDS: {config['default'].DB_HOST}")
    app.run(host='0.0.0.0', port=5000, debug=True)