import statistics

def runFCFS(requests):
    print("FCFS")
    currHeadPos=0
    requests = sorted(requests, key=lambda req: req.arrivalTime)
    time=0
    ended = []
    distances = []
    distanceSum = 0
    while(requests):
        if(requests[0].arrivalTime<= time):
            current = requests[0]
            time+= abs(current.headPos-currHeadPos)
            distanceSum+= abs(current.headPos-currHeadPos)
            distances.append(abs(current.headPos-currHeadPos))
            ended.append(current)
            currHeadPos=current.headPos
            requests.remove(current)
        else:
            time+=1

    print("dystans pokonany: "+ str(distanceSum) )
    print("srednie wychylenie glowicy: "+ str(statistics.mean(distances))+'\n')



def runSSTF(requests):
    print("SSTF")
    time=0
    toDo= []
    ended = []
    distanceSum=0
    currHeadPos=0
    distances = []
    while(requests or toDo ):
        for r in requests:
            if r.arrivalTime<=time:
                toDo.append(r)
                requests.remove(r)

        if(not toDo):
            time+=1
        else:
            closest = toDo[0]
            for t in toDo:
                if(abs(currHeadPos-closest.headPos)>abs(currHeadPos-t.headPos)):
                        closest = t
            if(abs(closest.arrivalTime-time)>1000):
                print("Zagłodzony :"+ str(closest)+"czas oczekiwania "+str(abs(closest.arrivalTime-time)))
            d = abs(currHeadPos-closest.headPos)
            distanceSum += d
            time+=d
            distances.append(d)
            ended.append(closest)
            currHeadPos = closest.headPos
            toDo.remove(closest)

    print("dystans pokonany: " + str(distanceSum))
    print("srednie wychylenie glowicy: " + str(statistics.mean(distances)) + '\n')


def runSCAN(requests):
    print("SCAN")
    diskSize=200
    distanceSum=0
    currHeadPos=0
    requests = sorted(requests, key=lambda req: req.arrivalTime)
    direction=1

    queue=[]
    waitingQueue=[]
    changeOfdirection=0
    reqCount=len(requests)

    while(reqCount>0):
        for req in requests:
            if req.arrivalTime<=distanceSum:
                if(direction>0 and req.headPos>=currHeadPos) or(direction<0 and req.headPos<=currHeadPos):
                    queue.append(req)
                if(direction<0 and req.headPos>currHeadPos) or(direction>0 and req.headPos<currHeadPos):
                    waitingQueue.append(req)
                requests.remove(req)
        if(queue):
            if(direction>0):
                queue = sorted(queue, key=lambda q: q.headPos)
            else:
                queue = sorted(queue, key=lambda q: q.headPos,reverse=True)
            while(queue and queue[0].headPos==currHeadPos):

                queue.remove(queue[0])
                reqCount-=1

        distanceSum+=1
        currHeadPos+=direction
        if(currHeadPos==diskSize or currHeadPos==0):
            direction = -direction
            changeOfdirection+=1
            queue.extend(waitingQueue)
            waitingQueue = []

    print("dystans pokonany: " + str(distanceSum))
    print("ilosc zmian kierunkow: " +str( changeOfdirection) + '\n')



def runCSCAN(requests):
    print("CSCAN")
    diskSize=200
    distanceSum=0
    currHeadPos=0
    requests = sorted(requests, key=lambda req: req.arrivalTime)


    turns=0
    queue=[]
    waitingQueue=[]

    reqCount=len(requests)

    while(reqCount>0):
        for req in requests:
            if req.arrivalTime<=distanceSum:
                if(req.headPos>=currHeadPos):
                    queue.append(req)
                else:
                    waitingQueue.append(req)
                requests.remove(req)

        if(queue):
            queue = sorted(queue, key=lambda q: q.headPos)
            while(queue and queue[0].headPos==currHeadPos):
                queue.remove(queue[0])
                reqCount-=1

        distanceSum+=1
        currHeadPos+=1
        if(currHeadPos==diskSize+1):
            currHeadPos=0
            turns+=1
            queue.extend(waitingQueue)
            waitingQueue = []

    print("dystans pokonany: " + str(distanceSum))
    print("ilosc zawrocen: " + str(turns) + '\n')

def runEDF(requests):
    print("EDF")
    currHeadPos = 0
    requests = sorted(requests, key=lambda req:  req.arrivalTime)
    time = 0
    ended = []
    distances = []
    distanceSum = 0
    toDo=[]
    while (requests or toDo):
        for r in requests:
            if r.arrivalTime <= time:
                toDo.append(r)
                requests.remove(r)

        if (not toDo):
            time += 1
        else:
            toDo = sorted(toDo, key=lambda req: (req.deadline,req.arrivalTime))
            current = toDo[0]
            time += abs(current.headPos - currHeadPos)
            distanceSum += abs(current.headPos - currHeadPos)
            distances.append(abs(current.headPos - currHeadPos))
            ended.append(current)
            currHeadPos = current.headPos
            toDo.remove(current)


    print("dystans pokonany: "+ str(distanceSum) +'\n')


def runFDSCAN(requests):
    print("FDSCAN")
    diskSize = 200
    distanceSum = 0
    currHeadPos = 0
    requests = sorted(requests, key=lambda req: req.arrivalTime)
    direction = 1

    queue = []
    waitingQueue = []
    reqCount = len(requests)
    turns=0
    while (reqCount > 0):
        for req in requests:
            if req.arrivalTime <= distanceSum:
                thrown = False
                if(req.deadline!=diskSize+1 and abs(req.headPos-currHeadPos)>req.deadline):
                    print("Niemożliwy do obsluzenia "+"Aktualna pozycja glowicy "+str(currHeadPos)+" docelowa pozycja " +str(req.headPos)+" deadline "+str(req.deadline))
                    req.direction=0

                elif(req.deadline!=diskSize+1):
                    if(currHeadPos>req.headPos):
                        turns+=1
                        direction=-1
                    else:
                        turns += 1
                        direction=1
                if ((direction > 0 and req.headPos >= currHeadPos) or (direction < 0 and req.headPos <= currHeadPos)):
                    queue.append(req)
                if ((direction < 0 and req.headPos > currHeadPos) or (direction > 0 and req.headPos < currHeadPos)):
                    waitingQueue.append(req)
                if(not thrown):
                    requests.remove(req)
        if (queue):
            if (direction > 0):
                queue = sorted(queue, key=lambda q: (q.deadline,q.headPos))
            else:
                queue = sorted(queue, key=lambda q: (q.deadline,q.headPos), reverse=True)
            while (queue and queue[0].headPos == currHeadPos):
                queue.remove(queue[0])
                reqCount -= 1

        distanceSum += 1
        currHeadPos += direction

        if (currHeadPos == diskSize or currHeadPos == 0):
            direction = -direction
            turns += 1
            queue.extend(waitingQueue)
            waitingQueue = []

    print("dystans pokonany: " + str(distanceSum))
    print("ilosc zmian kierunkow: " + str(turns) + '\n')