package com.fsk.ecommerce.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "hobbies")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Hobby {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "hobby_id", columnDefinition = "uuid")
    private UUID id;

    @Column(nullable = false, unique = true, length = 100)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private HobbyCategory category;

    @ManyToMany(mappedBy = "hobbies")
    private Set<User> users = new HashSet<>();
}

