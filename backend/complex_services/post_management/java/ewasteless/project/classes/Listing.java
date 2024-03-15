package ewasteless.project.classes;

import com.google.cloud.firestore.DocumentReference;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter 
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class Listing {

    // seller
    private String username ;

    private double price ;
    
    private String productDescription ;

    private int postalCode ;

    // reference to product sold
    private DocumentReference PID ;

    private String SID ;
}
