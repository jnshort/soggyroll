validator = {
    'validator': {
        '$jsonSchema': {
            'description': 'An anime that is being tracked by my program',
            'required': ['name', 'url', 'current_episode', 'episodes'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'name': {
                    'bsonType': 'string',
                    'description': 'name of the anime',
                },
                'current_episode': {
                    'bsonType': 'int',
                    'description': 'Next unwatched episode'
                },
                'url': {
                    'bsonType': 'string',
                    'description': 'url of anime episode list'
                },
                'episodes': {
                    'bsonType': 'array',
                    'description': 'list of episodes',
                    'minItems': 0,
                    'uniqueItems': True,
                    'items': {
                        'bsonType': 'object',
                        'description': 'individual episode of an anime',
                        'required': ['name',  'episode_number', 'url'],
                        'additionalProperties': False,
                        'properties': {
                            'name': {
                                'bsonType': 'string',
                                'description': 'name of the anime',
                            },
                            'episode_number': {
                                'bsonType': 'int',
                                'description': 'episode number in season'
                            },
                            'url': {
                                'bsonType': 'string',
                                'description': 'full url of the episode'
                            },
                        }
                    }
                }
            }
        }
    }
}
