def inPlanet(planet_center, position):
    rectangle = [(planet_center[0]-32, planet_center[1]-32), (planet_center[0]+32, planet_center[1]+32)]
    if(rectangle[0][0] <= position[0] <= rectangle[1][0]):
        if(rectangle[0][1] <= position[1] <= rectangle[1][1]):
            return True
    return False