# League of Legends Match Predictor
This project is a machine learning companion for League of Legends players. Unlike generic stat trackers that only show past performance, this system runs locally while you play to provide real-time win probability and performance benchmarking. It answers the question "Given my current gold, kills, and objectives, what are my chances of winning this game?"

## Context for Non Gamers
It can be difficult for players to understand how matches are going. A few bad plays can make a game feel unwinnable even when statistics say otherwise. 
Think of this tool as a coach that ignores the emotion of the moment and looks exclusively at the data (resources, map control, character scaling) to tell the player:  
1. "You're only down by 1,000 gold, the game is still a 48% coin flip. Dont give up!"
2. "You are ahead but your team compostition will fall off after 30 minutes. You should end the game now."

## Understanding the Game Dynamics
To understand why predicting this game is complex, imagine a 5v5 basketball game where scoring a point also gives your team money to buy better shoes, making you run faster for the rest of the game. That is League of Legends. It is an economy based territory control game. Players generate resources (Gold and Experience) by defeating enemies and securing objectives. These resources help increase a characters mathematical stats (Health, Damage, Speed, etc). A small early game lead can lead to an overwhelming late game statistical advantage. This is what my model is trying to calculate.

## Use Case: Why would a player use this?
* **Tilt Management (Psychology)**: It's very common for players to "surrender" games too early because they're frustrated. This tool will provide players with an object, data driven "Win %" to keep them focused if the game is actually winnable.
* **Strategic Decision Making**: If the model predicts low win probability in late game, the player knows they must take high risk, high reward plays to change the odds, rather than playing safely and losing.
* **Post Game Analysis**: By logging win probability over the course of the game, players can see the exact moment where they "throw", the minute where their chance of winning significantly dropped. This can allow them to understand what went wrong, and how to avoid it.

## Key Metrics Tracked by Model
For a non-player the data points observed can be translated as seen below:
* **Gold Difference:** The primary economic indicator. Shows which team has more purchasing power.
* **Experience (XP):** The primary metric of character growth. Higher XP means higher level and access to more powerful abilities.
* **Towers / Map Control:** Towers are defensive structures. Destroying them increases the area a team can safely play on them map.
* **Dragons / Neutral Objective:** Computer controlled monsters that provide buffs to a whole team when defeated (e.g, +5% attack damage).
* **Champion Scaling:** Time based power curves. Some characters are more dominant in early stages of the game (Sprinters), while some are weaker early on but become more powerful as the game progresses (Marathon Runners). 

## How it Works
1. **Pre-game (Draft Phase)**
   * Input: User's champion (character they're playing) pick, and teammates picks.
   * Insight: "Your team has a 52% win rate, but you are statistically weaker than another player. Play safe early."
2. **In Game (Live Prediciton)**
   * Input: Poll data periodically from the Live Client API to get data like Gold, XP, Towers, and Dragon counts.
   * Processing: Input data into a trained Gradient Boosted Machine (LightGBM)
   * Output: A live "Win Probability Graph" to be viewed on a second monitor. It will show the user how their actions are impacting the games outcome in real-time.


## Motivation
There are a handful of reason I picked this project, the main one being that I am currently addicted to League of Legends. The others being this is a great chance for me to learn and practice Python and Data Science. I also find it really interesting and this is something that I am actually really excited to create compared to other projects I have worked on.

## Timeline

**Phase 1:** Data Collection and Feature Engineering (2/18 - 3/4)
* **Goal:** Push pre-game accuracy from ~50% to 55-60%+.
* **Tasks:**
  * Download larger quantity of matches from the scraper.
  * Evaluate Riot Games Data Dragon for champion tags like "Tank" or "Assasin" to evaluate a teams composition in the pre-game phase allowing for a better prediciton.
  * Retrain LightGBM model on new data set with more entries, and finalize the pre-game model.

**Phase 2:** Live Client Pipeline (3/4-3/25)
* **Goal:** Shift from predicting pre-game to live game.
* **Tasks:**
  * Connect to the Riot Live Client API which allows me to access live match data.
  * Write a script to poll the game every 30-60 seconds to evaluate current Gold, Level, and Objectives.

**Phase 3:** The Second Monitor UI (3/25-4/8)
* **Goal:** Build tool for user interaction.
* **Tasks:**
  * Move away from the terminal. Build a visual win probability graph.

**Phase 4:** Buffer (4/8-Remaining time)
* **Goal:** Polish the project. Make up time for anything unfinished.
* **Tasks:**
  * Playtest the model.
  * Generate final graphs to displpay how the models accuracy improves as the game progresses.
  * Finalize presentation. 






