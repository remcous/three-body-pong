class Scene_base():
    def __init__(self):
        self.next = self
        
    def Process_input(self, events, pressed_keys):
        print("uh-oh, you didn't implement this in the child class")
        
    def Update(self):
        print("uh-oh, you didn't implement this in the child class")
        
    def Render(self, screen):
        print("uh-oh, you didn't implement this in the child class")
        
    def Switch_to_scene(self, next_scene):
        self.next = next_scene
        
    def Terminate(self):
        self.Switch_to_scene(None)