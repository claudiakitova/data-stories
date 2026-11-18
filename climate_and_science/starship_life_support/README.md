# Can Algae Keep a Starship Crew Breathing?

A crew of 15 wakes from hibernation; their air is maintained by a photobioreactor growing the alga *Chlorella*. From the reactor's telemetry: is it working, and is it enough to supply the crew's oxygen and absorb their carbon dioxide?

**Notebook:** [starship_life_support.ipynb](starship_life_support.ipynb) · **Data:** [telemetry.csv](telemetry.csv) (a fictional scenario dated 2230)

## Data and constants

- Reactor telemetry: culture mass, biomass density, growth rate, temperature, CO2 in the supply gas, air and light power.
- The crew's needs: 0.86 kg of oxygen and 0.95 kg of carbon dioxide per person per day (GOST R 50804-95).
- Gas exchange of chlorella per gram of dry biomass, by nitrogen source (Meleshko and Shepelev, *Biological Life Support Systems*).

## Approach

1. Calculated the crew's daily oxygen and carbon dioxide.
2. Estimated the reactor's output of dry biomass two ways: from its growth rate sensor, and from a mass balance of the culture it harvests.
3. Converted the output to oxygen released and carbon dioxide absorbed, and compared with the crew's needs.

## Results

- The crew needs 12.9 kg of oxygen per day and exhales 14.25 kg of carbon dioxide.
- The reactor works steadily and produces about 14 kg of dry biomass per day; both estimates agree within 1%.
- That releases about 26 kg of oxygen and absorbs about 27 kg of carbon dioxide per day, about twice the crew's needs, at only 20% of the reactor's light power.

## Tools

Python, pandas, NumPy, matplotlib
