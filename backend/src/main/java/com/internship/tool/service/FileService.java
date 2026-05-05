package com.internship.tool.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.*;
import java.util.Set;
import java.util.UUID;

@Service
public class FileService {

    private static final long MAX_SIZE = 10 * 1024 * 1024; // 10MB
    private static final Set<String> ALLOWED_TYPES = Set.of(
            "application/pdf", "image/png", "image/jpeg"
    );

    private final Path uploadDir = Paths.get("uploads");

    public FileService() throws IOException {
        if (!Files.exists(uploadDir)) {
            Files.createDirectories(uploadDir);
        }
    }

    public String uploadFile(MultipartFile file) throws IOException {

        // 1. size validation
        if (file.getSize() > MAX_SIZE) {
            throw new IllegalArgumentException("File size exceeds 10MB");
        }

        // 2. type validation
        if (!ALLOWED_TYPES.contains(file.getContentType())) {
            throw new IllegalArgumentException("Invalid file type");
        }

        // 3. generate UUID filename
        String originalName = file.getOriginalFilename();
        String extension = originalName != null && originalName.contains(".")
                ? originalName.substring(originalName.lastIndexOf("."))
                : "";

        String newFileName = UUID.randomUUID() + extension;

        // 4. save file
        Path filePath = uploadDir.resolve(newFileName);
        Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);

        return newFileName;
    }

    public byte[] getFile(String filename) throws IOException {
        Path filePath = uploadDir.resolve(filename);
        if (!Files.exists(filePath)) {
            throw new RuntimeException("File not found");
        }
        return Files.readAllBytes(filePath);
    }
}