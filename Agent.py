from pyprocessing import *
import random


class Agent:
    def __init__(self, group, emotionLevel, title, imagePath, entity):
        # emotion = group
        self.location = PVector(random.randint(0, width), random.randint(0, height))
        self.acceleration = PVector(0, 0)
        self.velocity = PVector(0, -2)
        if group == 0:                    # Sadness: slower
            self.max_speed = 1
            self.max_force = 0.008
        elif group == 1 or group == 4:  # Joy or anger: faster
            self.max_speed = 3
            self.max_force = 0.04
        else:                               # Fear or disgust: normal
            self.max_speed = 1.7
            self.max_force = 0.012
        self.radius = 8.0
        self.group = group
        self.emotion = group
        self.emotionLevel = map(emotionLevel, 0, 1, 0, 255)
        self.title = title
        self.imagePath = imagePath
        self.entity = entity

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
        self.color = color(self.r, self.g, self.b, self.emotionLevel)
        self.groupCenter = self.location

        self.count = [0, 0, 0, 0]

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
                    # noStroke()
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
            self.count[0] += 1
            self.count[1] = 0
            self.count[2] = 0
            self.count[3] = 0
            # print(self.count[0])
        if self.location.y < -self.radius:
            self.velocity.y = -1 * self.velocity.y
            self.count[0] = 0
            self.count[1] += 1
            self.count[2] = 0
            self.count[3] = 0
            # print(self.count[1])
        if self.location.x > width + self.radius:
            self.velocity.x = -1 * self.velocity.x
            self.count[0] = 0
            self.count[1] = 0
            self.count[2] += 1
            self.count[3] = 0
            # print(self.count[2])
        if self.location.y > height + self.radius:
            self.velocity.y = -1 * self.velocity.y
            self.count[0] = 0
            self.count[1] = 0
            self.count[2] = 0
            self.count[3] += 1
            # print(self.count[3])
        if max(self.count) > 100:
            self.__init__(self.group, self.emotionLevel, self.title, self.imagePath, self.entity)
            del self

            # index = self.count.index(max(self.count))
            # if index == 0:
            #     self.location.x += 5
            #     self.velocity.normalize()
            # elif index == 1:
            #     self.location.y += 5
            #     self.velocity.normalize()
            # elif index == 2:
            #     self.location.x -= 5
            #     self.velocity.normalize()
            # else:
            #     self.location.y -= 5
            #     self.velocity.normalize()

    def detailDisplay(self, myMouse, agents):
        fill(100)
        if self.isClosed(myMouse):
            dists = [dist(self.location.x, self.location.y, myMouse.x, myMouse.y)]
            for other in agents:
                if other.isClosed(myMouse):
                    dists.append(dist(other.location.x, other.location.y, myMouse.x, myMouse.y))
            if dists.index(max(dists)) == 0:
                if os.path.exists(self.imagePath):
                    img = loadImage(self.imagePath)
                    imageMode(CENTER)
                    image(img, width/2, height/2)
                    strokeWeight(1.5)
                    stroke(self.color)
                    line(self.location.x, self.location.y, width/2-img.width/2, height/2-img.height/2)
                    line(self.location.x, self.location.y, width/2+img.width/2, height/2-img.height/2)
                    line(self.location.x, self.location.y, width/2-img.width//2, height/2+img.height/2)
                    line(self.location.x, self.location.y, width/2+img.width//2, height/2+img.height/2)
                    noStroke()
                fill(color(self.r, self.g, self.b))
                textSize(15)
                if textWidth(self.title) < 400:
                    textAlign(CENTER, TOP)
                    text(self.title, width/2, height/2+80)
                    textAlign(LEFT, BASELINE)
                else:
                    text(self.title, width/2-200, height/2+80, width/2+100, height/2+150)

    def topicFollow(self):
        textSize(8)
        fill(100)
        if self.entity is not None:
            text(self.entity, self.location.x, self.location.y)

    def isClosed(self, myMouse):
        # Magnify the radius for easier pointing for text display
        r = self.radius * 2
        # Whether agent is closed to mouse
        if self.location.x-r < myMouse.x < self.location.x+r and self.location.y-r < myMouse.y < self.location.y+r:
            return True
        else:
            return False
