#----------------------------------------------------- 
# timerCallback.py
#
# Created by:   Michael Kuczynski
# Created on:   03-02-2020
#
# Description: Custom VTK timer callback for DYNACT Viewer.
#----------------------------------------------------- 

import glob

class MyTimerCallback():
    def __init__(self):
        self.timer_count = 0
        self.currentVolume = 0
        self.forward = True
        self.reverse = False

    def execute(self, obj, event):
        # iren = obj

        if self.currentVolume <= 0 :
            self.forward = True
            self.reverse = False
        elif self.currentVolume >= 18 :
            self.forward = False
            self.reverse = True

        if self.forward :
            # print('Forward')
            # print('current volume = ' + str(self.currentVolume))
            # print('length of volumes = ' + str(len(volumes)))
            # print()

            # Remove current actor
            # actorCollection = self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors()
            glob.renWindow.GetRenderers().GetFirstRenderer().RemoveActor( glob.volumes[self.currentVolume] )
            
            # Increment the current volume
            self.currentVolume = self.currentVolume + 1

            # Add next actor
            glob.renWindow.GetRenderers().GetFirstRenderer().AddActor( glob.volumes[self.currentVolume] )

            # Render
            # self.vtkWidget.Render()
            glob.renWindow.Render()
        elif self.reverse :
            # print('Backward')
            # print('current volume = ' + str(self.currentVolume))
            # print('length of volumes = ' + str(len(volumes)))
            # print()

            # Remove current actor
            glob.renWindow.GetRenderers().GetFirstRenderer().RemoveActor( glob.volumes[self.currentVolume] )

            # Decrement the current volume
            self.currentVolume = self.currentVolume - 1

            # Add next actor
            glob.renWindow.GetRenderers().GetFirstRenderer().AddActor( glob.volumes[self.currentVolume] )

            # Render
            # self.vtkWidget.Render()
            glob.renWindow.Render()