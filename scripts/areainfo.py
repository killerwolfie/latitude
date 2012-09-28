from ev import Script

class AreaInfo(Script):
    def at_script_creation(self):
        self.key = "area_info"
	self.desc = "Manages data on 'area' type room groupings"
	self.interval = 0
	self.persistent = True
