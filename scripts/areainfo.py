from ev import Script, search_script

class AreaInfo(Script):
    def at_script_creation(self):
        self.key = "area_info"
	self.desc = "Manages data on 'area' type room groupings"
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

    def get_region(self):
        region_id = self.db.region_id
        if region_id:
            # Sanity check the region_id first
            if region_id[0] != '#' or not region_id[1:].isdigit():
                region_id = None
        if region_id:
            return(search_script(region_id)[0])
        else:
            return(None)
