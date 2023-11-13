
class User():
    def __init__(self,fetched_query:str) -> None:
        self.parse_SQL(fetched_query)        

    def parse_SQL(self,fetched_query):
        self.id = fetched_query['userid']
        self.email = fetched_query['email']
        self.password = fetched_query['password']
        self.personal_token = fetched_query['personal_token']
        self.org_name = fetched_query["org_name"]
        self.external_token = fetched_query["external_token"]
        self.role = fetched_query["role"]
        self.is_confirmed = fetched_query["is_confirmed"]
    
    def __repr__(self) -> str:
        string = '<pre>'
        string += f"""
ID: {str(self.id)}
    email: {self.email}
    personal token: {self.personal_token}
    org. name: {str(self.org_name)}
    external token : {self.external_token}
    role : {self.role}
    is_confirmed : {self.is_confirmed}
"""
        string+="</pre>"
        return(string)
    
    def __str__(self) -> str:
        
        string = f"""
ID: {str(self.id)}
    email: {self.email}
    personal token: {self.personal_token}
    org. name: {str(self.org_name)}
    external token : {self.external_token}
    role : {self.role}
    is_confirmed : {self.is_confirmed}
"""
        
        return(string)


    
class All_users():
    def __init__(self) -> None:
        self.N_users = 0
        self.users = list()

    def add_user(self,user:User):
        self.users.append(user)
        self.N_users +=1
    def __str__(self) -> str:
        for x in self.users:
            print(x)
        return ""
    def __repr__(self) -> str:
        string = ''
        for x in self.users:
            string += repr(x)+"\n"
        
        return string
    