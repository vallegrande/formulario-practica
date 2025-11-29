# database/models.py
import os
from config import config

# Determinar qué motor usar
DB_ENGINE = config['default'].DB_ENGINE

if DB_ENGINE == 'mysql':
    import pymysql
    db_module = pymysql
else:
    import psycopg2
    db_module = psycopg2

def get_db_connection(max_retries=3, delay=2):
    """Establece conexión con la base de datos RDS con reintentos"""
    for attempt in range(max_retries):
        try:
            if DB_ENGINE == 'mysql':
                conn = pymysql.connect(
                    host=config['default'].DB_HOST,
                    database=config['default'].DB_NAME,
                    user=config['default'].DB_USER,
                    password=config['default'].DB_PASSWORD,
                    port=int(config['default'].DB_PORT),
                    connect_timeout=10,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            else:
                conn = psycopg2.connect(
                    host=config['default'].DB_HOST,
                    database=config['default'].DB_NAME,
                    user=config['default'].DB_USER,
                    password=config['default'].DB_PASSWORD,
                    port=config['default'].DB_PORT,
                    connect_timeout=10
                )
            
            print(f"✅ Conexión exitosa a {DB_ENGINE.upper()} RDS: {config['default'].DB_HOST}")
            return conn
        except db_module.Error as e:
            print(f"⚠️  Intento {attempt + 1} de {max_retries} falló: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Reintentando en {delay} segundos...")
                time.sleep(delay)
            else:
                print("❌ No se pudo conectar a la base de datos después de varios intentos")
                return None

def test_connection():
    """Función para probar la conexión a RDS"""
    print(f"🧪 Probando conexión a {DB_ENGINE.upper()} RDS...")
    print(f"📊 Host: {config['default'].DB_HOST}")
    print(f"📊 Database: {config['default'].DB_NAME}")
    print(f"📊 User: {config['default'].DB_USER}")
    print(f"📊 Port: {config['default'].DB_PORT}")
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            if DB_ENGINE == 'mysql':
                cur.execute("SELECT version()")
                db_version = cur.fetchone()
                print(f"✅ MySQL version: {db_version['version()']}")
            else:
                cur.execute("SELECT version();")
                db_version = cur.fetchone()
                print(f"✅ PostgreSQL version: {db_version[0]}")
            
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error en prueba: {e}")
            return False
    return False

def init_db():
    """Inicializa la base de datos y crea las tablas necesarias en RDS"""
    print(f"🚀 Inicializando base de datos en {DB_ENGINE.upper()} RDS...")
    
    if not test_connection():
        print("❌ No se puede inicializar la base de datos sin conexión")
        return False
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            if DB_ENGINE == 'mysql':
                # Verificar si la tabla ya existe en MySQL
                cur.execute("""
                    SELECT COUNT(*) as count
                    FROM information_schema.tables 
                    WHERE table_schema = %s 
                    AND table_name = 'leads'
                """, (config['default'].DB_NAME,))
                result = cur.fetchone()
                table_exists = result['count'] > 0
                
                if table_exists:
                    print("✅ La tabla 'leads' ya existe")
                else:
                    create_table_query = """
                    CREATE TABLE leads (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_completo VARCHAR(100) NOT NULL,
                        correo_electronico VARCHAR(100) UNIQUE NOT NULL,
                        telefono VARCHAR(20),
                        interes_servicio VARCHAR(100) NOT NULL,
                        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
            else:
                # Verificar si la tabla ya existe en PostgreSQL
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'leads'
                    );
                """)
                table_exists = cur.fetchone()[0]
                
                if table_exists:
                    print("✅ La tabla 'leads' ya existe")
                else:
                    create_table_query = """
                    CREATE TABLE leads (
                        id SERIAL PRIMARY KEY,
                        nombre_completo VARCHAR(100) NOT NULL,
                        correo_electronico VARCHAR(100) UNIQUE NOT NULL,
                        telefono VARCHAR(20),
                        interes_servicio VARCHAR(100) NOT NULL,
                        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
            
            if not table_exists:
                cur.execute(create_table_query)
                conn.commit()
                print("✅ Tabla 'leads' creada exitosamente")
            
            cur.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            return False
    return False

# Operaciones CRUD
def create_lead(nombre, correo, telefono, interes):
    """INSERT - Crear nuevo lead"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO leads (nombre_completo, correo_electronico, telefono, interes_servicio) VALUES (%s, %s, %s, %s)",
                (nombre, correo, telefono, interes)
            )
            conn.commit()
            cur.close()
            conn.close()
            print(f"✅ Lead creado: {nombre} - {correo}")
            return True
        except db_module.IntegrityError:
            print(f"❌ Error: El correo {correo} ya existe")
            return False
        except Exception as e:
            print(f"❌ Error creando lead: {e}")
            return False
    return False

def get_all_leads():
    """SELECT - Obtener todos los leads"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM leads ORDER BY fecha_registro DESC")
            
            if DB_ENGINE == 'mysql':
                leads = cur.fetchall()
            else:
                leads = cur.fetchall()
                # Convertir a formato similar para consistencia
                leads = [dict(zip([desc[0] for desc in cur.description], row)) for row in leads]
            
            cur.close()
            conn.close()
            print(f"✅ Leads obtenidos: {len(leads)} registros")
            return leads
        except Exception as e:
            print(f"❌ Error obteniendo leads: {e}")
            return []

def update_lead(lead_id, nombre, correo, telefono, interes):
    """UPDATE - Actualizar lead existente"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE leads SET nombre_completo = %s, correo_electronico = %s, telefono = %s, interes_servicio = %s WHERE id = %s",
                (nombre, correo, telefono, interes, lead_id)
            )
            conn.commit()
            cur.close()
            conn.close()
            print(f"✅ Lead actualizado: ID {lead_id}")
            return True
        except Exception as e:
            print(f"❌ Error actualizando lead: {e}")
            return False
    return False

def delete_lead(lead_id):
    """DELETE - Eliminar lead"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM leads WHERE id = %s", (lead_id,))
            conn.commit()
            cur.close()
            conn.close()
            print(f"✅ Lead eliminado: ID {lead_id}")
            return True
        except Exception as e:
            print(f"❌ Error eliminando lead: {e}")
            return False
    return False

def get_lead_by_id(lead_id):
    """Obtener lead por ID"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM leads WHERE id = %s", (lead_id,))
            
            if DB_ENGINE == 'mysql':
                lead = cur.fetchone()
            else:
                row = cur.fetchone()
                lead = dict(zip([desc[0] for desc in cur.description], row)) if row else None
            
            cur.close()
            conn.close()
            return lead
        except Exception as e:
            print(f"❌ Error obteniendo lead: {e}")
            return None