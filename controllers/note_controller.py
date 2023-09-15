# GET /notes
# POST /people/{person_id}/notes
# GET /people/{person_id}/notes/{note_id}
# PUT /people/{person_id}/notes/{note_id}
# DELETE /people/{person_id}/notes/{note_id}
from models.person_model import Person
from models.note_model import Note, NoteSchema
from flask import abort
from config import db

def create(person_id, note):

    #find person by id
    person = {
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    }

    #if person not exist abort
    if person is None:
        abort(404, f"Person with id {person_id} is not found")
    else:
        #if exist, add new note the that person
        content = note.get('content')
        new_note = Note(content = content, person_id = person.person_id)

        person.notes.append(new_note)
        # person.create_note()

        #person.save()
        db.session.commit()

        note_schema = NoteSchema()
        result = note_schema.dump(new_note)

        return result

def read_one(person_id, note_id):
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
        .filter(Note.note_id == note_id)
        .one_or_none()
    )

    print(note, "<<<<<<<")

    if note is None:
        abort(404, f"Note with id {note_id} own by person id {person_id} is not found")
    
    note_schema = NoteSchema()
    result = note_schema.dump(note)

    return result

def update(person_id, note_id, note):
    found_note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
            .filter(Note.note_id == note_id)
            .one_or_none()
    )

    if found_note is None:
        abort(404, f"Note with id {note_id} own by person id {person_id} is not found")
    
    content = note.get('content')
    found_note.update(content)

    note_schema = NoteSchema()
    result = note_schema.dump(found_note)

    return result