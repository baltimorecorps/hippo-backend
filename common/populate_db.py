from datetime import date

from models.contact_model import Contact, Gender, Race, Salutation
from models.email_model import Email, Type as EmailType

billy = Contact(
    id=123,
    first_name='Billy',
    last_name='Daly',
    email_primary=Email(
        id=45,
        is_primary=True,
        email='billy@example.com',
        type=EmailType('Personal'),
    ),
    gender=Gender('Male'),
    birthdate=date(1991, 1, 2),
    phone_primary='555-245-2351',
    race_all=Race('White'),
)
obama = Contact(
    id=124,
    first_name='Barack',
    last_name='Obama',
    email_primary=Email(
        id=90,
        is_primary=True,
        email='obama@whitehouse.gov',
        type=EmailType('Work'),
    ),
    gender=Gender('Male'),
    birthdate=date(1961, 8, 4),
    phone_primary='555-444-4444',
    race_all=Race('Black'),
)

def populate(db):
    db.session.add(billy)
    db.session.add(obama)
    db.session.commit()
