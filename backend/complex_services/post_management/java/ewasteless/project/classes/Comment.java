package ewasteless.project.classes;



import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Instant;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

public class Comment {
    private String comment;
    private String username; // Assuming this is the creator's username
    private String UID ;
    private Instant createdTimestamp; // This will store the creation timestamp
}

