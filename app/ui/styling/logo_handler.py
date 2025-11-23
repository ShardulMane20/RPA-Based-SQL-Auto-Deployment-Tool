import os
from PIL import Image, ImageTk

class LogoHandler:
    @staticmethod
    def create_logo_placeholder():
        """Load the actual logo image from assets/logo.png - Complete logic from original"""
        try:
            # Try to load the actual logo from assets folder
            logo_path = os.path.join("assets", "logo.png")
            if os.path.exists(logo_path):
                # Load and resize the logo image
                img = Image.open(logo_path)
                # Resize to reasonable dimensions for the login page (max 120x60)
                img.thumbnail((240, 120), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                # Fallback: create a simple colored rectangle as logo if file not found
                img = Image.new('RGB', (80, 40), color='#3498db')
                return ImageTk.PhotoImage(img)
        except Exception as e:
            # If any error occurs, create a simple fallback logo
            try:
                img = Image.new('RGB', (80, 40), color='#3498db')
                return ImageTk.PhotoImage(img)
            except:
                # If PIL completely fails, return None
                return None

    @staticmethod
    def load_logo(path, size=(240, 120)):
        """Load and resize logo image from specified path"""
        try:
            if os.path.exists(path):
                img = Image.open(path)
                # Resize using thumbnail to maintain aspect ratio
                img.thumbnail(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                # Return fallback logo if path doesn't exist
                return LogoHandler._create_fallback_logo(size)
        except Exception as e:
            # Return fallback logo on any error
            return LogoHandler._create_fallback_logo(size)

    @staticmethod
    def _create_fallback_logo(size=(80, 40), color='#3498db'):
        """Create a simple colored rectangle as fallback logo"""
        try:
            img = Image.new('RGB', size, color=color)
            return ImageTk.PhotoImage(img)
        except:
            return None

    @staticmethod
    def load_icon(path):
        """Load icon for window title bar"""
        try:
            if os.path.exists(path):
                return ImageTk.PhotoImage(file=path)
            else:
                return None
        except:
            return None

    @staticmethod
    def create_logo_with_text(text, size=(240, 120), bg_color='#3498db', text_color='white'):
        """Create a logo with text overlay"""
        try:
            from PIL import ImageDraw, ImageFont
            
            img = Image.new('RGB', size, color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Try to use a nice font, fallback to default if not available
            try:
                # Adjust font size based on image size
                font_size = max(12, min(size) // 8)
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the text
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            draw.text((x, y), text, fill=text_color, font=font)
            return ImageTk.PhotoImage(img)
        except:
            return LogoHandler._create_fallback_logo(size, bg_color)

    @staticmethod
    def resize_image(image_path, new_size, maintain_aspect=True):
        """Resize an image to new dimensions"""
        try:
            img = Image.open(image_path)
            
            if maintain_aspect:
                img.thumbnail(new_size, Image.Resampling.LANCZOS)
            else:
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            return ImageTk.PhotoImage(img)
        except Exception as e:
            return None

    @staticmethod
    def get_image_info(image_path):
        """Get information about an image file"""
        try:
            if not os.path.exists(image_path):
                return None
                
            img = Image.open(image_path)
            return {
                'size': img.size,
                'format': img.format,
                'mode': img.mode,
                'file_size': os.path.getsize(image_path)
            }
        except Exception as e:
            return None

    @staticmethod
    def validate_image_file(image_path):
        """Validate if file is a valid image"""
        try:
            if not os.path.exists(image_path):
                return False, "File does not exist"
                
            img = Image.open(image_path)
            img.verify()  # Verify it's a valid image
            return True, "Valid image file"
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"

    @staticmethod
    def create_company_logo(company_name="Zanvar", size=(240, 120)):
        """Create a company logo with company name"""
        return LogoHandler.create_logo_with_text(
            text=company_name,
            size=size,
            bg_color='#3498db',
            text_color='white'
        )

    @staticmethod
    def ensure_assets_directory():
        """Ensure the assets directory exists"""
        assets_dir = "assets"
        if not os.path.exists(assets_dir):
            try:
                os.makedirs(assets_dir)
                return True, f"Created assets directory: {assets_dir}"
            except Exception as e:
                return False, f"Failed to create assets directory: {str(e)}"
        return True, "Assets directory already exists"

    @staticmethod
    def get_supported_formats():
        """Get list of supported image formats"""
        return [
            ('PNG Files', '*.png'),
            ('JPEG Files', '*.jpg;*.jpeg'),
            ('GIF Files', '*.gif'),
            ('BMP Files', '*.bmp'),
            ('TIFF Files', '*.tiff'),
            ('All Image Files', '*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff'),
            ('All Files', '*.*')
        ]
