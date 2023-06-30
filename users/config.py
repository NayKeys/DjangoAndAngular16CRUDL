ROLE_PERMISSIONS = {
  'student': {
    'student': '_r__',
    'teacher': '_r__',
    'admin': '_r__',
    'parent': 'id',
  },
  'teacher': {
    'student': '_ru_',
    'teacher': '_r__',
    'admin': '_r__',
    'parent': '_r__',
  },
  'parent': {
    'student': 'id',
    'teacher': '____',
    'admin': '____',
    'parent': '____',
  },
  'schooladmin': {
    'student': 'crud',
    'teacher': '_ru_',
    'admin': '_r__',
    'parent': 'crud',
  },
  'admin': {
    'student': 'crud',
    'teacher': 'crud',
    'admin': 'crud',
    'parent': 'crud',
  },
}

USERS = {
  'student': [
    {
      'username': 'student1',
      'parent': ['parent1'],
    },
    {
      'username': 'student2',
      'parent': ['parent2'],
    },
    {
      'username': 'student3',
      'parent': ['parent3'],
    },
    {
      'username': 'student4',
      'parent': ['parent4'],
    },
    {
      'username': 'student4',
      'parent': ['parent4'],
    },
  ],
  'parent': [
    {
      'username': 'teacher1',
      'student': ['student1'],
    },
    {
      'username': 'teacher2',
      'student': ['student2'],
    },
    {
      'username': 'teacher3',
      'student': ['student3'],
    },
    {
      'username': 'teacher4',
      'student': ['student4'],
    },
    {
      'username': 'teacher5',
      'student': ['student5'],
    },
  ],
  'teacher': [
    { 'username': 'teacher1' },
    { 'username': 'teacher2' },
    { 'username': 'teacher3' },
    { 'username': 'teacher4' },
    { 'username': 'teacher5' },
  ],
  'schooladmin': [
    { 'username': 'school1' },
    { 'username': 'school2' },
    { 'username': 'school3' },
    { 'username': 'school4' },
    { 'username': 'school5' },
  ],
  'admin': [
    { 'username': 'admin1' },
    { 'username': 'admin2' },
    { 'username': 'admin3' },
    { 'username': 'admin4' },
    { 'username': 'admin5' },
  ],
}