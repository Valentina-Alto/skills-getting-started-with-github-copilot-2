"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports Activities
    "Basketball Team": {
        "description": "Competitive basketball team competing in regional tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "sarah@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Learn soccer skills and participate in inter-school matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "maya@mergington.edu"]
    },
    # Artistic Activities
    "Drama Club": {
        "description": "Explore acting, stage performance, and theater production",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lily@mergington.edu", "noah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Creative painting, drawing, and visual arts workshops",
        "schedule": "Fridays, 2:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu", "ethan@mergington.edu"]
    },
    # Intellectual Activities
    "Debate Society": {
        "description": "Develop critical thinking and public speaking through competitive debates",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments, explore STEM topics, and participate in science fairs",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ava@mergington.edu", "mason@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants/{email}")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if participant exists
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")

    # Remove participant
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
