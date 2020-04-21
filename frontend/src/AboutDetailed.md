# How it works

In short, the site ranks games as entertaining when it's unclear who's going to
win and discards games that are dominated by one team. As in,  watching OU beat
up some more middle-schoolers is a bit underwhelming when you could be watching
Tenessee almost lose six times in the fourth quarter. The site determines which
games are fun and which aren't by looking at the win-probability graph of a
game: if the graph swings from the top to the bottom frequently the algorithm
rates the game as interesting while the algorithm rates a game with a lopsided
graph as dull. However, there are plenty of plans to make the algorithm more
nuanced. This includes rating rivalry games higher, inflating the rating of
underdog wins, and rating a close game between good teams higher than a close
game between two bad teams.

## How it works for nerds
The site uses play-by-play data from
[collegefootballdata.com](https://api.collegefootballdata.com) to
generate a win probability graph of the game using the formulas at
[pro-football-reference.com](https://www.pro-football-reference.com/about/win_prob.htm).
It also uses betting
lines to bias the game in favor of a team before the game starts. Otherwise,
the graph would always start with each time having a 50% chance of winning.
Once it has created the graph, we score the game based on how quickly the graph
changes direction - essentially, the spikier the graph the better. 

## How it works for Uber-Nerds<sup>*tm*</sup>
Mathematically what we're doing to score the games is integrating the absolute
value of the derivative of the win probability of the game. This gives us a
value that measures the average change in the probability a team wins after
each play of the game. So a high score describes a game where each play changes
who's going to win the game while a low score represents a game where one team
has a 99% probability of winning for the whole game. 

The win probability is calculated for each play by subtracting the probability
the team is going to win in regulation time minus the probability the team is
going to lose in regulation time taking into account the current score and time
remaining. To calculate these numbers, we assume that the probability of a team
winning is represented by a bell curve. The bell curve loses variance as the
time remaining shrinks and the model becomes more certain of the outcome. This
lets us determine the odds that one of the teams will have won before the end
of the fourth quarter. 

However, not all games end during regulation time. Since the probability of a
team losing in regulation time and the probability of a team winning in
regulation time do not add up to 100%, the odds of a tie is whatever is
leftover. We assume that two teams are equally matched if they are in overtime,
so each team has a 50% chance of winning.

Putting it all together, the probability of a team winning at any given play is
equal to the probability a team wins in regulation plus half the probability
the game goes to overtime minus the probability that the team loses in
regulation.

The code for everything is in [this repository on
GitHub](https://github.com/BrandonHarrisonCode/weeklycfb) for anyone interested
in the implementation details.
