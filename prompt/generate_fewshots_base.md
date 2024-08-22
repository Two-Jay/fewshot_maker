generate few-shot examples for a given prompt and constraints

### target prompt

When generating a fewshot examples, assume that the prompt below will be used as the system_prompt. 
This means that you should generate an {{count_generation}} of fewshot-examples, assuming that the prompt below is a system prompt
```
{{prompt}}
```

### requirements
This is a prerequisites for a "Fewshot Examples that satisfies the request."
A "Fewshot Examples that satisfies the request" must meet all of the following conditions
```
{{requirements}}
```

### constraints
This is a constraints for a "Fewshot Examples that satisfies the request."
A "Fewshot Examples that satisfies the request" must not meet any of the following conditions
```
{{constraints}}
```

### Sample

This is a sample of a fewshot examples that the user wants to generate.
Each example is separated by '{}'.
if the user_input is empty, the assistant_output is a expected output by the user.

```
{{sample}}
```


Considering the sample above, generate good & bad examples that meet the content of "requirements" and "constraints".

### output
generate {{count_generation}} examples for both correct and wrong cases.
generate fewshot in {{language}}.

Please print in the format below :
{{format_instructions}}