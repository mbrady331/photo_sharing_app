from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import FileShare
import cv2
import time
import webbrowser


Builder.load_file('frontend.kv')

class CameraScreen(Screen):
    def start(self):
        """Starts camera and changes Button Text"""
        #change opacity for Camera widget when start method is called
        self.ids.camera.opacity = 1
        #Set play attribute of Camera widget to true when start function is called
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"
        #Bring image back to Image widget
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops camera and changes Button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        #remove image from camera widget
        self.ids.camera.texture = None

    def capture(self):
        """Creates a file name with the current time and captures and saves
        a photo image under that filename"""
        current_time = time.strftime('%Y%m%d-%H%M%S')
        #add self. to filepath so this can be access by other methods in the ImageScreen class
        self.filepath = f"files/{current_time}.png"
        #Create png file from last frame in Image widget when capture method is run(when capture button is pressed)
        self.ids.camera.export_to_png(self.filepath)
        #Navigate to ImageScreen
        self.manager.current = "image_screen"
        #Setting Image widget of current screen(ImageScreen) to captured image
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):

    link_text = "Create a Link First!"

    def create_link(self):
        """Accesses the photo filepath, uploads it to the web,
         and inserts the link in the Label widget"""
        #Access filepath created from capture method
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        #create FileShare object and assign the filepath parameter as file_path and upload it
        #to the web using the api key parameter of FileShare class
        filesharer = FileShare(filepath = file_path)
        #extract url using share method
        #add self. to url so it can be access by other methods in the ImageScreen class
        self.url = filesharer.share()
        #set text of Label widget to url
        self.ids.link.text = self.url

    def copy_link(self):
        """Copy url to clipboard"""
        #try/except to make sure a link was created by the Create Shareable link button being pressed.
        try:
            Clipboard.copy(self.url)
        #if no url, change Label widget text
        except:
            #since link_text is a variable of the class, need to use self. to access it
            self.ids.link.text = self.link_text

    def open_link(self):
        """Open url link in a browser when Open Link button is pressed"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_text

#create subclass of Screenmanager from kivy
#Creating a copy of ScreenManager class that allows us to add other methods to it
class RootWidget(ScreenManager):
    pass


#create subclass of App from kivy
class MainApp(App):

    def build(self): #overwriting build method that kivy already contains
        return RootWidget()

MainApp().run()