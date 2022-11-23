import requests
# import json
import dateutil.parser


# this function let us get the data from the Slang's API
def firstStep(url, headers):
    print("requesting to Slang API\n")
    requestToAPISlang = requests(url, headers = headers)
    responseOfAPISlang = requestToAPISlang.json()
    print(f"Slang API's response: \n{responseOfAPISlang}")
    
    return responseOfAPISlang
# Class that let us to process the receved data by the first step
class SedondStep():
    def __init__(self,listActivities): # when the class is instantiated, the constructor receives the data
        self.listActivities = listActivities
        self.user_session_preProd = {}
        
    # source: https://www.geeksforgeeks.org/python-program-for-heap-sort/
    # Heapsort, Choosen because its complexity, in any case, is O(nlog(n))
    # Note: remember that the best sorting algorithms have a runtime complexity between n^2 and nlog(n)  
    def __heapify(self,arr, n, i):
        largest = i  
        l = 2 * i + 1  
        r = 2 * i + 2
        
        if l < n and dateutil.parser.isoparse(arr[i]['first_seen_at']) < dateutil.parser.isoparse(arr[l]['first_seen_at']):
            largest = l
        if r < n and dateutil.parser.isoparse(arr[largest]['first_seen_at']) < dateutil.parser.isoparse(arr[r]['first_seen_at']):
            largest = r
        if largest != i:
            (arr[i]['first_seen_at'], arr[largest]['first_seen_at']) = (arr[largest]['first_seen_at'], arr[i]['first_seen_at'])  # swap
            self.__heapify(arr, n, largest)       
    def __heapSort(self,arr):
        n = len(arr)
        
        for i in range(n // 2 - 1, -1, -1):
            self.__heapify(arr, n, i)
            
        for i in range(n - 1, 0, -1):
            (arr[i], arr[0]) = (arr[0], arr[i])
            self.__heapify(arr, i, 0)

        return arr
    
    def orderBytimestamp(self,activities): # in case that the data is disordered, It's ordered using heapsort based on the "first_seen_at" 
        return self.__heapSort(activities)

    def differenceTimeStamp (self, answered_at , started_at): # method that it gets the diference between two given timestamps (answered_at, started_at)
        return(dateutil.parser.isoparse(answered_at) - dateutil.parser.isoparse(started_at)).total_seconds()/60

    # Method that process the activities and returns a list of user session objects that contains the data
    # Its runtime complexity, in any case, is O(n) such that n depends on the number of user activities 
    def getSessions(self,activities): 
        sessions = []
        started_at = activities[0]["first_seen_at"]
        session = {
                    "ended_at":"",
                    "started_at":started_at,
                    "activity_ids":[activities[0]["id"]],
                    "duration_seconds":0.00
                }
        for i in range(len(activities)):
            if i < len(activities)-1:
                duration = self.differenceTimeStamp(activities[i+1]["answered_at"],started_at)
                if duration <= 5.0:
                    session["activity_ids"].append(activities[i+1]["id"])
                else:
                    session["ended_at"] = activities[i]["answered_at"]
                    session["duration_seconds"] = duration * 60.0
                    sessions.append(session)
                    started_at = activities[i+1]["first_seen_at"]
                    session = {
                        "ended_at":"",
                        "started_at":started_at,
                        "activity_ids":[activities[i+1]["id"]],
                        "duration_seconds":0.00
                    }
            else:
                session["ended_at"] = activities[i]["answered_at"]
                session["duration_seconds"] = self.differenceTimeStamp(activities[i]["answered_at"],started_at) * 60.0
                sessions.append(session)
                
        
        
        return sessions

    # method that process the received data by the constructor, its runtime complexity, in any case, is O(n) such that n depends on the number of user activities
    def process_activities(self): 
        user_session_preProd = {i["user_id"]: []  for i in self.listActivities} # O(n) such that n depends on the number of user activities
        user_session_preProd1 = {}
        
        # the data is grouped based on user_id with a list of their activities
        for i in self.listActivities: # O(n) such that n depends on the number of user activities
            user_session_preProd[i["user_id"]].append({'id': i['id'],'answered_at':i['answered_at'],'first_seen_at':i['first_seen_at']}) 
        print("")
        
        # each list of users activities is sorted
        for key,value in user_session_preProd.items(): # O(n*mlog(m)) such that n depends on the number of users and m depends on the number of activities
            user_session_preProd[key] = self.orderBytimestamp(value) 

        # each list of user activities is sorted by user session
        for key,value in user_session_preProd.items(): # O(n*m) such that n depends on the number of users and m depends on the number of activities
            print(key,value)
            user_session_preProd1[key] = self.getSessions(value)
            print("\n")
            print(user_session_preProd1[key])
            print("\n")
        
        return user_session_preProd1
    
    # method that returns the data processed (dictionary of user sessions)
    def userSessions(self):
        print("Processing user sessions\n")
        return self.process_activities()
    

def thirdStep(url,headers,userSessions):
    print("Sending the data processed to Slang's API\n")
    requests.post(url,headers=headers,json=userSessions)


if __name__ == '__main__':
    url = "https://api.slangapp.com/challenges/v1/activities"
    
    headers = {
                "Content-Type": "application/json", 
                "Authorization":"Basic MTM4OmFaVlZ1MUdWVisxWTJOaTE1TW1RU3p0eEU1b045UElieTk4MFhvUWdMTms9"
            }
    
    responseOfAPISlang = firstStep(url,headers) # get the data from Slang's API
    s = SedondStep(responseOfAPISlang) # Processing the data 
    thirdStep(url,headers,s.userSessions()) # Posting the data processed to Slang's API'
    