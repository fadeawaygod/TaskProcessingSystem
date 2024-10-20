# Exceptions

## How to add a new exceptions
1. check the rule of error code: [here](#Error-Code-Rule)
2. find the corresponding module, e.g. you want to add an exception about auth, check auth.py
3. add an exception in it

## Error Code Rule
The rule of error code is: type{1 digit}app{2 digit}serial{2 digit}

- type code:
  - 1XXXX: general
  - 2XXXX: database
  - 3XXXX: data validation
  - 4XXXX: task

- app code:
  - x00xx: general
  - x01xx:Task Processing System
 
