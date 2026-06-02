from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from random import randint, choice

Window.clearcolor = (0.1, 0.4, 0.1, 1) # Ghaas

class CarGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_name = "Sahil bhai" # <-- Yaha apna naam
        self.start_game()

    def start_game(self):
        self.canvas.clear()
        for child in self.children[:]:
            self.remove_widget(child)

        self.score = 0
        self.base_speed = 5
        self.speed = self.base_speed
        self.game_over_flag = False
        self.road_x = Window.width * 0.15
        self.road_width = Window.width * 0.7
        self.trucks = []
        self.road_lines = []

        # Sadak + Lines
        with self.canvas:
            Color(0.15, 0.15, 0.15, 1)
            Rectangle(pos=(self.road_x, 0), size=(self.road_width, Window.height))

            Color(1, 1, 1, 1)
            for i in range(15):
                y = i * 60
                line = Rectangle(pos=(Window.width/2 - 5, y), size=(10, 30))
                self.road_lines.append(line)

        self.draw_trees()

        # Teri Car - Colorful
        with self.canvas:
            Color(1, 0.1, 0.1, 1) # Laal body
            self.player = Rectangle(pos=(Window.width/2 - 30, 60), size=(60, 100))
            Color(0.2, 0.6, 1, 1) # Neeli windshield
            self.windshield = Rectangle(pos=(Window.width/2 - 25, 125), size=(50, 25))
            Color(1, 1, 0, 1) # Peeli headlights
            self.headlight1 = Rectangle(pos=(Window.width/2 - 28, 155), size=(12, 8))
            self.headlight2 = Rectangle(pos=(Window.width/2 + 16, 155), size=(12, 8))
            Color(0, 0, 0, 1) # Kaale wheels
            self.w1 = Rectangle(pos=(Window.width/2 - 35, 70), size=(12, 20))
            self.w2 = Rectangle(pos=(Window.width/2 + 23, 70), size=(12, 20))
            self.w3 = Rectangle(pos=(Window.width/2 - 35, 130), size=(12, 20))
            self.w4 = Rectangle(pos=(Window.width/2 + 23, 130), size=(12, 20))

        # Naam + Score + Speed
        self.name_label = Label(text=f'Player: {self.player_name}', pos=(20, Window.height-60), size=(200, 50), font_size=20, color=(1,1,1,1))
        self.score_label = Label(text='Score: 0', pos=(Window.width-180, Window.height-60), size=(160, 25), font_size=20, color=(1,1,1,1))
        self.speed_label = Label(text='Speed: 5.0', pos=(Window.width-180, Window.height-85), size=(160, 25), font_size=18, color=(1,1,0,1))
        self.add_widget(self.name_label)
        self.add_widget(self.score_label)
        self.add_widget(self.speed_label)

        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_truck)
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_truck, 1.1)

    def draw_trees(self):
        with self.canvas:
            for i in range(8):
                Color(0.4, 0.2, 0, 1)
                x = randint(20, int(self.road_x - 50))
                y = i * 100 + randint(-20, 20)
                Rectangle(pos=(x+15, y), size=(15, 50))
                Color(0, 0.6, 0, 1)
                Ellipse(pos=(x, y+40), size=(45, 45))

                Color(0.4, 0.2, 0, 1)
                x = randint(int(self.road_x + self.road_width + 20), int(Window.width - 60))
                y = i * 100 + 50
                Rectangle(pos=(x+15, y), size=(15, 50))
                Color(0, 0.6, 0, 1)
                Ellipse(pos=(x, y+40), size=(45, 45))

    def on_touch_move(self, touch):
        if self.game_over_flag: return
        new_x = touch.x - 30
        if new_x < self.road_x + 5: new_x = self.road_x + 5
        if new_x > self.road_x + self.road_width - 65: new_x = self.road_x + self.road_width - 65

        self.player.pos = (new_x, self.player.pos[1])
        self.update_car_parts()

    def update_car_parts(self):
        x, y = self.player.pos
        self.windshield.pos = (x+5, y+65)
        self.headlight1.pos = (x+2, y+95)
        self.headlight2.pos = (x+46, y+95)
        self.w1.pos = (x-5, y+10)
        self.w2.pos = (x+53, y+10)
        self.w3.pos = (x-5, y+70)
        self.w4.pos = (x+53, y+70)

    def spawn_truck(self, dt):
        if self.game_over_flag: return
        with self.canvas:
            # ENEMY TRUCKS AB COLORFUL 🔥 WHITE NAHI
            truck_colors = [
                (1, 0.8, 0, 1), # Peela
                (0, 0.5, 1, 1), # Neela
                (1, 0.4, 0, 1), # Narangi
                (0.8, 0, 0.8, 1), # Baingani
                (0, 0.8, 0.8, 1), # Cyan
                (0.6, 0.6, 0.6, 1) # Grey
            ]
            Color(choice(truck_colors))
            truck_x = randint(int(self.road_x + 10), int(self.road_x + self.road_width - 80))
            truck = Rectangle(pos=(truck_x, Window.height), size=(70, 110))
            self.trucks.append(truck)

    def update(self, dt):
        if self.game_over_flag: return

        self.score += 1
        # SPEED KA FORMULA: Jitna score utni speed, lekin limit me
        self.speed = self.base_speed + (self.score / 400) # Har 400 score = +1 speed
        if self.speed > 40: self.speed = 50 # Max speed 50, warna impossible ho jayega

        self.score_label.text = f'Score: {self.score}'
        self.speed_label.text = f'Speed: {self.speed:.1f}'

        # Road lines
        for line in self.road_lines:
            line.pos = (line.pos[0], line.pos[1] - self.speed)
            if line.pos[1] < -30:
                line.pos = (line.pos[0], Window.height)

        # Trucks move
        for truck in self.trucks[:]:
            truck.pos = (truck.pos[0], truck.pos[1] - self.speed)
            if self.collision(self.player, truck):
                self.game_over()
            if truck.pos[1] < -120:
                self.trucks.remove(truck)

    def collision(self, r1, r2):
        return (r1.pos[0] < r2.pos[0] + r2.size[0] and
                r1.pos[0] + r1.size[0] > r2.pos[0] and
                r1.pos[1] < r2.pos[1] + r2.size[1] and
                r1.pos[1] + r1.size[1] > r2.pos[1])

    def game_over(self):
        self.game_over_flag = True
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_truck)

        over_label = Label(text=f'GAME OVER\nScore: {self.score}\nTop Speed: {self.speed:.1f}',
                          halign='center', pos=(0, Window.height/2-70),
                          size=(Window.width, 180), font_size=40, color=(1,0,0,1))
        self.add_widget(over_label)

        restart_btn = Button(text='RESTART', pos=(Window.width/2-100, Window.height/2-180),
                           size=(200,70), font_size=28, background_color=(0,1,0,1))
        restart_btn.bind(on_press=lambda x: self.start_game())
        self.add_widget(restart_btn)

class MyApp(App):
    def build(self):
        return CarGame()

MyApp().run()
