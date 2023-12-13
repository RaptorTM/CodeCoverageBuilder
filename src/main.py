import sys
import argparse


# variable=BuildReportPath;]$Env:BuildReportPath"
# variable=AllureProgramPath;]$Env:AllureProgramPath"
# variable=AllureHistoryPath;]$(BuildReportPath)\$(project_name)\allure\history-$(test_type)"
# variable=AllureReportPath;]$(BuildReportPath)\$(project_name)\allure\$(Build.BuildNumber)"
# variable=CoverageReportPath;]$(BuildReportPath)\$(project_name)\coverage\$(Build.BuildNumber)"

def getArguments():
    parser = argparse.ArgumentParser(description="Description: This program grab, sort allure & codecoverage reports and build final report")

    # Добавление аргументов
    parser.add_argument('-t', '--test-type', default='', required=True, help='Type of test to run')
    parser.add_argument('-p', '---project-name', default='', required=True, help='Name of current project')
    parser.add_argument('-g', '--git-name', default='', required=False, help='Name of current repo in multi-repo project or program stack')
    parser.add_argument('-a', '--max-allure-reports', default='30', required=False, help='Max codecoverage latest reports')
    parser.add_argument('-c', '--max-codecoverage-reports', default='30', required=False, help='Max codecoverage latest reports')

    return parser.parse_args()

if __name__ == "__main__":
    getArguments()
