import subprocess
import shutil

from app_core_dressdrive.general_settings import BASE_DIR


def run_tests(other_params, delete_folders: str = "no"):
    if delete_folders == ("yes" or "y" or "YES"):
        shutil.rmtree(BASE_DIR.child('allure_results'))
        shutil.rmtree(BASE_DIR.child('.pytest_cache'))

    subprocess.call(
        f"pytest {''.join(other_params)}",
        shell=True
    )

    subprocess.call(
        "allure serve allure_results",
        shell=True
    )


if __name__ == "__main__":
    print("""
          --maxfail=3
          -n # | auto, logic or a number
          -rsxX 
          -l 
          --tb=short
          """)

    try:
        other_params = input("Other params: ")
        delete_folders = input("Delete folders (yes/no): ")
        run_tests(other_params, delete_folders)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error:", e)
