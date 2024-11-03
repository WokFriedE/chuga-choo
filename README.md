# chuga-choo
HackNJIT 2024

| Location  |   Packages        |    Usage        | 
|-----------|-------------------|-----------------|
| Both      | Docker-compose    | running the app |
| Both      | Terraform         | Running the app on docker, simply |
| BE        | Flask             | Running the API and simulation |
| BE        | Loguru            | Logging |
| BE        | numpy             | Doing simulation calculations (thanks kamil) | 
| BE        | pprint, json, time, threading | In built packages used for their uses |
| FE        | svelte            | Framework for frontend |

## Utilized
- Gemeni + ChatGPT for photos
  - refer to frontend readme for links and cites for photos
- ChatGPT and Copilot for assisted coding

## Terraform Video
https://youtu.be/_uzTAj9zV7I

## Demonstration 
https://www.youtube.com/watch?v=bcXEG4K0BuM

## Devpost Submission
### Inspiration
We started with the idea of a nuclear reactor simulator game, and workshopped that to a steam engine simulator, and from there to a broader game/narrative of the player driving a train between various stations & upgrading their train over time.

### What it does
We built a train simulator game- where your goal is to drive the train a certain distance without blowing up the engine. Players have to manage engine temperature as well as the pressures at various points in the engine, using different steampunk-styled controls to regulate thee factors. 

### How we built it
The game is built using Svelte for the frontend, and using flask for the backend simulation. We started building both the backend and frontend independently and bound them together near the end- this allowed us to develop much faster than if we were to build it as a singular monolithic application.

### Challenges we ran into
User design/experience was a major challenge point for us- because the UI layout is very unorthodox, we struggled to develop the frontend in a responsive manner in the time given. The extremely advanced solution we found was to zoom in/out on the site until the components vaguely lined up with their intended locations.
Accomplishments that we're proud of
There were major accomplishments for everyone on the team in this project. We learned to set up CI/CD and Terraform, manage an arbitrary amount of live simulations on a per-user basis, and animating interactive components without breaking the steampunk aesthetic. These were all new things for the team, and we managed to get good results on all of these fronts.

### What we learned
In the course of this marathon, we learned how to use Terraform, how to use Svelte 5, and how to develop a reasonable emulation of a physical system.

### What's next for Chugga Chugga Choo Choo
The future for this project is implementing "stations" and "hubs"- where the player earns money for making trips between stations, and is able to upgrade their train using their money when they reach hubs. Currently, the primary gameplay loop (driving the train) is implemented but none of the surrounding game has been developed.
