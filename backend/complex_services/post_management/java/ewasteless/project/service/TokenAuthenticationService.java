package ewasteless.project.service;

// Spring import
import org.springframework.stereotype.Service;

// Firebase imports
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseToken;

@Service
public class TokenAuthenticationService {

    public FirebaseToken validateToken(String idToken) {
        try {
            return FirebaseAuth.getInstance().verifyIdToken(idToken);
        } catch (Exception e) {
            throw new RuntimeException(e.getMessage()); // or return a custom error message/response
        }
    }
}

