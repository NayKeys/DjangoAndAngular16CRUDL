ROLE_PERMISSIONS = {
  'student': {
    'view1': '_r__',
    'view2': '_r__',
    'view3': '_r__',
    'view4': '<spe>',
  },
  'teacher': {
    'view1': '_ru_',
    'view2': '_r__',
    'view3': '_r__',
    'view4': '_r__',
  },
  'parent': {
    'view1': '<spe>',
    'view2': '____',
    'view3': '____',
    'view4': '____',
  },
  'schooladmin': {
    'view1': 'crud',
    'view2': '_ru_',
    'view3': '_r__',
    'view4': 'crud',
  },
  'admin': {
    'view1': 'crud',
    'view2': 'crud',
    'view3': 'crud',
    'view4': 'crud',
  },
}

USERS = {
  'student': [
    {
      'username': 'student1',
      'view4': ['element1'],
    },
    {
      'username': 'student2',
      'view4': ['element2'],
    },
    {
      'username': 'student3',
      'view4': ['element3'],
    },
    {
      'username': 'student4',
      'view4': ['element4'],
    },
    {
      'username': 'student5',
      'view4': ['element5'],
    },
  ],
  'parent': [
    {
      'username': 'teacher1',
      'view1': ['element1'],
    },
    {
      'username': 'teacher2',
      'view1': ['element2'],
    },
    {
      'username': 'teacher3',
      'view1': ['element3'],
    },
    {
      'username': 'teacher4',
      'view1': ['element4'],
    },
    {
      'username': 'teacher5',
      'view1': ['element5'],
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
    { 'username': 'yanregoj64' },
  ],
}