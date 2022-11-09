#----------------------------------------------------- 
# volumeQTimerCallback.py
#
# Created by:   Michael Kuczynski
# Created on:   03-02-2020
#
# Description: Custom QT timer callback for rendering.
#----------------------------------------------------- 

class VolumeQTimerCallback:
    #------------------------------------------#
    # Class constructor
    #------------------------------------------#
    def __init__(self):
        self.iren = None
        self.volumes = []
        self.currentVolume = 0
        self.volTimer = None
        self.timerSpeed = 200
        self.forward = True
        self.reverse = False

    #------------------------------------------#
    # Class set functions
    #------------------------------------------#
    def setParameters(self, _iren, _volumes, _currentVolume):
        self.iren = _iren
        self.volumes = _volumes
        self.currentVolume = _currentVolume

    #------------------------------------------#
    # Start/pause animation
    #------------------------------------------#
    def startStop(self):
        if ( self.volTimer.isActive() ):
            self.volTimer.stop()
        else:
            self.volTimer.start(self.timerSpeed)

    #------------------------------------------#
    # Start the animation
    #------------------------------------------#
    def execute(self):
        if self.currentVolume == 0 :
            self.forward = True
            self.reverse = False
        elif self.currentVolume == 19 :
            self.forward = False
            self.reverse = True

        if self.forward :
            # Remove current actor
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( self.volumes[self.currentVolume].volActor )
            
            # Increment the current volume
            self.currentVolume = self.currentVolume + 1

            # Add next actor
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( self.volumes[self.currentVolume].volActor )

            # Render
            self.iren.GetRenderWindow().Render()

        elif self.reverse :
            # Remove current actor
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor( self.volumes[self.currentVolume].volActor )

            # Decrement the current volume
            self.currentVolume = self.currentVolume - 1

            # Add next actor
            self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor( self.volumes[self.currentVolume].volActor )

            # Render
            self.iren.GetRenderWindow().Render()