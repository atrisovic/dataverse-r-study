import unittest 
  
class SimpleTest(unittest.TestCase): 
  
    def test_parse_dependencies1(self):
        from set_environment import parse_dependencies
        line = "library(dplyr)"
        correct = 'if (!require(\"dplyr\")) install.packages(\"dplyr\")\n'
        self.assertEqual(parse_dependencies(line), correct) 

    def test_parse_dependencies2(self):
        from set_environment import parse_dependencies
        line = "require(dplyr)"
        correct = 'if (!require(\"dplyr\")) install.packages(\"dplyr\")\n'
        self.assertEqual(parse_dependencies(line), correct) 

    def test_fix_abs_paths1(self):
        from set_environment import fix_abs_paths
        line = "file.path(\"/Dropbox/myfile.csv\")"
        index = line.find('file.path(')
        correct = "basename(file.path(\"/Dropbox/myfile.csv\"))"
        self.assertEqual(fix_abs_paths(line,index), correct)

    def test_fix_abs_paths2(self):
        from set_environment import fix_abs_paths
        line = "source(\'Dropbox/user/anotherfile.R\')"
        index = line.find('source(')+7
        correct = "source(basename(\'Dropbox/user/anotherfile.R\'))"
        self.assertEqual(fix_abs_paths(line,index), correct)

    def test_fix_abs_paths2_2(self):
        from set_environment import fix_abs_paths
        line = "source(   \'Dropbox/user/anotherfile.R\')"
        index = line.find('source(')+7
        correct = "source(basename(   \'Dropbox/user/anotherfile.R\'))"
        self.assertEqual(fix_abs_paths(line,index), correct)

    def test_fix_abs_paths3(self):
        from set_environment import fix_abs_path_in_readcsv
        line = "data1 <- read.csv(\"data/vilno_1.csv\", header=FALSE)"
        correct = "data1 <- read.csv(basename(\"data/vilno_1.csv\"), header=FALSE)"
        self.assertEqual(fix_abs_path_in_readcsv(line), correct)
 
    def test_fix_abs_paths4(self):
        from set_environment import fix_abs_path_in_readcsv
        line = "data1 <- read.csv(\"data/vilno_1.csv\")"
        correct = "data1 <- read.csv(basename(\"data/vilno_1.csv\"))"
        self.assertEqual(fix_abs_path_in_readcsv(line), correct)

    def test_fix_abs_paths5(self):
        from set_environment import fix_abs_path_in_readcsv
        line = "data1 <- read.csv (\"data/vilno_1.csv\")"
        correct = "data1 <- read.csv (basename(\"data/vilno_1.csv\"))"
        self.assertEqual(fix_abs_path_in_readcsv(line), correct)

    def test_fix_abs_paths6(self):
        from set_environment import fix_abs_path_in_readcsv
        line = "data1 <- read.csv ( \"data/vilno_1.csv\", header=FALSE)"
        correct = "data1 <- read.csv (basename( \"data/vilno_1.csv\"), header=FALSE)"
        self.assertEqual(fix_abs_path_in_readcsv(line), correct)

    def test_detect_encoding(self):
        from set_environment import detect_encoding
        input = "this is some text"
        a, b = detect_encoding(input)
        self.assertEqual(a, 'ascii')
        self.assertEqual(b, 1.0)

    def test_parse_libraries(self):
        from set_environment import parse_libraries
        input = 'libraries("dplyr", "ggplot2", "RMySQL", "data.table")'
        correct = ['dplyr', 'ggplot2', 'RMySQL', 'data.table']
        result = parse_libraries(input)
        self.assertEqual(result, correct)

    def test_parse_packages1(self):
        from set_environment import parse_packages
        input = '    packages <- c("dplyr", "stringr", "stargazer", "ggplot2", "scales",\n\n\n'
        result = parse_packages(input)
        correct = ["dplyr", "stringr", "stargazer", "ggplot2", "scales"]
        self.assertEqual(result, correct)

    def test_parse_packages2(self):
        from set_environment import parse_packages
        input = '    packages <- c("dplyr", "stringr", "stargazer", "ggplot2", "scales")'
        result = parse_packages(input)
        correct = ["dplyr", "stringr", "stargazer", "ggplot2", "scales"]
        self.assertEqual(result, correct)

    # readability analysis
    # simple tests for readability analysis to make sure results are as expected
    def test_avg_commas(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code=",,\n,,", test=True)
        cor = 2.0
        self.assertEqual(res["avg_commas"], cor)

    def test_line_no(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="a<-2,\n,a+b\n,b\n,", test=True)
        cor = 4.0
        self.assertEqual(res["line_no"], cor)

    def test_avg_line_len(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="a\naa\n  ,", test=True)
        cor = 2.0
        self.assertEqual(res["avg_line_len"], cor)

        res = get_readability_metrics('a', all_code="a\naaa\n\n\nc", test=True)
        cor = 1.0
        self.assertEqual(res["avg_line_len"], cor)

    def test_max_line_len(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="a\naa\n  ,", test=True)
        cor = 3.0
        self.assertEqual(res["max_line_len"], cor)

    def test_max_line_len1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="a\naaaaa\n\n\nc", test=True)
        cor = 5.0
        self.assertEqual(res["max_line_len"], cor)

        res = get_readability_metrics('a', all_code="\n\n\n\n", test=True)
        cor = 0.0
        self.assertEqual(res["max_line_len"], cor)

    def test_avg_indentation(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="   a,,\n a,,", test=True)
        cor = 2.0
        self.assertEqual(res["avg_indentation"], cor)

        res = get_readability_metrics('a', all_code="   a,,\n   a,,", test=True)
        cor = 3.0
        self.assertEqual(res["avg_indentation"], cor)

    def test_max_indentation(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a\n  aaaaa\n\n\n        c", test=True)
        cor = 8.0
        self.assertEqual(res["max_indentation"], cor)

    def test_avg_numbers(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="1\n,  3,\n\n\na", test=True)
        cor = 0.4
        self.assertEqual(res["avg_numbers"], cor)

    def test_max_numbers(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="1\n,\3,\n\n\na", test=True)
        cor = 1
        self.assertEqual(res["max_numbers"], cor)

        res = get_readability_metrics('a', all_code="1029\n,\3,\n\n\na", test=True)
        cor = 4
        self.assertEqual(res["max_numbers"], cor)

    def test_avg_comments(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="1###\n,  3,#\n\n\na", test=True)
        cor = 0.4
        self.assertEqual(res["avg_comments"], cor)

    def test_avg_comments1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="1 #com ##\n#comment", test=True)
        cor = 1
        self.assertEqual(res["avg_comments"], cor)

    def test_avg_spaces(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="1 #com ##\n#comment", test=True)
        cor = 1
        self.assertEqual(res["avg_spaces"], cor)

        res = get_readability_metrics('a', all_code="1 #com    ##\n#comment", test=True)
        cor = 2.5
        self.assertEqual(res["avg_spaces"], cor)

    def test_max_vars_len(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="a 1 # a com ##\n#comment", test=True)
        cor = 1
        self.assertEqual(res["max_vars_len"], cor)

    def test_avg_vars_len(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a b c', all_code="a 1 # a com ##\n#comment", test=True)
        cor = 1
        self.assertEqual(res["avg_vars_len"], cor)

        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a2 temp c2', all_code="a 1 # a com ##\n#comment", test=True)
        cor = 2.6666666667
        self.assertAlmostEqual(res["avg_vars_len"], cor)

    def test_avg_keywords(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="a 1 # a com ##\n#comment", test=True)
        cor = 0
        self.assertEqual(res["avg_keywords"], cor)

    def test_avg_keywords1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', all_code="a 1 if # a com ##\n#comment", test=True)
        cor = 0.5
        self.assertEqual(res["avg_keywords"], cor)

    def test_avg_keywords2(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a com ##\n# while comment", test=True)
        cor = 1
        self.assertEqual(res["avg_keywords"], cor)

    def test_avg_keywords3(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a forinnextbreak ##\n#comment", test=True)
        cor = 2.5
        self.assertEqual(res["avg_keywords"], cor)

    def test_max_keywords(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a forinnextbreak ##\n#comment", test=True)
        cor = 5
        self.assertEqual(res["max_keywords"], cor)

    def test_avg_periods(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a forinnextbreak ##\n#comment", test=True)
        cor = 0
        self.assertEqual(res["avg_periods"], cor)

    def test_avg_periods1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a forinnextbreak. ##\n#comment\n\n", test=True)
        cor = 0.25
        self.assertEqual(res["avg_periods"], cor)

    def test_avg_parentheses(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a (forinnextbreak). ##\n#comment\n\n", test=True)
        cor = 0.5
        self.assertEqual(res["avg_parentheses"], cor)

    def test_avg_parentheses1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a [(forinnextbreak).]\{\} ##\n#comment\n\n", test=True)
        cor = 1.5
        self.assertEqual(res["avg_parentheses"], cor)

    def test_avg_loops(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a 1 if # a [(for() innextbreak).]\{\} ##\n#comment\n\n", test=True)
        cor = 0.25
        self.assertEqual(res["avg_loops"], cor)

    def test_avg_loops1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="for (r_file in r_files){", test=True)
        cor = 1.0
        self.assertEqual(res["avg_loops"], cor)

    def test_max_occurence_of_var1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i', \
            all_code="for (r_file in r_file){", test=True)
        cor = 0
        self.assertEqual(res["max_occurence_of_var"], cor)

    def test_vars(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i r_file', \
            all_code="for (r_file in r_file){", test=True)
        cor = "a;i;r_file"
        self.assertEqual(res["vars"], cor)
    
    def test_max_occurence_of_var(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a r_file', \
            all_code="for a a a a(r_file in r_file){ a", test=True)
        cor = 5
        self.assertEqual(res["max_occurence_of_var"], cor)

    def test_max_occurence_of_var2(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('r_file', \
            all_code="for (r_file in r_file){", test=True)
        cor = 2
        self.assertEqual(res["max_occurence_of_var"], cor)

    def test_max_vars_count(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i r_file', \
            all_code="for (r_file in r_file){", test=True)
        cor = 2
        self.assertEqual(res["max_vars_count"], cor)

    def test_max_vars_count1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('r_file r_text', \
            all_code="a 1 if # a [(for() innextbreak).]\{\} ##\n#comment\n\n", test=True)
        cor = 0
        self.assertEqual(res["max_vars_count"], cor)

    def test_avg_vars_count(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i r_file', \
            all_code="for (r_file in r_file){", test=True)
        cor = 2
        self.assertEqual(res["avg_vars_count"], cor)

    def test_avg_vars_count1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i r_file', \
            all_code="", test=True)
        cor = 0
        self.assertEqual(res["avg_vars_count"], cor)

    def test_avg_vars_count2(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i r_file', \
            all_code="a i i\n r_file i i\n a i", test=True)
        cor = 2.666666666667
        self.assertAlmostEqual(res["avg_vars_count"], cor)

    def test_avg_blank_lines(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i r_file', \
            all_code="a i i\n r_file i i\n a i", test=True)
        cor = 0
        self.assertEqual(res["avg_blank_lines"], cor)

    def test_avg_blank_lines1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a i r_file', \
            all_code="a i i\n \n\n r_file i i\n a i", test=True)
        cor = 0.4
        self.assertEqual(res["avg_blank_lines"], cor)

    def test_max_occurrence_of_character(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a i i\n \n\n r_file i i\n a i", test=True)
        cor = 3
        self.assertEqual(res["max_occurrence_of_character"], cor)

    def test_avg_arithmetic_operators(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a i + i\n \n\n r_file == i i\n a i", test=True)
        cor = 0.2
        self.assertEqual(res["avg_arithmetic_operators"], cor)

    def test_avg_arithmetic_operators1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a^b", test=True)
        cor = 1
        self.assertEqual(res["avg_arithmetic_operators"], cor)

    def test_avg_arithmetic_operators2(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a%/%b", test=True)
        cor = 1
        self.assertEqual(res["avg_arithmetic_operators"], cor)

    def test_avg_comparison_operators(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a i + i\n \n\n r_file == i i\n a i", test=True)
        cor = 0.2
        self.assertEqual(res["avg_comparison_operators"], cor)

    def test_avg_comparison_operators1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a<=b", test=True)
        cor = 1
        self.assertEqual(res["avg_comparison_operators"], cor)

    def test_avg_comparison_operators2(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a!=b", test=True)
        cor = 1
        self.assertEqual(res["avg_comparison_operators"], cor)

    def test_avg_assignments(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a<- i + i\n \n\n r_file <<-i i\n a i", test=True)
        cor = 0.4
        self.assertEqual(res["avg_assignments"], cor)

    def test_avg_assignments1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a=b", test=True)
        cor = 1
        self.assertEqual(res["avg_assignments"], cor)

    def test_avg_assignments2(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="a->>b", test=True)
        cor = 1
        self.assertEqual(res["avg_assignments"], cor)

    def test_avg_branches(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="if a<- i + i\n \n\nelse r_file <<-i i\n a i", test=True)
        cor = 0.4
        self.assertEqual(res["avg_branches"], cor)

    def test_avg_branches1(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code=" if a==b:", test=True)
        cor = 1
        self.assertEqual(res["avg_branches"], cor)

    def test_avg_branches2(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="if else if else if else", test=True)
        cor = 3
        self.assertEqual(res["avg_branches"], cor)

    def test_avg_branches3(self):
        from readability_analysis import get_readability_metrics
        res = get_readability_metrics('a', \
            all_code="if if if else if else", test=True)
        cor = 5
        self.assertEqual(res["avg_branches"], cor)

if __name__ == '__main__': 
    unittest.main()

