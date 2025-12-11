from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import re
from typing import List
import secrets

from database import get_db
import schema as schemas

app = FastAPI(title="Command Gateway API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTHENTICATION HELPER ---
def get_current_user(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    
    query = text("SELECT * FROM users WHERE api_key = :api_key")
    user = db.execute(query, {"api_key": x_api_key}).fetchone()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user

# --- CORE ENDPOINT: EXECUTE COMMAND ---
@app.post("/commands/execute", response_model=schemas.CommandResponse)
def execute_command(
    request: schemas.CommandRequest, 
    user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    command_text = request.command
    
    # 1. Check Credits
    if user.credits <= 0:
        raise HTTPException(status_code=403, detail="Insufficient credits")

    # 2. Fetch Rules (Ordered by ID for now, priority in real apps)
    rules = db.execute(text("SELECT * FROM rules ORDER BY id ASC")).fetchall()
    
    decision = "block" 
    matched_rule = "Default Block"

    # 3. Rule Engine (First Match Wins)
    for rule in rules:
        if re.search(rule.pattern, command_text):
            decision = rule.action 
            matched_rule = rule.pattern
            break 
    
    # 4. Handle Decision
    final_status = "REJECTED"
    response_msg = f"Blocked by rule: {matched_rule}"
    
    if decision == 'allow':
        try:
            
            update_credits = text("UPDATE users SET credits = credits - 1 WHERE id = :uid")
            db.execute(update_credits, {"uid": user.id})
            
            final_status = "EXECUTED"
            response_msg = "Command executed successfully"
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Transaction failed")

    # 5. Audit Log (Always log)
    log_query = text("""
        INSERT INTO audit_logs (user_id, command, status, response) 
        VALUES (:uid, :cmd, :stat, :resp)
    """)
    db.execute(log_query, {
        "uid": user.id, 
        "cmd": command_text, 
        "stat": final_status, 
        "resp": response_msg
    })
    
    db.commit() 

    
    user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user.id}).fetchone()

    return {
        "status": final_status,
        "message": response_msg,
        "credits_remaining": user.credits
    }

# --- ADMIN ENDPOINT: ADD RULES ---
@app.post("/rules", response_model=schemas.RuleResponse)
def create_rule(
    rule: schemas.RuleCreate,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    
    try:
        re.compile(rule.pattern)
    except re.error:
        raise HTTPException(status_code=400, detail="Invalid Regex Pattern")

    insert_query = text("""
        INSERT INTO rules (pattern, action, description) 
        VALUES (:pat, :act, :desc) RETURNING id, pattern, action, description
    """)
    new_rule = db.execute(insert_query, {
        "pat": rule.pattern, 
        "act": rule.action, 
        "desc": rule.description
    }).fetchone()
    
    db.commit()
    return new_rule

# --- USER ENDPOINT: PROFILE ---
@app.get("/users/me", response_model=schemas.UserProfile)
def get_profile(user = Depends(get_current_user)):
    return {
        "username": user.username,
        "role": user.role,
        "credits": user.credits
    }


# --- ADMIN ENDPOINT: VIEW LOGS ---
@app.get("/audit-logs", response_model=List[schemas.AuditLogResponse])
def get_audit_logs(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    
    
    sql = text("""
        SELECT audit_logs.*, users.username 
        FROM audit_logs 
        JOIN users ON audit_logs.user_id = users.id 
        ORDER BY audit_logs.timestamp DESC 
        LIMIT 50
    """)
    
    logs = db.execute(sql).fetchall()
    return logs

# --- ADMIN ENDPOINT: CREATE USER ---
@app.post("/users", response_model=schemas.UserCreateResponse)
def create_user(
    new_user: schemas.UserCreateRequest,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Authorization Check
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    
    # 2. Check if username exists
    existing = db.execute(text("SELECT id FROM users WHERE username = :u"), {"u": new_user.username}).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    # 3. Generate Secure API Key

    generated_key = secrets.token_urlsafe(16)
    initial_credits = 100
    
    try:
        insert_query = text("""
            INSERT INTO users (username, api_key, role, credits)
            VALUES (:name, :key, :role, :creds)
            RETURNING username, api_key, role, credits
        """)
        
        created_user = db.execute(insert_query, {
            "name": new_user.username,
            "key": generated_key,
            "role": new_user.role,
            "creds": initial_credits
        }).fetchone()
        
        db.commit()
        return created_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")