# Sequence Diagram Examples

This document contains sequence diagrams for testing the mermaid extraction tools.

## Basic Sequence Diagram

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    participant C as Charlie
    
    A->>B: Hello Bob, how are you?
    B-->>A: I'm fine, thanks!
    A->>C: How about you Charlie?
    C-->>A: I'm doing well too!
    
    Note over A,C: This is a note spanning multiple participants
    
    A->>B: Let's meet up
    B->>C: Are you free?
    C-->>B: Yes, I'm available
    B-->>A: Charlie can join us
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as Client
    participant S as Server
    participant D as Database
    
    U->>C: Enter credentials
    C->>S: Login request
    S->>D: Validate user
    D-->>S: User data
    S-->>C: Authentication token
    C-->>U: Login successful
    
    Note over U,D: User is now authenticated
    
    U->>C: Request protected resource
    C->>S: API call with token
    S->>S: Validate token
    S-->>C: Protected data
    C-->>U: Display data
```

## Error Handling Sequence

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Client->>API: Request data
    API->>Database: Query
    Database-->>API: Connection error
    API-->>Client: 500 Internal Server Error
    
    Note over Client,Database: Error handling flow
    
    Client->>API: Retry request
    API->>Database: Query retry
    Database-->>API: Data
    API-->>Client: 200 OK with data
```

These sequence diagrams demonstrate various communication patterns that should be extracted by our tools.
