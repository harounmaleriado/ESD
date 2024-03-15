package ewasteless.project.DTO;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.fasterxml.jackson.annotation.JsonProperty;

@Setter 
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class ListingDTO {

    private String username ;

    private double price ;
    
    private String productDescription ;

    private int postalCode ;

    private String type ;
    
    // reference to product sold
    @JsonProperty("PID")
    private String PID ;

    @JsonProperty("SID")
    private String SID ;
}
