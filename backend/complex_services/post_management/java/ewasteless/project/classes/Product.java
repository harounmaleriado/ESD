package ewasteless.project.classes;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Setter 
@Getter
@AllArgsConstructor
@NoArgsConstructor
public abstract class Product {
    private String brand;
    private String model;
    private Double benchmarkScore;
}
