package ewasteless.project.service;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.Firestore;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.UserRecord;

import ewasteless.project.DTO.UserDTO;

@Service
public class UserAuthenticationService {

    @Autowired
    private Firestore dbFirestore;

    public String signUp(UserDTO user) {
        try {
            
            UserRecord.CreateRequest AccountCreationRequest = new UserRecord.CreateRequest()
                .setEmail(user.getEmail())
                .setPassword(user.getPassword());
            UserRecord userRecord = FirebaseAuth.getInstance().createUser(AccountCreationRequest);
            
            DocumentReference userReference = dbFirestore.collection("users").document(userRecord.getUid());
            Map<String, Object> userProfileMap = new HashMap<>();
            userProfileMap.put("email", user.getEmail());
            userProfileMap.put("name", user.getName());
            userProfileMap.put("username", user.getUsername());
            userProfileMap.put("UID", userRecord.getUid());
            // ... add any other fields you want here
            userReference.set(userProfileMap);
            return userRecord.getUid(); 
        } catch (FirebaseAuthException e) {
            // handle exception
            throw new RuntimeException("Failed to register user");
        }
    }

    public String signIn(String email, String password) {
        try {
            UserRecord userRecord = FirebaseAuth.getInstance().getUserByEmail(email);
            // Here you can also check the password with your database if needed
            return userRecord.getUid();
        } catch (FirebaseAuthException e) {
            throw new RuntimeException("Failed to login");
        }
    }
}

