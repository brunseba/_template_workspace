# Mermaid Demonstration

This document demonstrates various types of diagrams that can be created using Mermaid.

## Chapter 1: Flowchart

```mermaid
flowchart TD;  
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

## Chapter 2: Sequence Diagram

```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>Bob: Hello Bob, how are you?
    Bob-->>Alice: I am good thanks!
```

## Chapter 3: Class Diagram

```mermaid
classDiagram
    class Animal{
      +String name
      +int age
      +void makeSound()
    }
    class Dog{
      +String breed
      +void bark()
    }
    Animal <|-- Dog
```

## Chapter 4: State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Working
    Working --> Idle
    Working --> Done
    Done --> [*]
```

## Chapter 5: Pie Chart

```mermaid
pie title Pet Ownership
    "Cats" : 38
    "Dogs" : 45
    "Fish" : 17
```

## Chapter 6: Gantt Chart

```mermaid
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2025-07-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2025-08-01  , 12d
    another task    : 24d
```

## Chapter 7: Journey

```mermaid
journey
    title My Working Day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 2: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me
```

## Chapter 8: Graph

```mermaid
graph TB
  A[Start] --> B[Process1]
  B --> C{Decision}
  C -->|Yes| D[Process2]
  C -->|No| E[Process3]
  D --> F[End]
  E --> F
```

## Chapter 9: Quadrant Chart

```mermaid
quadrantChart
    title Productivity During the Day
    x-axis Low --> High
    y-axis Low --> High
    quadrant-1 High Energy - Productive
    quadrant-2 High Energy - Low Productivity
    quadrant-3 Low Energy - Low Productivity
    quadrant-4 Low Energy - High Productivity
    Morning Vibes: [0.2, 0.8]
    Afternoon Dip: [0.8, 0.2]
    Evening Revive: [0.6, 0.5]
```

## Chapter 10: XY Chart

```mermaid
xychart-beta
    title "Monthly Sales Record"
    x-axis [Jan, Feb, Mar, Apr, May]
    y-axis "Sales" 0 --> 100
    bar [10, 30, 20, 40, 60]
```

## Chapter 11: Block Diagram

```mermaid
block-beta
    columns 3
    doc>"Document"]:3
    space down1<[" "]>(down) space

  block:e:3
          l["left"]
          m("A wide one in the middle")
          r["right"]
  end
    space down2<[" "]>(down) space
    db[("DB")]:3
    space:3
    D space C
    db --> D
    C --> db
    D --> C
    style m fill:#d6d,stroke:#333,stroke-width:4px
```

## Chapter 12: Git Graph

```mermaid
gitGraph
  commit id: "Initial commit"
  branch develop
  commit
  commit id: "Implement feature X"
  checkout main
  merge develop
  commit id: "Release v1.0"
```

## Chapter 13: Mindmap

```mermaid
mindmap
  root((Tech Stack))
    node((Frontend))
      React
      Angular
    node((Backend))
      Node.js
      Python
    node((DevOps))
      Docker
      Kubernetes
```

Each of the above chapters provides an example of a different type of diagram that can be created using Mermaid.
