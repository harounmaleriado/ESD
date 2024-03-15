package ewasteless.project.classes;

import java.time.Instant;

import com.google.cloud.Timestamp;
import com.google.cloud.firestore.annotation.ServerTimestamp;

import com.google.cloud.Timestamp;


import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter 
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class Post {

    private String title ;
    private String message;
    private String PostID ;
    private String username ;
    private String UID;
    
    private Instant createdTimestamp;
}
