# Robotfactory

## Task description

After the pilot study, we decided to change the experiment and the instructions more towards the study by Zorowitz 2023 [^zorowitz2023]. The main changes here, were that there now 8 instead of 4 robots, that participants had to associated with go or no-go responses. However, in this experiment, the reward context was clearly indicated, here we replaced the response cue by a "scanner light", a transparent blue (winning) or red (losing) cone that was put above the robot. Furthermore, the robots did not differ in color anymore, but had letters on their chest plate. These letters were taken from the Brussels Artificial Character Set 2 [^vidal2017]. To use these stimuli, you will need to download the stimuli or use the `core/assets/download_bacs.py` script.

Following the story in the instructions, participants were tasked to repair a robot (press key with index finger) or leave it alone (do nothing), when the scanner light turns on. The color of the scanner light indicates if it is a "dangerous" robot (they play to not lose -1 or -5 points) or a "safe" robot (they play to win 1 or 5 points). They were further told that the different robots had different need to be repaired. However, that this outcome would be probabilistic.

As in the go, no/go task above, participants started with a 0.3 s cueing phase (only fixation), after which the robot appeared for $[0.5 s, 0.75 s,1.0 s, 1.25 s]$, which was repeated 16 times to generate blocks of 64 trials. These blocks were then permuted randomly. Then the scanner turned on for 1 s, cueing the participants response. After a 1 s delay (only fixation cross and scanner out line), reward feedback was given for 1 s. Each trial was followed by a inter trial interval which was randomly drawn from the set $[0.5 s, 0.75 s, 1.0 s, 1.25 s]$, which was repeated 16 times to generate blocks of 64 trials, uniformly sampled, without replacement. As in other experiments, we added the time left in the response window to the ITI to ensure a reliable trial length.

Stimulus order was created pseudorandomly and in blocks of 64. Where each block of 64 trials contained each of the four conditions ("go-win", "go-punish", "nogo-win", "nogo-punish") 8 times, with each stimulus appearing 8 times. In the first block it was made sure, that participants see each of the eight stimuli at least once within the first 8 trials.

Probabilistic rewards were generated pseudorandomly, by permuting lists of length 10 (e.g. [-1, -1, -1, -1, -1, -1, -1, -1, -5, -5]), removing the reward from the list and selecting the next one. After selecting a stimulus 10 times, a new randomly permuted list was generated.

After each set of 64 trials, there was a 45 second break.

## References

[^zorowitz2023]: Zorowitz, S., Karni, G., Paredes, N., Daw, N., & Niv, Y. (2023). Improving the reliability of the Pavlovian go/no-go task for computational psychiatry research. OSF. https://doi.org/10.31234/osf.io/eb697

[^vidal2017]: Vidal, C., Content, A., & Chetail, F. (2017). BACS: The Brussels Artificial Character Sets for studies in cognitive psychology and neuroscience. Behavior Research Methods, 49(6), 2093–2112. https://doi.org/10.3758/s13428-016-0844-8
