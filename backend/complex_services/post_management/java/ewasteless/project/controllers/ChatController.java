package ewasteless.project.controllers;


import java.util.concurrent.ExecutionException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import ewasteless.project.DTO.ChatDTO;
import ewasteless.project.DTO.CommentDTO;
import ewasteless.project.classes.Chat;
import ewasteless.project.classes.Comment;
import ewasteless.project.service.ChatService;

@RestController
@RequestMapping("/api/chats")
public class ChatController {

    @Autowired
    private ChatService ChatService;

    @PostMapping
    public ResponseEntity<String> createChat(@RequestBody ChatDTO chatDTO) {
        try {
            String updateTime = ChatService.createChat(chatDTO);
            return ResponseEntity.ok(updateTime);
        } catch (ExecutionException | InterruptedException e) {
            // Handle exceptions properly
            return ResponseEntity.status(500).body("Error when creating the chat: " + e.getMessage());
        }
    }


    @PostMapping("/{LID}/comments")
    public ResponseEntity<String> addCommentToPost(
            @PathVariable String CID,
            @RequestBody CommentDTO commentDTO) throws Exception {
            
                

        try {
            // Map the DTO to your Comment entity
            Comment comment = new Comment();
            comment.setUsername(commentDTO.getUsername());
            comment.setComment(commentDTO.getComment());
            comment.setUID(commentDTO.getUID()) ;
            // Set any other fields required by your Comment entity

            String updateTime = ChatService.addCommentToChat(CID, comment);
            return ResponseEntity.ok(updateTime);
        } catch (ExecutionException | InterruptedException e) {
            // Handle the exceptions properly here
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }

    }
}

