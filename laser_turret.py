import pygame

from game.turret import Turret
from game.laser import Laser


class LaserTurret(Turret):
    
    def __init__(self, initial_position, build_cost, image_atlas, *groups):
        initial_radius = 128
        super().__init__(initial_position, build_cost, initial_radius, "laser_turret", *groups)
        self.image_atlas = image_atlas
        self.set_image_direct(self.image_atlas.subsurface((0, 128, 32, 32)))

        self.active_beam = None
        self.damage_per_tick = 5
        self.rotate_speed = 15.0

        self.beam_colour = pygame.Color("#FA3232AF")  # set default laser colour

    def update_shooting(self, time_delta, monsters, projectiles):
        # Check if we need to find a new target
        if self.current_target is None or self.current_target.should_die or self.target_distance > self.radius:
            # Kill the laser beam if we have one
            if self.active_beam is not None:
                self.active_beam.should_die = True
                self.active_beam = None
            # ------------------------------------------------------
            # Challenge 3 - Part B  (1 Line of code)
            # ----------------------
            # 
            # We need to get a new target for our laser beam turret
            # to make it fire.
            #
            # HINT
            #
            # - Try examining the missile_turret code file in
            #  the game subdirectory.
            # -------------------------------------------------------
            
            if self.current_target is not None:
                # found a target, so create a laser beam
                laser_pos = [self.position[0] + self.current_vector[0] * 16,
                             self.position[1] + self.current_vector[1] * 16]
                self.active_beam = Laser(laser_pos, self.current_vector, self.current_target,
                                         self.damage_per_tick, self.beam_colour)
                projectiles.append(self.active_beam)

        # if we have an active laser beam, update it's position.
        if self.active_beam is not None and self.current_target is not None:
            laser_start_pos = [self.position[0] + self.current_vector[0] * 16,
                               self.position[1] + self.current_vector[1] * 16]
            self.target_distance = self.calc_distance_to_target(self.current_target)
            results = self.calculate_aiming_vector(self.current_target, self.target_distance)
            self.target_vector = results[0]
            relative_angle_to_target = self.rotate_current_angle_to_target(time_delta)
            self.active_beam.set_beam_data(laser_start_pos, self.current_vector, self.beam_colour)
                
    # ----------------------------------------------
    # Challenge 3 - Part C
    # ----------------------
    #
    # Set the laser beam to different colours when
    # you level up.
    #
    # - Set it to a green colour for level 2.
    # - Set it to a blue colour for level 3
    # ----------------------------------------------
    def upgrade(self):
        self.level += 1
        self.radius += (12 * self.level)
        self.damage_per_tick += 3
        
        if self.level == 2:
            self.set_image_direct(self.image_atlas.subsurface((32, 128, 32, 32)))
            
        if self.level == 3:
            self.set_image_direct(self.image_atlas.subsurface((64, 128, 32, 32)))
