package ewasteless.project.classes;

import java.util.List;


import com.google.cloud.firestore.DocumentReference;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class User {

    
    private String name;
    private String username;
    private String email;
    private int forumScore;

    // A map of product type to product ID reference
    // private Map<String, String> products;

    private String UID ; // same as document ID
    
    private List<DocumentReference> listings;

}
