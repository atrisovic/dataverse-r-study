import unittest 
  
class SimpleTest(unittest.TestCase): 
  
    def test_parse_dependencies1(self):
        from set_environment import parse_dependencies
        line = "library(dplyr)"
        correct = 'install.packages(\"dplyr\", repos=\"http://cran.us.r-project.org\")\n'
        self.assertEqual(parse_dependencies(line), correct) 

    def test_parse_dependencies2(self):
        from set_environment import parse_dependencies
        line = "require(dplyr)"
        correct = 'install.packages(\"dplyr\", repos=\"http://cran.us.r-project.org\")\n'
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

    def test_detect_encoding(self):
        from set_environment import detect_encoding
        input = "this is some text"
        a, b = detect_encoding(input)
        self.assertEqual(a, 'ascii')
        self.assertEqual(b, 1.0)

if __name__ == '__main__': 
    unittest.main()
