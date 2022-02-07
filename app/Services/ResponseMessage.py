class ResponseMessage:
    def __init__(self):
        pass
    
    def dataNotFound(self):
        return {
            "message":"data not found"
        },404
        
    def internalServerError(self):
        return {
            "message":"Internal server error occured"
        },500
        
    def badRequest(self):
        return {
            "message":"request cannot be processed"
        },400
        
    def authRequired(self):
        return {
            "message":"Auth is required"
        },401
        
    def resourceCreated(self):
        return {
            "message":"new resource created"
        },201
        
    def resourceCreatedSendDetails(self,details):
        return {
            "message":"new resource created",
            "details":details
        },201
        
    def requestOk(self):
        return {
            "message":"request processed successfully"
        },200
        
    def requestOkSendDetails(self,detials):
        return { 
            "message":"request processed successfully",
            "details":details
        },200
        
    def requestOkSendData(self,data):
        return { 
            "message":"request processed successfully",
            "data":data
        },200
        
    
    def dataMissing(self,data):
        return {
            "message":"missing json key-value pair",
        },400
    
rm = ResponseMessage()