# Class Diagram Examples

This document contains class diagrams for testing the mermaid extraction tools.

## Basic Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
        +eat()
    }
    
    class Dog {
        +String breed
        +bark()
        +wagTail()
    }
    
    class Cat {
        +String color
        +meow()
        +purr()
    }
    
    Animal <|-- Dog
    Animal <|-- Cat
```

## University System

```mermaid
classDiagram
    class University {
        +String name
        +String location
        +List~Student~ students
        +List~Professor~ professors
        +enrollStudent(Student)
        +hireProfessor(Professor)
    }
    
    class Person {
        <<abstract>>
        +String name
        +int age
        +String email
        +getName()
        +getAge()
    }
    
    class Student {
        +String studentId
        +String major
        +float gpa
        +study()
        +takeExam()
    }
    
    class Professor {
        +String employeeId
        +String department
        +List~Course~ courses
        +teach()
        +research()
    }
    
    class Course {
        +String courseId
        +String title
        +int credits
        +Professor instructor
        +List~Student~ enrolledStudents
        +addStudent(Student)
    }
    
    Person <|-- Student
    Person <|-- Professor
    University "1" --> "*" Student : contains
    University "1" --> "*" Professor : employs
    Professor "1" --> "*" Course : teaches
    Course "*" --> "*" Student : enrolled
```

## Payment System

```mermaid
classDiagram
    class PaymentProcessor {
        <<interface>>
        +processPayment(amount, method)
        +validatePayment(details)
    }
    
    class CreditCardProcessor {
        +String apiKey
        +processPayment(amount, method)
        +validatePayment(details)
        +chargeCreditCard(cardNumber, amount)
    }
    
    class PayPalProcessor {
        +String clientId
        +String clientSecret
        +processPayment(amount, method)
        +validatePayment(details)
        +chargePayPal(email, amount)
    }
    
    class BankTransferProcessor {
        +String bankCode
        +processPayment(amount, method)
        +validatePayment(details)
        +initiateBankTransfer(account, amount)
    }
    
    PaymentProcessor <|.. CreditCardProcessor
    PaymentProcessor <|.. PayPalProcessor
    PaymentProcessor <|.. BankTransferProcessor
```

These class diagrams demonstrate various object-oriented design patterns that should be extracted by our tools.
