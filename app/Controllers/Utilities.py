from flask import send_file
from io import BytesIO

class Utilities:
    def __init__(self):
        self.dpi=300
        pass

    #A wrapper for converting plot to BytesIO image
    def wrap_to_bytesio(self,plt):
        bytesIO = BytesIO()
        plt.savefig(bytesIO,dpi=self.dpi)
        bytesIO.seek(0)
        return bytesIO
    
    #return plot as image/png format
    #A wrapper for sending BytesIO object as png image around flask's send_file()
    def send_plot(self,plt,mimetype='image/png'):
        return send_file(plt,mimetype)

    