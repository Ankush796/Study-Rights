from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Study Rights"]
lectures = db["lectures"]

def add_subject(subject_name: str):
    if not lectures.find_one({"subject": subject_name}):
        lectures.insert_one({
            "subject": subject_name,
            "faculties": []
        })

def add_faculty(subject_name: str, faculty_name: str):
    lectures.update_one(
        {"subject": subject_name, "faculties.name": {"$ne": faculty_name}},
        {"$push": {"faculties": {"name": faculty_name, "chapters": []}}}
    )

def add_chapter(subject_name: str, faculty_name: str, chapter_name: str, link: str):
    lectures.update_one(
        {"subject": subject_name, "faculties.name": faculty_name},
        {"$push": {"faculties.$.chapters": {"name": chapter_name, "link": link}}}
    )

def get_subjects():
    return [s["subject"] for s in lectures.find()]

def get_faculties(subject_name: str):
    subject = lectures.find_one({"subject": subject_name})
    return [f["name"] for f in subject["faculties"]] if subject else []

def get_chapters(subject_name: str, faculty_name: str):
    subject = lectures.find_one({"subject": subject_name})
    if subject:
        for f in subject["faculties"]:
            if f["name"] == faculty_name:
                return f["chapters"]
    return []

