from binance.client import Client
import config

class Connect:
    def make_connection(self):
        #Write your api keys here

        # Demo Keys
        api_key = "49TAi8MMYQhgQEcP5OG45hPYWAfvmOtEimHYkPz948iImY1o3hSP7mtWxz2ui60y"
        api_secret = "SkMIpu4jK8aqcoADBTyLCIWkk4qLI2sUZyE4ge3jGsumh22llWEWo3R9Uv4L4Wx0"

        # # Live Keys
        # api_key = "BTdaIWF1lja6IwHJCbEwt9ZLAJFI9dw0M3noZAbwdPT4zbpilp6ewISTEOTznA36"
        # api_secret = "LPwbn33DvHN9v3nBL54dsmR8mchNNVFQQYchybQARcXNZMgTFG2RRTbsRMpQpVMP"
        
        
        return Client(api_key, api_secret)