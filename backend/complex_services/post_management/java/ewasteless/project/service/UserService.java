package ewasteless.project.service;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

// Firebase imports
import com.google.api.core.ApiFuture;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.DocumentSnapshot;
import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.QuerySnapshot;

// Model import
import ewasteless.project.classes.User;

@Service
public class UserService {

    @Autowired
    private Firestore dbFirestore;

    public boolean deleteUser(String UID) throws Exception {
        dbFirestore.collection("users").document(UID).delete().get();
        return true;
    }

    



    public User getUserByUID(String UID) throws Exception {
        DocumentReference documentReference = dbFirestore.collection("users").document(UID);
        ApiFuture<DocumentSnapshot> future = documentReference.get();
        DocumentSnapshot document = future.get();

        if (document.exists()) {
            return document.toObject(User.class);
        } else {
            return null;
        }
    }


    
}

