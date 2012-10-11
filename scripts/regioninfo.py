from ev import Script

class RegionInfo(Script):
    def at_script_creation(self):
        self.key = "region_info"
	self.desc = "Manages data on the 'regions' of the world"
	self.interval = 0
	self.persistent = True
