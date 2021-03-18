import json, os, psutil, random
from datetime import datetime

class App(object):
    def __init__ (self):
        self.PROCESS_LIST = [
            'wallpaper32.exe',
            'wallpaper64.exe'
        ]
        self.time = datetime.now()
        self.process_list = self.create_process_list()
        self.wallpaper_directory = self.process_list[0].cwd()
        self.config = self.load_config()
        self.steam_workshop_dir = self.get_workshop_dir()
        self.users_wallpapers = self.get_list_of_wallpapers()
        

    def get_process(self, process_name):
        for process in psutil.process_iter(attrs=["pid", "name"]):
            if process.info['name'] == process_name:
                return process

    def create_process_list(self):
        processes = []
        for process_name in self.PROCESS_LIST:
            process = self.get_process(process_name)
            if not process == None:
                processes.append(process)
        return processes
    
    def get_workshop_dir(self):
        return '/'.join(self.config[list(self.config.keys())[2]]['general']['wallpaperconfig']['selectedwallpapers'][list(self.config[list(self.config.keys())[2]]['general']['wallpaperconfig']['selectedwallpapers'].keys())[0]]['file'].split('/')[:-2])

    def kill_process(self, process):
        if process.is_running:
            process.kill()

    def load_config(self):
        with open(self.wallpaper_directory + '\\config.json', 'r') as f:
            return json.load(f)

    def get_list_of_wallpapers(self):
        # wallpaperconfigrecent = self.config[list(self.config.keys())[2]]['general']['wallpaperconfigrecent']
        wallpapers = []
        # for wallpaper in wallpaperconfigrecent:
        #     files.append(wallpaper['config']['selectedwallpapers'][list(wallpaper['config']['selectedwallpapers'].keys())[0]])
        
        
        for root, dirs, files in os.walk(self.steam_workshop_dir):
            for file in files:
                if file.endswith(".mp4") or file.endswith(".pkg"):
                    wallpapers.append(os.path.join(root, file))
                   
        return wallpapers

    def change_wallpaper(self):
   
        [self.kill_process(process) for process in self.process_list]
        
        self.config[list(self.config.keys())[2]]['general']['wallpaperconfig']['selectedwallpapers'][list(self.config[list(self.config.keys())[2]]['general']['wallpaperconfig']['selectedwallpapers'].keys())[0]]['file'] = random.choice(self.users_wallpapers)
        with open(self.wallpaper_directory + '\\config.json', 'w+') as f:
            f.write(json.dumps(self.config, indent=4, sort_keys=True))

        os.startfile(f"{self.wallpaper_directory}/wallpaper32.exe")
        
        

app = App()
app.change_wallpaper()

# print(app.get_list_of_wallpapers())
