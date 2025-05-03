from app import app, db  
from models import Incident

def seed_data():
    
    with app.app_context():
        db.drop_all()
        db.create_all()

        sample_incidents = [
            Incident(
                title="Autonomous vehicle crash",
                description="AI failed to stop at red light",
                severity="High"
            ),
            Incident(
                title="AI bias in resume screening",
                description="AI favored male candidates disproportionately",
                severity="Medium"
            ),
            Incident(
                title="Incorrect medical diagnosis",
                description="AI misdiagnosed patient due to limited dataset",
                severity="High"
            ),
        ]

        db.session.bulk_save_objects(sample_incidents)
        db.session.commit()
        print("Sample incidents added!")

if __name__ == "__main__":
    seed_data()
