package ewasteless.project.controllers;

// Spring imports
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// Model imports
import ewasteless.project.classes.User;
import ewasteless.project.service.UserService;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;



    @GetMapping("/uid/{UID}")
    public ResponseEntity<User> getUserByUID(@PathVariable String UID) {
        try {
            User user = userService.getUserByUID(UID);
            if (user != null) {
                return ResponseEntity.ok(user);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    } 

    @DeleteMapping("/{UID}")
    public ResponseEntity<Void> deleteUser(@PathVariable String UID) {

        try {
            userService.deleteUser(UID);
            return ResponseEntity.noContent().build();
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    }
}