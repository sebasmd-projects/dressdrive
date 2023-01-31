from datetime import date
from PIL import Image


def optimize_image(sender, instance, *args, **kwargs):
    """
    This function is used as a signal handler for the post_save signal of a model with an avatar field. It opens the image file, saves it with a quality of 40 and optimizes the image.
    """
    if instance.avatar:
        avatar = Image.open(instance.avatar.path)
        avatar.save(instance.avatar.path, quality=40, optimize_image=True)


def avatar_directory_path(instance, filename):
    """
    This function is used to generate a file path for an avatar image when a user is saved. The path includes the current year, month, and day, as well as the full name of the user and the original filename of the image.
    """
    return f"user/{instance.full_name}-{instance.id}/avatar/{date.today().year}-{date.today().month}-{date.today().day}/{filename}"