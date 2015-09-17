from app import Request
from subprocess import call

COMMAND = "echo"

for request in Request.query.all():
    print("Do you want to generate a certificate for {}, {} ?".format(request.id, request.email))
    print("Type y to continue")
    confirm  = input('>')
    if confirm in ['Y', 'y']:
         print('generating certificate')
         call([COMMAND, request.id, request.email])
         print()
    else:
         print('skipping generation \n')
