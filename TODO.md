Fix issue when file edits fail and there are no file changes but the file is
stored in the file_edits variable. This leads to the agent detecting file edits
but there is nothing printed when we review them.
