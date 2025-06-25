#distortions kısmı tamamlandı diğer kısımlarla devam edebilirsin 
import random
import numpy as np
from PIL import Image, ImageFilter

class ImageDistorter:
    """
    A utility class for applying various image distortion techniques.

    This class provides methods for augmenting images by introducing random distortions
    such as rotation, blurring, noise, and resolution degradation. These distortions
    are typically used in OCR and computer vision pipelines to simulate real-world imperfections.
    """

    def __init__(
        self,
        blur_radius_range=(1, 2),
        noise_level_range=(0.1, 0.15),
        scale_factor_range=(0.7, 0.9),
        rotation_angle_range=(-15, 15)
    ):
        """
        Initializes the distortion parameters.

        Args:
            blur_radius_range (tuple): Min and max values for blur radius.
            noise_level_range (tuple): Min and max values for Gaussian noise level.
            scale_factor_range (tuple): Min and max downscaling factor for resolution degradation.
            rotation_angle_range (tuple): Min and max rotation angles in degrees.
        """
        self.blur_radius_range = blur_radius_range
        self.noise_level_range = noise_level_range
        self.scale_factor_range = scale_factor_range
        self.rotation_angle_range = rotation_angle_range

    def apply_random_rotation(self, image):
        """
        Applies a random rotation to the given image.

        Args:
            image (PIL.Image): The image to be rotated.

        Returns:
            PIL.Image: The rotated image.
        """
        angle = random.randint(*self.rotation_angle_range)
        rotated_image = image.rotate(angle, expand=True)
        return rotated_image

    def apply_random_blur(self, image,blur_radius_range):
        """
        Applies a Gaussian blur effect with a random radius to the image.

        Args:
            image (PIL.Image): The input image to be blurred.

        Returns:
            PIL.Image: The blurred image.
        """
        blur_radius = random.uniform(*self.blur_radius_range)
        return image.filter(ImageFilter.GaussianBlur(blur_radius))

    def apply_random_noise(self, image,noise_level_range):
        """
        Adds random Gaussian noise to the image.

        Args:
            image (PIL.Image): The input image to apply noise on.

        Returns:
            PIL.Image: The image with added noise.
        """
        image_np = np.array(image).astype(np.float32)
        noise_level = random.uniform(*self.noise_level_range)
        noise = np.random.normal(0, 255 * noise_level, image_np.shape)
        noisy_image_np = np.clip(image_np + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_image_np)

    def apply_random_resolution_reduce(self, image,scale_factor_range):
        """
        Randomly downscales an image and then restores it to its original size.

        This process is typically used for data augmentation by simulating low-resolution images.

        Args:
            image (PIL.Image): The input image to be degraded.

        Returns:
            PIL.Image: The distorted image, resized back to its original dimensions.
        """
        original_size = image.size
        scale_factor = random.uniform(*self.scale_factor_range)
        new_width = max(1, int(original_size[0] * scale_factor))
        new_height = max(1, int(original_size[1] * scale_factor))
        degraded_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        restored_image = degraded_image.resize(original_size, Image.Resampling.LANCZOS)
        return restored_image
