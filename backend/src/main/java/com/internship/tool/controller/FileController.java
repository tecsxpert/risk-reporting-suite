package com.internship.tool.controller;

import com.internship.tool.service.FileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api")
public class FileController {

    @Autowired
    private FileService fileService;

    // POST /upload
    @PostMapping("/upload")
    public ResponseEntity<String> upload(@RequestParam("file") MultipartFile file) throws Exception {

        String filename = fileService.uploadFile(file);

        return ResponseEntity.ok("Uploaded: " + filename);
    }

    // GET /files/{filename}
    @GetMapping("/files/{filename}")
    public ResponseEntity<byte[]> download(@PathVariable String filename) throws Exception {

        byte[] data = fileService.getFile(filename);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + filename)
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(data);
    }
}