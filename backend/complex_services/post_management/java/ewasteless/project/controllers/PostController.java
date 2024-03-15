package ewasteless.project.controllers;

import java.util.concurrent.ExecutionException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import ewasteless.project.DTO.CommentDTO;
import ewasteless.project.classes.Comment;
import ewasteless.project.DTO.PostDTO;

import ewasteless.project.service.PostService;

@RestController
@RequestMapping("/api/posts")
public class PostController {

    @Autowired
    private PostService postService;

    @PostMapping
    public ResponseEntity<String> createPost(@RequestBody PostDTO postDTO) throws Exception {
        try {
           
            String updateTime = postService.createPost(postDTO);
            return ResponseEntity.ok(updateTime);
        } catch (ExecutionException | InterruptedException e) {
            // Handle exceptions properly
            return ResponseEntity.status(500).body("Error when creating the post: " + e.getMessage());
        }
    }

    @PostMapping("/{postId}/comments")
    public ResponseEntity<String> addCommentToPost(
            @PathVariable String postId,
            @RequestBody CommentDTO commentDTO) throws Exception {
            
                

        try {
            // Map the DTO to your Comment entity
            Comment comment = new Comment();
            comment.setUsername(commentDTO.getUsername());
            comment.setComment(commentDTO.getComment());
            comment.setUID(commentDTO.getUID()) ;
            // Set any other fields required by your Comment entity

            String updateTime = postService.addCommentToPost(postId, comment);
            return ResponseEntity.ok(updateTime);
        } catch (ExecutionException | InterruptedException e) {
            // Handle the exceptions properly here
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }

    }
}




   

