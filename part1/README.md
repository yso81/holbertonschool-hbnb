# HBnB - UML #

## Example of a generic package diagram using Mermaid.js: ##

```
classDiagram
class PresentationLayer {
    <<Interface>>
    +ServiceAPI
}
class BusinessLogicLayer {
    +ModelClasses
}
class PersistenceLayer {
    +DatabaseAccess
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```

## Part 1: Technical Documentation: ##
https://docs.google.com/document/d/1Bxd6bMBMDjJ9oqW4MzW1oGtKb_mWs9SpjHhFxnLvwC0/edit?usp=sharing