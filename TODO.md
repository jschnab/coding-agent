Add feature to read a local instructions file (e.g. codi.md) that provide
context into code organization.

Add whitelist of commands (so the user does not have to approve every time).

Add support for other agents.

Add CLI options:
* agent type (Gemini, etc.)
* model name
* whitelist enabled or not
* custom prompt (inline or file)

Add tool extensibility, where user can provide a function via a Python module
and a tool definition via a YAML file.

Add functionality to work with lines in read_text_file (instead of working with
one giant string). This will save tokens, speed up model thinking, and reduce
costs.
