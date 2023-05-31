import hashlib
import cloudinary
import cloudinary.uploader

from src.conf.config import settings


class UploadService:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    @staticmethod
    def create_name_avatar(email: str, prefix: str):
        """
        The create_name_avatar function takes an email and a prefix,
        and returns a string of the form 'prefix/name'. The name is
        the first 10 characters of the SHA256 hash of the email.


        :param email: str: Specify the type of input that is expected
        :param prefix: str: Specify the folder where the avatar will be saved
        :return: A string
        """
        name = hashlib.sha256(email.encode()).hexdigest()[:10]
        return f"{prefix}/{name}"

    @staticmethod
    def upload(file, public_id):
        """
        The upload function takes a file and public_id as arguments.
        It then uploads the file to Cloudinary using the public_id provided.
        The function returns a dictionary containing information about the uploaded image.

        :param file: Specify the file to upload
        :param public_id: Set the public id of the image
        :return: A dictionary with the following fields
        """
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_avatar(public_id, version):
        """
        The get_url_avatar function takes in a public_id and version number,
            then returns the url of the avatar image.

        :param public_id: Identify the image in the cloudinary database
        :param version: Get the latest version of an image
        :return: A url to an image
        """
        src_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop="fill", version=version)
        return src_url

    
