from __future__ import division
import collections
import re

def get_readability_metrics(all_code):
    code_lines = all_code.split('\n')
    line_no = len(code_lines) # no of lines

    loops = 0
    spaces = 0
    commas = 0
    periods = 0
    numbers = 0
    comments = 0
    branches = 0
    line_len = 0
    blank_line = 0
    assignments = 0
    max_numbers = 0
    indentation = 0
    parentheses = 0
    max_line_len = 0 
    max_indentation = 0
    arithmetic_operators = 0
    comparison_operators = 0
    max_occurrence_of_character = 0

    for line in code_lines:
        line_len += len(line)
        max_line_len = max(len(line), max_line_len)

        if (len(line.strip())==0):
            blank_line += 1
            continue

        if '#' in line:
            comments += 1

        indentation += len(line) - len(line.lstrip())
        max_indentation = max(max_indentation, len(line) - len(line.lstrip()))

        numbers_in_line = sum(c.isdigit() for c in line)
        numbers += numbers_in_line
        max_numbers = max(numbers_in_line, max_numbers)

        spaces  += sum(c.isspace() for c in line)
        commas += line.count(',')
        periods += line.count('.')

        loops += len(re.findall(r'for\W|while\W|repeat\W', line))
        parentheses += len(re.findall(r'\[|\(|\{|\}|\)|\]', line))
        branches += len(re.findall(r'else if\W|if\W|else\W', line))
        arithmetic_operators += len(re.findall(r'\+|-|\*\*|\*|\/|\^|%%|%\/%', line))
        comparison_operators += len(re.findall(r'<|>|==|<=|>=|!=', line))
        assignments += len(re.findall(r'(?<!\!|<|>|=)=|<-|->|<<-|->>', line))

        char, char_count = collections.Counter(line).most_common(1)[0]
        max_occurrence_of_character = max (max_occurrence_of_character, char_count)

        # letters = sum(c.isalpha() for c in line)

    metrics_dict = {
                'avg_line_len': line_len / line_no,
                'max_line_len': max_line_len,
                'avg_indentation': indentation / line_no,
                'max_indentation': max_indentation,
                'avg_numbers': numbers / line_no,
                'avg_comments': comments / line_no,
                'max_numbers': max_numbers,
                'avg_periods': periods / line_no,
                'avg_commas': commas / line_no,
                'avg_spaces': spaces / line_no,
                'avg_parentheses': parentheses / line_no,
                'avg_arithmetic_operators': arithmetic_operators / line_no,
                'avg_comparison_operators': comparison_operators / line_no,
                'avg_assignments': assignments / line_no,
                'avg_branches': branches / line_no,
                'avg_loops': loops / line_no,
                'avg_blank_lines': blank_line / line_no,
                'max_occurrence_of_character': max_occurrence_of_character
				}
    
    print(metrics_dict)