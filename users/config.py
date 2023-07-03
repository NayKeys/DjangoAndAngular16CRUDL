view_1 = "view_1"
view_2 = "view_2"
view_3 = "view_3"
view_4 = "view_4"

student = "student"
teacher = "teacher"
parent = "parent"
schooladmin = "schooladmin"
admin = "admin"

ROLE_PERMISSIONS = {
  student: {
    view_1: '_r__',
    view_2: '_r__',
    view_3: '_r__',
    view_4: '<spe>',
  },
  teacher: {
    view_1: '_ru_',
    view_2: '_r__',
    view_3: '_r__',
    view_4: '_r__',
  },
  parent: {
    view_1: '<spe>',
    view_2: '____',
    view_3: '____',
    view_4: '____',
  },
  schooladmin: {
    view_1: 'crud',
    view_2: '_ru_',
    view_3: '_r__',
    view_4: 'crud',
  },
  admin: {
    view_1: 'crud',
    view_2: 'crud',
    view_3: 'crud',
    view_4: 'crud',
  },
}

USERS = {
  student: [
    {
      'username': 'student1',
      view_4: ['element1'],
    },
    {
      'username': 'student2',
      view_4: ['element2'],
    },
    {
      'username': 'student3',
      view_4: ['element3'],
    },
    {
      'username': 'student4',
      view_4: ['element4'],
    },
    {
      'username': 'student5',
      view_4: ['element5'],
    },
  ],
  parent: [
    {
      'username': 'teacher1',
      view_1: ['element1'],
    },
    {
      'username': 'teacher2',
      view_1: ['element2'],
    },
    {
      'username': 'teacher3',
      view_1: ['element3'],
    },
    {
      'username': 'teacher4',
      view_1: ['element4'],
    },
    {
      'username': 'teacher5',
      view_1: ['element5'],
    },
  ],
  teacher: [
    { 'username': 'teacher1' },
    { 'username': 'teacher2' },
    { 'username': 'teacher3' },
    { 'username': 'teacher4' },
    { 'username': 'teacher5' },
  ],
  schooladmin: [
    { 'username': 'school1' },
    { 'username': 'school2' },
    { 'username': 'school3' },
    { 'username': 'school4' },
    { 'username': 'school5' },
  ],
  admin: [
    { 'username': 'admin1' },
    { 'username': 'admin2' },
    { 'username': 'admin3' },
    { 'username': 'admin4' },
    { 'username': 'admin5' },
    { 'username': 'yanregoj64' },
  ],
}