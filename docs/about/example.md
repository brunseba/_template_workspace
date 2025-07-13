# 🎨 Example Page

Welcome to the **{{ metadata.project.name }}**! This example page demonstrates various features:

## Mermaid Diagram

Below is a Mermaid diagram with custom colorization:

```mermaid
flowchart LR

A-->B
```

---

```mermaid
flowchart TD 
    A[Start Process] --> B{Decision Point}
    B -->|Yes| C[Success Path]
    B -->|No| D[Retry Path]
    C --> E[Complete]
    D --> B
    
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#000
    classDef startNode fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000
    classDef decisionNode fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef successNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef retryNode fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
    classDef completeNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px,color:#000
    
    class A startNode
    class B decisionNode
    class C successNode
    class D retryNode
    class E completeNode
```

## Using Variables

Here are some project details sourced from `.metadata.yaml`:

- **Version**: `{{ metadata.version }}` - {{ metadata.version_name }}
- **Release Date**: {{ metadata.release_date }}
- **Project Name**: {{ metadata.project.name }}
- **Description**: {{ metadata.project.description }}

## Markdown Features

- **Bold Text**: Double asterisks `**bold**`
- **Italic Text**: Single asterisks `*italic*`
- **Links**: [Project Repository]({{ metadata.project.repository }})

### Lists

- Item 1
  - Sub-item 1.1
  - Sub-item 1.2
- Item 2

### Code Block

```python
# Sample Python Code
print("Hello, world!")
```

For more information, visit the [Documentation Site]({{ metadata.project.documentation }}).

