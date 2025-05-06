from manim import *
import math

class Sheild(Scene):
    def construct(self):
        radius = 2
        n = 3
        angle_per_slice = 360 / n
        a = [2,1,2]
        deg = [0,120,240]
        pos = []
        c = [RED,YELLOW,BLUE,GREEN,WHITE]
        status = VGroup()
        shield_group = VGroup()
        # circle_group = VGroup()
        imps = Group()
        labels = VGroup()
        path = VGroup()

        shield = Tex(R"Shield : $10^9+7$", font_size=24).to_edge(UP)
        score = Text("Score : 0", font_size=24).next_to(shield,DOWN)
        time = Text("T = 0", font_size=24).next_to(score,DOWN)
        log = Text("-", font_size=24).to_edge(DOWN*0.7)

        status.add(shield,score,time,log)
        self.add(status)

        for i in range(n):
            start_angle = -(deg[i]+angle_per_slice+30) * DEGREES
            
            sector = Sector(
                radius=radius,
                angle=-angle_per_slice * DEGREES,
                start_angle=start_angle,
                color=BLACK,
                fill_opacity=0.6,
                stroke_color=WHITE,
                stroke_width=2
            )

            theta_deg = -deg[i]+30
            theta_rad = math.radians(theta_deg)
            r = radius * 0.5
            x = r * math.cos(theta_rad)
            y = r * math.sin(theta_rad)
            position = [x, y, 0]
            self.add(Text(str(i+1), color=WHITE, fill_opacity=1, font_size=24).move_to([x*2.2,y*2.2,0]))
            pos.append(position)
            imp = ImageMobject("imp.png")
            imp.scale(0.175)
            imp.move_to(position)
            imps.add(imp)
            label = Text(str(a[i]), 
                         color=BLACK, 
                        #  color=c[i], 
                         font_size=24).move_to(position)
            
            shield_group.add(sector)
            labels.add(label)
            path.add(Arc(stroke_opacity=0, color = c[i], radius=r, start_angle=(30+angle_per_slice*i)*DEGREES, angle=angle_per_slice*DEGREES, arc_center=[0,0,0]))
        
        self.add(shield_group)
        self.add(imps)
        self.add(labels)
        self.add(path)

        human = ImageMobject("vlyadis2.png")
        human.scale(0.8)
        human.move_to([2,2,0])
        self.add(human)

        k = 1.7
        extra = Arc(stroke_opacity=0, color = c[i], radius=r*k, start_angle=(30)*DEGREES, angle=-2*angle_per_slice*DEGREES, arc_center=[0,0,0])
        self.add(extra)
        self.wait()
        for i in range(n):
            new_time = Text("T="+str(i+1), font_size=24).move_to(time.get_center())
            self.play(Transform(time, new_time))
            self.wait()
            if i==0:
                new_shield = Text("Shield : 2", font_size=24).move_to(shield.get_center())
                new_score = Text("Score : 1", font_size=24).move_to(score.get_center())
                new_log = Text("Player jumps from Outside to Sector 1", font_size=24).move_to(log.get_center())
                
                self.play(
                    Transform(shield, new_shield),
                    Transform(score, new_score),
                    Transform(log, new_log),
                )
                self.play(
                    human.animate.move_to([pos[0][0]*k,pos[0][1]*k,0]),
                )
            elif i==1:
                new_shield = Text("Shield : 2", font_size=24).move_to(shield.get_center())
                new_score = Text("Score : 2", font_size=24).move_to(score.get_center())
                new_log = Text("Player jumps from Sector 1 to Sector 2", font_size=24).move_to(log.get_center())
                
                self.play(
                    Transform(shield, new_shield),
                    Transform(score, new_score),
                    Transform(log, new_log),
                )
                self.play(
                    # MoveAlongPath(human,extra)
                    human.animate.move_to([pos[1][0]*k,pos[1][1]*k,0]),
                )
            elif i==2:
                new_shield = Text("Shield : 2", font_size=24).move_to(shield.get_center())
                new_score = Text("Score : 3", font_size=24).move_to(score.get_center())
                new_log = Text("Player jumps from Sector 2 to Sector 3", font_size=24).move_to(log.get_center())
                
                self.play(
                    Transform(shield, new_shield),
                    Transform(score, new_score),
                    Transform(log, new_log),
                )
                self.play(
                    human.animate.move_to([pos[2][0]*k,pos[2][1]*k,0]),
                )
            else:
                new_log = Text("No Jump", font_size=24).move_to(log.get_center())
                self.play(Transform(log, new_log))
            self.wait()
            
            new_log = Text("Monsters rotate counter clockwise!", font_size=24).move_to(log.get_center())
            self.play(Transform(log, new_log))
            self.play(
                *[
                    anim
                    for j in range(n)
                    for anim in [
                        MoveAlongPath(imps[j]  , path[(i+n-j) % n]),
                        MoveAlongPath(labels[j], path[(i+n-j) % n])
                    ]
                ]
            )
            self.wait()

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        self.wait()
        self.play(Write(Text("Game Ends!", font_size=36)))
        self.wait()
