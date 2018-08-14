from pyprocessing import *
import random


class Agent:
    def __init__(self, group, emotion, entity=None, relevance=None):
        self.location = PVector(random.randint(0, width), random.randint(0, height))
        self.acceleration = PVector(0, 0)
        self.velocity = PVector(0, -2)
        if emotion == 0:                    # Sadness: slower
            self.max_speed = 1
            self.max_force = 0.008
        elif emotion == 1 or emotion == 4:  # Joy or anger: faster
            self.max_speed = 3
            self.max_force = 0.04
        else:                               # Fear or disgust: normal
            self.max_speed = 1.7
            self.max_force = 0.012
        self.radius = 8.0
        self.group = group
        self.emotion = emotion
        self.text = entity
        self.relevance = map(relevance, 0, 1, 0, 255)
        # Choose color
        col_blue = (120, 225, 255)  # sadness
        col_orange = (255, 167, 0)  # joy
        col_black = (0, 0, 0)       # fear
        col_brown = (141, 85, 36)   # disgust
        col_red = (214, 45, 32)     # anger
        palette = [col_blue, col_orange, col_black, col_brown, col_red]
        self.r = palette[self.emotion][0]
        self.g = palette[self.emotion][1]
        self.b = palette[self.emotion][2]
        self.color = color(self.r, self.g, self.b, self.relevance)
        self.groupCenter = self.location

    def update(self):
        self.location.add(self.velocity)
        self.velocity.add(self.acceleration)
        self.velocity.normalize()
        self.velocity.mult(self.max_speed)
        self.acceleration.mult(0)

    def seek(self, target):
        desired = PVector.sub(target, self.location)
        # d = desired.mag()
        desired.normalize()
        desired.mult(self.max_speed)
        # The closer to the target, the lower the speed
        # When the distance lower than 100, slow down
        # if d < 100:
        #     m = map(d, 0, 100, 0, self.max_speed)
        #     # print("m:", m)
        #     desired.mult(m)
        #     # print("desired:", desired)
        # else:
        #     desired.mult(self.max_speed)

        steer = PVector.sub(desired, self.velocity)
        if steer.mag() > self.max_force:
            steer.normalize()
            steer.mult(self.max_force)
        return steer

    def display(self):
        # print("velocity:", self.velocity)
        theta = self.velocity.heading()
        # print(theta)
        # print("theta:", theta)
        fill(self.color)
        strokeWeight(0.5)
        pushMatrix()
        translate(self.location.x, self.location.y)
        rotate(theta)
        beginShape(TRIANGLES)
        vertex(2 * self.radius, 0)
        vertex(-2 * self.radius, -self.radius)
        vertex(-2 * self.radius, self.radius)
        endShape(CLOSE)
        popMatrix()

    def applyForce(self, force):
        self.acceleration.add(force)

    def applyBehaviour(self, agents, myMouse):
        [alignForce, separateForce, cohesionForce, fleeForce] = self.flock(agents)
        seekForce = self.seek(myMouse)
        borderForce = self.awayBorders()

        # Weight different forces

        alignForce.mult(2)
        separateForce.mult(6)
        seekForce.mult(0)
        cohesionForce.mult(3)
        fleeForce.mult(2)
        # borderForce.mult(2)

        self.applyForce(alignForce)
        self.applyForce(separateForce)
        self.applyForce(seekForce)
        self.applyForce(cohesionForce)
        self.applyForce(fleeForce)
        self.applyForce(borderForce)

    def flock(self, agents):
        # The radius of being neighbours and requiring separation
        visionDist = 150
        # neighbourDist = 50
        separationDist = 20
        # The sum velocity of neighbours and separation
        sepVel = PVector(0, 0)
        fleVel = PVector(0, 0)
        sumVel = PVector(0, 0)
        sumLoc = PVector(0, 0)
        steerAlign = PVector(0, 0)
        steerSep = PVector(0, 0)
        steerCoh = PVector(0, 0)
        steerFle = PVector(0, 0)
        # neighbourNum = 0
        separateNum = 0
        fleeNum = 0
        friendNum = 0
        for other in agents:
            d = dist(self.location.x, self.location.y, other.location.x, other.location.y)
            # Viewable range
            if 0 < d < visionDist:
                # First check if they are in the same group
                if self.group != other.group:
                    flee = PVector.sub(self.location, other.location)
                    flee.normalize()
                    flee.x /= d
                    flee.y /= d
                    fleVel.add(flee)
                    fleeNum += 1
                else:
                    # If they are in the same group, calculate the center and average velocity of neighbours
                    sumLoc.add(other.location)
                    sumVel.add(other.velocity)
                    friendNum += 1
                    # Display the connected line
                    # stroke(100, 30)
                    # line(self.location.x, self.location.y, other.location.x, other.location.y)
                    noStroke()
                # if 0 < d < neighbourDist:
                    # If they are neighbours, calculate the center and average velocity of neighbours
                    # sumVel.add(other.velocity)
                    # sumLoc.add(other.location)
                    # neighbourNum += 1
                    # stroke(100, 50)
                    # line(self.location.x, self.location.y, other.location.x, other.location.y)
                    # Then check if they are enemies

                    # self.color = self.colorMerge(other.color)
                    # Then check if it is too close
                    if 0 < d < separationDist:
                        diff = PVector.sub(self.location, other.location)
                        diff.normalize()
                        diff.x /= d
                        diff.y /= d
                        sepVel.add(diff)
                        separateNum += 1

        if friendNum > 0:
            # sumVel.div(neighbourNum)
            # The two lines below mean use the direction of neighbours with max speed.
            # Or to try the original sum of velocity
            sumVel.normalize()
            sumVel.mult(self.max_speed)
            steerAlign = PVector.sub(sumVel, self.velocity)
            if steerAlign.mag() != 0:
                steerAlign.normalize()
                steerAlign.mult(self.max_force)
            # sumLoc.x /= neighbourNum
            # sumLoc.y /= neighbourNum
            # steerCoh = self.seek(sumLoc)

        if friendNum > 0:
            sumLoc.x /= friendNum
            sumLoc.y /= friendNum
            self.groupCenter = sumLoc
            steerCoh = self.seek(self.groupCenter)

        if separateNum > 0 and sepVel.mag() > 0:
            # sepVel.div(separateNum)
            sepVel.normalize()
            sepVel.mult(self.max_speed)
            steerSep = PVector.sub(sepVel, self.velocity)
            if steerSep.mag() != 0:
                steerSep.normalize()
                steerSep.mult(self.max_force)

        if fleeNum > 0 and fleVel.mag() > 0:
            fleVel.normalize()
            fleVel.mult(self.max_speed)
            steerFle = PVector.sub(fleVel, self.velocity)
            if steerFle.mag() != 0:
                steerFle.normalize()
                steerFle.mult(self.max_force)

        return [steerAlign, steerSep, steerCoh, steerFle]

    def awayBorders(self):
        # steerBor = PVector(0, 0)
        margin = 100
        if self.location.x < margin:
            steerBor = PVector(self.max_force, 0)
            if self.location.x > 0:
                steerBor.x /= self.location.x
        elif self.location.x > width - margin:
            steerBor = PVector(-self.max_force, 0)
            if self.location.x < width:
                steerBor.x /= width - self.location.x
        elif self.location.y < margin:
            steerBor = PVector(0, self.max_force)
            if self.location.y > 0:
                steerBor.y /= self.location.y
        elif self.location.y > width - margin:
            steerBor = PVector(0, -self.max_force)
            if self.location.y < height:
                steerBor.y /= height - self.location.y
        else:
            steerBor = PVector(0, 0)
        return steerBor

    def borders(self):

        if self.location.x < -self.radius:
            self.velocity.x = -1 * self.velocity.x
            # print("1111")
        if self.location.y < -self.radius:
            self.velocity.y = -1 * self.velocity.y
            # print("2222")
        if self.location.x > width + self.radius:
            self.velocity.x = -1 * self.velocity.x
            # print("3333")
        if self.location.y > height + self.radius:
            self.velocity.y = -1 * self.velocity.y
            # print("4444")

    def detailDisplay(self, myMouse=None, imagePaths=None, titles=None, agents=None):
        fill(100)
        if myMouse is None:
            # When myMouse is not passed, text follows the agent
            text(self.text, self.location.x, self.location.y)
        else:
            if self.isClosed(myMouse):
                # If myMouse is passed and agent is close to mouse, display the text
                text(self.text, self.location.x, self.location.y)
                if imagePaths is not None:
                    # If imagePaths is passed, show details info, compute the distance to let the closest one to display
                    dists = [dist(myMouse.x, myMouse.y, self.location.x, self.location.y)]
                    for other in agents:
                        if other.isClosed(myMouse):
                            # If there are other agent close to mouse at the same time, find the closest one
                            dists.append(dist(myMouse.x, myMouse.y, other.location.x, other.location.y))
                    if dists.index(max(dists)) == 0:
                        # If agent is the closest one, display its detail info
                        img = loadImage(imagePaths[self.group])
                        imageMode(CENTER)
                        image(img, width / 2, height / 2)
                        strokeWeight(1.5)
                        stroke(self.color)
                        line(self.location.x, self.location.y, width / 2 - img.width / 2, height / 2 - img.height / 2)
                        line(self.location.x, self.location.y, width / 2 + img.width / 2, height / 2 - img.height / 2)
                        line(self.location.x, self.location.y, width / 2 - img.width / 2, height / 2 + img.height / 2)
                        line(self.location.x, self.location.y, width / 2 + img.width / 2, height / 2 + img.height / 2)
                        noStroke()
                        textAlign(CENTER, TOP)
                        fill(color(self.r, self.g, self.b))
                        text(titles[self.group], width / 2, height / 2 + img.height / 2)
                        textAlign(LEFT, BASELINE)

    def isClosed(self, myMouse):
        # Magnify the radius for easier pointing for text display
        r = self.radius * 3
        # Whether mouse is close to agents
        if self.location.x-r < myMouse.x < self.location.x+r and self.location.y-r < myMouse.y < self.location.y+r:
            return True
        else:
            return False

