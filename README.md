# pkmn (Title TBD)
All mechanics are meant to mirror Gen 9 of pokemon.
## Stat Calculator
The only part that perfectly matches the games. The Mon class takes inputs for level, any number of types, the six base stats, a nickname, IVs, EVs, and nature. Items and Abilities have their own attribute but do nothing atm. The Mon class automatically runs statCalc() to convert the IVs, EVs, Nature, and level into the final stats of the pokemon--this should match how stats are calculated in Scarlet/Violet or Pokemon Showdown.
## Damage calculator
Damage values are slightly higher than what they would be in game--working to fix. Otherwise, calculations are matched to Gen 9 damage calcs, but only included "extra" factors are critical hits, the 0.85-1.00 random value, type interactions and STAB. Moves can be created with the Move class (take ONE type as input--"types" naming is for consistency. May change.) and then added to Mon objects' movelists with the Mon class's .add_move(move). This registers the Move object and its max PP into the dict in the .moves attribute of the Mon object. These moves can be used independently with the Move class's .calc(user, target) method or through the Mon class's .use_move(move, target) method.

Mons lose hit points but do not faint. The beginnings to stat (and crit chance) boosts are in place but nonfunctional.
