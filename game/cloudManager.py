# -*- coding: utf-8 -*-

class CloudManager:
    def __init__(self):
        self.clouds = None
        self.stars = None
        self.spawn_timer = None
        self.scroll_speed = 120.0
        self.spawn_interval = 1.2
        self.danger_ratio = 0.15

    def spawn(self, ):
        pass

    def update(self, dt):
        pass

    def cull_offscreen(self, ):
        pass

    def draw(self, win):
        pass

    def apply_difficulty(self, speed, danger_ratio, spawn_interval):
        pass
