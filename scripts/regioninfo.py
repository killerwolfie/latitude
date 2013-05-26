from ev import Script

class RegionInfo(Script):
    def at_script_creation(self):
        self.key = "region_info"
	self.desc = "Manages data on the 'regions' of the world"
	self.interval = 0
	self.persistent = True

    def get_name(self):
        if self.db.name:
            return self.db.name
        return self.key

    def get_name_within(self):
        if self.db.name_within:
            return self.db.name_within
        return 'in ' + self.get_name()
