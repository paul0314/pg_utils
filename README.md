INPUT:
1) Define Number of People in Excel Table
2) Define all start dates of sprints
3) Define all end dates of sprints (ideally 1 day before the following start date of the next sprint)
4) Excel Table "TaskVerwaltung.csv" in same folder as this python file during execution
   (csv format is important) with the following column format:
   (1 row is reserved for headers, first issue starts at second row)
  - Task Number (Format: # followed by a number without space)
  - Task Name (Format: String)
  - Task Description (Format: String)
  - Task Difficulty (Format: Number)
  - Task Risk (Format: one of the three values +, o, -)
  - Task Start [when the task was first added to a sprint] (Format: dd/mm/yyyy)
  - Task End [when the task has been completed] (Format: dd/mm/yyyy)
  - Status [+ for finished, o for in progress, - for cancelled without completion (this case will be ignored for
  calculating scope and completed points)] (Format: one of the three values +, o, -)
  - Person1 [hours spent on issue by Person1] (Format: String)
  - ...
  - PersonN [hours spent on issue by PersonN] (Format: String)
  - (additional Columns will be ignored)
