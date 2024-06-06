class InsectDTO:
    def __init__(self, insect_id, lat_name, ru_name, img, squad_id, squad_name, family_id, family_name, description, category_and_status, distribution, area, habitat, limiting_factors, count, security_notes):
        self.insect_id = insect_id
        self.lat_name = lat_name
        self.ru_name = ru_name
        self.img = img
        self.squad_id = squad_id
        self.squad_name = squad_name
        self.family_id = family_id
        self.family_name = family_name
        self.description = description
        self.category_and_status = category_and_status
        self.distribution = distribution
        self.area = area
        self.habitat = habitat
        self.limiting_factors = limiting_factors
        self.count = count
        self.security_notes = security_notes

    def __str__(self):
        return f"Insect {self.lat_name} (ID: {self.insect_id}) - {self.family_name} ({self.squad_name})"

