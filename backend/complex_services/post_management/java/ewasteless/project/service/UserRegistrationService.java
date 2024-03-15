package ewasteless.project.service;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.google.api.core.ApiFuture;
import com.google.cloud.firestore.CollectionReference;
// Firebase imports
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.QuerySnapshot;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.UserRecord;

// Java imports
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutionException;

// Model imports
import ewasteless.project.DTO.UserDTO;

@Service
public class UserRegistrationService {

    @Autowired
    private Firestore dbFirestore;

    // Expects User object from UserRegistrationController 
    // Returns UID of successful new user
    public String signUp(UserDTO user) throws InterruptedException, ExecutionException {

        CollectionReference usersRef = dbFirestore.collection("users");

        // Check if the username already exists
        ApiFuture<QuerySnapshot> query = usersRef.whereEqualTo("username", user.getUsername()).get();
        if (!query.get().isEmpty()) {
            // Username is already taken
            throw new RuntimeException("Username is already taken");
        }
        try {
            
            UserRecord.CreateRequest createRequest = new UserRecord.CreateRequest()
            .setEmail(user.getEmail())
            .setPassword(user.getPassword())
            .setDisplayName(user.getUsername()); // This sets the display name in Firebase Auth

            UserRecord userRecord = FirebaseAuth.getInstance().createUser(createRequest);
            

            // Create user in firestore with matching DocID
            DocumentReference userReference = dbFirestore.collection("users").document(userRecord.getUid());
            Map<String, Object> userProfileMap = new HashMap<>();

            // Populate user fields with:
            userProfileMap.put("email", user.getEmail());
            userProfileMap.put("name", user.getName());
            userProfileMap.put("username", user.getUsername());
            userProfileMap.put("UID", userRecord.getUid());
            userProfileMap.put("forumScore", 0);
            // ... add any other fields you want here
            userReference.set(userProfileMap);
            return userRecord.getUid(); 
        } catch (FirebaseAuthException e) {
            // handle exception
            throw new RuntimeException("Failed to register user");
        }
    }
}

