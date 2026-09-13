import database as db

def reset_second_milestones():
    conn = db.get_db_connection()
    
    # Target Milestone 2 specifically (matching by title or sequence)
    conn.execute("""
        UPDATE milestones 
        SET status = 'Pending Review', 
            certificate_signature = NULL 
        WHERE title LIKE '%Milestone 2%' 
            OR title LIKE '%District Pilot Deployment%'
    """)
    
    conn.commit()
    conn.close()
    print("✅ Successfully reset Milestone 2 across all accounts to 'Pending Review'. Milestone 1 remains untouched!")

if __name__ == "__main__":
    reset_second_milestones()