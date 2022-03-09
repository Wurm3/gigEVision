import os, shutil
from settings import Settings



def delete_folder_content(folder):
    for filename in os.listdir("./" + folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


settings = Settings()
delete_folder_content(settings.INFRARED_IMAGES_PATH)
delete_folder_content(settings.VISIBLE_IMAGES_PATH)