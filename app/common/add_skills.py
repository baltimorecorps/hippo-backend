from app.models.skill_model import (
    Skill, 
    Capability, 
    SkillRecommendation,
    CapabilitySkillSuggestion
)
from app.resources.skill_utils import get_skill_id, get_or_make_skill

CAPABILITIES = {
    ('cap:advocacy', 'Advocacy and Public Policy'): [
        'Advocacy',
        'Public Policy',
        'Community Organizing',
        'Canvassing',
        'Volunteer Mobilization',
    ],
    ('cap:outreach', 'Community Engagement and Outreach'): [
        'Community Engagement',
        'Community Organizing',
        'Client Recruitment',
        'Partnership Building',
        'Event Planning',
    ],
    ('cap:analysis', 'Data Analysis'): [
        'Metrics',
        'Data Visualization',
        'Microsoft Excel',
        'R',
        'Python',
    ],
    ('cap:fundraising', 'Fundraising and Development'): [
        'Fundraising',
        'Business Development',
        'Grant Coordination',
        'Grant Writing',
        'Strategic Management',
    ],
    ('cap:marketing', 'Marketing and Public Relations'): [
        'Marketing',
        'Public Relations',
        'Social Media Management',
        'SEO',
        'Media Management' ,
        'Community Relations',
    ],
    ('cap:operations', 'Operations and Administration'): [
        'Operations Management',
        'Business Administration',
        'Portfolio Management',
        'Public Administration',
        'Strategic Planning',
    ],
    ('cap:prog_mgmt', 'Program Management'): [
        'Task Management',
        'Quality Management',
        'Budgeting',
        'Risk Management',
        'Program Management',
    ]
}

def capabilities_to_skills(): 
    skills = set()
    for capability in CAPABILITIES:
        skills.update(CAPABILITIES[capability])
    return skills

def get_capability(id_):
    return Capability.query.get(id_)

def get_skill(name):
    return Skill.query.get(get_skill_id(name))

def populate(db):
    for name in capabilities_to_skills():
        db.session.add(get_or_make_skill(name))
    for id_, name in CAPABILITIES:
        db.session.add(Capability(id=id_, name=name))
    db.session.commit()

    for cap in CAPABILITIES:
        db_cap = get_capability(cap[0])
        for (i, name) in enumerate(CAPABILITIES[cap]):
            db.session.add(SkillRecommendation(
                capability_id=cap[0],
                skill_id=get_skill_id(name),
                order=i
            ))
            db_cap.related_skills.append(get_skill(name))
    db.session.commit()
