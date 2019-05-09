# How to Contribute to WebIDE

  Thank you for considering contributing to WebIDE!

## Requesting New Features

  If you wish to request a new programming language or feature that isn't on the road map, it is recommended to use the issue tracker with a `feature request` label for the time being.

  <b>Note:</b> Be sure to check both the road map and current feature requests before opening a new request. If an unfulfilled request exists, make a comment to simulate voting. This avoids cluttering.

## Reporting Issues

  - Describe what you expected to happen.
  - Describe what actually happened. Unless it only occurs with a certain file created by using the app, it is unnecessary to include any code that has been written.
  - Describe the browser being used if it's an issue with using the app, and include all extensions.
  - If a security vulnerability is found that is within our app, mark the issue as high priority.

  <b>Note:</b> At no point will this project ever support Internet Explorer, or any other "dead" browser. Any issues regarding any such browser will be ignored.

## Project Standards

  1. comments should describe <b>what</b> your code does, <b>not how</b> it's being done. How it's done should be plainly evident by your code
      * classes should have comments about what it does, and a brief (read 1-2 short sentences) description of each function
      * functions within classes should have an expanded explanation. Standalone functions should describe what it does
      * any sufficiently complex lines of code require explanation
      * files should be clean of code that was commented out for testing purposes
  1. Python requires following PEP8 standards, with some notable exceptions
      * the line limit is flexible, but appreciated
      * camelCase is preferred for functions and variables, while PascalCase is preferred for classes
  1. All variables, classes, and functions should be well named, but not overly verbose.
  1. All new code requires test cases. This includes bug fixes, new files, and new functions.
  1. New Bash code is not expected to work on any distro outside of Debian based systems. Established standards, as found in `call-compiler`, are preferred.
  1. Any system level change, like adding a new language or driver, requires editing all the necessary files by the same person.
  1. If a file is created by the app, it should never be on git.
