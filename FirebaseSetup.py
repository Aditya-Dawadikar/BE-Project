from firebase_admin import credentials, initialize_app, storage,firestore
from Config import storageconfig

class FirebaseSetup:
    def __init__(self):
        self.cred = credentials.Certificate("Config/be-project-4b4bf-firebase-adminsdk-wjqnp-4dd24d1742.json")
        self.app = initialize_app(self.cred,{'storageBucket': storageconfig.firebaseConfig["storageBucket"]})
        # file storage
        self.bucket = storage.bucket()

        # audio meta storage
        self.db = firestore.client()
        self.audioMetaCollection = self.db.collection('audio_meta')
        
        
    def getStorageBucket(self):
        return self.bucket
    
    def getAudioMetaCollection(self):
        return self.audioMetaCollection
    
    
fbs = FirebaseSetup()
    