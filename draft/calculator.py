
def car_emissions(miles_driven):
#returns number of kilograms emitted 
#assuming 404 grams emitted per mile on avg
	return (404*miles_driven)/1000


def plane_emissions(miles_flown):
#returns the number of kilograms emitted
#assuming 53 pounds/mile on avg
	return miles_flown*53*0.45359237


def meat_emissions(lamb=0, beef=0, cheese=0, pork=0, turkey=0, chicken=0):
	#each meat is multiplied by its emissions and how many grams are in each serving
	#returns number of kilograms emitted
	return (39.2*lamb*100 + 27*beef*85 + 13.5*cheese*43 + 12.1*pork*85 + 10.9*turkey*85 + 6.9*chicken*85)/1000


def washer_emissions(hours_used):
#returns number of kilograms emitted
	return (255*hours_used)/1000*0.78


def dryer_emissions(hours_used):
#returns number of kilograms emitted
	return (2790*hours_used)/1000*0.78