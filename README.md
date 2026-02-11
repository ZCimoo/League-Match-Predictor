# League of Legends Match Predictor
This project is a machine learning companion for League of Legends players. Unlike generic stat trackers that only show past performance, this system runs locally while you play to provide real-time win probability and performance benchmarking. It answers the question "Given my current gold, kills, and objectives, what are my chances of winning this game?"

## Context for Non Gamers
It can be difficult for players to understand how matches are going. A few bad plays can make a game feel unwinnable even when statistics say otherwise. 
Think of this tool as a coach that ignores the emotion of the moment and looks exclusively at the data (resources, map control, character scaling) to tell the player:  
1. "You're only down by 1,000 gold, the game is still a 48% coin flip. Dont give up!"
2. "You are ahead byt your team compostition will fall off after 30 minutes. You should end the game now."

## Use Case: Why would a player use this?
* **Tilt Management (Pyschology)**: It's very common for players to "surrender" games too early because they're frustrated. This tool will provide players with an object, data driven "Win %" to keep them focused if the game is actually winnable.
* **Strategic Decision Making**: If the model predicts low win probability in late game, the player knows they must take high risk, high reward plays to change the odds, rather than playing safely and losing.
* **Post Game Analysis**: By logging win probability over the course of the game, players can see the exact moment where they "throw", the minute where their chance of winning significantly dropped. This can allow them to understand what went wrong, and how to avoid it.

## How it Works
1. **Pre-game (Draft Phase)**
   * Input: User's champion (character they're playing) pick, and teammates picks.
   * Insight: "Your team has a 52% win rate, but you are statistically weaker than another player. Play safe early."
2. **In Game (Live Prediciton)**
   * Input: Poll data periodically from the Live Client API to get data like Gold, XP, Towers, and Dragon counts.
   * Processing: Input data into a trained Gradient Boosted Machine (LightGBM)
   * Output: A live "Win Probability Graph" to be viewed on a second monitor. It will show the user how their actions are impacting the games outcom in real-time.


## Motivation
There are a handful of reason I picked this project, the main one being that I am currently addicted to League of Legends. The others being this is a great chance for me to learn and practice Python and Data Science. I also find it really interesting and this is something that I am actually really excited to create compared to other projects I have worked on.

