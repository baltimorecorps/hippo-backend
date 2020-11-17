
SKILLS_NAMES = [
    'Python',
    'C++',
    'Web Development',
    'Public Health',
    'Advocacy and Public Policy',
    'Community Organizing',
    'Canvassing',
    'Advocacy',
    'Policy Writing',
    'Volunteer Mobilization',
    'Community Engagement and Outreach',
    'Community Engagement',
    'Client Recruitment',
    'Partnership Building',
    'Event Planning',
    'Information Technology',
    'Flask',
]

SKILLS_API = {
    'community_organizing': {
        'id': '74BgThI2os9wEdyArofEKA==',
        'name': 'Community Organizing',
    },
    'flask': {
        'id': 'QUEVjv1tcq6uLmzCku6ikg==',
        'name': 'Flask'
    },
    'public_health': {
        'id': 'n1N02ypni69EZg0SggRIIg==',
        'name': 'Public Health',
    },
    'python': {
        'id': '4R9tqGuK2672PavRTJrN_A==',
        'name': 'Python',
    },
    'web_dev': {
        'id': 'hbBWJS6x6gDxGMUC5HAOYg==',
        'name': 'Web Development',
    },
}


CONTACT_SKILLS = {
    'billy': [
        SKILLS_API['community_organizing'],
        SKILLS_API['flask'],
        SKILLS_API['public_health'],
        SKILLS_API['python'],
        SKILLS_API['web_dev'],
    ],
    'obama': [
        SKILLS_API['public_health']
    ],
}

CAPABILITIES_API = {
    'billy': {
        'contact_id': 123,
        'capabilities': [
            {
                'id': 'cap:it',
                'name': 'Information Technology',
                'score': 2,
                'skills': [
                    SKILLS_API['python'],
                    SKILLS_API['web_dev']
                ],
                'suggested_skills': [
                    SKILLS_API['flask']
                ]
            },
            {
                'id': 'cap:advocacy',
                'name': 'Advocacy and Public Policy',
                'score': 1,
                'skills': [
                    SKILLS_API['community_organizing']
                ],
                'suggested_skills': []
            },
            {
                'id': 'cap:outreach',
                'name': 'Community Engagement and Outreach',
                'score': 0,
                'skills': [
                    SKILLS_API['community_organizing']
                ],
                'suggested_skills': []
            }
        ],
        'other_skills': [
            SKILLS_API['public_health']
        ]
    }
}
