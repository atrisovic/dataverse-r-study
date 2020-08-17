# Datasets

| Version | Env & code cleaning                                  | No env & no code cleaning                                  |
|---------|------------------------------------------------------|------------------------------------------------------------|
| R 3.2   | `run_log_r32_env.csv` `run_log_r32_env_download.csv` | `run_log_r32_no_env.csv` `run_log_r32_no_env_download.csv` |
| R 3.6   |                                                      |                                                            |
| R 4.0   | `run_log_r40_env.csv` `run_log_r40_env_download.csv` | `run_log_r40_no_env.csv` `run_log_r40_no_env_download.csv` |


## Heading for `run_log_rXY_(no_)env.csv`

| doi | file_name | run_result |
|-----|-----------|------------|


## Heading for `run_log_rXY_(no_)env_download.csv`

| doi | file_id | download_status |
|-----|---------|-----------------|

## Readability metrics header

doi,filename,line_no,avg_line_len,max_line_len,avg_indentation,max_indentation,avg_numbers,avg_comments,max_numbers,avg_periods,avg_commas,avg_spaces,avg_parentheses,avg_arithmetic_operators,avg_comparison_operators,avg_assignments,avg_branches,avg_loops,avg_keywords,max_keywords,avg_blank_lines,max_occurrence_of_character,avg_vars_len,max_vars_len,avg_vars_count,max_vars_count,max_occurence_of_var,vars

-  'doi': doi,
-  'filename': filename,
-  'line_no': line_no,
-  'avg_line_len': line_len / line_no,
-  'max_line_len': max_line_len,
-  'avg_indentation': indentation / line_no,
-  'max_indentation': max_indentation,
-  'avg_numbers': numbers / line_no,
-  'avg_comments': comments / line_no,
-  'max_numbers': max_numbers,
-  'avg_periods': periods / line_no,
-  'avg_commas': commas / line_no,
-  'avg_spaces': spaces / line_no,
-  'avg_parentheses': parentheses / line_no,
-  'avg_arithmetic_operators': arithmetic_operators / line_no,
-  'avg_comparison_operators': comparison_operators / line_no,
-  'avg_assignments': assignments / line_no,
-  'avg_branches': branches / line_no,
-  'avg_loops': loops / line_no,
-  'avg_keywords': keywords / line_no,
-  'max_keywords': max_keywords,
-  'avg_blank_lines': blank_line / line_no,
-  'max_occurrence_of_character': max_occurrence_of_character,
-  'avg_vars_len': avg_vars_len,
-  'max_vars_len': max_vars_len,
-  'avg_vars_count': vars_count / line_no,
-  'max_vars_count': max_vars_count,
-  'max_occurence_of_var': max_occurence_of_var,
-  'vars': ";".join(vars)


[doi.S,filename.S,line_no.S,avg_line_len.S,max_line_len.S,avg_indentation.S,max_indentation.S,avg_numbers.S,avg_comments.S,max_numbers.S,avg_periods.S,avg_commas.S,avg_spaces.S,avg_parentheses.S,avg_arithmetic_operators.S,avg_comparison_operators.S,avg_assignments.S,avg_branches.S,avg_loops.S,avg_keywords.S,max_keywords.S,avg_blank_lines.S,max_occurrence_of_character.S,avg_vars_len.S,max_vars_len.S,avg_vars_count.S,max_vars_count.S,max_occurence_of_var.S,vars.S]
