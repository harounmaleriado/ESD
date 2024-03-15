package ewasteless.project;

import java.util.concurrent.ExecutionException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import ewasteless.project.service.ProductUpdateService;


@SpringBootApplication
public class ProjectApplication {

	public static void main(String[] args) throws InterruptedException, ExecutionException {
        
		SpringApplication.run(ProjectApplication.class, args);

        // update product collections
        // ProductUpdateService.uploadDataFromCSV("SpringBoot/src/main/resources/Data/CPU_UserBenchmarks.csv") ;      
	}
}

