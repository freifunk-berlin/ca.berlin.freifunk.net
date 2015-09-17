import datetime
from subprocess import call

from app import Request, db

COMMAND = "echo"

for request in Request.query.filter(Request.generation_date == None).all():
    print("Do you want to generate a certificate for {}, {} ?".format(request.id, request.email))
    print("Type y to continue")
    confirm = input('>')
    if confirm in ['Y', 'y']:
        print('generating certificate')
        call([COMMAND, request.id, request.email])
        request.generation_date = datetime.date.today()
        db.session.commit()
        print()
    else:
        print('skipping generation \n')
