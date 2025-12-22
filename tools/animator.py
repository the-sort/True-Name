"""
Module for animation handling
"""
import os
import pygame

class CAnimations:
    """
    Class for loading sprites into 
    animation and playing it
    """

    def __init__(self, path, fps = 30):
        directory     = os.listdir(path)
        self.__am_frames     = len(directory)

        self.__frames = [pygame.image.load(path + "/" + frame) for frame in directory]

        self.__frame_index = 0
        self.__timer       = 0
        self.__frame_time  = fps / self.__am_frames

    def rescale(self, transform):
        """
        Rescales all frames of animation
        """
        self.__frames = [pygame.transform.scale(frame, transform) for frame in self.__frames]

    def play(self, screen : pygame.Surface, delta_time, cordinates : tuple):
        """
        Plays animation in scene
        """
        self.__timer += delta_time

        if self.__timer >= self.__frame_time:
            self.__timer -= self.__frame_time
            self.__frame_index = (self.__frame_index + 1) % self.__am_frames

        screen.blit(self.__frames[self.__frame_index], cordinates)

    def get_rect(self, top_left = 0):
        """
        Return rect of first frame 
        in animation
        """
        return self.__frames[0].get_rect(top_left)

    def get_keyframe(self):
        """
        Returns first frame of animation
        """
        return self.__frames[0]



if __name__ == "__main__":
    animator = CAnimations("assets/dripping")
