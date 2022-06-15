class Configurations:

    def get_configuarations():
        config = {
            "CORS":{r'/*':{'origins':'*'}},
            "PORT":8000,
            "DEBUG":True
                }
        return config
        