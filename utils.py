from datetime import timezone
from config.constants import ERROR, MESSAGE, DESCRIPTION

def convert2Local(utcDT):
    #Assumption: the server is local
    return utcDT.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None)

def createResponse(status, message, description=''):
    return {
        ERROR: status,
        MESSAGE: message,
        DESCRIPTION: description
    }