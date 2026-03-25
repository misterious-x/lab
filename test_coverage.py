import coverage
import unittest

if __name__ == "__main__":
    cov = coverage.Coverage(source=['model'], branch=True)
    cov.start()
    
    from test_model import TestParser, TestRepository, TestCommands
    
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestParser))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRepository))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCommands))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    cov.stop()
    cov.report(show_missing=True)
    #cov.html_report(directory='htmlcov')