# Sample Flowchart Documentation

This document contains a sample flowchart for testing the mermaid extraction tools.

## Basic Flowchart

```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Fix it]
    D --> B
    C --> E[End]
```

## Process Flow

Here's another example of a process flow:

```mermaid
flowchart LR
    A[Input] --> B[Process]
    B --> C{Decision}
    C -->|Option 1| D[Result A]
    C -->|Option 2| E[Result B]
    C -->|Option 3| F[Result C]
```

## Subgraph Example

```mermaid
graph TB
    subgraph "User Interface"
        A[Login Form]
        B[Dashboard]
        C[Settings]
    end
    
    subgraph "Backend Services"
        D[Authentication]
        E[Data Processing]
        F[Database]
    end
    
    A --> D
    B --> E
    C --> F
    D --> B
    E --> F
```

This document demonstrates various types of flowcharts that should be extracted by our tools.
