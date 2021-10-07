class Config:
    DEBUG = True
    
    URL_START = "http://localhost:5000/"
    if not DEBUG:
        URL_START = "https://greyshortner.herokuapp.com/"
        
            

        