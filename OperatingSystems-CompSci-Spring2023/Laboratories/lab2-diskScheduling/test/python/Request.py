class Request:
    def __init__(self,arrivaltime,pos,deadline):
        self.arrivalTime=arrivaltime
        self.headPos=  pos
        self.deadline = deadline

    def __repr__(self):
        return "Czas pojawienia: " +str( self.arrivalTime) + " " + "Nr cylindra: " + str(self.headPos) + " " + "Deadline: "+ str(self.deadline)+'\n'




