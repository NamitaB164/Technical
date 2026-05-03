class DataSanitizer:

    def fix_units(self, measurements):
        fixed = {}
        for key, value in measurements.items():
            if key == "Height":
                if value < 100:
                    value = value * 2.54  
            else:
                if value < 50:
                    value = value * 2.54
            fixed[key] = round(value, 1)
        return fixed

    def check_outliers(self, measurements):
        problems = []
        height = measurements.get("Height")
        waist = measurements.get("Waist")
        chest = measurements.get("Chest")

        if height and waist:
            if waist > height:
                problems.append("Waist is bigger than height")

        if height and chest:
            if chest < height * 0.30:
                problems.append("Chest smaller compared to the hight")

        return problems

    def estimate_missing(self, measurements):
        height = measurements.get("height")
        if not height:
            return measurements  
        ratios = {
            "Arm Length": 0.44,   
            "Leg Length": 0.47,   
            "Shoulder":   0.23,   
        }

        for part, ratio in ratios.items():
            if part not in measurements:
                estimated = round(height * ratio, 1)
                measurements[part] = estimated
                print(f"Estimated {part}: {estimated} cm")

        return measurements

    def process(self, measurements):
        print("Original:", measurements)

        measurements = self.fix_units(measurements)
        print("After unit fix:", measurements)

        
        problems = self.check_outliers(measurements)
        if problems:
            print("OUTLIERS FOUND:")
            for p in problems:
                print(" -", p)
        else:
            print("No outliers found")

    
        measurements = self.estimate_missing(measurements)
        print("Final:", measurements)

        return measurements


#input in inches
user_input = {
    "Height": 70,    
    "Chest": 38,     
    "Waist": 32,     
    "Hip": 40,       
}

sanitizer = DataSanitizer()
result = sanitizer.process(user_input)