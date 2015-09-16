from app import Request
from subprocess import call

COMMAND = "echo"

for request in Request.query.all():
    call([COMMAND, request.id, request.email])
