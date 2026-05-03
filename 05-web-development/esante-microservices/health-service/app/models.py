"""
MongoDB document schemas (documentation — no ORM needed with MongoDB).

Collection: patients
{
    "_id": ObjectId,
    "doctor_id": int,
    "first_name": str,
    "last_name": str,
    "date_of_birth": str (YYYY-MM-DD),
    "gender": int (0=Female, 1=Male),
    "created_at": datetime,
    "updated_at": datetime
}

Collection: health_data
{
    "_id": ObjectId,
    "patient_id": str,
    "doctor_id": int,
    "data": {
        "age": int,
        "gender": int,
        "smoking": int (0-10),
        "alcohol_use": int (0-10),
        "obesity": int (0-10),
        "family_history": bool,
        "diet_red_meat": int (0-10),
        "diet_salted_processed": int (0-10),
        "fruit_veg_intake": int (0-10),
        "physical_activity": int (0-10),
        "air_pollution": int (0-10),
        "occupational_hazards": int (0-10),
        "brca_mutation": bool,
        "h_pylori_infection": bool,
        "calcium_intake": int (0-10),
        "bmi": float,
        "physical_activity_level": int (0-10)
    },
    "created_at": datetime
}

Collection: predictions
{
    "_id": ObjectId,
    "patient_id": str,
    "doctor_id": int,
    "risk_level": str ("Low" | "Medium" | "High"),
    "confidence": float (0.0 - 1.0),
    "status": str ("pending" | "completed" | "error"),
    "created_at": datetime
}
"""
