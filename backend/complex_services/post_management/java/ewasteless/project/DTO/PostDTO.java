package ewasteless.project.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter 
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class PostDTO {

    private String title ;
    private String message;
    private String username ;

    @JsonProperty("UID")
    private String UID ;
    
}
