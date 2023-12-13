import os
import re
import shutil
import subprocess
from pathlib import Path


directory_with_reports = ''
allure_history_path = ''
report_path = ''


def addEnv():
    build_report_path = os.environ.get('BuildReportPath', '')
    allure_program_path = os.environ.get('AllureProgramPath', '')
    project_name = os.environ.get('project_name', '')
    test_type = os.environ.get('test_type', '')

    allure_history_path = os.path.join(build_report_path, project_name, 'allure', f'history-{test_type}')
    allure_report_path = os.path.join(build_report_path, project_name, 'allure',
                                      os.environ.get('Build.BuildNumber', ''))
    coverage_report_path = os.path.join(build_report_path, project_name, 'coverage',
                                        os.environ.get('Build.BuildNumber', ''))

    # Вывод переменных окружения в консоль
    print(f"BuildReportPath: {build_report_path}")
    print(f"AllureProgramPath: {allure_program_path}")
    print(f"AllureHistoryPath: {allure_history_path}")
    print(f"AllureReportPath: {allure_report_path}")
    print(f"CoverageReportPath: {coverage_report_path}")

def downloadArtifacts():
    """DownloadArtifacts
    :return
    """

def addHistory(test_type):
    """ Копирует историю в текущий билд
    :return
    """
    current_history_dir = os.environ.get('directoryWithReports', directory_with_reports)
    saved_history_dir = os.environ.get('allureHistoryPath', allure_history_path)

    print(f"SavedHistoryDir: {saved_history_dir}")

    if os.path.exists(saved_history_dir):
        shutil.copytree(saved_history_dir, current_history_dir, dirs_exist_ok=True)
        print("Copy Allure history to current report")
        print(f"AllureHistoryPath: {allure_history_path}")
        print(f"CurrentHistoryDir: {current_history_dir}")
        print("Contents of CurrentHistoryDir:\n" + os.listdir(current_history_dir))
    else:
        current_history_dir = directory_with_reports
        saved_history_dir = allure_history_path
        os.makedirs(saved_history_dir, exist_ok=True)
        print(f"Created Allure History folder for {test_type} test types. Path: {saved_history_dir}")

def generateReport(report_path):
    """Генерирует HTML отчёт allure
    :return
    """
    # Используем os.path.join для создания полного пути к каталогу allure-report
    allure_report_path = os.path.join(report_path, 'allure-report')

    # Генерация отчета Allure
    generate_command = [os.path.join(os.environ.get('AllureProgramPath'), 'bin', 'allure.bat'), 'generate',
                        'allure-results', '--clean', '-o', allure_report_path]
    subprocess.run(generate_command, check=True)

    # Проверка наличия файла index.html в сгенерированном отчете
    if os.path.isfile(os.path.join(allure_report_path, 'index.html')):
        print(f"Allure report is generated to {report_path}\\allure-report")
        # Вывод содержимого каталога allure-report
        print("Contents of allure-report:")
        print(os.listdir(allure_report_path))
    else:
        print(f"Error: Allure report is NOT generated to {report_path}\\allure-report")
        exit(1)

def excludePathFromReport():
    """ExcludePathFromReport
    :return
    """
    path_to_delete = os.environ.get('pathToDelete')

    # Копирование содержимого указанного каталога в текущий каталог
    for root, dirs, files in os.walk(path_to_delete):
        for name in dirs:
            src_dir = os.path.join(root, name)
            dest_dir = os.path.join('.', os.path.relpath(src_dir, path_to_delete))
            os.makedirs(dest_dir, exist_ok=True)

        for name in files:
            src_file = os.path.join(root, name)
            dest_file = os.path.join('.', os.path.relpath(src_file, path_to_delete))
            with open(src_file, 'rb') as src, open(dest_file, 'wb') as dest:
                dest.write(src.read())

    # Удаление указанного каталога и его содержимого
    for root, dirs, files in os.walk(path_to_delete, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path_to_delete)


def addCodeCoverageURLInReport():
    """addCodeCoverageURLInReport
    :return
    """
    file_to_fix = "index.html"
    link_template = os.environ.get('linkForCoverageReports')

    # Открываем файл для чтения
    with open(file_to_fix, 'r', encoding='utf-8') as file:
        content = file.read()

    # Создаем строку для вставки
    link = f'\n<a href="{link_template}" style="color:#fff; background:#343434; font-weight: 700; padding-left: 14px; padding-right: 14px; width: 180px;" target="_blank">Code Coverage Report</a>'

    # Используем регулярное выражение для поиска места вставки
    regex = re.compile(r'^<body>', re.MULTILINE)
    replace_substring = r'\g<0>' + link
    updated_content = regex.sub(replace_substring, content)

    # Открываем файл для записи
    with open(file_to_fix, 'w', encoding='utf-8') as file:
        file.write(updated_content)


def deleteOldReport():
    """DeleteOldReport
     :return
     """
    max_count_of_build_directories = int(os.environ.get('saveAllureLatestReports'))
    current_build_directories = [entry for entry in Path('.').iterdir() if entry.is_dir()]

    current_count_of_build_directories = len(current_build_directories)

    print(f"Current count of build directories: {current_count_of_build_directories}")

    if current_count_of_build_directories >= max_count_of_build_directories:
        while current_count_of_build_directories >= max_count_of_build_directories:
            folders_to_exclude = ["history-*"]
            directories_to_remove = [directory for directory in current_build_directories if
                                     not any(pattern in str(directory) for pattern in folders_to_exclude)]
            directory_to_remove = min(directories_to_remove, key=lambda d: d.stat().st_mtime)

            shutil.rmtree(directory_to_remove, ignore_errors=True)

            print(f"Build directory '{directory_to_remove}' was removed")

            current_build_directories = [entry for entry in Path('.').iterdir() if entry.is_dir()]
            current_count_of_build_directories = len(current_build_directories)
    else:
        print(
            f"Count of build directories is less than {max_count_of_build_directories}. Don't need to delete directory")





