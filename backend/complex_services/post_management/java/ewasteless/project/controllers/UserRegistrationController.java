package ewasteless.project.controllers;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

// Javax import
import javax.validation.Valid;

// Model imports
import ewasteless.project.DTO.UserDTO;
import ewasteless.project.service.UserRegistrationService;

// Java imports
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/newUserRegistration")
public class UserRegistrationController {

    @Autowired
    private UserRegistrationService authService;

    // Expects formData following constraints as defined in UserDTO.java
    // Returns ResponseEntity.ok(response)
    @PostMapping
    public ResponseEntity<?> signUp(@Valid @RequestBody UserDTO user) {
        try {
            // Returns new user UID
            String userId = authService.signUp(user);
            Map<String, Object> response = new HashMap<>();
            response.put("status", "OK");
            response.put("uid", userId);
            return ResponseEntity.ok(response);
        } catch(Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }
    }
}