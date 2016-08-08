# -*- coding: utf-8 -*-

from good import Schema, Required, Email, Optional, In, All, Length, Match

signup_schema = Schema({
    Required('name'): unicode,
    Required('password'): All(unicode, Length(min=3, max=32)),
    Required('email'): Email(),
    Required('phone'): All(unicode, Length(11), Match('^09[0-9]{9}$'), lambda n: int(n)),
    Required('student_id'): All(unicode, Length(min=8, max=9), lambda x: int(x)),
    Required('university'): In('iust', 'sharif', 'tehran', 'other'),
    Optional('national_code'): All(unicode, Length(10)),
})
