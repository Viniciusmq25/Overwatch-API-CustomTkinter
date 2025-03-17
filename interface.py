import customtkinter
from PIL import Image, ImageTk
import requests
from io import BytesIO
from functools import lru_cache


# API settings
base_url = "https://overfast-api.tekrop.fr/"

def get_hero_info(name):
    '''Obtém informações detalhadas de um herói'''
    url = f"{base_url}heroes/{name}"  
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        hero_data = response.json()
        print(hero_data)
        # Agendar a atualização na thread principal
        return hero_data
    else:
        print(f"Failed to retrieve:{response.status_code}")
        return None

class ShooterCounterApp:
    def __init__(self):
        self.base_url = base_url
        self.font_family = "Roboto"
        self.small_font = (12)
        self.medium_font = (24)
        self.large_font = (30)
        self.max_columns = 5
        self.tank_color = "#F15A29"
        self.support_color = "#4CAF50"
        self.damage_color = "#9C27B0"
        self.all_color = "#4B8BF5"
        
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        
        # Inicializa a janela principal
        self.root = customtkinter.CTk() # Cria a janela principal
        self.root.title("ShooterCounter")
        self.root.iconbitmap("shootcounter.ico")
        self.root.geometry("1200x750")
        
        self.main_container = customtkinter.CTkScrollableFrame(
          self.root,
          scrollbar_button_color=self.all_color,
        )
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Header
        self.header_frame = customtkinter.CTkFrame(self.main_container, corner_radius=15, height=80)
        self.header_frame.pack(fill="x")
        
        # App title and subtitle
        self.title_frame = customtkinter.CTkFrame(self.header_frame)
        self.title_frame.pack(side="left", fill="both", expand=True)
        
        self.title_label = customtkinter.CTkLabel(
            self.title_frame, 
            text="ShooterCounter", 
            font=(self.font_family, self.large_font, "bold"),
            text_color=self.all_color
        )
        self.title_label.pack(side="left", pady=30, padx=10)
        
        self.subtitle_label = customtkinter.CTkLabel(
            self.title_frame, 
            text="Hero Database", 
            font=(self.font_family, self.medium_font),
            text_color="#888888"
        )
        self.subtitle_label.pack(side="left", padx=10)
        
        # Variáveis de controle do grid e lista de cards
        self.current_row = 0
        self.current_column = 0
        self.cards_info = []  # [(card, role), ...]
        
        # Frame com scroll para os cards
        # Filter section
        self.filter_frame = customtkinter.CTkFrame(self.main_container, corner_radius=15, height=100)
        self.filter_frame.pack(fill="x", pady=(0, 20))
        # Cards section
        self.cards_frame = customtkinter.CTkFrame(self.main_container)
        self.cards_frame.pack(fill="both", expand=True)
        
        self.filter_title = customtkinter.CTkLabel(
            self.filter_frame, 
            text="Filter Heroes", 
            font=(self.font_family, self.medium_font, "bold"),
            anchor="w" # Align text to left (w = west)
        )
        self.filter_title.pack(fill="x", pady=(15, 10), padx=20)
    
        self.buttons_container = customtkinter.CTkFrame(self.filter_frame, fg_color="transparent")
        self.buttons_container.pack(fill="x", expand=True, padx=20, pady=(0, 15))
            
        # Create modern style buttons
        self.button_all = self.create_filter_button(
            self.buttons_container, "All Heroes", self.all_color, self.on_button_all_click
        )
        self.button_all.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        self.button_tank = self.create_filter_button(
            self.buttons_container, "Tank", self.tank_color, self.on_button_tank_click
        )
        self.button_tank.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        self.button_support = self.create_filter_button(
            self.buttons_container, "Support", self.support_color, self.on_button_sup_click
        )
        self.button_support.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        self.button_damage = self.create_filter_button(
            self.buttons_container, "Damage", self.damage_color, self.on_button_dps_click
        )
        self.button_damage.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
    def filter_cards(self, role_filter=None):
        new_row = 0
        new_col = 0
        for card, role in self.cards_info:
            if role_filter is None or role.lower() == role_filter:
                card.grid(row=new_row, column=new_col, padx=5, pady=5, sticky="nsew")
                new_col += 1
                if new_col >= self.max_columns:
                    new_col = 0
                    new_row += 1
            else:
                card.grid_remove()
    
    def create_filter_button(self, parent, text, accent_color, command):
      """Create custom styled filter button"""
      button = customtkinter.CTkButton(
          parent,
          text=text,
          font=(self.font_family, self.small_font, "bold"),
          height=40,
          corner_radius=8,
          hover_color=accent_color,
          fg_color="#333333",
          command=command
      )
      # Store the accent color for active state
      button.accent_color = accent_color
      return button
    
    def update_button_states(self, active_button=None):
        """Update button appearances based on active filter"""
        # Reset all buttons
        for button in [self.button_all, self.button_tank, self.button_support, self.button_damage]:
            button.configure(fg_color="#333333")
        
        # Set active button
        if active_button:
            active_button.configure(fg_color=active_button.accent_color)
    
    def on_button_all_click(self):
        print("All button clicked")
        self.update_button_states(self.button_all)
        self.filter_cards(None)
    
    def on_button_tank_click(self):
        print("Tank button clicked")
        self.update_button_states(self.button_tank)
        self.filter_cards("tank")
    
    def on_button_sup_click(self):
        print("Support button clicked")
        self.update_button_states(self.button_support)
        self.filter_cards("support")
    
    def on_button_dps_click(self):
        print("Damage button clicked")
        self.update_button_states(self.button_damage)
        self.filter_cards("damage")
    
    def open_hero_info(self, hero):
        print(f"Hero Info button clicked for {hero}")
        ToplevelWindow(self.root, hero)
        
    def load_heroes(self):
        response = requests.get(f"{self.base_url}heroes")
        if response.status_code == 200:
            heroes = response.json()
            print(heroes)
            for hero in heroes:
                self.add_hero_card(hero)
        else:
            print("Failed to load heroes")
    
    def add_hero_card(self, hero):
        '''Adiciona um card de herói com dimensões fixas'''
        hero_image_url = hero['portrait']
        hero_name = hero['name']
        hero_role = hero['role']
        
        hero_card = customtkinter.CTkFrame(self.cards_frame, width=250, height=250)
        
        hero_card.grid(row=self.current_row, column=self.current_column, padx=5, pady=5, sticky="nsew")
        
        # Carregar e redimensionar a imagem
        response = requests.get(hero_image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((100, 100))
        hero_image = customtkinter.CTkImage(light_image=img, dark_image=img, size=(100, 100))
        hero_image_label = customtkinter.CTkLabel(hero_card, text="", image=hero_image)
        hero_image_label.pack(pady=10, padx=10)
        
        hero_label = customtkinter.CTkLabel(hero_card, text=hero_name, font=(self.font_family, self.medium_font), wraplength=220)
        hero_label.pack(pady=5, padx=5)
        
        role_frame = customtkinter.CTkFrame(
          hero_card, 
          fg_color="transparent"
        )
        role_frame.pack(pady=5)
        
        role_color = self.tank_color if hero_role == "tank" else self.support_color if hero_role == "support" else self.damage_color
        role_label = customtkinter.CTkLabel(
          role_frame,
          text=f"Role: ",
          font=(self.font_family, self.small_font),
          wraplength=220
          )
        role_label.pack(side="left")
        
        role_value = customtkinter.CTkLabel(
          role_frame, 
          text=f"{hero_role}", 
          font=(self.font_family, self.small_font), 
          text_color=role_color, 
          wraplength=220
          )
        role_value.pack(side="left", fill="x", expand=True)
        
        bind_label = customtkinter.CTkLabel(hero_card, text="Click for more info", font=(self.font_family, self.small_font),text_color=self.all_color, wraplength=220)
        bind_label.bind("<Button-1>", lambda e: self.open_hero_info(hero['key']))
        bind_label.pack(pady=5, padx=5)
        
        self.cards_info.append((hero_card, hero_role))
        
        self.current_column += 1
        if self.current_column >= self.max_columns:
            self.current_column = 0
            self.current_row += 1
        
        for i in range(self.max_columns):
            self.cards_frame.grid_columnconfigure(i, weight=1)
  
    def run(self):
        self.load_heroes()
        self.root.mainloop()

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, hero, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.font_family = "Roboto"
        self.small_font = 12
        self.medium_font = 18
        self.large_font = 26
        
        # Get hero info
        hero_info = get_hero_info(hero)
        
        self.title(f"{hero_info['name']} - Hero Details")
        self.iconphoto(False, ImageTk.PhotoImage(file="shootcounter.ico"))
        self.geometry("800x800")
        
        # Hero basic information
        hero_image_url = hero_info['portrait']
        hero_name = hero_info['name']
        hero_role = hero_info['role']
        hero_description = hero_info['description']
        hero_location = hero_info['location']
        hero_age = hero_info['age']
        hero_birthdate = hero_info['birthday'] if hero_info['birthday'] is not None else "Unknown"
        
        # Hero hitpoints information
        hero_health = hero_info['hitpoints']['health']
        hero_armor = hero_info['hitpoints']['armor']
        hero_shield = hero_info['hitpoints']['shields']
        hero_total_health = hero_info['hitpoints']['total']
        
        # Create main container with padding
        container = customtkinter.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section with hero image and name
        header_frame = customtkinter.CTkFrame(container, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Load and display hero image
        response = requests.get(hero_image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((140, 140))
        hero_image = customtkinter.CTkImage(light_image=img, dark_image=img, size=(140, 140))
        hero_image_label = customtkinter.CTkLabel(header_frame, text="", image=hero_image)
        hero_image_label.pack(side="left", pady=15, padx=20)
        
        # Hero name and role
        hero_title_frame = customtkinter.CTkFrame(header_frame, fg_color="transparent")
        hero_title_frame.pack(side="left", fill="both", expand=True, pady=15, padx=10)
        
        hero_name_label = customtkinter.CTkLabel(
            hero_title_frame, 
            text=hero_name, 
            font=(self.font_family, self.large_font, "bold"),
            anchor="w" # Align text to left (w = west)
        )
        hero_name_label.pack(fill="x", pady=(15, 5), padx=5) # Add padding to top and bottom (15 at top, 5 at bottom)
        
        hero_role_label = customtkinter.CTkLabel(
            hero_title_frame, 
            text=f"Role: {hero_role}", 
            font=(self.font_family, self.medium_font),
            text_color="#4B8BF5",
            anchor="w" # Align text to left (w = west)
        )
        hero_role_label.pack(fill="x", pady=2, padx=5)
        
        # Two-column layout for hero details
        details_frame = customtkinter.CTkScrollableFrame(container, )
        details_frame.pack(fill="both", expand=True, pady=10)
        details_frame.grid_columnconfigure(0, weight=3) # Make left column 3 times larger than right column
        details_frame.grid_columnconfigure(1, weight=2) # Make right column 2 times larger than left column
        details_frame.grid_rowconfigure(0, weight=1) # Make row 1 times larger than other rows
        details_frame.grid_rowconfigure(1, weight=1) # Make row 1 times larger than other rows
        
        # Left column - Bio information
        bio_frame = customtkinter.CTkFrame(details_frame, corner_radius=15)
        bio_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        bio_title = customtkinter.CTkLabel(
            bio_frame, 
            text="Hero Biography", 
            font=(self.font_family, self.medium_font, "bold"),
            anchor="w"
        )
        bio_title.pack(fill="x", pady=(15, 10), padx=20)
        
        # Bio details in a nice layout
        bio_details = customtkinter.CTkFrame(bio_frame, fg_color="transparent")
        bio_details.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Location info
        location_frame = customtkinter.CTkFrame(bio_details, fg_color="transparent")
        location_frame.pack(fill="x", pady=5)
        
        location_label = customtkinter.CTkLabel(
            location_frame, 
            text="Location:", 
            font=(self.font_family, self.small_font, "bold"),
            width=80,
            anchor="w"
        )
        location_label.pack(side="left")
        
        location_value = customtkinter.CTkLabel(
            location_frame, 
            text=hero_location, 
            font=(self.font_family, self.small_font),
            anchor="w",
            wraplength=200
        )
        location_value.pack(side="left", fill="x", expand=True)
        
        # Age/Birthday info
        age_frame = customtkinter.CTkFrame(bio_details, fg_color="transparent")
        age_frame.pack(fill="x", pady=5)
        
        age_label = customtkinter.CTkLabel(
            age_frame, 
            text="Age:", 
            font=(self.font_family, self.small_font, "bold"),
            width=80,
            anchor="w"
        )
        age_label.pack(side="left")
        
        age_value = customtkinter.CTkLabel(
            age_frame, 
            text=f"{hero_age}" if hero_age else "Unknown", 
            font=(self.font_family, self.small_font),
            anchor="w"
        )
        age_value.pack(side="left", fill="x", expand=True)
        
        # Birthday info
        birthday_frame = customtkinter.CTkFrame(bio_details, fg_color="transparent")
        birthday_frame.pack(fill="x", pady=5)
        
        birthday_label = customtkinter.CTkLabel(
            birthday_frame, 
            text="Birthday:", 
            font=(self.font_family, self.small_font, "bold"),
            width=80,
            anchor="w"
        )
        birthday_label.pack(side="left")
        
        birthday_value = customtkinter.CTkLabel(
            birthday_frame, 
            text=hero_birthdate, 
            font=(self.font_family, self.small_font),
            anchor="w"
        )
        birthday_value.pack(side="left", fill="x", expand=True)
        
        # Description with a separator
        separator = customtkinter.CTkFrame(bio_details, height=1, fg_color="#555555")
        separator.pack(fill="x", pady=15)
        
        description_title = customtkinter.CTkLabel(
            bio_details, 
            text="Background", 
            font=(self.font_family, self.medium_font, "bold"),
            anchor="w"
        )
        description_title.pack(fill="x", pady=(0, 10))
        
        description_tabel = customtkinter.CTkFrame(bio_details)
        description_tabel.pack(fill="x")
        
        description_text = customtkinter.CTkLabel(
            description_tabel, 
            text=hero_description, 
            font=(self.font_family, self.small_font),
            wraplength=300,
            justify="left"
        )
        description_text.pack(fill="x", expand=True, side="left")
        
        #Stats and abilities 
        stats_frame = customtkinter.CTkFrame(details_frame, corner_radius=15)
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0)) # Columnspan to make it full width of the grid
        
        stats_title = customtkinter.CTkLabel(
            stats_frame, 
            text="Hero Stats", 
            font=(self.font_family, self.medium_font, "bold"),
            anchor="w"
        )
        stats_title.pack(fill="x", pady=(15, 10), padx=20)
        
        # Create visual health bar displays
        health_frame = customtkinter.CTkFrame(stats_frame, fg_color="transparent")
        health_frame.pack(fill="x", padx=20, pady=(5, 20))
        
        # Health bar
        health_label = customtkinter.CTkLabel(
            health_frame, 
            text=f"Health: {hero_health}", 
            font=(self.font_family, self.small_font, "bold"),
            anchor="w"
        )
        health_label.pack(fill="x", pady=(10, 2))
        
        health_bar_bg = customtkinter.CTkFrame(health_frame, height=20, fg_color="#333333", corner_radius=5)
        health_bar_bg.pack(fill="x", pady=2)
        
        health_bar_width = int((int(hero_health) / int(hero_total_health)) * 100) if hero_total_health > 0 else 0
        health_bar = customtkinter.CTkFrame(health_bar_bg, height=20, width=health_bar_width, fg_color="#3CB371", corner_radius=5)
        health_bar.place(relheight=1, relwidth=health_bar_width/100)
        
        # Armor bar
        armor_label = customtkinter.CTkLabel(
            health_frame, 
            text=f"Armor: {hero_armor}", 
            font=(self.font_family, self.small_font, "bold"),
            anchor="w"
        )
        armor_label.pack(fill="x", pady=(10, 2))
        
        armor_bar_bg = customtkinter.CTkFrame(health_frame, height=20, fg_color="#333333", corner_radius=5)
        armor_bar_bg.pack(fill="x", pady=2)
        
        armor_bar_width = int((int(hero_armor) / int(hero_total_health)) * 100) if hero_total_health > 0 else 0
        armor_bar = customtkinter.CTkFrame(armor_bar_bg, height=20, width=armor_bar_width, fg_color="#FF9800", corner_radius=5)
        armor_bar.place(relheight=1, relwidth=armor_bar_width/100)
        
        # Shield bar
        shield_label = customtkinter.CTkLabel(
            health_frame, 
            text=f"Shield: {hero_shield}", 
            font=(self.font_family, self.small_font, "bold"),
            anchor="w"
        )
        shield_label.pack(fill="x", pady=(10, 2))
        
        shield_bar_bg = customtkinter.CTkFrame(health_frame, height=20, fg_color="#333333", corner_radius=5)
        shield_bar_bg.pack(fill="x", pady=2)
        
        shield_bar_width = int((int(hero_shield) / int(hero_total_health)) * 100) if hero_total_health > 0 else 0
        shield_bar = customtkinter.CTkFrame(shield_bar_bg, height=20, width=shield_bar_width, fg_color="#4B8BF5", corner_radius=5)
        shield_bar.place(relheight=1, relwidth=shield_bar_width/100)
        
        # Total health bar
        total_label = customtkinter.CTkLabel(
            health_frame, 
            text=f"Total HP: {hero_total_health}", 
            font=(self.font_family, self.small_font, "bold"),
            anchor="w"
        )
        total_label.pack(fill="x", pady=(15, 2))
        
        total_bar_bg = customtkinter.CTkFrame(health_frame, height=20, fg_color="#333333", corner_radius=5)
        total_bar_bg.pack(fill="x", pady=2)
        
        total_bar = customtkinter.CTkFrame(total_bar_bg, height=20, fg_color="#9370DB", corner_radius=5)
        total_bar.place(relheight=1, relwidth=1)
        
        abilities_row = customtkinter.CTkFrame(details_frame, corner_radius=15)
        abilities_row.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=0, columnspan=2)
        
        # Abilities section (placeholder - you would iterate through abilities here)
        abilities_title = customtkinter.CTkLabel(
            abilities_row, 
            text="Abilities", 
            font=(self.font_family, self.medium_font, "bold"),
            anchor="w"
        )
        abilities_title.pack(fill="x", pady=(10, 5), padx=20)
        
        # Add a scrollable frame for abilities
        abilities_scroll = customtkinter.CTkScrollableFrame(abilities_row, height=150)
        abilities_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # You would normally iterate through abilities here
        # Placeholder for demonstration
        if 'abilities' in hero_info and hero_info['abilities']:
            for ability in hero_info['abilities']:
                ability_frame = customtkinter.CTkFrame(abilities_scroll, fg_color="#2B2B2B", corner_radius=10)
                ability_frame.pack(fill="x", pady=5, padx=2)
                
                try:
                    # Try to load ability icon if available
                    response = requests.get(ability['icon'])
                    icon_img = Image.open(BytesIO(response.content))
                    icon_img = icon_img.resize((30, 30))
                    ability_icon = customtkinter.CTkImage(light_image=icon_img, dark_image=icon_img, size=(30, 30))
                    ability_icon_label = customtkinter.CTkLabel(ability_frame, text="", image=ability_icon)
                    ability_icon_label.pack(side="left", padx=10, pady=10)
                except:
                    # Use a placeholder if icon can't be loaded
                    placeholder = customtkinter.CTkFrame(ability_frame, width=30, height=30, fg_color="#555")
                    placeholder.pack(side="left", padx=10, pady=10)
                
                ability_info = customtkinter.CTkFrame(ability_frame, fg_color="transparent")
                ability_info.pack(side="left", fill="both", expand=True, padx=5, pady=10)
                
                ability_name = customtkinter.CTkLabel(
                    ability_info, 
                    text=ability['name'], 
                    font=(self.font_family, self.small_font, "bold"),
                    anchor="w"
                )
                ability_name.pack(fill="x")
                
                ability_desc = customtkinter.CTkLabel(
                    ability_info, 
                    text=ability['description'], 
                    font=(self.font_family, 10),
                    wraplength=200,
                    justify="left"
                )
                ability_desc.pack(fill="x", pady=(0, 3)) # Add padding to top and bottom (0 at top, 3 at bottom)
        
        # Bottom button frame
        button_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        close_button = customtkinter.CTkButton(
            button_frame, 
            text="Close", 
            command=self.destroy, 
            width=200, 
            height=40,
            font=(self.font_family, self.small_font, "bold"),
            corner_radius=10,
            hover_color="#1E5CBF"
        )
        close_button.pack(side="right")
        

if __name__ == '__main__':
    app = ShooterCounterApp()
    app.run()