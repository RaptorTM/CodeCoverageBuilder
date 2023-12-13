import os
import shutil
import subprocess

def updateHistory():
    """updateHistory
    :return
    """
    current_build_history_dir = os.path.join(os.environ.get('reportPath'), 'allure-report', 'history')
    saved_history_dir = os.environ.get('SavedHistoryDir')

    print(f"SavedHistoryDir: {saved_history_dir}")

    # Проверка существования SavedHistoryDir
    if os.path.exists(saved_history_dir):
        print(f"SavedHistoryDir: {saved_history_dir}")

        # Удаление файлов, исключая те, которые содержат "history-"
        for file_name in os.listdir(saved_history_dir):
            if not file_name.startswith("history-"):
                file_path = os.path.join(saved_history_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)

        print("Clean old history")

    # Проверка существования CurrentBuildHistoryDir
    if os.path.exists(current_build_history_dir):
        # Копирование содержимого CurrentBuildHistoryDir в SavedHistoryDir
        shutil.copytree(current_build_history_dir, saved_history_dir, dirs_exist_ok=True)
        print("Update history")
        print(f"Latest history saved in: {saved_history_dir}")
        print("Contents of SavedHistoryDir:")
        print(os.listdir(saved_history_dir))
    else:
        print(f"{current_build_history_dir} does not exist")

def saveCurrentHistory():
    """saveCurrentHistory
    :return
    """
