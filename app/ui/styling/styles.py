from tkinter import ttk
from app.core.config import AppConfig

class StyleManager:
    def __init__(self, root, app_controller):
        self.root = root
        self.app = app_controller
        self.style = None
        self.setup_colors()
        self.setup_fonts()
        self.setup_styles()

    def setup_colors(self):
        """Define color scheme from AppConfig"""
        # Colors are already defined in AppConfig, just reference them
        self.colors = AppConfig.COLORS
        
        # Set root background
        self.root.configure(bg=self.colors['bg_color'])

    def setup_fonts(self):
        """Define font scheme from AppConfig"""
        # Fonts are already defined in AppConfig, just reference them
        self.fonts = AppConfig.FONTS

    def setup_styles(self):
        """Configure TTK styles - Complete implementation from original setup_style"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure modern button styles
        self._setup_button_styles()
        
        # Configure labels
        self._setup_label_styles()
        
        # Configure Progressbar
        self._setup_progressbar_styles()
        
        # Configure Treeview
        self._setup_treeview_styles()

    def _setup_button_styles(self):
        """Setup all button styles from original"""
        # Accent button style
        self.style.configure('Accent.TButton', 
                           foreground='white', 
                           background=self.colors['button_accent'],
                           font=self.fonts['normal'],
                           padding=(12, 8),
                           borderwidth=0,
                           relief='flat')
        self.style.map('Accent.TButton',
                      background=[('active', self.colors['button_accent_hover']), 
                                ('pressed', self.colors['button_accent_pressed'])],
                      foreground=[('active', 'white')])
        
        # Modern button style
        self.style.configure('Modern.TButton', 
                           foreground='white', 
                           background=self.colors['button_modern'],
                           font=self.fonts['normal'],
                           padding=(12, 8),
                           borderwidth=0,
                           relief='flat')
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['button_modern_hover'])],
                      foreground=[('active', 'white')])
        
        # Warning button style
        self.style.configure('Warning.TButton', 
                           foreground='white', 
                           background=self.colors['button_warning'],
                           font=self.fonts['normal'],
                           padding=(12, 8),
                           borderwidth=0,
                           relief='flat')
        self.style.map('Warning.TButton',
                      background=[('active', self.colors['button_warning_hover'])],
                      foreground=[('active', 'white')])
        
        # Red button style
        self.style.configure('Red.TButton', 
                           foreground='white', 
                           background=self.colors['button_red'],
                           font=self.fonts['bold'],
                           padding=(12, 8),
                           borderwidth=0,
                           relief='flat')
        self.style.map('Red.TButton',
                      background=[('active', self.colors['button_red_hover'])],
                      foreground=[('active', 'white')])

    def _setup_label_styles(self):
        """Setup label styles from original"""
        # Header label style
        self.style.configure('Header.TLabel', 
                           background=self.colors['card_bg'],
                           foreground=self.colors['muted_color'],
                           font=self.fonts['normal'])
        
        # Header bold label style
        self.style.configure('Header.Bold.TLabel', 
                           background=self.colors['card_bg'],
                           foreground=self.colors['primary_color'],
                           font=self.fonts['bold'])
        
        # Section label style
        self.style.configure('Section.TLabel', 
                           background=self.colors['bg_color'],
                           foreground=self.colors['primary_color'],
                           font=self.fonts['header'])

    def _setup_progressbar_styles(self):
        """Setup progressbar styles from original"""
        self.style.configure('Custom.Horizontal.TProgressbar',
                           troughcolor=self.colors['progress_trough'],
                           background=self.colors['progress_bar'],
                           borderwidth=0)

    def _setup_treeview_styles(self):
        """Setup treeview styles from original"""
        self.style.configure("Treeview.Heading", 
                           font=self.fonts['bold'],
                           background=self.colors['treeview_heading_bg'],
                           foreground=self.colors['treeview_heading_fg'])
        self.style.configure("Treeview", 
                           font=self.fonts['normal'], 
                           rowheight=25,
                           background=self.colors['treeview_bg'],
                           foreground=self.colors['treeview_fg'])

    def get_style(self):
        """Get the TTK style object"""
        return self.style

    def update_theme(self, theme_name):
        """Update the TTK theme"""
        if theme_name in self.style.theme_names():
            self.style.theme_use(theme_name)
            # Reapply custom styles after theme change
            self.setup_styles()

    def get_available_themes(self):
        """Get list of available TTK themes"""
        return self.style.theme_names()

    def configure_custom_style(self, style_name, **kwargs):
        """Configure a custom style"""
        self.style.configure(style_name, **kwargs)

    def map_custom_style(self, style_name, **kwargs):
        """Map state-based style properties"""
        self.style.map(style_name, **kwargs)

    def create_button_style(self, name, bg_color, fg_color='white', hover_color=None):
        """Create a custom button style"""
        self.style.configure(f'{name}.TButton',
                           foreground=fg_color,
                           background=bg_color,
                           font=self.fonts['normal'],
                           padding=(12, 8),
                           borderwidth=0,
                           relief='flat')
        
        if hover_color:
            self.style.map(f'{name}.TButton',
                          background=[('active', hover_color)],
                          foreground=[('active', fg_color)])

    def create_label_style(self, name, bg_color, fg_color, font_key='normal'):
        """Create a custom label style"""
        self.style.configure(f'{name}.TLabel',
                           background=bg_color,
                           foreground=fg_color,
                           font=self.fonts[font_key])

    def get_color(self, color_key):
        """Get color from color scheme"""
        return self.colors.get(color_key, '#000000')

    def get_font(self, font_key):
        """Get font from font scheme"""
        return self.fonts.get(font_key, ('Segoe UI', 11))

    def apply_widget_style(self, widget, bg=None, fg=None, font=None):
        """Apply styling to a regular tkinter widget"""
        if bg:
            widget.configure(bg=bg)
        if fg:
            widget.configure(fg=fg)
        if font:
            widget.configure(font=font)

    def get_themed_colors(self):
        """Get current themed colors"""
        return {
            'background': self.colors['bg_color'],
            'foreground': self.colors['primary_color'],
            'card_background': self.colors['card_bg'],
            'accent': self.colors['accent_color'],
            'success': self.colors['success_color'],
            'error': self.colors['error_color'],
            'warning': self.colors['warning_color']
        }
