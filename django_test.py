import subprocess
import shutil

from app_core_dressdrive.general_settings import BASE_DIR


def run_tests(other_params, delete_folders: bool = False):
    if delete_folders:
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
        # other_params = input("Other params: ")
        # delete_folders = bool(input("Delete folders: "))
        other_params = ""
        delete_folders = True
        run_tests(other_params, delete_folders)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error:", e)
