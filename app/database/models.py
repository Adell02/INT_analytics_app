
class User():
    def __init__(self,fetched_query:str) -> None:
        self.parse_SQL(fetched_query)        

    def parse_SQL(self,fetched_query):
        self.id = fetched_query[0]
        self.email = fetched_query[1]
        self.password = fetched_query[2]
        self.company = fetched_query[3]
        self.role = fetched_query[4]
        self.is_confirmed = fetched_query[5]
    
    def __repr__(self) -> str:
        string = '<pre>'
        string += f"""
ID: {str(self.id)}
    email: {self.email}
    company: {self.company}
    is_confirmed: {str(self.is_confirmed)}
"""
        string+="</pre>"
        return(string)
    
    def __str__(self) -> str:
        
        string = f"""
ID: {str(self.id)}
    email: {self.email}
    company: {self.company}
    is_confirmed: {str(self.is_confirmed)}
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
    