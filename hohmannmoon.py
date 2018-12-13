GlowScript 2.7 VPython

# Hohmann Moon Transfer Orbit
# David Kirschman
# 2018-12-12
# Transfer orbit from earth to moon

#Set Scene
scene.background = color.white
scene.userspin = False
scene.fov = 0.01
scene.width = 600
scene.height = 600

# Setup variables for the system
t = 0
xInit = x
initRate = 2000

# Moon variables
thetaMoon = 317
thetaRad = (thetaMoon * pi)/180
mMoon = 0.0123
rMoon = 60.3359
xMoon = cos(thetaRad) * rMoon
yMoon = sin(thetaRad) * rMoon
vxMoon = -(sqrt(4*pi*pi/rMoon)*yMoon)/rMoon
vyMoon = (sqrt(4*pi*pi/rMoon)*xMoon)/rMoon

# Rocket variables
mRocket = 4.9665e-19
rRocket = 1.0261 # ~118 km above Earth's surface
xRocket = -rRocket
yRocket = 0
thetaRocket = atan2(yRocket, xRocket)
# Used to make adjusting V easier
vxRocket = 0
vyRocket = -sqrt(4*pi*pi/rRocket) * 1.401049

# Get the initial DeltaV (going from circular LOE to Hohmann Transfer)
totalDeltaV = deltaV(vyRocket, -sqrt(4*pi*pi/rRocket))

# Make the simulation objects
moon = sphere(color = color.black, pos = vec(xMoon,yMoon,0), radius = .2726, make_trail = True, trail_type = "points", trail_radius = .1, interval = 1000)
Earth = sphere(color = color.blue, pos =vec(0,0,0), radius = 1)
rocket = sphere(color = color.red, pos = vec(xRocket,yRocket,0), radius = .2, make_trail = True, trail_type = "points", trail_radius = .1, interval = 1000)

# Initial accelerations of objects
axMoon = acceleration(rMoon, mRocket, xMoon, xRocket)
ayMoon = acceleration(rMoon, mRocket, yMoon, yRocket)
axRocket = acceleration(rRocket, mMoon, xRocket, xMoon)
ayRocket = acceleration(rRocket, mMoon, yRocket, yMoon)
accelerationXRocket = acceleration(rRocket, mMoon, xRocket, xMoon)
accelerationYRocket = acceleration(rRocket, mMoon, yRocket, yMoon)

running = False
hohmannComplete = False
i = 0

scene.append_to_caption("Current Velocity: ")
velocityReadout=wtext(text=sqrt(vxRocket**2 + vyRocket**2))
scene.append_to_caption("<br>")

scene.append_to_caption("Total Delta V: ")
deltaVReadout=wtext(text=totalDeltaV)
scene.append_to_caption("<br>")

# Create play/pause button
btnPlayPause = button(text="Play", bind=pausePlay)

# Create reset button
btnReset = button(text="Reset", bind=reset)

# Create reset button
btnDecreaseV = button(text="Decrease", bind=decreaseVelocity)

# Create reset button
btnIncreaseV = button(text="Increase", bind=increaseVelocity)

scene.append_to_caption("\n\n")
rateSlider = slider(left=2, min=0, max=2, step=0.1, value=1, bind=adjustRate)
scene.append_to_caption("    Rate: ")
rateSliderReadout=wtext(text="1")

scene.append_to_caption("\n\n")
velocitySlider = slider(left=.5, min=0, max=.5, step=0.01, value=0, bind=showVelocity)
scene.append_to_caption("    Adjust Velocity By: ")
velocitySliderReadout=wtext(text="0%")

# Reset simulation to initial state
def reset():
    global xMoon, yMoon, vxMoon, vyMoon, axMoon, ayMoon, xRocket, yRocket, rRocket, vxRocket, vyRocket, axRocket, ayRocket, hohmannComplete, accelerationXRocket, accelerationYRocket
    # Moon variables
    xMoon = cos(thetaRad) * rMoon
    yMoon = sin(thetaRad) * rMoon
    vxMoon = -(sqrt(4*pi*pi/rMoon)*yMoon)/rMoon
    vyMoon = (sqrt(4*pi*pi/rMoon)*xMoon)/rMoon
    axMoon = acceleration(rMoon, mRocket, xMoon, xRocket)
    ayMoon = acceleration(rMoon, mRocket, yMoon, yRocket)
    moon.pos = vec(xMoon,yMoon,0)
    moon.clear_trail()
    
    # Rocket variables
    rRocket = 1.0261 # ~118 km above Earth's surface
    xRocket = -rRocket
    yRocket = 0
    vxRocket = 0
    vyRocket = -sqrt(4*pi*pi/rRocket) * 1.401049
    axRocket = acceleration(rRocket, mMoon, xRocket, xMoon)
    ayRocket = acceleration(rRocket, mMoon, yRocket, yMoon)
    rocket.pos = vec(xRocket,yRocket,0)
    rocket.clear_trail()
    hohmannComplete = False
    
    scene.camera.follow(Earth)
    scene.range = 50

# Display the amount to adjust the velocity by
def showVelocity():
    velocitySliderReadout.text = (velocitySlider.value * 100) + "%"

# Increase the velocity
def increaseVelocity():
    increaseBy = velocitySlider.value
    adjustVelocity(increaseBy, "increase")

# Decrease the velocity
def decreaseVelocity():
    decreaseBy = velocitySlider.value
    adjustVelocity(decreaseBy, "decrease")
    
# Adjust the velocity based on Increase/DecreaseVelocity functions
def adjustVelocity(adjustBy, direction):
    global vxRocket, vyRocket
    
    totalVelocity = sqrt(vxRocket**2 + vyRocket**2)
    
    if (direction == "increase" and totalVelocity < 0) or (direction == "decrease" and totalVelocity > 0):
        adjustBy = -adjustBy
        
    adjustedVelocity = totalVelocity + (totalVelocity * adjustBy)
    vxRocket = adjustedVelocity*(vxRocket/totalVelocity)
    vyRocket = adjustedVelocity*(vyRocket/totalVelocity)
    
    totalDeltaV += deltaV(adjustedVelocity, totalVelocity)
    deltaVReadout.text = totalDeltaV
    
# Adjust the simulation speed
def adjustRate():
    rateSliderReadout.text = rateSlider.value

# Simulate the burn to circularize the orbit to complete the Hohmann transfer
def finalBurn():
    global vxRocket, vyRocket, totalDeltaV
    theta = atan2(vyRocket, vxRocket)
    v = sqrt(vxRocket**2 + vyRocket**2)
    vxRocket = -(sqrt(4*pi*pi/rMoon)*yMoon)/rMoon * cos(theta)
    vyRocket = (sqrt(4*pi*pi/rMoon)*xMoon)/rMoon * sin(theta)
    vFinal = sqrt(vxRocket**2 + vyRocket**2)
    totalDeltaV += deltaV(vFinal, v)
    deltaVReadout.text = totalDeltaV
 
# Return the difference in velocities to determine the overall efficiency of the maneuver
def deltaV(v0, v1):
    # Need to account for signs...
    return abs(v1 - v0)
    
# Define the acceleration calculation
def acceleration(r, otherMass, position, otherPosition):
    d = (moon.pos - rocket.pos).mag
    return -((4 * pi**2 * position) / r**3) - ((4 * pi**2 * (position - otherPosition) * otherMass) / d**3)
    
# Function to play and pause the simulation
def pausePlay():
    global running
    running = not running
    btnPlayPause.text = "pause" if play else "play"

# Begin the simulation
while True:
    rate(10000 * rateSlider.value)
    
    if running:
        dt = 0.001
        # Verlet for moon
        # Probably should fix this so both moon and rocket are bing calculated as one verlet to (slightly) increase accuracy.
        xMoon += (vxMoon * dt) + (axMoon * dt**2 *.5)
        yMoon += (vyMoon * dt) + (ayMoon * dt**2 *.5)
        rMoon = sqrt(xMoon**2 + yMoon**2)
        vxMoon += .5 * axMoon * dt
        vyMoon += .5 * ayMoon * dt
        axMoon = acceleration(rMoon, mRocket, xMoon, xRocket)
        ayMoon = acceleration(rMoon, mRocket, yMoon, yRocket)
        vxMoon += .5 * axMoon * dt
        vyMoon += .5 * ayMoon * dt
        
        # Verlet for rocket
        xRocket += (vxRocket * dt) + (axRocket * dt**2 *.5)
        yRocket += (vyRocket * dt) + (ayRocket * dt**2 *.5)
        rRocket = sqrt(xRocket**2 + yRocket**2)
        
        if sqrt(xRocket**2 + yRocket**2) >= rMoon and !hohmannComplete:
            # Perform the calculated burn to curcularize the orbit at the end of the Hohmann transfer
            finalBurn()
            hohmannComplete = True
            scene.camera.follow(moon)
            scene.range = sqrt((xMoon - xRocket)**2 + (yMoon - yRocket)**2)
        else:
            vxRocket += .5 * axRocket * dt
            vyRocket += .5 * ayRocket * dt
            
        axRocket = acceleration(rRocket, mMoon, xRocket, xMoon)
        ayRocket = acceleration(rRocket, mMoon, yRocket, yMoon)
        vxRocket += .5 * axRocket * dt
        vyRocket += .5 * ayRocket * dt
        
        t += dt
        
        # Plot the positions
        moon.pos.x = xMoon
        moon.pos.y = yMoon
        rocket.pos.x = xRocket
        rocket.pos.y = yRocket
        
        i += 1
        if i == 1000:
            # Update current velocity readout
            velocityReadout.text = sqrt(vxRocket**2 + vyRocket**2)
            i = 0
