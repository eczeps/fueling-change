
def car_emissions(miles_driven):
#returns number of kilograms emitted per year given monthy mileage
#assuming 404 grams emitted per mile on avg
	return ((404*miles_driven)/1000)*12


def plane_emissions(miles_flown):
#returns the number of kilograms emitted per year given yearly mileage
#assuming 53 pounds/mile on avg
	return miles_flown*53*0.45359237


def meat_emissions(lamb=0, beef=0, cheese=0, pork=0, turkey=0, chicken=0):
	#each meat is multiplied by its emissions and how many grams are in each serving
	#returns number of kilograms emitted per year given weekly servings
	return ((39.2*lamb*100 + 27*beef*85 + 13.5*cheese*43 + 12.1*pork*85 + 10.9*turkey*85 + 6.9*chicken*85)/1000)*52


def washer_emissions(hours_used):
#returns number of kilograms emitted per year given weekly hours used
#assumes one hour per load of laundry
	return ((255*hours_used)/1000*0.78)*52


def dryer_emissions(hours_used):
#returns number of kilograms emitted
#assumes one hour per load, and that the dryer is used for every load of washing
	return ((2790*hours_used)/1000*0.78)*52