# Projectile Launcher Models

Last Updated: May 2024

## Introduction

A common theme in First Robotics is to launch game pieces into openings. This is one of those things that's easier said than done, and requires precise alignment and positioning, and a strong understanding of physics to solve.

## Relative Motion: Vector Addition

There are many reference frames to use when talking about movement, but picking a specific reference frame and staying consistent (and being able to swap between them) is important for advanced robotics, rocket science, and a whole lot more.

You can sit on a train, playing with marbles on a table top, and what you perceive as a marble moving 1 meter per second away from you, is in fact a marble moving 1 meter per second faster than a train. This scales up into 3 dimensions cleanly, and a marble moving away from you and to the left at 1.2 meters per second is also moving forward and left more than the train is. This can be represented as something called Vector Addition.

There's a video from the show Mythbusters that [illustrates this](https://www.youtube.com/watch?v=BLuI118nhzc) decently well. Bonus points if you recognize what Kari Byron yells out. They are trying to see if they released a ball backwards at the same speed as the vehicle it's on is moving, will it stay stationary relative to the ground the truck is driving over. You see, these are two different reference frames, one is with respect to the truck, and the other is respect to the ground. No matter how you setup your equation, the terms should cancel out, and the relative ground speed between asphalt and the ball is 0.

That's a really trivial case though, what happens in the more dynamic environments? Well, the same thing really. Instead of adding single values together, you add multiple ones. See the diagram below, and observe that the x and y values are both going through the same thing.

![Vector Image Not Found.](vectors.png "Pull out a ruler and try it yourself!")

Seen here as: _actual = aim+moving_

If you were to take the _moving_ vector and add it to the _aim_ vector, you would get the _actual_ vector. You can line this up visually and take the tail of the _moving_ vector (side without the arrow) and place it over the tip of the _aim_ vector (side with the arrow tip), and see how the tip of the _moving_ vector touches the tip of the _actual_ vector. This is a core concept of Linear Algebra.

More formally, this can be written as:

$$ v_{final} = \sum_v v $$

Kinda simple, right?

## Kinematic Equations

![Parabola Image Not Found.](parabola.png "Note: the origin doesn't really matter.")

Relative release angles are cool and all, but what happens after the piece is up in the air in free fall? It experiences a different type of motion called a parabolic trajectory. These can be calculated with a series of equations listed below.

$$
\begin{aligned}
\Delta x &= (\frac{v_f+v_0}{2})t \\
\Delta x &= v_0t + \frac{1}{2}at^2 \\
   v_f^2 &= v_0^2 + 2a \Delta x \\
     v_f &= v_0 + at
\end{aligned}
$$

Some of these are quite linear, by being able to drop larger polynomial terms we get equations like the last one. These are very powerful when used efficiently. They can also be used in pieces, solving for one thing, then swapping to another to leverage that intermediate value.

For instance, you can calculate the time in the air given a launch vector by using {$\cancel{v_f}0 = v_0 +at$}, pair it with {$\Delta x = (\frac{\cancel{v_f}+v_0}{2})t$} for the first half of an arc, then solve for the second half with {$\Delta x = \cancel{v_0t} + \frac{1}{2}at^2$}. Solving it this way also cancels out many terms in the process. You can also substitute the equations into eachother to derive new ones. For instance, {$(v_0 + at)^2 = v_f^2 = v_0^2 + 2a \Delta x$} which reduces down to {$\cancel{v_0^2}+2v_0at + (at)^2 = \cancel{v_0^2} + 2a \Delta x$}. Maybe this isn't what you're looking for, but being able to remove {$v_f$} from the equation is pretty handy in the right situation!

## What To Solve For?

If you're thinking ahead, you can typically reduce the problems to a lower dimension, or solve for a specific case. If you notice above, some equations cancel one term or another out. For instance, notice how the first kinematic equation listed doesn't include an acceleration? How about the last one not having a distance variable? This is powerful, because it allows you to setup solutions to specific problems.

### Velocity At A Location

```python
# Calculate velocity needed to reach a target height and speed along the span
v0 = math.sqrt(end_velocity * end_velocity - 2 * GRAVITY[Z] * (target_position[Z] - current_position[Z]))
t = (end_velocity - v0) / GRAVITY[Z]

ground_vector = target_position - current_position
ground_vector[Z] = 0

final = ground_vector / t - current_velocity
final[Z] = v0
```

### Location Given An Angle
