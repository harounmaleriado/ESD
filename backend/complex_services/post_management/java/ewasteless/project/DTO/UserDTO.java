package ewasteless.project.DTO;



import javax.validation.constraints.Email;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter
@Getter 
@NoArgsConstructor
@AllArgsConstructor
public class UserDTO {
    
    @NotNull(message = "Name cannot be empty")
    @Size(min = 7, max = 40, message = "Name must be between 7 and 50 characters")
    private String name;

    @NotNull
    @Email(message = "Invalid email format")
    private String email;

    @NotNull(message = "Username cannot be empty")
    @Size(min = 7, max = 20, message = "Username must be between 7 and 20 characters")
    private String username;

    @NotNull(message = "Password cannot be empty")
    @Size(min = 6, message = "Password must be at least 6 characters long") // Firebase requires a minimum of 6 characters
    private String password;

    
}

